import { useNavigate } from "react-router-dom";
import Button from "../ui/Button";
import { ArrowRight } from "lucide-react";

export default function Footer() {
  const navigate = useNavigate();

  return (
    <footer style={{ borderTop: "1px solid var(--border-subtle)", padding: "4rem 2rem" }}>
      <div
        className="container-full"
        style={{
          display: "flex",
          alignItems: "center",
          justifyContent: "space-between",
          flexWrap: "wrap",
          gap: "2rem",
        }}
      >
        <div>
          <h3
            className="gradient-text"
            style={{ fontSize: "1.5rem", fontWeight: 800, marginBottom: "0.3rem" }}
          >
            SkillSync
          </h3>
          <p style={{ color: "var(--text-dim)", fontSize: "0.88rem" }}>
            AI-Powered Career Guide
          </p>
        </div>

        <Button onClick={() => navigate("/app")} icon={<ArrowRight size={16} />}>
          Try Now
        </Button>

        <p style={{ color: "var(--text-dimmer)", fontSize: "0.78rem" }}>
          &copy; {new Date().getFullYear()} SkillSync
          <br />
          Powered by open-source AI
        </p>
      </div>
    </footer>
  );
}
