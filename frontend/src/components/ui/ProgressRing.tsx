import { useEffect, useState, useRef, useCallback } from "react";

interface Props {
  active: boolean;
  onComplete?: () => void;
}

const R = 42;
const CIRCUMFERENCE = 2 * Math.PI * R;

export default function ProgressRing({ active, onComplete }: Props) {
  const [progress, setProgress] = useState(0);
  const intervalRef = useRef<ReturnType<typeof setInterval>>(undefined);

  const start = useCallback(() => {
    setProgress(0);
    if (intervalRef.current) clearInterval(intervalRef.current);
    intervalRef.current = setInterval(() => {
      setProgress((p) => {
        if (p >= 92) {
          clearInterval(intervalRef.current);
          return 92;
        }
        const inc = p < 25 ? 2.5 : p < 50 ? 1.8 : p < 75 ? 1 : 0.4;
        return Math.min(p + inc, 92);
      });
    }, 350);
  }, []);

  const finish = useCallback(() => {
    if (intervalRef.current) clearInterval(intervalRef.current);
    setProgress(100);
    if (onComplete) setTimeout(onComplete, 350);
  }, [onComplete]);

  useEffect(() => {
    if (active) start();
    else finish();
  }, [active, start, finish]);

  useEffect(() => {
    return () => {
      if (intervalRef.current) clearInterval(intervalRef.current);
    };
  }, []);

  const pct = Math.round(progress);
  const offset = CIRCUMFERENCE * (1 - pct / 100);

  return (
    <div className="loader-container">
      <div className="loader-ring">
        <svg width="100" height="100" viewBox="0 0 100 100">
          <defs>
            <linearGradient id="loader-grad" x1="0%" y1="0%" x2="100%" y2="0%">
              <stop offset="0%" stopColor="var(--accent-cyan)" />
              <stop offset="100%" stopColor="var(--accent-purple)" />
            </linearGradient>
          </defs>
          <circle className="loader-ring-bg" cx="50" cy="50" r={R} />
          <circle
            className="loader-ring-fill"
            cx="50" cy="50" r={R}
            strokeDasharray={CIRCUMFERENCE}
            strokeDashoffset={offset}
          />
        </svg>
        <span className="loader-pct">{pct}%</span>
      </div>
    </div>
  );
}
