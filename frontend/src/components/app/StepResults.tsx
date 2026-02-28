import { useEffect, useState, useRef, useCallback } from "react";
import type { Job, Profile } from "../../types";
import { searchJobs } from "../../api/client";
import StepBadge from "../ui/StepBadge";
import InfoBox from "../ui/InfoBox";
import Button from "../ui/Button";
import ProgressRing from "../ui/ProgressRing";
import JobCard from "./JobCard";
import { ArrowRight, ArrowLeft, RefreshCw } from "lucide-react";

interface Props {
  goal: string;
  profile: Profile;
  cachedJobs?: Job[];
  onSelectJob: (job: Job) => void;
  onJobsLoaded: (jobs: Job[]) => void;
  onBack: () => void;
}

export default function StepResults({
  goal,
  profile,
  cachedJobs,
  onSelectJob,
  onJobsLoaded,
  onBack,
}: Props) {
  const [jobs, setJobs] = useState<Job[]>(cachedJobs || []);
  const [loading, setLoading] = useState(!cachedJobs?.length);
  const [fetchDone, setFetchDone] = useState(false);
  const [error, setError] = useState("");
  const [selectedIdx, setSelectedIdx] = useState(0);
  const fetched = useRef(false);

  const doSearch = useCallback(() => {
    setFetchDone(false);
    searchJobs(goal, profile)
      .then((res) => {
        if (!res.jobs.length) {
          setError(
            res.message ||
            "No vacancies found. Try broadening your goal or adjusting filters."
          );
        }
        setJobs(res.jobs);
        onJobsLoaded(res.jobs);
      })
      .catch((err) => setError(err.message))
      .finally(() => setFetchDone(true));
  }, [goal, profile, onJobsLoaded]);

  useEffect(() => {
    if (cachedJobs?.length || fetched.current) return;
    fetched.current = true;
    setLoading(true);
    setError("");
    doSearch();
  }, [cachedJobs, doSearch]);

  const handleRetry = () => {
    fetched.current = false;
    setJobs([]);
    setError("");
    setSelectedIdx(0);
    setLoading(true);
    doSearch();
  };

  if (loading) {
    return (
      <div className="glass-panel" style={{ animation: "fadeInUp 0.5s ease" }}>
        <StepBadge step={3} label="MATCHING VACANCIES" />
        <ProgressRing
          active={!fetchDone}
          onComplete={() => setLoading(false)}
        />
      </div>
    );
  }

  if (error && !jobs.length) {
    return (
      <div className="glass-panel" style={{ animation: "fadeInUp 0.5s ease" }}>
        <StepBadge step={3} label="MATCHING VACANCIES" />
        <InfoBox variant="error">
          <strong>Error:</strong> {error}
        </InfoBox>
        <InfoBox>
          <strong>Tips:</strong>
          <ul style={{ margin: "0.5rem 0 0 1.2rem", lineHeight: 1.8 }}>
            <li>Broaden your goal (e.g. "lawyer" instead of "tax lawyer")</li>
            <li>Change city to "Any city"</li>
            <li>Change work format to "Any format"</li>
            <li>Check that the backend server is running</li>
          </ul>
        </InfoBox>
        <div style={{ display: "flex", gap: "0.75rem", flexWrap: "wrap" }}>
          <Button onClick={handleRetry} icon={<RefreshCw size={15} />}>
            Try Again
          </Button>
          <Button variant="secondary" onClick={onBack} icon={<ArrowLeft size={15} />}>
            Adjust filters
          </Button>
        </div>
      </div>
    );
  }

  return (
    <div className="glass-panel" style={{ animation: "fadeInUp 0.5s ease" }}>
      <StepBadge step={3} label="MATCHING VACANCIES" />
      <h2 style={{ fontSize: "1.4rem", fontWeight: 700, marginBottom: "0.5rem" }}>
        Top {jobs.length} Vacancies for You
      </h2>
      <p
        style={{
          color: "var(--text-muted)",
          fontSize: "0.85rem",
          marginBottom: "1.25rem",
        }}
      >
        Goal: <span style={{ color: "var(--accent-cyan)", fontWeight: 600 }}>{goal}</span>
        {" "}&middot;{" "}
        <strong>{jobs.length}</strong> matches &middot; Ranked by AI similarity
      </p>

      {jobs.map((job, i) => (
        <JobCard key={job.id} job={job} index={i + 1} />
      ))}

      <hr className="divider" />

      <h3 style={{ fontSize: "1.1rem", fontWeight: 700, marginBottom: "0.5rem" }}>
        Build your personal roadmap
      </h3>
      <p style={{ fontSize: "0.85rem", color: "var(--text-muted)", marginBottom: "1rem" }}>
        Choose the vacancy that interests you most.
      </p>

      <label htmlFor="vacancy-select" style={{ marginBottom: "0.3rem" }}>
        Select a vacancy:
      </label>
      <select
        id="vacancy-select"
        value={selectedIdx}
        onChange={(e) => setSelectedIdx(Number(e.target.value))}
        style={{ marginBottom: "1rem" }}
      >
        {jobs.map((job, i) => (
          <option key={job.id} value={i}>
            {i + 1}. {job.name} — {job.match_score}% match
          </option>
        ))}
      </select>

      <div style={{ display: "flex", gap: "0.75rem", flexWrap: "wrap" }}>
        <Button onClick={() => onSelectJob(jobs[selectedIdx])} icon={<ArrowRight size={16} />}>
          Build My Roadmap
        </Button>
        <Button variant="secondary" onClick={onBack} icon={<ArrowLeft size={15} />}>
          Search again
        </Button>
      </div>
    </div>
  );
}
