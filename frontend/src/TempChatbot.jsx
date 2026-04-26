import { useState, useEffect, useRef, useCallback } from "react";

// ─── Utility: linkify text ───────────────────────────────────────────────────
function Linkified({ text }) {
  const urlRegex = /(https?:\/\/[^\s]+)/g;
  const parts = text.split(urlRegex);
  return (
    <>
      {parts.map((part, i) =>
        urlRegex.test(part) ? (
          <a
            key={i}
            href={part}
            target="_blank"
            rel="noopener noreferrer"
            style={{ color: "#4fc3f7", wordBreak: "break-all" }}
          >
            {part}
          </a>
        ) : (
          <span key={i}>{part}</span>
        )
      )}
    </>
  );
}

// ─── Loading Dots ────────────────────────────────────────────────────────────
function LoadingDots() {
  const [dots, setDots] = useState(1);
  useEffect(() => {
    const t = setInterval(() => setDots((d) => (d % 3) + 1), 500);
    return () => clearInterval(t);
  }, []);
  return (
    <div style={styles.botBubble}>
      <span style={styles.loadingSpinner} />
      <span style={{ fontStyle: "italic", color: "#888" }}>
        ⏳ Please wait{".".repeat(dots)}
      </span>
    </div>
  );
}

// ─── Message Bubble ──────────────────────────────────────────────────────────
function MessageBubble({ msg }) {
  const isUser = msg.role === "user";
  return (
    <div
      style={{
        display: "flex",
        justifyContent: isUser ? "flex-end" : "flex-start",
        animation: "msgIn 0.25s ease",
      }}
    >
      <div style={isUser ? styles.userBubble : styles.botBubble}>
        {isUser ? (
          <span>{msg.content}</span>
        ) : (
          <Linkified text={msg.content} />
        )}
      </div>
    </div>
  );
}

// ─── FAQ Chip ────────────────────────────────────────────────────────────────
function FAQChip({ faq, onSelect }) {
  return (
    <button
      onClick={() => onSelect(faq.question)}
      style={styles.faqChip}
      onMouseEnter={(e) => {
        e.currentTarget.style.background = "rgba(3,62,124,0.12)";
        e.currentTarget.style.borderColor = "#033e7c";
      }}
      onMouseLeave={(e) => {
        e.currentTarget.style.background = "rgba(3,62,124,0.04)";
        e.currentTarget.style.borderColor = "rgba(3,62,124,0.2)";
      }}
    >
      <span style={styles.faqChipLabel}>{faq.stream}</span>
      <span style={styles.faqChipQ}>{faq.question}</span>
      <span style={styles.faqChipP}>{faq.preview}</span>
    </button>
  );
}

