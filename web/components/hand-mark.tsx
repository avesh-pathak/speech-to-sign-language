import { cn } from "@/lib/utils";

export function HandMark({
  className,
  ...props
}: React.ComponentProps<"svg">) {
  return (
    <svg
      viewBox="0 0 100 100"
      fill="none"
      aria-hidden="true"
      className={cn("shrink-0", className)}
      {...props}
    >
      <rect x="26" y="20" width="12" height="45" rx="6" fill="currentColor" opacity=".62" />
      <rect x="41" y="10" width="12" height="55" rx="6" fill="currentColor" opacity=".9" />
      <rect x="56" y="16" width="12" height="49" rx="6" fill="currentColor" opacity=".76" />
      <rect x="71" y="28" width="11" height="37" rx="5.5" fill="currentColor" opacity=".6" />
      <rect
        x="8"
        y="45"
        width="12"
        height="29"
        rx="6"
        fill="currentColor"
        opacity=".82"
        transform="rotate(-30 14 59)"
      />
      <path
        d="M24 50h56v14c0 17-12 30-28 30S24 81 24 64V50Z"
        fill="currentColor"
      />
      <rect x="38" y="88" width="24" height="10" rx="5" fill="currentColor" opacity=".88" />
    </svg>
  );
}
