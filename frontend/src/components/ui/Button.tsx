import type { ButtonHTMLAttributes, ReactNode } from "react";

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: "primary" | "secondary" | "ghost";
  loading?: boolean;
  icon?: ReactNode;
}

export default function Button({
  variant = "primary",
  loading = false,
  icon,
  children,
  disabled,
  style,
  ...props
}: ButtonProps) {
  const isDisabled = disabled || loading;

  const base: React.CSSProperties = {
    fontFamily: "var(--font-heading)",
    fontWeight: 700,
    fontSize: "0.9rem",
    border: "none",
    borderRadius: "var(--radius-lg)",
    padding: "0.65rem 1.5rem",
    cursor: isDisabled ? "not-allowed" : "pointer",
    transition: "all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1)",
    opacity: isDisabled ? 0.5 : 1,
    display: "inline-flex",
    alignItems: "center",
    gap: "0.5rem",
    whiteSpace: "nowrap",
  };

  const variants: Record<string, React.CSSProperties> = {
    primary: {
      background: "var(--gradient-button)",
      color: "var(--bg-primary)",
      boxShadow: "0 4px 20px rgba(167, 139, 250, 0.2)",
    },
    secondary: {
      background: "rgba(255, 255, 255, 0.05)",
      color: "var(--text-secondary)",
      border: "1px solid rgba(255, 255, 255, 0.1)",
      backdropFilter: "blur(8px)",
    },
    ghost: {
      background: "transparent",
      color: "var(--text-secondary)",
    },
  };

  return (
    <button
      style={{ ...base, ...variants[variant], ...style }}
      disabled={isDisabled}
      aria-busy={loading}
      onMouseEnter={(e) => {
        if (!isDisabled) {
          e.currentTarget.style.transform = "translateY(-1px)";
          if (variant === "primary") {
            e.currentTarget.style.boxShadow = "0 6px 28px rgba(167, 139, 250, 0.35)";
          }
        }
      }}
      onMouseLeave={(e) => {
        if (!isDisabled) {
          e.currentTarget.style.transform = "translateY(0)";
          if (variant === "primary") {
            e.currentTarget.style.boxShadow = "0 4px 20px rgba(167, 139, 250, 0.2)";
          }
        }
      }}
      onMouseDown={(e) => {
        if (!isDisabled) e.currentTarget.style.transform = "scale(0.97)";
      }}
      onMouseUp={(e) => {
        e.currentTarget.style.transform = "translateY(-1px)";
      }}
      {...props}
    >
      {loading && <Loader />}
      {!loading && icon}
      {children}
    </button>
  );
}

function Loader() {
  return (
    <span
      style={{
        width: 16,
        height: 16,
        border: "2px solid currentColor",
        borderTopColor: "transparent",
        borderRadius: "50%",
        animation: "spin 0.7s linear infinite",
        display: "inline-block",
        flexShrink: 0,
      }}
      aria-hidden="true"
    />
  );
}
