import type { AppStep } from "../../types";

const STEPS: { key: AppStep; label: string }[] = [
  { key: "goal", label: "Goal" },
  { key: "profile", label: "Profile" },
  { key: "results", label: "Results" },
  { key: "roadmap", label: "Roadmap" },
];

const ORDER: Record<AppStep, number> = { goal: 0, profile: 1, results: 2, roadmap: 3 };

export default function StepProgress({ current }: { current: AppStep }) {
  const idx = ORDER[current];

  return (
    <nav className="step-progress" aria-label="Progress">
      {STEPS.map((s, i) => {
        const isCompleted = i < idx;
        const isActive = i === idx;
        return (
          <div className="step-progress-item" key={s.key}>
            {i > 0 && (
              <div
                className={`step-progress-line${isCompleted ? " completed" : ""}`}
              />
            )}
            <div style={{ display: "flex", flexDirection: "column", alignItems: "center" }}>
              <div
                className={`step-progress-dot${isActive ? " active" : ""}${isCompleted ? " completed" : ""}`}
                aria-current={isActive ? "step" : undefined}
              >
                {isCompleted ? "\u2713" : i + 1}
              </div>
              <span className="step-progress-label">{s.label}</span>
            </div>
          </div>
        );
      })}
    </nav>
  );
}
