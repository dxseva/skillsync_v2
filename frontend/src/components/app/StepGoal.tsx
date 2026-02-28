import { useState, useEffect, useRef } from "react";
import StepBadge from "../ui/StepBadge";
import Button from "../ui/Button";
import { ArrowRight, Sparkles } from "lucide-react";

interface Props {
  initialGoal?: string;
  onNext: (goal: string) => void;
}

const SUGGESTIONS = ["Data Analyst", "UX Designer", "Backend Developer", "Marketing Manager"];

export default function StepGoal({ initialGoal = "", onNext }: Props) {
  const [goal, setGoal] = useState(initialGoal);
  const inputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    inputRef.current?.focus();
  }, []);

  const isValid = goal.trim().length >= 3;

  const submit = () => {
    if (isValid) onNext(goal.trim());
  };

  return (
    <div className="glass-panel" style={{ animation: "fadeInUp 0.5s ease" }}>
      <StepBadge step={1} label="YOUR GOAL" />

      <h2
        style={{
          fontSize: "1.5rem",
          fontWeight: 700,
          marginBottom: "0.5rem",
          color: "var(--text-primary)",
        }}
      >
        What career are you aiming for?
      </h2>

      <p
        style={{
          color: "var(--text-muted)",
          fontSize: "0.9rem",
          marginBottom: "1.5rem",
          lineHeight: 1.6,
        }}
      >
        Tell us in plain English — a role, a field, or even just a dream.
      </p>

      <input
        ref={inputRef}
        type="text"
        placeholder="e.g. I want to become a lawyer, data science, UX designer..."
        value={goal}
        onChange={(e) => setGoal(e.target.value)}
        onKeyDown={(e) => e.key === "Enter" && submit()}
        aria-label="Your career goal"
        style={{ marginBottom: "0.75rem" }}
      />

      {/* Quick suggestions */}
      <div
        style={{
          display: "flex",
          gap: "0.5rem",
          flexWrap: "wrap",
          marginBottom: "1.5rem",
        }}
      >
        <Sparkles size={14} color="var(--text-dim)" style={{ marginTop: 3 }} />
        {SUGGESTIONS.map((s) => (
          <button
            key={s}
            type="button"
            onClick={() => setGoal(s)}
            style={{
              background: goal === s ? "rgba(167, 139, 250, 0.15)" : "rgba(255, 255, 255, 0.04)",
              border: `1px solid ${goal === s ? "rgba(167, 139, 250, 0.3)" : "rgba(255, 255, 255, 0.08)"}`,
              color: goal === s ? "var(--accent-purple)" : "var(--text-dim)",
              padding: "4px 12px",
              borderRadius: "var(--radius-full)",
              fontSize: "0.78rem",
              cursor: "pointer",
              transition: "all 0.2s",
              fontFamily: "var(--font-body)",
            }}
          >
            {s}
          </button>
        ))}
      </div>

      <Button onClick={submit} disabled={!isValid} icon={<ArrowRight size={16} />}>
        Continue
      </Button>

      {goal.length > 0 && !isValid && (
        <p style={{ fontSize: "0.8rem", color: "var(--text-dim)", marginTop: "0.5rem" }}>
          Please enter at least 3 characters.
        </p>
      )}
    </div>
  );
}
