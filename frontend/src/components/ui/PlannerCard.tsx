"use client";

import { useState, useRef, useEffect, useCallback } from "react";
import { useLanguage } from "@/context/LanguageContext";
import { SectionLabel } from "@/components/ui/SectionLabel";
import { isApiAvailable, streamChat } from "@/services/api";
import { Bot, Loader2, Send, User } from "lucide-react";

interface PlannerCardProps {
  transparent?: boolean;
}

interface ChatMessage {
  role: "user" | "assistant";
  content: string;
}

/**
 * AI Trip Planner — Chat-based itinerary generator.
 *
 * This shared component renders a conversational prompt interface where users
 * describe their ideal trip. When a backend API is configured, messages stream
 * from the NVIDIA AI in real-time via SSE. Otherwise, the form falls back to a
 * static "coming soon" mode.
 *
 * Used on both the landing page (hero CTA) and the user Dashboard.
 *
 * @param transparent - If true, removes the background color and reduces padding.
 */
export default function PlannerCard({ transparent = false }: PlannerCardProps) {
  const { t } = useLanguage();
  const p = t.planner;

  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [input, setInput] = useState("");
  const [isStreaming, setIsStreaming] = useState(false);
  const [submitted, setSubmitted] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  const apiReady = isApiAvailable();

  const scrollToBottom = useCallback(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, []);

  useEffect(() => {
    scrollToBottom();
  }, [messages, scrollToBottom]);

  /**
   * Sends the user message to the AI backend and streams the response.
   */
  const handleSendToAI = async () => {
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

  /**
   * Fallback submit for when no backend is available (static mode).
   */
  const handleStaticSubmit = () => {
    setSubmitted(true);
    setTimeout(() => setSubmitted(false), 4000);
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      if (apiReady) {
        handleSendToAI();
      } else {
        handleStaticSubmit();
      }
    }
  };

  return (
    <section id="planner" className={`${transparent ? "bg-transparent py-12" : "bg-bg-secondary py-24"}`}>
      <div className="max-w-[1440px] w-full mx-auto px-8 lg:px-16 flex flex-col gap-10">
        <div className="flex flex-col gap-4">
          <SectionLabel>{p.label}</SectionLabel>
          <h2 className="text-4xl lg:text-5xl font-medium text-text-primary tracking-[-1px] leading-tight">
            {p.title}
          </h2>
        </div>

        {/* PROMPT MODE — Layla.ai style with categories */}
        <div className="bg-bg-card border border-border rounded-2xl p-8 lg:p-10 flex flex-col gap-6">

          {/* Category quick actions */}
          <div className="flex flex-wrap justify-center gap-3">
            {[
              { label: "Vuelos", icon: "✈️" },
              { label: "Hoteles", icon: "🏨" },
              { label: "Restaurantes", icon: "🍽️" },
              { label: "Atracciones", icon: "🎡" },
            ].map(({ label, icon }) => (
              <button
                key={label}
                type="button"
                className="flex items-center gap-2 px-4 py-2 bg-bg-secondary hover:bg-bg-card border border-border-soft text-text-primary rounded-xl text-sm font-medium transition-all"
              >
                <span>{icon}</span>
                {label}
              </button>
            ))}
          </div>

          {/* Chat messages area — only shown when there are messages */}
          {messages.length > 0 && (
            <div className="max-h-80 overflow-y-auto space-y-3 px-1">
              {messages.map((msg, i) => (
                <div
                  key={i}
                  className={`flex gap-2.5 ${msg.role === "user" ? "flex-row-reverse" : "flex-row"}`}
                >
                  <div
                    className={`flex h-7 w-7 shrink-0 items-center justify-center rounded-lg ${
                      msg.role === "user" ? "bg-accent/20" : "bg-purple/20"
                    }`}
                  >
                    {msg.role === "user" ? (
                      <User size={14} className="text-accent" />
                    ) : (
                      <Bot size={14} className="text-purple" />
                    )}
                  </div>
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
          )}

          {/* Label */}
          <label className="text-[12px] font-medium text-text-secondary tracking-[0.1em] uppercase">
            Escribe tu viaje
          </label>

          {/* Textarea */}
          <textarea
            ref={textareaRef}
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Crea un itinerario de 7 días en París o Japón para una escapada de ensueño"
            disabled={isStreaming}
            className="w-full h-32 bg-bg-primary border border-border-soft rounded-xl p-4 text-[15px] text-text-primary placeholder-text-secondary/50 focus:outline-none focus:border-accent/60 transition-colors disabled:opacity-50"
          />

          {/* Bottom action bar */}
          <div className="flex items-center justify-between border border-border-soft bg-bg-primary rounded-xl px-4 py-3">
            <button
              type="button"
              className="text-text-secondary hover:text-text-primary transition text-xl"
            >
              📎
            </button>

            {apiReady && (
              <button
                type="button"
                onClick={handleSendToAI}
                disabled={!input.trim() || isStreaming}
                className="flex items-center gap-2 text-accent hover:text-accent-hover transition disabled:opacity-40 disabled:cursor-not-allowed"
                aria-label="Send message"
              >
                {isStreaming ? (
                  <Loader2 size={18} className="animate-spin" />
                ) : (
                  <Send size={18} />
                )}
              </button>
            )}

            {!apiReady && (
              <button
                type="button"
                className="text-text-secondary hover:text-text-primary transition text-xl"
              >
                🎤
              </button>
            )}
          </div>

          {/* Main button */}
          <button
            type="button"
            onClick={() => {
              if (apiReady) {
                handleSendToAI();
              } else {
                handleStaticSubmit();
              }
            }}
            disabled={isStreaming || (apiReady && !input.trim())}
            className="w-full h-14 bg-accent hover:bg-accent-hover text-white font-medium text-lg rounded-xl transition-all duration-300 shadow-lg shadow-accent/40 flex items-center justify-center gap-3 active:scale-[0.98] disabled:opacity-60 disabled:cursor-not-allowed"
          >
            {isStreaming ? (
              <>
                <Loader2 size={20} className="animate-spin" />
                <span>Generando...</span>
              </>
            ) : submitted ? (
              <span>✅ ¡Próximamente!</span>
            ) : (
              <>
                <span>✨</span>
                <span>Planificar viaje</span>
              </>
            )}
          </button>

        </div>
      </div>
    </section>
  );
}
