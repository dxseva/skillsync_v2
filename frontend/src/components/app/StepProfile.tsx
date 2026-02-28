import { useState, useEffect } from "react";
import type { Profile } from "../../types";
import { getCities } from "../../api/client";
import StepBadge from "../ui/StepBadge";
import Button from "../ui/Button";
import { ArrowRight, ArrowLeft, AlertCircle } from "lucide-react";

interface Props {
  goal: string;
  initialProfile?: Profile;
  onNext: (profile: Profile) => void;
  onBack: () => void;
}

const DEFAULT_CITIES = [
  "Any city", "Москва", "Санкт-Петербург", "Новосибирск", "Екатеринбург",
  "Казань", "Нижний Новгород", "Ташкент", "Алматы", "Минск",
];

export default function StepProfile({ goal, initialProfile, onNext, onBack }: Props) {
  const [cities, setCities] = useState<string[]>(DEFAULT_CITIES);
  const [citiesLoading, setCitiesLoading] = useState(true);
  const [citiesError, setCitiesError] = useState(false);
  const [skills, setSkills] = useState(initialProfile?.skills ?? "");
  const [skillLevel, setSkillLevel] = useState(initialProfile?.skill_level ?? "intermediate");
  const [year, setYear] = useState(initialProfile?.year ?? 3);
  const [city, setCity] = useState(initialProfile?.city ?? "Any city");
  const [format, setFormat] = useState(initialProfile?.format ?? "any");
  const [relocation, setRelocation] = useState(initialProfile?.relocation ?? false);

  useEffect(() => {
    let cancelled = false;
    setCitiesLoading(true);
    getCities()
      .then((c) => {
        if (!cancelled) {
          setCities(c);
          setCitiesError(false);
        }
      })
      .catch(() => {
        if (!cancelled) setCitiesError(true);
      })
      .finally(() => {
        if (!cancelled) setCitiesLoading(false);
      });
    return () => { cancelled = true; };
  }, []);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onNext({ skills, skill_level: skillLevel, year, city, format, relocation });
  };

  return (
    <div className="glass-panel" style={{ animation: "fadeInUp 0.5s ease" }}>
      <StepBadge step={2} label="YOUR PROFILE" />

      <h2 style={{ fontSize: "1.5rem", fontWeight: 700, marginBottom: "0.3rem" }}>
        Tell us about yourself
      </h2>

      <p style={{ color: "var(--text-muted)", fontSize: "0.88rem", marginBottom: "0.25rem" }}>
        Goal: <span style={{ color: "var(--accent-cyan)", fontWeight: 600 }}>{goal}</span>
      </p>
      <p style={{ color: "var(--text-dim)", fontSize: "0.82rem", marginBottom: "1.5rem" }}>
        A few quick questions to find the best-matching vacancies.
      </p>

      {citiesError && (
        <div
          style={{
            background: "rgba(248, 113, 113, 0.08)",
            border: "1px solid rgba(248, 113, 113, 0.2)",
            borderRadius: "var(--radius-lg)",
            padding: "0.75rem 1rem",
            fontSize: "0.82rem",
            color: "var(--accent-red)",
            marginBottom: "1rem",
            display: "flex",
            alignItems: "center",
            gap: "0.5rem",
          }}
        >
          <AlertCircle size={14} />
          Could not load cities. Using default list.
        </div>
      )}

      <form
        onSubmit={handleSubmit}
        style={{ display: "flex", flexDirection: "column", gap: "1.25rem" }}
      >
        <div>
          <label htmlFor="skills">Your skills & experience</label>
          <textarea
            id="skills"
            rows={3}
            placeholder="e.g. Python, React, completed internship at a tech company, English B2..."
            value={skills}
            onChange={(e) => setSkills(e.target.value)}
          />
        </div>

        <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "1rem" }}>
          <div>
            <label htmlFor="skill-level">Skill level</label>
            <select
              id="skill-level"
              value={skillLevel}
              onChange={(e) => setSkillLevel(e.target.value)}
            >
              <option value="beginner">Beginner</option>
              <option value="intermediate">Intermediate</option>
              <option value="advanced">Advanced</option>
            </select>
          </div>

          <div>
            <label htmlFor="year">Study status</label>
            <select id="year" value={year} onChange={(e) => setYear(Number(e.target.value))}>
              <option value={0}>Graduate</option>
              {[1, 2, 3, 4, 5, 6].map((y) => (
                <option key={y} value={y}>Year {y}</option>
              ))}
            </select>
          </div>
        </div>

        <div>
          <label htmlFor="city">
            Preferred city
            {citiesLoading && (
              <span
                style={{
                  display: "inline-block",
                  width: 12,
                  height: 12,
                  border: "2px solid var(--border-primary)",
                  borderTopColor: "var(--accent-purple)",
                  borderRadius: "50%",
                  animation: "spin 0.7s linear infinite",
                  marginLeft: 6,
                  verticalAlign: "middle",
                }}
                aria-label="Loading cities"
              />
            )}
          </label>
          <select id="city" value={city} onChange={(e) => setCity(e.target.value)} disabled={citiesLoading}>
            {cities.map((c) => (
              <option key={c} value={c}>{c}</option>
            ))}
          </select>

          {/* Toggle switch — relocate */}
          <div
            className="toggle-wrap"
            style={{ marginTop: "0.6rem" }}
            onClick={() => setRelocation(!relocation)}
            role="switch"
            aria-checked={relocation}
            tabIndex={0}
            onKeyDown={(e) => {
              if (e.key === " " || e.key === "Enter") {
                e.preventDefault();
                setRelocation(!relocation);
              }
            }}
          >
            <div className={`toggle-track${relocation ? " active" : ""}`}>
              <div className="toggle-thumb" />
            </div>
            <span className={`toggle-label${relocation ? " active" : ""}`}>
              I'm willing to relocate
            </span>
          </div>
        </div>

        <div>
          <label htmlFor="format">Work format</label>
          <select id="format" value={format} onChange={(e) => setFormat(e.target.value)}>
            <option value="any">Any format</option>
            <option value="remote">Remote only</option>
            <option value="office">Office only</option>
            <option value="hybrid">Hybrid</option>
          </select>
        </div>

        <div style={{ display: "flex", gap: "0.75rem", flexWrap: "wrap", marginTop: "0.25rem" }}>
          <Button type="submit" icon={<ArrowRight size={16} />}>
            Find matching vacancies
          </Button>
          <Button variant="ghost" type="button" onClick={onBack} icon={<ArrowLeft size={16} />}>
            Back
          </Button>
        </div>
      </form>
    </div>
  );
}
