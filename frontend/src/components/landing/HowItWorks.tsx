import { motion } from "framer-motion";
import { Crosshair, UserRound, Briefcase, Route } from "lucide-react";

const steps = [
  {
    icon: Crosshair,
    title: "Set Your Goal",
    desc: "Tell us your dream career in plain English — a role, a field, or even just a passion.",
  },
  {
    icon: UserRound,
    title: "Build Profile",
    desc: "Share your skills, study year, preferred city and work format. Takes 30 seconds.",
  },
  {
    icon: Briefcase,
    title: "Get Matches",
    desc: "We fetch live vacancies, rank them by AI-powered semantic similarity, and show the best fits.",
  },
  {
    icon: Route,
    title: "Follow Roadmap",
    desc: "Pick a vacancy and get a personalized learning plan with time estimates and curated resources.",
  },
];

export default function HowItWorks() {
  return (
    <section style={{ padding: "6rem 2rem", background: "var(--bg-secondary)" }}>
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
            How it <span className="gradient-text">works</span>
          </h2>
          <p style={{ color: "var(--text-dim)", fontSize: "1rem" }}>
            Four simple steps from career idea to actionable plan.
          </p>
        </motion.div>

        <div
          style={{
            display: "grid",
            gridTemplateColumns: "repeat(4, 1fr)",
            gap: "2rem",
          }}
        >
          {steps.map((s, i) => (
            <motion.div
              key={s.title}
              initial={{ opacity: 0, y: 25 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true, margin: "-30px" }}
              transition={{ delay: i * 0.1, duration: 0.45 }}
              style={{ textAlign: "center" }}
            >
              <div
                style={{
                  width: 64,
                  height: 64,
                  borderRadius: "50%",
                  background: "var(--gradient-badge)",
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",
                  margin: "0 auto 1rem",
                  boxShadow: "0 0 30px rgba(110, 231, 247, 0.1)",
                }}
              >
                <s.icon size={28} color="var(--bg-primary)" />
              </div>
              <span
                style={{
                  fontSize: "0.72rem",
                  color: "var(--text-dim)",
                  fontWeight: 600,
                  letterSpacing: "1px",
                  textTransform: "uppercase",
                }}
              >
                Step {i + 1}
              </span>
              <h3 style={{ fontSize: "1.15rem", fontWeight: 700, margin: "0.35rem 0 0.5rem" }}>
                {s.title}
              </h3>
              <p style={{ fontSize: "0.88rem", color: "var(--text-muted)", lineHeight: 1.65 }}>
                {s.desc}
              </p>
            </motion.div>
          ))}
        </div>
      </div>

      <style>{`
        @media (max-width: 900px) {
          section > .container-full > div:last-child {
            grid-template-columns: repeat(2, 1fr) !important;
          }
        }
        @media (max-width: 520px) {
          section > .container-full > div:last-child {
            grid-template-columns: 1fr !important;
          }
        }
      `}</style>
    </section>
  );
}
