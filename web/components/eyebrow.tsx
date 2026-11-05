import { cn } from "@/lib/utils";

export function Eyebrow({
  children,
  className,
  tone = "light",
}: {
  children: React.ReactNode;
  className?: string;
  tone?: "light" | "dark";
}) {
  return (
    <span
      className={cn(
        "inline-flex items-center gap-2 font-mono text-[11px] font-medium tracking-[0.12em] uppercase",
        tone === "dark" ? "text-white/50" : "text-muted-foreground",
        className
      )}
    >
      <span className="size-1.5 shrink-0 rounded-[1px] bg-signal" aria-hidden="true" />
      {children}
    </span>
  );
}
