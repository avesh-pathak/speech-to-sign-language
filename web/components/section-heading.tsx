import { Eyebrow } from "@/components/eyebrow";
import { Reveal } from "@/components/reveal";
import { cn } from "@/lib/utils";

export function SectionHeading({
  eyebrow,
  title,
  description,
  tone = "light",
  className,
}: {
  eyebrow: string;
  title: React.ReactNode;
  description?: React.ReactNode;
  tone?: "light" | "dark";
  className?: string;
}) {
  return (
    <Reveal
      className={cn(
        "mb-12 flex flex-col items-start justify-between gap-7 lg:mb-14 xl:flex-row xl:items-end xl:gap-14",
        className
      )}
    >
      <div>
        <Eyebrow tone={tone}>{eyebrow}</Eyebrow>
        <h2
          className={cn(
            "mt-4 max-w-[760px] font-display text-[clamp(2rem,3.4vw,2.6rem)] leading-[1.06] font-normal tracking-[-0.04em] text-balance",
            tone === "dark" ? "text-white" : "text-foreground"
          )}
        >
          {title}
        </h2>
      </div>
      {description ? (
        <p
          className={cn(
            "max-w-[400px] font-display text-[15.5px] leading-[1.6]",
            tone === "dark" ? "text-white/55" : "text-muted-foreground"
          )}
        >
          {description}
        </p>
      ) : null}
    </Reveal>
  );
}
