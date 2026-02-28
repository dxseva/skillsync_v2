import { useNavigate } from "react-router-dom";
import { motion } from "framer-motion";
import Button from "../ui/Button";
import { ArrowRight, Sparkles, Globe, Cpu } from "lucide-react";

export default function Hero() {
  const navigate = useNavigate();

  return (
    <section
      style={{
        position: "relative",
        padding: "6rem 2rem 5rem",
        overflow: "hidden",
        minHeight: "90vh",
        display: "flex",
        alignItems: "center",
      }}
    >
      {/* Gradient wave orbs — soft blue & purple */}
      <div
        aria-hidden="true"
        style={{
          position: "absolute",
          top: "-10%",
          left: "-5%",
          width: 700,
          height: 700,
          background:
            "radial-gradient(ellipse, rgba(110,231,247,0.07) 0%, rgba(110,231,247,0.03) 40%, transparent 70%)",
          borderRadius: "50%",
          filter: "blur(80px)",
          pointerEvents: "none",
        }}
      />
      <div
        aria-hidden="true"
        style={{
          position: "absolute",
          top: "30%",
          right: "-10%",
          width: 600,
          height: 600,
          background:
            "radial-gradient(ellipse, rgba(167,139,250,0.08) 0%, rgba(167,139,250,0.03) 40%, transparent 70%)",
          borderRadius: "50%",
          filter: "blur(100px)",
          pointerEvents: "none",
        }}
      />
      <div
        aria-hidden="true"
        style={{
          position: "absolute",
          bottom: "0%",
          left: "30%",
          width: 500,
          height: 400,
          background:
            "radial-gradient(ellipse, rgba(110,231,247,0.05) 0%, rgba(167,139,250,0.03) 50%, transparent 70%)",
          borderRadius: "50%",
          filter: "blur(90px)",
          pointerEvents: "none",
        }}
      />

      <div className="container-full" style={{ position: "relative", zIndex: 1, width: "100%" }}>
        <div
          style={{
            display: "grid",
            gridTemplateColumns: "1fr 1fr",
            gap: "4rem",
            alignItems: "center",
          }}
        >
          {/* Left — text */}
          <motion.div
            initial={{ opacity: 0, x: -30 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.7, ease: "easeOut" }}
          >
            <motion.div
              initial={{ opacity: 0, y: -10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.15, duration: 0.5 }}
              style={{
                display: "inline-block",
                background: "var(--glass-bg)",
                backdropFilter: "blur(12px)",
                border: "1px solid var(--glass-border)",
                borderRadius: "var(--radius-full)",
                padding: "5px 16px",
                fontSize: "0.78rem",
                color: "var(--text-muted)",
                marginBottom: "1.5rem",
              }}
            >
              Powered by HH.ru API &middot; No sign-up required
            </motion.div>

            <h1
              className="gradient-text"
              style={{
                fontSize: "clamp(2.4rem, 5vw, 4rem)",
                fontWeight: 800,
                letterSpacing: "-2px",
                lineHeight: 1.08,
                marginBottom: "1.25rem",
              }}
            >
              Your AI Career
              <br />
              Guide
            </h1>

            <p
              style={{
                fontSize: "clamp(1rem, 1.8vw, 1.2rem)",
                color: "var(--text-secondary)",
                lineHeight: 1.65,
                marginBottom: "2.5rem",
                maxWidth: 520,
              }}
            >
              Find real vacancies from HH.ru, get AI-ranked matches based on
              semantic similarity, and build a personalized learning roadmap —
              all in one flow.
            </p>

            <div style={{ display: "flex", gap: "0.75rem", flexWrap: "wrap" }}>
              <Button
                onClick={() => navigate("/app")}
                icon={<ArrowRight size={18} />}
                style={{ fontSize: "1rem", padding: "0.75rem 2rem" }}
              >
                Get Started
              </Button>
              <Button
                variant="secondary"
                onClick={() => {
                  document
                    .getElementById("features")
                    ?.scrollIntoView({ behavior: "smooth" });
                }}
                style={{ fontSize: "1rem", padding: "0.75rem 2rem" }}
              >
                Learn More
              </Button>
            </div>
          </motion.div>

          {/* Right — feature highlights (glass cards) */}
          <motion.div
            initial={{ opacity: 0, x: 30 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.7, delay: 0.2, ease: "easeOut" }}
            style={{ display: "flex", flexDirection: "column", gap: "1.2rem" }}
          >
            {[
              {
                icon: Globe,
                title: "Live HH.ru Data",
                text: "Real-time vacancy search across Russia & CIS with maximum coverage.",
              },
              {
                icon: Cpu,
                title: "Semantic AI Matching",
                text: "Multilingual embeddings rank jobs by meaning — not just keywords.",
              },
              {
                icon: Sparkles,
                title: "Personal Roadmap",
                text: "Skill gap analysis with time estimates, curated resources, and learning plans.",
              },
            ].map((item, i) => (
              <motion.div
                key={item.title}
                initial={{ opacity: 0, y: 15 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.4 + i * 0.12, duration: 0.4 }}
                className="card"
                style={{
                  display: "flex",
                  gap: "1rem",
                  alignItems: "flex-start",
                }}
              >
                <div
                  style={{
                    background: "rgba(167, 139, 250, 0.1)",
                    borderRadius: "var(--radius-lg)",
                    padding: 10,
                    flexShrink: 0,
                    display: "flex",
                    alignItems: "center",
                    justifyContent: "center",
                  }}
                >
                  <item.icon size={22} color="var(--accent-purple)" />
                </div>
                <div>
                  <h3 style={{ fontSize: "0.95rem", fontWeight: 700, marginBottom: "0.2rem" }}>
                    {item.title}
                  </h3>
                  <p style={{ fontSize: "0.84rem", color: "var(--text-muted)", lineHeight: 1.55 }}>
                    {item.text}
                  </p>
                </div>
              </motion.div>
            ))}
          </motion.div>
        </div>
      </div>

      <style>{`
        @media (max-width: 768px) {
          section > .container-full > div {
            grid-template-columns: 1fr !important;
            gap: 2.5rem !important;
          }
        }
      `}</style>
    </section>
  );
}
