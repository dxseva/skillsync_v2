export default function Spinner({ text = "Loading..." }: { text?: string }) {
  return (
    <div
      role="status"
      aria-live="polite"
      style={{
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "center",
        padding: "4rem 1rem",
        gap: "1.2rem",
      }}
    >
      <div
        aria-hidden="true"
        style={{
          width: 44,
          height: 44,
          border: "3px solid var(--border-primary)",
          borderTopColor: "var(--accent-purple)",
          borderRadius: "50%",
          animation: "spin 0.8s linear infinite",
        }}
      />
      <p style={{ color: "var(--text-muted)", fontSize: "0.92rem", textAlign: "center" }}>
        {text}
      </p>
      <style>{`@keyframes spin { to { transform: rotate(360deg); } }`}</style>
    </div>
  );
}
