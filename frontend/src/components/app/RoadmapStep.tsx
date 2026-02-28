import type { RoadmapStep as RoadmapStepType } from "../../types";

export default function RoadmapStep({ step }: { step: RoadmapStepType }) {
  const isImprove = step.status === "Improve";
  const statusColor = isImprove ? "var(--accent-yellow)" : "var(--accent-red)";
  const statusLabel = isImprove ? "Improve" : "Learn from scratch";

  return (
    <div
      style={{
        background: "rgba(255, 255, 255, 0.03)",
        backdropFilter: "blur(8px)",
        borderLeft: "3px solid var(--accent-purple)",
        borderRadius: "0 var(--radius-lg) var(--radius-lg) 0",
        padding: "1rem 1.25rem",
        marginBottom: "0.6rem",
        transition: "background 0.2s",
      }}
    >
      <div
        style={{
          display: "flex",
          flexWrap: "wrap",
          alignItems: "center",
          gap: "0.5rem",
        }}
      >
        <span
          style={{
            fontFamily: "var(--font-heading)",
            fontWeight: 700,
            fontSize: "0.95rem",
            color: "var(--text-primary)",
          }}
        >
          {step.skill}
        </span>
        <span
          style={{
            background: "rgba(167, 139, 250, 0.12)",
            color: "var(--accent-purple)",
            fontSize: "0.75rem",
            fontWeight: 600,
            padding: "2px 10px",
            borderRadius: "var(--radius-full)",
            border: "1px solid rgba(167, 139, 250, 0.2)",
          }}
        >
          {step.estimated_time}
        </span>
        <span style={{ color: statusColor, fontSize: "0.75rem", fontWeight: 600 }}>
          &#x25CF; {statusLabel} &middot; {step.level} &middot;{" "}
          {step.current_match_pct}%
        </span>
      </div>

      <p
        style={{
          fontSize: "0.85rem",
          color: "var(--text-secondary)",
          marginTop: "0.4rem",
          lineHeight: 1.55,
        }}
      >
        {step.suggested_actions}
      </p>

      <p style={{ fontSize: "0.78rem", color: "var(--text-dim)", marginTop: "0.3rem" }}>
        Resources: {step.resources}
      </p>
    </div>
  );
}
