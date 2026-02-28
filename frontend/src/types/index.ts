export interface Job {
  id: string;
  name: string;
  url: string;
  employer: string;
  employer_en?: string;
  area: string;
  requirement: string;
  responsibility: string;
  salary: {
    from?: number;
    to?: number;
    currency?: string;
  } | null;
  schedule: string;
  experience: string;
  match_score: number;
  snippet_en?: string;
}

export interface Profile {
  skills: string;
  skill_level: string;
  year: number;
  city: string;
  format: string;
  relocation: boolean;
}

export interface RoadmapStep {
  skill: string;
  level: string;
  status: string;
  current_match_pct: number;
  estimated_time: string;
  min_months: number;
  max_months: number;
  suggested_actions: string;
  resources: string;
}

export interface Roadmap {
  job_title: string;
  missing_skills: string[];
  already_strong: string[];
  roadmap_steps: RoadmapStep[];
  total_estimated_time: string;
  match_after_preparation: string;
  notes: string;
}

export interface SearchResponse {
  jobs: Job[];
  message: string;
}

export type AppStep = "goal" | "profile" | "results" | "roadmap";
