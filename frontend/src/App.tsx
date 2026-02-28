import { BrowserRouter, Routes, Route, Link } from "react-router-dom";
import Navbar from "./components/ui/Navbar";
import LandingPage from "./pages/LandingPage";
import AppFlow from "./pages/AppFlow";

function NotFound() {
  return (
    <div
      className="container"
      style={{
        textAlign: "center",
        paddingTop: "6rem",
        paddingBottom: "4rem",
      }}
    >
      <h1
        className="gradient-text"
        style={{ fontSize: "4rem", fontWeight: 800, marginBottom: "0.5rem" }}
      >
        404
      </h1>
      <p style={{ color: "var(--text-muted)", fontSize: "1.1rem", marginBottom: "2rem" }}>
        Page not found
      </p>
      <Link
        to="/"
        style={{
          display: "inline-flex",
          alignItems: "center",
          gap: "0.5rem",
          background: "var(--gradient-button)",
          color: "var(--bg-primary)",
          fontFamily: "var(--font-heading)",
          fontWeight: 700,
          fontSize: "0.9rem",
          padding: "0.65rem 1.5rem",
          borderRadius: "var(--radius-lg)",
          textDecoration: "none",
        }}
      >
        Back to Home
      </Link>
    </div>
  );
}

export default function App() {
  return (
    <BrowserRouter>
      <Navbar />
      <Routes>
        <Route path="/" element={<LandingPage />} />
        <Route path="/app" element={<AppFlow />} />
        <Route path="*" element={<NotFound />} />
      </Routes>
    </BrowserRouter>
  );
}
