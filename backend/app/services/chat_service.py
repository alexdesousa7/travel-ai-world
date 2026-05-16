"""Chat service — business logic for AI chat streaming.

Manages NVIDIA API streaming via httpx with retry + exponential backoff.
Ported from monorepo, adapted to target's architecture (no DI constructor).
"""

import asyncio
import json
import logging
from collections.abc import AsyncGenerator

import httpx

from app.core.config import settings
from app.core.constants import (
    NVIDIA_BASE_URL,
    NVIDIA_CHAT_MODEL,
    NVIDIA_CONNECT_TIMEOUT,
    NVIDIA_MAX_RETRIES,
    NVIDIA_READ_TIMEOUT,
)

logger = logging.getLogger(__name__)


class ChatService:
    """Manages AI chat completions via NVIDIA API.

    Uses httpx.AsyncClient for true async streaming.
    """

    def _get_headers(self) -> dict[str, str]:
        """Build authorization headers for NVIDIA API."""
        if not settings.NVIDIA_API_KEY:
            raise ValueError("NVIDIA API key not configured")
        return {
            "Authorization": f"Bearer {settings.NVIDIA_API_KEY}",
            "Accept": "text/event-stream",
            "Content-Type": "application/json",
        }

    def _build_payload(self, messages: list[dict[str, str]]) -> dict:
        """Build the request payload matching NVIDIA API spec."""
        return {
            "model": NVIDIA_CHAT_MODEL,
            "messages": messages,
            "max_tokens": 16384,
            "temperature": 1.00,
            "top_p": 1.00,
            "stream": True,
            "chat_template_kwargs": {"thinking": True},
        }

    async def stream_completion(
        self, messages: list[dict[str, str]]
    ) -> AsyncGenerator[str]:
        """Generator that yields SSE-formatted chunks from NVIDIA API.

        Includes retry logic with exponential backoff for transient errors.
        """
        headers = self._get_headers()
        payload = self._build_payload(messages)
        url = f"{NVIDIA_BASE_URL}/chat/completions"
        timeout = httpx.Timeout(
            connect=NVIDIA_CONNECT_TIMEOUT,
            read=NVIDIA_READ_TIMEOUT,
            write=10.0,
            pool=10.0,
        )

        last_error: Exception | None = None

        for attempt in range(NVIDIA_MAX_RETRIES + 1):
            try:
                async with (
                    httpx.AsyncClient(timeout=timeout) as client,
                    client.stream(
                        "POST", url, headers=headers, json=payload
                    ) as response,
                ):
                    if response.status_code != 200:
                        body = await response.aread()
                        error_msg = (
                            f"NVIDIA API returned {response.status_code}: "
                            f"{body.decode('utf-8', errors='replace')}"
                        )
                        logger.error(error_msg)
                        raise httpx.HTTPStatusError(
                            error_msg, request=response.request, response=response
                        )

                    buffer = ""
                    async for chunk in response.aiter_text():
                        buffer += chunk
                        lines = buffer.split("\n")
                        buffer = lines.pop()

                        for line in lines:
                            line = line.strip()
                            if not line or not line.startswith("data: "):
                                continue

                            data = line[6:].strip()
                            if data == "[DONE]":
                                continue

                            try:
                                parsed = json.loads(data)
                                choices = parsed.get("choices", [])
                                if choices:
                                    delta = choices[0].get("delta", {})
                                    content = delta.get("content")
                                    if content:
                                        yield f"data: {json.dumps({'content': content})}\n\n"
                            except json.JSONDecodeError:
                                logger.debug("Skipping malformed SSE data: %s", data)

                yield "data: [DONE]\n\n"
                return  # Success — exit retry loop

            except ValueError:
                # NVIDIA_API_KEY not configured — don't retry
                raise
            except httpx.TimeoutException as exc:
                last_error = exc
                if attempt < NVIDIA_MAX_RETRIES:
                    wait = 2**attempt
                    logger.warning(
                        "NVIDIA API timeout, retrying in %ds (attempt %d/%d)",
                        wait,
                        attempt + 1,
                        NVIDIA_MAX_RETRIES,
                    )
                    await asyncio.sleep(wait)
                    continue
                break
            except httpx.HTTPError as exc:
                last_error = exc
                if attempt < NVIDIA_MAX_RETRIES:
                    wait = 2**attempt
                    logger.warning(
                        "NVIDIA API error, retrying in %ds (attempt %d/%d)",
                        wait,
                        attempt + 1,
                        NVIDIA_MAX_RETRIES,
                    )
                    await asyncio.sleep(wait)
                    continue
                break
            except Exception as exc:
                last_error = exc
                logger.exception("Unexpected error during NVIDIA streaming: %s", exc)
                break

        # All retries exhausted
        error_msg = str(last_error) if last_error else "Unknown error"
        logger.error("NVIDIA streaming failed after retries: %s", error_msg)
        yield f"data: {json.dumps({'error': error_msg})}\n\n"
        yield "data: [DONE]\n\n"
