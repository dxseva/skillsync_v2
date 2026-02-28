import { useEffect, useState, useRef, useCallback } from "react";
import type { Job, Roadmap } from "../../types";
import { generateRoadmap } from "../../api/client";
import StepBadge from "../ui/StepBadge";
import InfoBox from "../ui/InfoBox";
import Button from "../ui/Button";
import ProgressRing from "../ui/ProgressRing";
import RoadmapStepComp from "./RoadmapStep";
import SkillChip from "./SkillChip";
import { ArrowLeft, RefreshCw, Search } from "lucide-react";

interface Props {
  job: Job;
  userSkills: string;
  skillLevel: string;
  onBackToResults: () => void;
  onNewSearch: () => void;
}

export default function StepRoadmap({
  job,
  userSkills,
  skillLevel,
  onBackToResults,
  onNewSearch,
}: Props) {
  const [roadmap, setRoadmap] = useState<Roadmap | null>(null);
  const [loading, setLoading] = useState(true);
  const [fetchDone, setFetchDone] = useState(false);
  const [error, setError] = useState("");
  const fetched = useRef(false);

  const doFetch = useCallback(() => {
    setFetchDone(false);
    setError("");
    setRoadmap(null);
    generateRoadmap(job, userSkills, undefined, skillLevel)
      .then(setRoadmap)
      .catch((err) => setError(err.message))
      .finally(() => setFetchDone(true));
  }, [job, userSkills, skillLevel]);

  useEffect(() => {
    if (fetched.current) return;
    fetched.current = true;
    setLoading(true);
    doFetch();
  }, [doFetch]);

  if (loading) {
    return (
      <div className="glass-panel" style={{ animation: "fadeInUp 0.5s ease" }}>
        <StepBadge step={4} label="YOUR PERSONAL ROADMAP" />
        <ProgressRing
          active={!fetchDone}
          onComplete={() => setLoading(false)}
        />
      </div>
    );
  }

  if (error || !roadmap) {
    return (
      <div className="glass-panel" style={{ animation: "fadeInUp 0.5s ease" }}>
        <StepBadge step={4} label="YOUR PERSONAL ROADMAP" />
        <InfoBox variant="error">
          <strong>Error:</strong> {error || "Failed to generate roadmap."}
        </InfoBox>
        <div style={{ display: "flex", gap: "0.75rem", flexWrap: "wrap" }}>
          <Button onClick={() => { fetched.current = false; setLoading(true); doFetch(); }} icon={<RefreshCw size={15} />}>
            Try Again
          </Button>
          <Button variant="secondary" onClick={onBackToResults} icon={<ArrowLeft size={15} />}>
            Choose different vacancy
          </Button>
        </div>
      </div>
    );
  }

  return (
    <div className="glass-panel" style={{ animation: "fadeInUp 0.5s ease" }}>
      <StepBadge step={4} label="YOUR PERSONAL ROADMAP" />

      <h2 style={{ fontSize: "1.4rem", fontWeight: 700, marginBottom: "0.5rem" }}>
        Roadmap to: {roadmap.job_title}
      </h2>

      <div
        style={{
          display: "flex",
          gap: "1.5rem",
          flexWrap: "wrap",
          marginBottom: "1.5rem",
          fontSize: "0.88rem",
        }}
      >
        <div>
          <span style={{ color: "var(--text-dim)" }}>Current match</span>
          <br />
          <span style={{ fontWeight: 700, fontSize: "1.1rem", color: "var(--accent-cyan)" }}>
            {job.match_score}%
          </span>
        </div>
        <div>
          <span style={{ color: "var(--text-dim)" }}>After roadmap</span>
          <br />
          <span style={{ fontWeight: 700, fontSize: "1.1rem", color: "var(--accent-green)" }}>
            {roadmap.match_after_preparation}
          </span>
        </div>
        <div>
          <span style={{ color: "var(--text-dim)" }}>Estimated time</span>
          <br />
          <span style={{ fontWeight: 700, fontSize: "1.1rem", color: "var(--accent-purple)" }}>
            {roadmap.total_estimated_time}
          </span>
        </div>
      </div>

      {roadmap.already_strong.length > 0 && (
        <div style={{ marginBottom: "1.5rem" }}>
          <h3
            style={{
              fontSize: "1rem",
              fontWeight: 700,
              marginBottom: "0.5rem",
              color: "var(--accent-green)",
            }}
          >
            Skills you already have
          </h3>
          <div style={{ display: "flex", flexWrap: "wrap", gap: "4px" }}>
            {roadmap.already_strong.map((s) => (
              <SkillChip key={s} skill={s} />
            ))}
          </div>
        </div>
      )}

      {roadmap.roadmap_steps.length > 0 ? (
        <>
          <h3 style={{ fontSize: "1rem", fontWeight: 700, marginBottom: "0.75rem" }}>
            Skills to develop ({roadmap.roadmap_steps.length})
          </h3>
          {roadmap.roadmap_steps.map((step, i) => (
            <RoadmapStepComp key={i} step={step} />
          ))}
          <InfoBox style={{ marginTop: "1.5rem" }}>
            <strong>Note:</strong> {roadmap.notes}
          </InfoBox>
        </>
      ) : (
        <InfoBox variant="success">
          <strong>You look like a strong candidate already!</strong>{" "}
          Focus on polishing your CV, practicing interviews, and networking.
          Apply now!
        </InfoBox>
      )}

      <hr className="divider" />
      <div style={{ display: "flex", gap: "0.75rem", flexWrap: "wrap" }}>
        <Button variant="secondary" onClick={onBackToResults} icon={<ArrowLeft size={15} />}>
          Different vacancy
        </Button>
        <Button variant="secondary" onClick={onNewSearch} icon={<Search size={15} />}>
          New search
        </Button>
        <Button
          variant="secondary"
          onClick={() => { fetched.current = false; setLoading(true); doFetch(); }}
          icon={<RefreshCw size={15} />}
        >
          Regenerate
        </Button>
      </div>
    </div>
  );
}
