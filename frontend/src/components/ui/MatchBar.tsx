export default function MatchBar({ score }: { score: number }) {
  const width = Math.max(0, Math.min(score, 100));
  return (
    <div style={{ margin: "0.5rem 0" }} role="progressbar" aria-valuenow={width} aria-valuemin={0} aria-valuemax={100} aria-label={`Match score ${width}%`}>
      <div
        style={{
          background: "var(--border-primary)",
          borderRadius: "var(--radius-sm)",
          height: 6,
          width: "100%",
        }}
      >
        <div
          style={{
            borderRadius: "var(--radius-sm)",
            height: 6,
            width: `${width}%`,
            background: "var(--gradient-bar)",
            transition: "width 0.6s ease",
          }}
        />
      </div>
    </div>
  );
}
