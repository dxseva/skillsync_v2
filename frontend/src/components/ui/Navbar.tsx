import { Link, useLocation } from "react-router-dom";
import Button from "./Button";

export default function Navbar() {
  const location = useLocation();
  const isApp = location.pathname === "/app";

  return (
    <nav
      style={{
        position: "sticky",
        top: 0,
        zIndex: 100,
        background: "rgba(11, 15, 26, 0.7)",
        backdropFilter: "blur(16px)",
        WebkitBackdropFilter: "blur(16px)",
        borderBottom: "1px solid var(--border-subtle)",
        padding: "0.65rem 1.5rem",
        display: "flex",
        alignItems: "center",
        justifyContent: "space-between",
      }}
    >
      <Link
        to="/"
        style={{
          fontFamily: "var(--font-heading)",
          fontWeight: 800,
          fontSize: "1.15rem",
          textDecoration: "none",
        }}
      >
        <span className="gradient-text">SkillSync</span>
      </Link>

      {!isApp && (
        <Link to="/app" style={{ textDecoration: "none" }}>
          <Button style={{ padding: "0.4rem 1.2rem", fontSize: "0.82rem" }}>
            Launch App
          </Button>
        </Link>
      )}
      {isApp && (
        <Link
          to="/"
          style={{
            fontSize: "0.85rem",
            color: "var(--text-dim)",
            textDecoration: "none",
          }}
        >
          &larr; Back to Home
        </Link>
      )}
    </nav>
  );
}
