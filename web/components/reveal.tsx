import { cn } from "@/lib/utils";

/**
 * A layout block used by sections. Motion is intentionally absent here:
 * the page uses Lenis for scroll feel, not repeated entrance animations.
 */
export function Reveal({
  children,
  className,
}: {
  children: React.ReactNode;
  className?: string;
  delay?: number;
}) {
  return <div className={cn(className)}>{children}</div>;
}
