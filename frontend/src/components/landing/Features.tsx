import { motion } from "framer-motion";
import {
  Radio,
  Brain,
  Target,
  Map,
} from "lucide-react";

const features = [
  {
    icon: Radio,
    title: "Live Job Data",
    desc: "Real vacancies fetched from the HH.ru API — always up-to-date, never stale. Covers Russia and CIS region.",
  },
  {
    icon: Brain,
    title: "Semantic Matching",
    desc: "AI-powered ranking using multilingual embeddings — far beyond keyword matching. Understands context and meaning.",
  },
  {
    icon: Target,
    title: "Skill Gap Analysis",
    desc: "Vector similarity compares your skills against job requirements precisely, identifying exactly what to learn.",
  },
  {
    icon: Map,
    title: "Personal Roadmap",
    desc: "Step-by-step learning plan with time estimates, difficulty levels, and curated resources for each skill.",
  },
];

export default function Features() {
  return (
    <section id="features" className="wave-bg" style={{ padding: "6rem 2rem" }}>
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
              marginBottom: "0.6rem",
            }}
          >
            What makes it <span className="gradient-text">different</span>
          </h2>
          <p style={{ color: "var(--text-dim)", fontSize: "1rem", maxWidth: 560, margin: "0 auto" }}>
            Four powerful features working together to bridge the gap between you and your
            dream career.
          </p>
        </motion.div>

        <div
          style={{
            display: "grid",
            gridTemplateColumns: "repeat(2, 1fr)",
            gap: "1.25rem",
          }}
        >
          {features.map((f, i) => (
            <motion.div
              key={f.title}
              className="card"
              initial={{ opacity: 0, y: 24 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true, margin: "-40px" }}
              transition={{ delay: i * 0.07, duration: 0.4 }}
              style={{
                display: "flex",
                gap: "1rem",
                alignItems: "flex-start",
                padding: "1.5rem",
              }}
            >
              <div
                style={{
                  background: "rgba(167, 139, 250, 0.1)",
                  borderRadius: "var(--radius-lg)",
                  padding: 12,
                  flexShrink: 0,
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",
                }}
              >
                <f.icon size={24} color="var(--accent-purple)" />
              </div>
              <div>
                <h3 style={{ fontSize: "1.05rem", fontWeight: 700, marginBottom: "0.35rem" }}>
                  {f.title}
                </h3>
                <p style={{ fontSize: "0.88rem", color: "var(--text-muted)", lineHeight: 1.65 }}>
                  {f.desc}
                </p>
              </div>
            </motion.div>
          ))}
        </div>
      </div>

      <style>{`
        @media (max-width: 580px) {
          #features .container-full > div:last-child {
            grid-template-columns: 1fr !important;
          }
        }
      `}</style>
    </section>
  );
}
