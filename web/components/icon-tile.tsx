import { cn } from "@/lib/utils";

export function IconTile({
  children,
  variant = "signal",
  className,
}: {
  children: React.ReactNode;
  variant?: "signal" | "paper" | "outline" | "peach";
  className?: string;
}) {
  return (
    <span
      className={cn(
        "grid size-6 shrink-0 place-items-center rounded-[5px]",
        variant === "signal" && "bg-signal text-white",
        variant === "paper" && "border border-border bg-card text-foreground",
        variant === "outline" && "border border-white/25 bg-transparent text-white",
        variant === "peach" && "bg-accent text-signal-text",
        className
      )}
    >
      {children}
    </span>
  );
}
