import { useState, useCallback } from "react";
import type { AppStep, Job, Profile } from "../types";
import StepProgress from "../components/ui/StepProgress";
import StepGoal from "../components/app/StepGoal";
import StepProfile from "../components/app/StepProfile";
import StepResults from "../components/app/StepResults";
import StepRoadmap from "../components/app/StepRoadmap";

const INITIAL_PROFILE: Profile = {
  skills: "",
  skill_level: "intermediate",
  year: 3,
  city: "Any city",
  format: "any",
  relocation: false,
};

export default function AppFlow() {
  const [step, setStep] = useState<AppStep>("goal");
  const [goal, setGoal] = useState("");
  const [profile, setProfile] = useState<Profile>(INITIAL_PROFILE);
  const [selectedJob, setSelectedJob] = useState<Job | null>(null);
  const [cachedJobs, setCachedJobs] = useState<Job[]>([]);

  const handleJobsLoaded = useCallback((jobs: Job[]) => {
    setCachedJobs(jobs);
  }, []);

  const resetAll = () => {
    setGoal("");
    setProfile(INITIAL_PROFILE);
    setSelectedJob(null);
    setCachedJobs([]);
    setStep("goal");
  };

  return (
    <div
      className="container"
      style={{
        paddingTop: "1.5rem",
        paddingBottom: "4rem",
        position: "relative",
      }}
    >
      {/* Ambient glow */}
      <div
        style={{
          position: "fixed",
          top: 0,
          left: 0,
          right: 0,
          bottom: 0,
          pointerEvents: "none",
          zIndex: 0,
          background:
            "radial-gradient(ellipse 50% 40% at 30% 20%, rgba(110, 231, 247, 0.04) 0%, transparent 60%), " +
            "radial-gradient(ellipse 40% 35% at 70% 70%, rgba(167, 139, 250, 0.04) 0%, transparent 60%)",
        }}
      />

      <div style={{ position: "relative", zIndex: 1 }}>
        {/* Header */}
        <div style={{ textAlign: "center", padding: "1rem 0 0.5rem" }}>
          <h1
            className="gradient-text"
            style={{
              fontSize: "clamp(1.6rem, 4vw, 2.2rem)",
              fontWeight: 800,
              letterSpacing: "-1px",
              margin: 0,
            }}
          >
            SkillSync
          </h1>
          <p style={{ color: "var(--text-dim)", fontSize: "0.85rem", marginTop: "0.3rem" }}>
            AI Career Guide
          </p>
        </div>

        {/* Step Progress */}
        <StepProgress current={step} />

        {/* Steps */}
        {step === "goal" && (
          <StepGoal
            initialGoal={goal}
            onNext={(g) => {
              setGoal(g);
              setStep("profile");
            }}
          />
        )}

        {step === "profile" && (
          <StepProfile
            goal={goal}
            initialProfile={profile}
            onNext={(p) => {
              setProfile(p);
              setCachedJobs([]);
              setStep("results");
            }}
            onBack={() => setStep("goal")}
          />
        )}

        {step === "results" && (
          <StepResults
            goal={goal}
            profile={profile}
            cachedJobs={cachedJobs.length ? cachedJobs : undefined}
            onSelectJob={(job) => {
              setSelectedJob(job);
              setStep("roadmap");
            }}
            onJobsLoaded={handleJobsLoaded}
            onBack={() => setStep("profile")}
          />
        )}

        {step === "roadmap" && selectedJob && (
          <StepRoadmap
            job={selectedJob}
            userSkills={profile.skills}
            skillLevel={profile.skill_level}
            onBackToResults={() => setStep("results")}
            onNewSearch={resetAll}
          />
        )}
      </div>
    </div>
  );
}
