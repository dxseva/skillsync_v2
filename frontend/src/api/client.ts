import type { Profile, SearchResponse, Roadmap, Job } from "../types";

const BASE = import.meta.env.VITE_API_URL || "http://localhost:8000";

class ApiError extends Error {
  status: number;
  constructor(message: string, status: number) {
    super(message);
    this.status = status;
  }
}

async function request<T>(url: string, options?: RequestInit): Promise<T> {
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), 120_000);

  try {
    const res = await fetch(url, {
      ...options,
      signal: controller.signal,
    });
    if (!res.ok) {
      const body = await res.json().catch(() => ({}));
      const detail =
        body.detail || body.message || `Request failed (HTTP ${res.status})`;
      throw new ApiError(detail, res.status);
    }
    return res.json();
  } catch (err) {
    if (err instanceof ApiError) throw err;
    if ((err as Error).name === "AbortError") {
      throw new ApiError(
        "Request timed out. The server may be loading ML models for the first time (~30s). Please try again.",
        408
      );
    }
    throw new ApiError(
      "Network error — cannot reach the backend. Make sure the server is running on " + BASE,
      0
    );
  } finally {
    clearTimeout(timeout);
  }
}

export async function getCities(): Promise<string[]> {
  return request<string[]>(`${BASE}/api/cities`);
}

export async function searchJobs(
  goal: string,
  profile: Profile
): Promise<SearchResponse> {
  return request<SearchResponse>(`${BASE}/api/search`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ goal, profile }),
  });
}

export async function generateRoadmap(
  job: Job,
  userSkills: string,
  keySkills?: string[],
  skillLevel?: string
): Promise<Roadmap> {
  return request<Roadmap>(`${BASE}/api/roadmap`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      job,
      user_skills: userSkills,
      key_skills: keySkills,
      skill_level: skillLevel || "intermediate",
    }),
  });
}
