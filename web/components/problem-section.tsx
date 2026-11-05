import { ArrowRight } from "lucide-react";
import { Badge } from "@/components/ui/badge";
import { Card } from "@/components/ui/card";
import { Container } from "@/components/container";
import { HandMark } from "@/components/hand-mark";
import { Reveal } from "@/components/reveal";
import { SectionHeading } from "@/components/section-heading";

const problems = [
  {
    number: "01",
    title: "Telugu is underserved.",
    copy: "Assistive speech tooling is overwhelmingly English-first. Telugu needs its own recognition path, its own vocabulary, and its own route into sign language.",
    tag: "A language-specific problem",
  },
  {
    number: "02",
    title: "ISL is not word-for-word.",
    copy: "Telugu and Indian Sign Language differ in grammar and structure. A usable system has to produce an ordered gloss sequence, not a subtitle with the same words in the same order.",
    tag: "Grammar, not substitution",
  },
  {
    number: "03",
    title: "A missing sign cannot erase a word.",
    copy: "Corpora are never complete. When a sign has no frames, the system must still show the meaning. Silently dropping the token would hide part of the sentence.",
    tag: "Fallback is a feature",
  },
];

export function ProblemSection() {
  return (
    <section
      id="problem"
      className="relative pt-24 pb-16 md:pt-28 lg:pt-[150px] lg:pb-[88px]"
    >
      <Container>
        <SectionHeading
          eyebrow="The gap"
          title="A transcript is not a translation."
          description="Most speech tools stop when the words appear on screen. For a Deaf Telugu speaker, the meaning has to become visual — and ISL does not follow Telugu word for word."
        />

        <div className="grid gap-4 md:grid-cols-3">
          {problems.map((problem, index) => (
            <Reveal key={problem.number} delay={index * 60} className="h-full">
              <Card className="flex h-full min-h-[300px] flex-col gap-0 rounded-[17px] border border-border bg-card py-0 ring-0 shadow-[0_1px_2px_rgba(25,14,9,.03)] max-sm:min-h-0">
                <div className="px-6 pt-6">
                  <span className="font-mono text-[10px] tracking-[0.12em] text-signal-text">
                    {problem.number}
                  </span>
                  <h3 className="mt-8 font-display text-[22px] leading-[1.2] font-medium tracking-[-0.025em] text-foreground">
                    {problem.title}
                  </h3>
                  <p className="mt-2.5 text-[14.5px] leading-[1.62] text-muted-foreground">
                    {problem.copy}
                  </p>
                </div>
                <div className="mt-auto px-6 pt-5 pb-5">
                  <div className="border-t border-border pt-3.5 font-mono text-[10px] tracking-[0.1em] text-muted-foreground uppercase">
                    {problem.tag}
                  </div>
                </div>
              </Card>
            </Reveal>
          ))}
        </div>

        <Reveal className="mt-14">
          <div className="grid overflow-hidden rounded-[20px] border border-border bg-card md:grid-cols-[1fr_58px_1fr]">
            <div className="flex min-w-0 flex-col p-6 sm:p-8">
              <span className="flex items-center gap-2 font-mono text-[10px] font-medium tracking-[0.12em] text-muted-foreground uppercase">
                <span className="size-[5px] rounded-[1px] bg-border" aria-hidden="true" />
                Typical speech tool
              </span>
              <div
                lang="te"
                className="mt-6 font-telugu text-[28px] leading-[1.5] break-words text-foreground max-sm:text-2xl"
              >
                మీరు ఎలా ఉన్నారు?
              </div>
              <span className="mt-4 inline-flex w-fit items-center gap-1.5 rounded-[4px] border border-border bg-muted px-1.5 py-1 font-mono text-[10px] tracking-[0.1em] text-muted-foreground uppercase">
                <span className="size-1 rounded-full bg-muted-foreground/60" />
                Transcript only
              </span>
              <p className="mt-4 max-w-[440px] text-[13.5px] leading-[1.6] text-muted-foreground">
                Words on a screen. No ISL order, no visual equivalent, and no way
                to carry the meaning for someone who relies on signing.
              </p>
            </div>

            <div
              className="grid min-h-11 place-items-center border-y border-border bg-card text-signal md:border-x md:border-y-0"
              aria-hidden="true"
            >
              <ArrowRight className="size-5 rotate-90 md:rotate-0" />
            </div>

            <div className="flex min-w-0 flex-col bg-[linear-gradient(125deg,var(--accent),var(--card)_62%,var(--card))] p-6 sm:p-8">
              <span className="flex items-center gap-2 font-mono text-[10px] font-medium tracking-[0.12em] text-signal-text uppercase">
                <span className="size-[5px] rounded-[1px] bg-signal" aria-hidden="true" />
                VaniSign
              </span>
              <div className="mt-6 flex flex-wrap items-center gap-2.5">
                <Badge
                  variant="outline"
                  className="h-auto rounded-md border-[rgba(232,60,0,.28)] bg-[rgba(232,60,0,.09)] px-2.5 py-1.5 font-mono text-[11px] font-normal tracking-[0.01em] text-signal-text"
                >
                  how_are_you
                </Badge>
                <span className="grid size-10 place-items-center rounded-lg border border-[rgba(232,60,0,.28)] bg-card/65 text-signal">
                  <HandMark className="size-6" />
                </span>
              </div>
              <span className="mt-4 inline-flex w-fit items-center gap-1.5 rounded-[4px] border border-live/25 bg-live/10 px-1.5 py-1 font-mono text-[10px] tracking-[0.1em] text-[#217a4c] dark:text-live uppercase">
                <span className="size-1 rounded-full bg-live" />
                Gloss + playback
              </span>
              <p className="mt-4 max-w-[440px] text-[13.5px] leading-[1.6] text-muted-foreground">
                An ordered ISL gloss, a sign frame sequence, and a readable text
                card for anything the corpus does not contain.
              </p>
            </div>
          </div>
        </Reveal>
      </Container>
    </section>
  );
}
