import { describe, it, expect, vi, beforeEach, afterEach } from "vitest";
import { getCities, searchJobs, generateRoadmap } from "../api/client";

const mockFetch = vi.fn();
vi.stubGlobal("fetch", mockFetch);

beforeEach(() => {
  mockFetch.mockReset();
});

afterEach(() => {
  vi.restoreAllMocks();
});

function jsonResponse(data: unknown, status = 200) {
  return Promise.resolve({
    ok: status >= 200 && status < 300,
    status,
    json: () => Promise.resolve(data),
  });
}

describe("getCities", () => {
  it("returns city list", async () => {
    mockFetch.mockReturnValueOnce(jsonResponse(["Any city", "Москва"]));
    const cities = await getCities();
    expect(cities).toEqual(["Any city", "Москва"]);
  });

  it("throws ApiError on HTTP error", async () => {
    mockFetch.mockReturnValueOnce(
      jsonResponse({ detail: "Server error" }, 500)
    );
    await expect(getCities()).rejects.toThrow("Server error");
  });

  it("throws on network failure", async () => {
    mockFetch.mockRejectedValueOnce(new TypeError("Failed to fetch"));
    await expect(getCities()).rejects.toThrow("Network error");
  });
});

describe("searchJobs", () => {
  const profile = {
    skills: "Python",
    skill_level: "intermediate",
    year: 3,
    city: "Any city",
    format: "any",
    relocation: false,
  };

  it("sends correct POST body", async () => {
    mockFetch.mockReturnValueOnce(jsonResponse({ jobs: [], message: "ok" }));
    await searchJobs("developer", profile);
    expect(mockFetch).toHaveBeenCalledTimes(1);
    const [url, opts] = mockFetch.mock.calls[0];
    expect(url).toContain("/api/search");
    expect(opts.method).toBe("POST");
    const body = JSON.parse(opts.body);
    expect(body.goal).toBe("developer");
    expect(body.profile.skills).toBe("Python");
  });

  it("returns search response", async () => {
    const mockResponse = {
      jobs: [{ id: "1", name: "Dev", match_score: 85 }],
      message: "Found 1 match",
    };
    mockFetch.mockReturnValueOnce(jsonResponse(mockResponse));
    const result = await searchJobs("developer", profile);
    expect(result.jobs).toHaveLength(1);
    expect(result.jobs[0].match_score).toBe(85);
  });

  it("throws on 502 (HH.ru error)", async () => {
    mockFetch.mockReturnValueOnce(
      jsonResponse({ detail: "Could not reach HH.ru" }, 502)
    );
    await expect(searchJobs("dev", profile)).rejects.toThrow("HH.ru");
  });
});

describe("generateRoadmap", () => {
  const job = {
    id: "1",
    name: "Dev",
    url: "",
    employer: "",
    area: "",
    requirement: "",
    responsibility: "",
    salary: null,
    schedule: "",
    experience: "",
    match_score: 80,
  };

  it("sends correct POST body with skill_level", async () => {
    mockFetch.mockReturnValueOnce(
      jsonResponse({
        job_title: "Dev",
        missing_skills: [],
        already_strong: [],
        roadmap_steps: [],
        total_estimated_time: "0",
        match_after_preparation: "95%",
        notes: "",
      })
    );
    await generateRoadmap(job, "Python", undefined, "advanced");
    const body = JSON.parse(mockFetch.mock.calls[0][1].body);
    expect(body.skill_level).toBe("advanced");
    expect(body.user_skills).toBe("Python");
    expect(body.job.id).toBe("1");
  });

  it("defaults skill_level to intermediate", async () => {
    mockFetch.mockReturnValueOnce(
      jsonResponse({
        job_title: "Dev",
        missing_skills: [],
        already_strong: [],
        roadmap_steps: [],
        total_estimated_time: "0",
        match_after_preparation: "95%",
        notes: "",
      })
    );
    await generateRoadmap(job, "Python");
    const body = JSON.parse(mockFetch.mock.calls[0][1].body);
    expect(body.skill_level).toBe("intermediate");
  });
});
