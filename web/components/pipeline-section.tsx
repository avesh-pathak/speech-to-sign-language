import {
  AudioWaveform,
  Film,
  Languages,
  Mic,
  Play,
  type LucideIcon,
} from "lucide-react";
import { Card } from "@/components/ui/card";
import { Container } from "@/components/container";
import { Reveal } from "@/components/reveal";
import { SectionHeading } from "@/components/section-heading";
import { SystemMap } from "@/components/system-map";
import { DOCS } from "@/lib/project";

type Step = {
  number: string;
  title: string;
  copy: string;
  meta: string;
  icon: LucideIcon;
};

const steps: Step[] = [
  {
    number: "01",
    title: "Capture",
    copy: "Speak into the microphone, upload WAV / MP3 / FLAC / OGG, or type Telugu directly. Audio is normalised to 16 kHz mono.",
    meta: "Mic · file · text",
    icon: Mic,
  },
  {
    number: "02",
    title: "Recognise",
    copy: "Google Speech Recognition runs with te-IN and returns UTF-8 Telugu. The acoustic model branch is a separate, optional path.",
    meta: "Google ASR · te-IN",
    icon: AudioWaveform,
  },
  {
    number: "03",
    title: "Translate",
    copy: "A curated 214-entry dictionary runs first. An English pivot and fuzzy stem matching extend coverage when the direct lookup misses.",
    meta: "Direct → pivot → stem",
    icon: Languages,
  },
  {
    number: "04",
    title: "Sequence",
    copy: "Each gloss resolves to a frame directory, sorted by frame number. Frames are loaded lazily and cached after the first decode.",
    meta: ".jpg · .jpeg · .png",
    icon: Film,
  },
  {
    number: "05",
    title: "Animate",
    copy: "A single Tk clock plays frames at roughly 10 fps. Missing signs hold a readable text card for about 900 ms before moving on.",
    meta: "~10 fps · 400 × 400",
    icon: Play,
  },
];

export function PipelineSection() {
  return (
    <section
      id="how"
      className="relative pt-20 pb-16 md:pt-24 lg:pt-[150px] lg:pb-[88px]"
    >
      <Container>
        <SectionHeading
          eyebrow="The pipeline"
          title="Five steps from microphone to moving sign."
          description={
            <>
              One{" "}
              <span className="font-mono text-[11px] tracking-[0.04em] text-foreground normal-case">
                SpeechToSignPipeline
              </span>{" "}
              object orchestrates the runtime. The GUI, CLI, and tests all call
              the same path, so behaviour cannot drift between interfaces.
            </>
          }
        />

        <Reveal className="mb-4">
          <SystemMap />
        </Reveal>

        <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-5">
          {steps.map((step, index) => {
            const Icon = step.icon;
            return (
              <Reveal
                key={step.number}
                delay={index * 50}
                className={
                  index === steps.length - 1
                    ? "h-full sm:max-xl:col-span-2"
                    : "h-full"
                }
              >
                <Card className="relative flex h-full min-h-[270px] flex-col gap-0 rounded-2xl border border-border bg-card py-0 ring-0 shadow-[0_1px_2px_rgba(25,14,9,.03)] max-sm:min-h-0">
                  <span className="absolute top-0 left-5 h-0.5 w-6 rounded-b-sm bg-signal/85" />
                  <div className="px-5 pt-5">
                    <div className="flex items-start justify-between gap-3">
                      <span className="font-mono text-[10px] tracking-[0.12em] text-signal-text">
                        {step.number}
                      </span>
                      <span className="grid size-8 place-items-center rounded-[7px] bg-accent text-signal-text">
                        <Icon className="size-3.5" strokeWidth={1.5} />
                      </span>
                    </div>
                    <h3 className="mt-6 font-display text-[19px] font-medium tracking-[-0.025em] text-foreground">
                      {step.title}
                    </h3>
                    <p className="mt-2 text-[13.5px] leading-[1.58] text-muted-foreground">
                      {step.copy}
                    </p>
                  </div>
                  <div className="mt-auto px-5 pt-4 pb-4">
                    <div className="border-t border-border pt-3 font-mono text-[10px] tracking-[0.08em] text-muted-foreground uppercase">
                      {step.meta}
                    </div>
                  </div>
                </Card>
              </Reveal>
            );
          })}
        </div>

        <Reveal className="mt-4">
          <div className="flex items-start gap-5 rounded-[14px] border border-border bg-card px-5 py-4 text-foreground shadow-[0_16px_30px_rgba(60,20,5,.06)] sm:items-center sm:px-6">
            <span className="shrink-0 rounded-[4px] border border-signal/30 bg-signal/10 px-1.5 py-1 font-mono text-[10px] font-medium tracking-[0.12em] text-signal-text uppercase">
              Fallback by design
            </span>
            <p className="flex-1 font-display text-sm leading-[1.55] text-muted-foreground">
              <b className="font-medium text-foreground">
                A missing sign never deletes a word.
              </b>{" "}
              If no frames exist for a gloss, the app renders the token as a text
              card and keeps the sequence moving.
            </p>
            <a
              href={DOCS.architecture}
              target="_blank"
              rel="noreferrer"
              className="hidden shrink-0 border-b border-foreground/30 pb-0.5 font-display text-[13px] text-foreground transition-colors hover:border-signal hover:text-signal-text sm:block"
            >
              Read the contract &rarr;
            </a>
          </div>
        </Reveal>
      </Container>
    </section>
  );
}
