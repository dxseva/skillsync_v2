import type { Job } from "../../types";
import ScoreBadge from "../ui/ScoreBadge";
import MatchBar from "../ui/MatchBar";
import { ExternalLink } from "lucide-react";

interface JobCardProps {
  job: Job;
  index: number;
}

export default function JobCard({ job, index }: JobCardProps) {
  const snippet =
    job.snippet_en ||
    ((job.requirement || "") + " " + (job.responsibility || "")).trim();
  const snippetDisplay =
    snippet.length > 250 ? snippet.slice(0, 250) + "..." : snippet;

  const salary = job.salary;
  let salaryStr = "";
  if (salary) {
    const { from, to, currency = "RUB" } = salary;
    if (from && to)
      salaryStr = `${from.toLocaleString()}\u2013${to.toLocaleString()} ${currency}`;
    else if (from) salaryStr = `from ${from.toLocaleString()} ${currency}`;
    else if (to) salaryStr = `up to ${to.toLocaleString()} ${currency}`;
  }

  const meta = [
    job.employer_en || job.employer || "Company",
    job.area || null,
    job.schedule || null,
    job.experience || null,
    salaryStr || null,
  ]
    .filter(Boolean)
    .join(" \u00B7 ");

  return (
    <article
      style={{
        background: "rgba(255, 255, 255, 0.03)",
        backdropFilter: "blur(12px)",
        border: "1px solid rgba(255, 255, 255, 0.07)",
        borderRadius: "var(--radius-xl)",
        padding: "1.25rem 1.5rem",
        marginBottom: "0.75rem",
        position: "relative",
        transition: "border-color 0.3s, box-shadow 0.3s, background 0.3s",
      }}
      onMouseEnter={(e) => {
        e.currentTarget.style.borderColor = "rgba(167, 139, 250, 0.25)";
        e.currentTarget.style.boxShadow = "var(--shadow-glow-hover)";
        e.currentTarget.style.background = "rgba(255, 255, 255, 0.05)";
      }}
      onMouseLeave={(e) => {
        e.currentTarget.style.borderColor = "rgba(255, 255, 255, 0.07)";
        e.currentTarget.style.boxShadow = "none";
        e.currentTarget.style.background = "rgba(255, 255, 255, 0.03)";
      }}
    >
      <ScoreBadge score={job.match_score} />

      <h3
        style={{
          fontFamily: "var(--font-heading)",
          fontSize: "1.05rem",
          fontWeight: 700,
          color: "var(--text-primary)",
          margin: "0 0 0.25rem",
          paddingRight: "4.5rem",
          lineHeight: 1.3,
        }}
      >
        {index}. {job.name}
      </h3>

      <p style={{ fontSize: "0.82rem", color: "var(--text-dim)", marginBottom: "0.5rem" }}>
        {meta}
      </p>

      <MatchBar score={job.match_score} />

      <p
        style={{
          fontSize: "0.87rem",
          color: "var(--text-secondary)",
          lineHeight: 1.55,
          marginTop: "0.4rem",
        }}
      >
        {snippetDisplay || "No description available."}
      </p>

      {job.url && (
        <div style={{ marginTop: "0.6rem" }}>
          <a
            href={job.url}
            target="_blank"
            rel="noopener noreferrer"
            style={{
              color: "var(--accent-cyan)",
              fontSize: "0.82rem",
              display: "inline-flex",
              alignItems: "center",
              gap: "0.3rem",
            }}
          >
            View on HH.ru <ExternalLink size={13} />
          </a>
        </div>
      )}
    </article>
  );
}
