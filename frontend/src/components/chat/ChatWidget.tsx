"use client";

import React, { useState, useRef, useEffect, useCallback } from "react";
import { MessageSquare, Send, X, Bot, User, Loader2, Sparkles } from "lucide-react";
import { isApiAvailable, streamChat } from "@/services/api";
import { useAuth } from "@/context/AuthContext";

interface ChatMessage {
  role: "user" | "assistant";
  content: string;
}

/**
 * Floating AI chatbot widget.
 *
 * Renders a toggle button in the bottom-right corner that opens a chat panel.
 * Messages are streamed from the backend via SSE for a real-time typing effect.
 */
export default function ChatWidget() {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [input, setInput] = useState("");
  const [isStreaming, setIsStreaming] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);
  const { isAuthenticated } = useAuth();

  const scrollToBottom = useCallback(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, []);

  useEffect(() => {
    scrollToBottom();
  }, [messages, scrollToBottom]);

  useEffect(() => {
    if (isOpen && inputRef.current) {
      inputRef.current.focus();
    }
  }, [isOpen]);

  // Don't render if no API is configured
  if (!isApiAvailable()) return null;

  const handleSend = async () => {
    const trimmed = input.trim();
    if (!trimmed || isStreaming) return;

    const userMessage: ChatMessage = { role: "user", content: trimmed };
    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setIsStreaming(true);

    // Add empty assistant message that will be filled by stream
    setMessages((prev) => [...prev, { role: "assistant", content: "" }]);

    try {
      const history = messages.map((m) => ({
        role: m.role,
        content: m.content,
      }));

      for await (const chunk of streamChat(trimmed, history)) {
        setMessages((prev) => {
          const updated = [...prev];
          const last = updated[updated.length - 1];
          if (last?.role === "assistant") {
            updated[updated.length - 1] = {
              ...last,
              content: last.content + chunk,
            };
          }
          return updated;
        });
      }
    } catch (error) {
      setMessages((prev) => {
        const updated = [...prev];
        const last = updated[updated.length - 1];
        if (last?.role === "assistant" && last.content === "") {
          updated[updated.length - 1] = {
            ...last,
            content: "Sorry, I couldn't process your request. Please try again.",
          };
        }
        return updated;
      });
      console.error("Chat error:", error);
    } finally {
      setIsStreaming(false);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <>
      {/* Floating toggle button */}
      <button
        id="chat-toggle"
        onClick={() => setIsOpen(!isOpen)}
        className="fixed bottom-6 right-6 z-50 flex h-14 w-14 items-center justify-center rounded-full bg-accent text-white shadow-lg transition-all duration-300 hover:bg-accent-hover hover:scale-105 active:scale-95"
        aria-label={isOpen ? "Close chat" : "Open AI chat"}
      >
        {isOpen ? <X size={22} /> : <MessageSquare size={22} />}
      </button>

      {/* Chat panel */}
      {isOpen && (
        <div className="fixed bottom-24 right-6 z-50 flex w-[380px] max-w-[calc(100vw-3rem)] flex-col overflow-hidden rounded-2xl border border-border-soft bg-bg-card shadow-2xl animate-in fade-in slide-in-from-bottom-4 duration-300"
          style={{ height: "min(520px, calc(100vh - 8rem))" }}
        >
          {/* Header */}
          <div className="flex items-center gap-3 border-b border-border px-5 py-4">
            <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-accent/20">
              <Sparkles size={18} className="text-accent" />
            </div>
            <div className="flex-1">
              <h3 className="text-sm font-heading font-medium text-text-primary">
                Travel AI Assistant
              </h3>
              <p className="text-xs text-text-secondary">
                Powered by NVIDIA Kimi K2.6
              </p>
            </div>
            <button
              onClick={() => setIsOpen(false)}
              className="rounded-lg p-1.5 text-text-secondary transition-colors hover:bg-border-soft hover:text-text-primary"
              aria-label="Close chat"
            >
              <X size={16} />
            </button>
          </div>

          {/* Messages */}
          <div className="flex-1 overflow-y-auto px-4 py-4 space-y-4">
            {messages.length === 0 && (
              <div className="flex flex-col items-center justify-center h-full text-center px-4">
                <div className="flex h-14 w-14 items-center justify-center rounded-2xl bg-accent/10 mb-4">
                  <Bot size={28} className="text-accent" />
                </div>
                <p className="text-sm font-medium text-text-primary mb-1">
                  How can I help you?
                </p>
                <p className="text-xs text-text-secondary leading-relaxed">
                  Ask me about travel destinations, itinerary tips, local cuisine, or anything travel-related!
                </p>
              </div>
            )}

            {messages.map((msg, i) => (
              <div
                key={i}
                className={`flex gap-2.5 ${msg.role === "user" ? "flex-row-reverse" : "flex-row"}`}
              >
                {/* Avatar */}
                <div
                  className={`flex h-7 w-7 shrink-0 items-center justify-center rounded-lg ${
                    msg.role === "user"
                      ? "bg-accent/20"
                      : "bg-purple/20"
                  }`}
                >
                  {msg.role === "user" ? (
                    <User size={14} className="text-accent" />
                  ) : (
                    <Bot size={14} className="text-purple" />
                  )}
                </div>

                {/* Bubble */}
                <div
                  className={`max-w-[80%] rounded-xl px-3.5 py-2.5 text-sm leading-relaxed ${
                    msg.role === "user"
                      ? "bg-accent text-white rounded-br-sm"
                      : "bg-bg-surface text-text-primary border border-border rounded-bl-sm"
                  }`}
                >
                  {msg.content}
                  {msg.role === "assistant" && msg.content === "" && isStreaming && (
                    <span className="inline-flex items-center gap-1 text-text-secondary">
                      <Loader2 size={12} className="animate-spin" />
                      <span className="text-xs">Thinking…</span>
                    </span>
                  )}
                </div>
              </div>
            ))}
            <div ref={messagesEndRef} />
          </div>

          {/* Input */}
          <div className="border-t border-border px-4 py-3">
            {!isAuthenticated ? (
              <p className="text-center text-xs text-text-secondary py-2">
                Please sign in to use the AI assistant.
              </p>
            ) : (
              <div className="flex items-center gap-2">
                <input
                  ref={inputRef}
                  id="chat-input"
                  type="text"
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  onKeyDown={handleKeyDown}
                  placeholder="Ask about your next trip…"
                  disabled={isStreaming}
                  className="flex-1 rounded-xl border border-border bg-bg-primary px-4 py-2.5 text-sm text-text-primary placeholder:text-text-muted outline-none transition-colors focus:border-accent disabled:opacity-50"
                />
                <button
                  id="chat-send"
                  onClick={handleSend}
                  disabled={!input.trim() || isStreaming}
                  className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-accent text-white transition-all hover:bg-accent-hover disabled:opacity-40 disabled:cursor-not-allowed"
                  aria-label="Send message"
                >
                  {isStreaming ? (
                    <Loader2 size={16} className="animate-spin" />
                  ) : (
                    <Send size={16} />
                  )}
                </button>
              </div>
            )}
          </div>
        </div>
      )}
    </>
  );
}
