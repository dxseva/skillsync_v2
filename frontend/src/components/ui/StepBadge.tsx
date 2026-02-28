interface StepBadgeProps {
  step: number;
  label: string;
}

export default function StepBadge({ step, label }: StepBadgeProps) {
  return (
    <span
      role="status"
      style={{
        display: "inline-block",
        background: "linear-gradient(135deg, rgba(110, 231, 247, 0.15), rgba(167, 139, 250, 0.15))",
        border: "1px solid rgba(167, 139, 250, 0.2)",
        color: "var(--accent-cyan)",
        fontFamily: "var(--font-heading)",
        fontWeight: 700,
        fontSize: "0.72rem",
        padding: "4px 14px",
        borderRadius: "var(--radius-full)",
        letterSpacing: "0.5px",
        marginBottom: "1rem",
      }}
    >
      STEP {step} / 4 — {label}
    </span>
  );
}
