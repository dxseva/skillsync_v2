import { motion } from "framer-motion";

const techs = [
  { name: "SentenceTransformers", desc: "Multilingual embeddings for cross-language matching" },
  { name: "HH.ru API", desc: "Live vacancy data across Russia & CIS" },
  { name: "FastAPI", desc: "High-performance Python backend" },
  { name: "React + TypeScript", desc: "Modern, type-safe frontend" },
  { name: "PyTorch (CPU)", desc: "ML inference without GPU required" },
];

export default function TechStack() {
  return (
    <section style={{ padding: "6rem 2rem" }}>
      <div className="container-full">
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
              marginBottom: "0.6rem",
            }}
          >
            Built with <span className="gradient-text">modern tools</span>
          </h2>
          <p style={{ color: "var(--text-dim)", fontSize: "1rem" }}>
            Production-grade open-source stack — no paid APIs required.
          </p>
        </motion.div>

        <div
          style={{
            display: "grid",
            gridTemplateColumns: "repeat(5, 1fr)",
            gap: "1.25rem",
          }}
        >
          {techs.map((t, i) => (
            <motion.div
              key={t.name}
              className="card"
              initial={{ opacity: 0, scale: 0.92 }}
              whileInView={{ opacity: 1, scale: 1 }}
              viewport={{ once: true }}
              transition={{ delay: i * 0.06, duration: 0.35 }}
              style={{
                textAlign: "center",
                padding: "1.5rem 1rem",
              }}
            >
              <h4 style={{ fontSize: "0.95rem", fontWeight: 700, marginBottom: "0.35rem" }}>
                {t.name}
              </h4>
              <p style={{ fontSize: "0.82rem", color: "var(--text-muted)", lineHeight: 1.5 }}>
                {t.desc}
              </p>
            </motion.div>
          ))}
        </div>
      </div>

      <style>{`
        @media (max-width: 900px) {
          section > .container-full > div:last-child {
            grid-template-columns: repeat(3, 1fr) !important;
          }
        }
        @media (max-width: 520px) {
          section > .container-full > div:last-child {
            grid-template-columns: repeat(2, 1fr) !important;
          }
        }
      `}</style>
    </section>
  );
}
