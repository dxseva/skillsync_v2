export default function SkillChip({ skill }: { skill: string }) {
  return (
    <span
      style={{
        display: "inline-block",
        background: "rgba(74, 222, 128, 0.1)",
        color: "var(--accent-green)",
        border: "1px solid rgba(74, 222, 128, 0.2)",
        fontSize: "0.8rem",
        fontWeight: 500,
        padding: "3px 12px",
        borderRadius: "var(--radius-full)",
        margin: "2px",
      }}
    >
      &#10003; {skill}
    </span>
  );
}