// ─── Main App ────────────────────────────────────────────────────────────────
export default function App() {
  const [open, setOpen] = useState(false);
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [sessionId] = useState(() => crypto.randomUUID());
  const [isListening, setIsListening] = useState(false);
  const [faqs, setFaqs] = useState([]);
  const [showFAQs, setShowFAQs] = useState(false);
  const [voiceMode, setVoiceMode] = useState(false);

  const messagesEndRef = useRef(null);
  const recognitionRef = useRef(null);
  const inputRef = useRef(null);

  // Auto scroll
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  // Load FAQs once
  useEffect(() => {
    fetch("/get_faqs")
      .then((r) => r.json())
      .then((d) => setFaqs(d.faqs || []))
      .catch(() => {});
  }, []);

  // Focus input when chat opens
  useEffect(() => {
    if (open) setTimeout(() => inputRef.current?.focus(), 200);
  }, [open]);

  // ── Send message ──────────────────────────────────────────────────────────
  const sendMessage = useCallback(
    async (overrideText) => {
      const text = (overrideText ?? input).trim();
      if (!text || loading) return;
      setInput("");
      setShowFAQs(false);
      setMessages((prev) => [...prev, { role: "user", content: text }]);
      setLoading(true);

      try {
        const res = await fetch("/api", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ message: text, session_id: sessionId }),
        });
        const data = await res.json();
        setMessages((prev) => [
          ...prev,
          { role: "bot", content: data.response },
        ]);
        if (voiceMode) {
          speakText(data.response);
          setVoiceMode(false);
        }
      } catch {
        setMessages((prev) => [
          ...prev,
          {
            role: "bot",
            content: "❌ Error connecting. Please check if Flask is running.",
          },
        ]);
      } finally {
        setLoading(false);
      }
    },
    [input, loading, sessionId, voiceMode]
  );

  // ── Voice ─────────────────────────────────────────────────────────────────
  const speakText = (text) => {
    let clean = text.replace(/(https?:\/\/[^\s]+)/g, "");
    clean = clean
      .replace(/[\u{1F300}-\u{1FFFF}]/gu, "")
      .replace(/[*#_~`>]/g, "")
      .replace(/\s+/g, " ")
      .trim();
    if (!clean) return;
    const utt = new SpeechSynthesisUtterance(clean);
    utt.lang = "en-US";
    utt.rate = 0.9;
    speechSynthesis.cancel();
    speechSynthesis.speak(utt);
  };

  const startVoice = () => {
    if (isListening) {
      recognitionRef.current?.abort();
      return;
    }
    const SR = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SR) {
      setMessages((prev) => [
        ...prev,
        { role: "bot", content: "❌ Voice not supported. Use Chrome." },
      ]);
      return;
    }
    const r = new SR();
    r.lang = "en-US";
    r.interimResults = false;
    r.maxAlternatives = 1;
    r.continuous = false;
    recognitionRef.current = r;

    r.onstart = () => {
      setIsListening(true);
      setMessages((prev) => [
        ...prev,
        { role: "bot", content: "🎤 Listening… Speak now!" },
      ]);
    };
    r.onresult = (e) => {
      const t = e.results[0][0].transcript.trim();
      setVoiceMode(true);
      setIsListening(false);
      sendMessage(t);
    };
    r.onerror = (e) => {
      setIsListening(false);
      const errs = {
        "not-allowed": "❌ Mic permission denied.",
        "no-speech": "⚠️ No speech detected.",
        network: "❌ Network error for speech.",
        "audio-capture": "❌ No microphone found.",
        aborted: "⚠️ Recognition stopped.",
      };
      setMessages((prev) => [
        ...prev,
        { role: "bot", content: errs[e.error] || `❌ Voice error: ${e.error}` },
      ]);
    };
    r.onend = () => setIsListening(false);

    try {
      r.start();
    } catch (e) {
      setMessages((prev) => [
        ...prev,
        { role: "bot", content: `❌ Could not start mic: ${e.message}` },
      ]);
    }
  };

  // ── Clear history ─────────────────────────────────────────────────────────
  const clearChat = () => {
    setMessages([]);
    fetch("/clear_history", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ session_id: sessionId }),
    }).catch(() => {});
  };

  // ─────────────────────────────────────────────────────────────────────────
  return (
    <>
      <style>{globalCSS}</style>

      {/* ── Hero Banner ─────────────────────────────────────────── */}
      <div style={styles.page}>
        <nav style={styles.nav}>
          <div style={styles.navBrand}>CKPCET</div>
          <div style={styles.navLinks}>
            <a href="/" style={styles.navLink}>Home</a>
            <a href="/faq" style={styles.navLink}>FAQ</a>
            <a href="/aboutus" style={styles.navLink}>About</a>
            <a href="/contactus" style={styles.navLink}>Contact</a>
          </div>
        </nav>

        <main style={styles.hero}>
          <div style={styles.heroInner}>
            <div style={styles.heroBadge}>Engineering Excellence Since 1999</div>
            <h1 style={styles.heroTitle}>
              C. K. Pithawala College of<br />
              <span style={styles.heroAccent}>Engineering & Technology</span>
            </h1>
            <p style={styles.heroSub}>
              Your intelligent assistant for admissions, academics, placements,
              and campus life — available 24 × 7.
            </p>
            <button style={styles.heroCTA} onClick={() => setOpen(true)}>
              💬 Chat with CKPCET Bot
            </button>
          </div>
          <div style={styles.heroCard}>
            <div style={styles.cardStat}><span style={styles.cardNum}>6+</span><span style={styles.cardLbl}>B.E. Branches</span></div>
            <div style={styles.cardDivider} />
            <div style={styles.cardStat}><span style={styles.cardNum}>3000+</span><span style={styles.cardLbl}>Students</span></div>
            <div style={styles.cardDivider} />
            <div style={styles.cardStat}><span style={styles.cardNum}>100%</span><span style={styles.cardLbl}>Placement Drive</span></div>
          </div>
        </main>

        {/* FAQ chips on main page */}
        {faqs.length > 0 && (
          <section style={styles.faqSection}>
            <h2 style={styles.faqHeading}>Common Questions</h2>
            <div style={styles.faqGrid}>
              {faqs.map((f, i) => (
                <FAQChip key={i} faq={f} onSelect={(q) => { setOpen(true); setTimeout(() => sendMessage(q), 300); }} />
              ))}
            </div>
          </section>
        )}

        <footer style={styles.footer}>© 2025 CKPCET Chatbot</footer>
      </div>

      {/* ── Floating Toggle ──────────────────────────────────────── */}
      <button
        style={{ ...styles.fab, ...(open ? styles.fabOpen : {}) }}
        onClick={() => setOpen((o) => !o)}
        aria-label="Toggle chat"
      >
        {open ? "✖" : "💬"}
      </button>

      {/* ── Chat Widget ──────────────────────────────────────────── */}
      <div style={{ ...styles.widget, ...(open ? styles.widgetOpen : {}) }} aria-hidden={!open}>

        {/* Header */}
        <div style={styles.widgetHeader}>
          <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
            <div style={styles.avatar}>🤖</div>
            <div>
              <div style={{ fontWeight: 700, fontSize: 14 }}>CKPCET Assistant</div>
              <div style={{ fontSize: 11, opacity: 0.75 }}>Powered by Gemini 2.0</div>
            </div>
          </div>
          <div style={{ display: "flex", gap: 8, alignItems: "center" }}>
            <button style={styles.clearBtn} onClick={clearChat} title="Clear chat">Clear</button>
            <button style={styles.closeBtn} onClick={() => setOpen(false)}>✖</button>
          </div>
        </div>

        {/* Messages */}
        <div style={styles.messages}>
          {messages.length === 0 && (
            <div style={styles.emptyState}>
              <div style={styles.emptyIcon}>🎓</div>
              <p style={{ fontWeight: 600, margin: "8px 0 4px" }}>Welcome to CKPCET Bot!</p>
              <p style={{ fontSize: 13, color: "#888", lineHeight: 1.5 }}>
                Ask me about admissions, fees, courses, placements, or facilities.
              </p>
              {faqs.length > 0 && (
                <button style={styles.faqToggle} onClick={() => setShowFAQs((s) => !s)}>
                  {showFAQs ? "Hide suggestions ▲" : "Show quick questions ▼"}
                </button>
              )}
              {showFAQs && (
                <div style={styles.inlineFAQs}>
                  {faqs.map((f, i) => (
                    <button
                      key={i}
                      style={styles.inlineFAQ}
                      onClick={() => sendMessage(f.question)}
                    >
                      {f.question}
                    </button>
                  ))}
                </div>
              )}
            </div>
          )}

          {messages.map((m, i) => (
            <MessageBubble key={i} msg={m} />
          ))}

          {loading && <LoadingDots />}
          <div ref={messagesEndRef} />
        </div>

        {/* Input */}
        <div style={styles.inputRow}>
          <input
            ref={inputRef}
            style={styles.inputField}
            value={input}
            placeholder="Ask about admissions…"
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && !e.shiftKey && (e.preventDefault(), sendMessage())}
          />
          <button
            style={{
              ...styles.iconBtn,
              ...(isListening ? styles.iconBtnListening : {}),
            }}
            onClick={startVoice}
            title={isListening ? "Stop listening" : "Voice input"}
          >
            🎤
          </button>
          <button
            style={{ ...styles.iconBtn, opacity: !input.trim() || loading ? 0.5 : 1 }}
            onClick={() => sendMessage()}
            disabled={!input.trim() || loading}
            title="Send"
          >
            ➤
          </button>
        </div>
      </div>
    </>
  );
}

