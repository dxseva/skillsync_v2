import type { ReactNode } from "react";

interface InfoBoxProps {
  children: ReactNode;
  variant?: "default" | "error" | "success";
  style?: React.CSSProperties;
}

export default function InfoBox({
  children,
  variant = "default",
  style,
}: InfoBoxProps) {
  const colors: Record<string, { bg: string; border: string }> = {
    default: {
      bg: "rgba(255, 255, 255, 0.03)",
      border: "rgba(255, 255, 255, 0.06)",
    },
    error: {
      bg: "rgba(248, 113, 113, 0.06)",
      border: "rgba(248, 113, 113, 0.2)",
    },
    success: {
      bg: "rgba(74, 222, 128, 0.06)",
      border: "rgba(74, 222, 128, 0.2)",
    },
  };

  const { bg, border } = colors[variant];

  return (
    <div
      role={variant === "error" ? "alert" : undefined}
      style={{
        background: bg,
        border: `1px solid ${border}`,
        borderRadius: "var(--radius-lg)",
        padding: "1rem 1.25rem",
        fontSize: "0.88rem",
        color: "var(--text-muted)",
        margin: "1rem 0",
        lineHeight: 1.65,
        backdropFilter: "blur(8px)",
        ...style,
      }}
    >
      {children}
    </div>
  );
}
