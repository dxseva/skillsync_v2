import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { ChevronDown } from "lucide-react";

const items = [
  {
    q: "Is it free?",
    a: "Yes — completely free. No sign-up, no API key required. HH.ru's public API is used for job data.",
  },
  {
    q: "What job markets does it cover?",
    a: "HH.ru is the largest job board in Russia and CIS countries (Belarus, Kazakhstan, Uzbekistan, etc.).",
  },
  {
    q: "How accurate is the matching?",
    a: "We use a state-of-the-art multilingual embedding model that understands meaning across languages — far beyond simple keyword matching.",
  },
  {
    q: "How long does the first search take?",
    a: "The first search may take 30-60 seconds because ML models (~500MB) need to be downloaded and loaded. After that, searches are much faster.",
  },
  {
    q: "Can I use it on mobile?",
    a: "Yes, the interface is fully responsive and works on all devices — phones, tablets, and desktops.",
  },
  {
    q: "Do I need any setup?",
    a: "Just run the backend and frontend servers. No database, no external API keys, no authentication required.",
  },
];

export default function FAQ() {
  const [open, setOpen] = useState<number | null>(null);

  return (
    <section className="wave-bg" style={{ padding: "6rem 2rem", background: "var(--bg-secondary)" }}>
      <div className="container-full" style={{ position: "relative", zIndex: 1 }}>
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.5 }}
          style={{ textAlign: "center", marginBottom: "3.5rem" }}
        >
          <h2
            style={{
              fontSize: "clamp(1.8rem, 4vw, 2.4rem)",
              fontWeight: 700,
            }}
          >
            Frequently asked <span className="gradient-text">questions</span>
          </h2>
        </motion.div>

        <div
          style={{
            display: "grid",
            gridTemplateColumns: "repeat(2, 1fr)",
            gap: "0.75rem",
          }}
        >
          {items.map((item, i) => {
            const isOpen = open === i;
            return (
              <motion.div
                key={i}
                className="card"
                initial={{ opacity: 0, y: 12 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: i * 0.04 }}
                style={{ cursor: "pointer", padding: "1.1rem 1.4rem", alignSelf: "start" }}
                onClick={() => setOpen(isOpen ? null : i)}
                role="button"
                aria-expanded={isOpen}
                tabIndex={0}
                onKeyDown={(e) => {
                  if (e.key === "Enter" || e.key === " ") {
                    e.preventDefault();
                    setOpen(isOpen ? null : i);
                  }
                }}
              >
                <div
                  style={{
                    display: "flex",
                    justifyContent: "space-between",
                    alignItems: "center",
                    gap: "1rem",
                  }}
                >
                  <h3 style={{ fontSize: "0.95rem", fontWeight: 700 }}>
                    {item.q}
                  </h3>
                  <ChevronDown
                    size={18}
                    color="var(--text-dim)"
                    style={{
                      transform: isOpen ? "rotate(180deg)" : "rotate(0deg)",
                      transition: "transform 0.25s",
                      flexShrink: 0,
                    }}
                    aria-hidden="true"
                  />
                </div>
                <AnimatePresence>
                  {isOpen && (
                    <motion.p
                      initial={{ height: 0, opacity: 0 }}
                      animate={{ height: "auto", opacity: 1 }}
                      exit={{ height: 0, opacity: 0 }}
                      transition={{ duration: 0.25 }}
                      style={{
                        fontSize: "0.87rem",
                        color: "var(--text-muted)",
                        lineHeight: 1.65,
                        marginTop: "0.6rem",
                        overflow: "hidden",
                      }}
                    >
                      {item.a}
                    </motion.p>
                  )}
                </AnimatePresence>
              </motion.div>
            );
          })}
        </div>
      </div>

      <style>{`
        @media (max-width: 700px) {
          section > .container-full > div:last-child {
            grid-template-columns: 1fr !important;
          }
        }
      `}</style>
    </section>
  );
}