// ─── Styles ──────────────────────────────────────────────────────────────────
const BLUE = "#033e7c";
const BLUE_DARK = "#022b5a";

const styles = {
  // Page
  page: { minHeight: "100vh", background: "#f4f6fb", fontFamily: "'Segoe UI', sans-serif", display: "flex", flexDirection: "column" },

  // Nav
  nav: { background: BLUE_DARK, color: "white", padding: "14px 32px", display: "flex", justifyContent: "space-between", alignItems: "center", position: "sticky", top: 0, zIndex: 100 },
  navBrand: { fontSize: 22, fontWeight: 800, letterSpacing: 1 },
  navLinks: { display: "flex", gap: 24 },
  navLink: { color: "rgba(255,255,255,0.85)", textDecoration: "none", fontSize: 14, fontWeight: 500 },

  // Hero
  hero: { background: `linear-gradient(135deg, ${BLUE_DARK}, ${BLUE})`, color: "white", padding: "64px 32px", display: "flex", flexWrap: "wrap", gap: 40, alignItems: "center", justifyContent: "center" },
  heroInner: { maxWidth: 560 },
  heroBadge: { background: "rgba(255,255,255,0.15)", display: "inline-block", padding: "6px 14px", borderRadius: 20, fontSize: 12, letterSpacing: 1, marginBottom: 18 },
  heroTitle: { fontSize: "clamp(26px, 4vw, 42px)", fontWeight: 800, lineHeight: 1.2, margin: "0 0 16px" },
  heroAccent: { color: "#76c7df" },
  heroSub: { fontSize: 16, opacity: 0.85, lineHeight: 1.7, margin: "0 0 28px" },
  heroCTA: { background: "white", color: BLUE, border: "none", padding: "14px 28px", borderRadius: 30, fontSize: 15, fontWeight: 700, cursor: "pointer", boxShadow: "0 6px 20px rgba(0,0,0,0.25)", transition: "transform 0.2s" },

  heroCard: { background: "rgba(255,255,255,0.1)", backdropFilter: "blur(12px)", border: "1px solid rgba(255,255,255,0.2)", borderRadius: 20, padding: "28px 36px", display: "flex", gap: 24, alignItems: "center" },
  cardStat: { display: "flex", flexDirection: "column", alignItems: "center", gap: 4 },
  cardNum: { fontSize: 28, fontWeight: 800 },
  cardLbl: { fontSize: 12, opacity: 0.8, textAlign: "center" },
  cardDivider: { width: 1, height: 48, background: "rgba(255,255,255,0.25)" },

  // FAQs (main page)
  faqSection: { maxWidth: 960, margin: "48px auto", padding: "0 24px", width: "100%" },
  faqHeading: { fontSize: 22, fontWeight: 700, color: BLUE_DARK, marginBottom: 20 },
  faqGrid: { display: "grid", gridTemplateColumns: "repeat(auto-fill, minmax(260px, 1fr))", gap: 14 },
  faqChip: { textAlign: "left", background: "rgba(3,62,124,0.04)", border: "1px solid rgba(3,62,124,0.2)", borderRadius: 12, padding: "14px 16px", cursor: "pointer", transition: "all 0.2s", display: "flex", flexDirection: "column", gap: 4 },
  faqChipLabel: { fontSize: 10, fontWeight: 700, color: BLUE, textTransform: "uppercase", letterSpacing: 0.5 },
  faqChipQ: { fontSize: 13, fontWeight: 600, color: "#222" },
  faqChipP: { fontSize: 12, color: "#777", lineHeight: 1.4 },

  // Footer
  footer: { textAlign: "center", padding: "20px", color: "#888", fontSize: 13, marginTop: "auto" },

  // FAB
  fab: { position: "fixed", bottom: 24, right: 24, width: 56, height: 56, borderRadius: "50%", background: `linear-gradient(135deg, ${BLUE}, ${BLUE_DARK})`, color: "white", fontSize: 22, border: "none", cursor: "pointer", zIndex: 9999, boxShadow: "0 8px 28px rgba(2,43,90,0.4)", transition: "all 0.3s ease", display: "flex", alignItems: "center", justifyContent: "center" },
  fabOpen: { background: "#555" },

  // Widget
  widget: { position: "fixed", bottom: 92, right: 24, width: 360, height: 500, background: "rgba(255,255,255,0.92)", backdropFilter: "blur(16px)", borderRadius: 20, boxShadow: "0 24px 60px rgba(0,0,0,0.22)", display: "flex", flexDirection: "column", overflow: "hidden", zIndex: 9998, opacity: 0, transform: "translateY(40px) scale(0.92)", pointerEvents: "none", transition: "all 0.35s cubic-bezier(0.25,0.8,0.25,1)" },
  widgetOpen: { opacity: 1, transform: "translateY(0) scale(1)", pointerEvents: "auto" },

  // Widget Header
  widgetHeader: { background: `linear-gradient(135deg, ${BLUE}, ${BLUE_DARK})`, color: "white", padding: "14px 16px", display: "flex", justifyContent: "space-between", alignItems: "center" },
  avatar: { width: 34, height: 34, background: "rgba(255,255,255,0.15)", borderRadius: "50%", display: "flex", alignItems: "center", justifyContent: "center", fontSize: 16 },

  clearBtn: { background: "rgba(255,255,255,0.12)", color: "white", border: "1px solid rgba(255,255,255,0.2)", padding: "4px 10px", borderRadius: 8, fontSize: 12, cursor: "pointer" },
  closeBtn: { background: "none", border: "none", color: "white", fontSize: 16, cursor: "pointer", padding: "2px 6px" },

  // Messages
  messages: { flex: 1, overflowY: "auto", padding: "14px", display: "flex", flexDirection: "column", gap: 8, background: "linear-gradient(to bottom, #f9f9f9, #f1f1f1)" },

  // Bubbles
  userBubble: { background: `linear-gradient(135deg, ${BLUE}, ${BLUE_DARK})`, color: "white", padding: "10px 14px", borderRadius: "18px 18px 4px 18px", maxWidth: "75%", fontSize: 14, boxShadow: "0 3px 8px rgba(0,0,0,0.15)", lineHeight: 1.5 },
  botBubble: { background: "white", color: "#333", padding: "10px 14px", borderRadius: "18px 18px 18px 4px", maxWidth: "75%", fontSize: 14, boxShadow: "0 3px 8px rgba(0,0,0,0.1)", lineHeight: 1.5, display: "flex", alignItems: "center", gap: 8 },

  // Loading
  loadingSpinner: { width: 10, height: 10, borderRadius: "50%", background: `linear-gradient(90deg, ${BLUE}, #4fc3f7)`, display: "inline-block", animation: "pulse 1s infinite ease-in-out", flexShrink: 0 },

  // Empty state
  emptyState: { textAlign: "center", padding: "24px 12px", color: "#555" },
  emptyIcon: { fontSize: 40, marginBottom: 8 },
  faqToggle: { marginTop: 14, background: "none", border: `1px solid ${BLUE}`, color: BLUE, padding: "6px 14px", borderRadius: 20, fontSize: 12, cursor: "pointer" },
  inlineFAQs: { display: "flex", flexDirection: "column", gap: 8, marginTop: 12, textAlign: "left" },
  inlineFAQ: { background: "white", border: "1px solid #dde", padding: "8px 12px", borderRadius: 10, fontSize: 13, textAlign: "left", cursor: "pointer", color: "#333" },

  // Input
  inputRow: { display: "flex", gap: 8, padding: "10px 12px", background: "rgba(255,255,255,0.95)", borderTop: "1px solid rgba(0,0,0,0.06)" },
  inputField: { flex: 1, padding: "10px 14px", borderRadius: 25, border: "1px solid #ddd", outline: "none", fontSize: 13, fontFamily: "inherit" },
  iconBtn: { width: 38, height: 38, borderRadius: "50%", background: `linear-gradient(135deg, ${BLUE}, ${BLUE_DARK})`, border: "none", color: "white", fontSize: 14, cursor: "pointer", display: "flex", alignItems: "center", justifyContent: "center", flexShrink: 0, transition: "transform 0.2s" },
  iconBtnListening: { background: "linear-gradient(135deg, #c00, #900)", animation: "pulse 1.5s infinite" },
};

const globalCSS = `
  @keyframes msgIn {
    from { opacity: 0; transform: translateY(10px) scale(0.95); }
    to   { opacity: 1; transform: translateY(0) scale(1); }
  }
  @keyframes pulse {
    0%,100% { transform: scale(1); }
    50%      { transform: scale(1.15); }
  }
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body { background: #f4f6fb; }
  ::-webkit-scrollbar { width: 5px; }
  ::-webkit-scrollbar-thumb { background: rgba(0,0,0,0.18); border-radius: 10px; }
`;