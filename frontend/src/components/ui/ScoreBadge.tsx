export default function ScoreBadge({ score }: { score: number }) {
  const clamped = Math.max(0, Math.min(100, Math.round(score)));
  const bg =
    clamped >= 70
      ? "var(--accent-green)"
      : clamped >= 50
        ? "var(--accent-yellow)"
        : "var(--accent-red)";

  return (
    <span
      aria-label={`Match score ${clamped}%`}
      style={{
        position: "absolute",
        top: "1rem",
        right: "1rem",
        fontFamily: "var(--font-heading)",
        fontWeight: 700,
        fontSize: "0.85rem",
        padding: "3px 11px",
        borderRadius: "var(--radius-full)",
        color: "var(--bg-primary)",
        background: bg,
      }}
    >
      {clamped}%
    </span>
  );
}
