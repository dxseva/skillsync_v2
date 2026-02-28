import { describe, it, expect, vi } from "vitest";
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import StepGoal from "../components/app/StepGoal";
import StepBadge from "../components/ui/StepBadge";
import InfoBox from "../components/ui/InfoBox";
import MatchBar from "../components/ui/MatchBar";
import ScoreBadge from "../components/ui/ScoreBadge";
import SkillChip from "../components/app/SkillChip";

describe("StepBadge", () => {
  it("renders step number and label", () => {
    render(<StepBadge step={2} label="YOUR PROFILE" />);
    expect(screen.getByText(/STEP 2/)).toBeInTheDocument();
    expect(screen.getByText(/YOUR PROFILE/)).toBeInTheDocument();
  });
});

describe("InfoBox", () => {
  it("renders children", () => {
    render(<InfoBox>Hello world</InfoBox>);
    expect(screen.getByText("Hello world")).toBeInTheDocument();
  });

  it("renders error variant with alert role", () => {
    render(<InfoBox variant="error">Error msg</InfoBox>);
    expect(screen.getByRole("alert")).toBeInTheDocument();
  });

  it("renders default variant without alert role", () => {
    const { container } = render(<InfoBox>Info msg</InfoBox>);
    expect(container.querySelector("[role='alert']")).toBeNull();
  });
});

describe("MatchBar", () => {
  it("renders with correct aria attributes", () => {
    render(<MatchBar score={75} />);
    const bar = screen.getByRole("progressbar");
    expect(bar).toHaveAttribute("aria-valuenow", "75");
    expect(bar).toHaveAttribute("aria-valuemin", "0");
    expect(bar).toHaveAttribute("aria-valuemax", "100");
  });

  it("clamps score to 0-100", () => {
    render(<MatchBar score={150} />);
    const bar = screen.getByRole("progressbar");
    expect(bar).toHaveAttribute("aria-valuenow", "100");
  });
});

describe("ScoreBadge", () => {
  it("renders clamped score", () => {
    render(<ScoreBadge score={85} />);
    expect(screen.getByText("85%")).toBeInTheDocument();
  });

  it("clamps to 100", () => {
    render(<ScoreBadge score={120} />);
    expect(screen.getByText("100%")).toBeInTheDocument();
  });
});

describe("SkillChip", () => {
  it("renders skill name with checkmark", () => {
    render(<SkillChip skill="Python" />);
    expect(screen.getByText(/Python/)).toBeInTheDocument();
  });
});

describe("StepGoal", () => {
  it("renders input and button", () => {
    render(<StepGoal onNext={vi.fn()} />);
    expect(screen.getByLabelText("Your career goal")).toBeInTheDocument();
    expect(screen.getByText("Continue")).toBeInTheDocument();
  });

  it("button is disabled with short goal", () => {
    render(<StepGoal onNext={vi.fn()} />);
    expect(screen.getByText("Continue").closest("button")).toBeDisabled();
  });

  it("calls onNext with trimmed goal", async () => {
    const onNext = vi.fn();
    render(<StepGoal onNext={onNext} />);
    const input = screen.getByLabelText("Your career goal");
    await userEvent.type(input, "data analyst");
    await userEvent.click(screen.getByText("Continue"));
    expect(onNext).toHaveBeenCalledWith("data analyst");
  });

  it("shows validation message for short input", async () => {
    render(<StepGoal onNext={vi.fn()} />);
    const input = screen.getByLabelText("Your career goal");
    await userEvent.type(input, "ab");
    expect(screen.getByText(/at least 3 characters/)).toBeInTheDocument();
  });

  it("fills goal from suggestion chip", async () => {
    const onNext = vi.fn();
    render(<StepGoal onNext={onNext} />);
    await userEvent.click(screen.getByText("Data Analyst"));
    expect(screen.getByLabelText("Your career goal")).toHaveValue("Data Analyst");
  });

  it("submits on Enter key", async () => {
    const onNext = vi.fn();
    render(<StepGoal onNext={onNext} />);
    const input = screen.getByLabelText("Your career goal");
    await userEvent.type(input, "developer{enter}");
    expect(onNext).toHaveBeenCalledWith("developer");
  });

  it("uses initialGoal prop", () => {
    render(<StepGoal initialGoal="lawyer" onNext={vi.fn()} />);
    expect(screen.getByLabelText("Your career goal")).toHaveValue("lawyer");
  });
});
