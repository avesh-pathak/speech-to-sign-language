import {
  ArrowUpRight,
  BookOpen,
  CheckCheck,
  Film,
  Layers,
  Monitor,
  Workflow,
  type LucideIcon,
} from "lucide-react";
import { Badge } from "@/components/ui/badge";
import { Card } from "@/components/ui/card";
import { Container } from "@/components/container";
import { GitHubIcon } from "@/components/github-icon";
import { Reveal } from "@/components/reveal";
import { SectionHeading } from "@/components/section-heading";
import { GITHUB_URL, project } from "@/lib/project";

const icons: LucideIcon[] = [
  Workflow,
  BookOpen,
  Layers,
  Film,
  Monitor,
  CheckCheck,
];

export function BuildSection() {
  return (
    <section id="build" className="relative pt-24 pb-16 md:pt-28 lg:pt-[150px] lg:pb-[88px]">
      <Container>
        <SectionHeading
          eyebrow="What I built"
          title="A complete runtime, not a concept render."
          description="I built the pipeline, the trainable research model, the Tkinter interface, the data contracts, and the tests as one coherent project. Everything described here exists in the repository."
        />

        <div className="grid min-w-0 gap-4 md:grid-cols-2 lg:grid-cols-3">
          {project.capabilities.map((capability, index) => {
            const Icon = icons[index];
            return (
              <Reveal
                key={capability.name}
                delay={index * 50}
                className="h-full min-w-0"
              >
                <Card className="flex h-full min-h-[245px] min-w-0 flex-col gap-0 overflow-hidden rounded-2xl border border-border bg-card py-0 ring-0 shadow-[0_1px_2px_rgba(25,14,9,.03)] max-sm:min-h-0">
                  <div className="px-6 pt-6">
                    <div className="flex items-start justify-between gap-3.5">
                      <span className="grid size-9 shrink-0 place-items-center rounded-lg bg-accent text-signal-text">
                        <Icon className="size-4" strokeWidth={1.5} />
                      </span>
                      <span className="max-w-[62%] text-right font-mono text-[10px] leading-[1.55] tracking-[0.02em] break-all text-muted-foreground">
                        {capability.path}
                      </span>
                    </div>
                    <h3 className="mt-5 font-display text-[21px] font-medium tracking-[-0.025em] text-foreground">
                      {capability.name}
                    </h3>
                    <p className="mt-2 text-[13.5px] leading-[1.6] text-muted-foreground">
                      {capability.description}
                    </p>
                  </div>
                  <div className="mt-auto flex flex-wrap gap-1.5 px-6 pt-4 pb-5">
                    {capability.tags.map((tag) => (
                      <Badge
                        key={tag}
                        variant="secondary"
                        className="h-auto rounded-[4px] border border-border bg-muted px-1.5 py-1 font-mono text-[10px] font-normal tracking-[0.08em] text-muted-foreground uppercase"
                      >
                        {tag}
                      </Badge>
                    ))}
                  </div>
                </Card>
              </Reveal>
            );
          })}
        </div>

        <Reveal className="mt-6 flex justify-end">
          <a
            href={GITHUB_URL}
            target="_blank"
            rel="noreferrer"
            className="inline-flex items-center gap-2 border-b border-foreground/30 pb-0.5 font-display text-[13px] transition-colors hover:border-signal hover:text-signal-text"
          >
            <GitHubIcon className="size-3.5" />
            Browse the source on GitHub
            <ArrowUpRight className="size-3" />
          </a>
        </Reveal>
      </Container>
    </section>
  );
}
