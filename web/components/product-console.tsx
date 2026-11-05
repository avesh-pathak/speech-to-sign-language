import {
  ArrowRight,
  Pause,
  Play,
  RotateCcw,
  Square,
} from "lucide-react";
import { Badge } from "@/components/ui/badge";
import { SignHand } from "@/components/sign-hand";
import { VaniSignMark } from "@/components/vanisign-mark";

const bars = Array.from({ length: 48 }, (_, index) => {
  const raw =
    6 +
    Math.round(
      (Math.sin(index * 0.78) * 0.5 + 0.5) * 20 +
        Math.cos(index * 0.31) * 3
    );

  return {
    height: Math.max(4, Math.min(30, raw)),
    delay: -((index % 13) * 0.055),
  };
});

function ConsoleLabel({ children }: { children: React.ReactNode }) {
  return (
    <span className="font-mono text-[10px] font-medium tracking-[0.12em] text-white/85 uppercase">
      {children}
    </span>
  );
}

export function ProductConsole() {
  return (
    <div
      role="img"
      aria-label="Illustrative VaniSign preview: the app recognises the Telugu phrase namaskaram danyavadalu, translates it into the ISL glosses hello_hi and thank, and plays the matching sign frames when a corpus is present."
      className="hero-console relative mx-auto mt-8 max-w-[1040px] overflow-hidden rounded-[18px] border border-white/10 text-white xl:max-w-[1080px] 2xl:max-w-[1120px]"
    >
      <div
        className="relative z-10 flex items-center gap-4 border-b border-white/[0.08] px-4 py-3 sm:px-5"
        aria-hidden="true"
      >
        <div className="flex items-center gap-2 font-display text-sm tracking-[-0.02em] whitespace-nowrap">
          <VaniSignMark className="size-[18px] text-white" />
          <span>VaniSign console</span>
        </div>

        <div className="hidden items-center gap-0.5 sm:flex">
          {["Session", "Gloss", "Corpus"].map((tab, index) => (
            <span
              key={tab}
              className={
                index === 0
                  ? "rounded-md bg-white/10 px-2.5 py-1.5 font-display text-xs text-white"
                  : "rounded-md px-2.5 py-1.5 font-display text-xs text-white/85"
              }
            >
              {tab}
            </span>
          ))}
        </div>

        <span className="ml-auto flex items-center gap-1.5 font-mono text-[10px] tracking-[0.12em] text-white/85 uppercase">
          <span className="size-1.5 rounded-[1px] bg-signal" />
          Preview
        </span>
      </div>

      <div className="relative z-10 grid md:grid-cols-[1.55fr_1fr]" aria-hidden="true">
        <div className="flex min-w-0 flex-col border-b border-white/[0.08] p-4 sm:p-5 md:border-r md:border-b-0">
          <div className="flex min-h-3.5 items-center gap-2.5">
            <span className="font-mono text-[10px] font-medium tracking-[0.1em] text-signal-bright uppercase">
              Telugu ASR
            </span>
            <span className="font-mono text-[10px] tracking-[0.08em] text-white/85 uppercase">
              Google Speech · te-IN
            </span>
            <span className="ml-auto font-mono text-[10px] text-white/85 tabular-nums">
              00:06
            </span>
          </div>

          <div className="my-3 flex h-9 items-center gap-[2px] overflow-hidden">
            {bars.map((bar, index) => (
              <i
                key={index}
                className={
                  index < 34
                    ? "block w-[2px] flex-none rounded-[2px] bg-[linear-gradient(#FF6B2C,#E83C00)]"
                    : "block w-[2px] flex-none rounded-[2px] bg-white/15"
                }
                style={{ height: `${bar.height}px` }}
              />
            ))}
          </div>

          <div className="border-t border-white/[0.07] pt-3">
            <ConsoleLabel>Recognised · Telugu</ConsoleLabel>
            <div
              lang="te"
              className="mt-1.5 font-telugu text-[22px] leading-[1.55] text-white max-sm:text-lg"
            >
              నమస్కారం ధన్యవాదాలు
            </div>
            <div className="mt-0.5 font-display text-xs tracking-[0.01em] text-white/85">
              hello · thank you
            </div>
          </div>

          <div className="mt-4">
            <div className="flex items-center">
              <ConsoleLabel>ISL gloss sequence</ConsoleLabel>
              <span className="ml-1.5 font-mono text-[10px] tracking-[0.12em] text-signal-bright uppercase">
                2 signs
              </span>
            </div>
            <div className="mt-2 flex flex-wrap items-center gap-2">
              <Badge
                variant="outline"
                className="h-auto gap-2 rounded-md border-[rgba(232,60,0,.34)] bg-[rgba(232,60,0,.12)] px-2.5 py-1.5 font-mono text-[10px] font-normal tracking-[0.03em] text-[#FFD9C8]"
              >
                <b className="font-normal text-white">hello_hi</b>
                <em className="font-mono text-[10px] tracking-[0.1em] text-live uppercase not-italic">
                  direct
                </em>
              </Badge>
              <ArrowRight className="size-3 text-white/85" />
              <Badge
                variant="outline"
                className="h-auto gap-2 rounded-md border-[rgba(232,60,0,.34)] bg-[rgba(232,60,0,.12)] px-2.5 py-1.5 font-mono text-[10px] font-normal tracking-[0.03em] text-[#FFD9C8]"
              >
                <b className="font-normal text-white">thank</b>
                <em className="font-mono text-[10px] tracking-[0.1em] text-live uppercase not-italic">
                  direct
                </em>
              </Badge>
            </div>
          </div>

          <div className="mt-4 flex items-center gap-2 border-t border-white/[0.07] pt-3">
            <ConsoleLabel>Pipeline</ConsoleLabel>
            <div className="ml-auto flex flex-wrap items-center gap-2">
              {["ASR", "NLP", "Frames"].map((stage) => (
                <span
                  key={stage}
                  className="inline-flex items-center gap-1 font-mono text-[10px] tracking-[0.06em] text-white/85 uppercase"
                >
                  <span className="size-1 rounded-full bg-live" />
                  {stage}
                </span>
              ))}
              <span className="inline-flex items-center gap-1 font-mono text-[10px] tracking-[0.06em] text-signal-bright uppercase">
                <span className="size-1 rounded-full bg-signal" />
                Render
              </span>
            </div>
          </div>

          <div className="mt-auto flex items-center justify-between gap-3 border-t border-white/[0.07] pt-3">
            <span className="inline-flex items-center gap-1.5 font-mono text-[10px] tracking-[0.1em] text-live uppercase">
              <span className="size-1 rounded-full bg-live" />
              2 glosses ready
            </span>
            <span className="font-mono text-[10px] tracking-[0.08em] text-white/85 uppercase">
              214 dictionary entries
            </span>
          </div>
        </div>

        <div className="flex min-w-0 flex-col bg-white/[0.015] p-4 sm:p-5">
          <div className="flex items-center justify-between gap-3">
            <ConsoleLabel>Sign playback</ConsoleLabel>
            <span className="font-mono text-[10px] tracking-[0.08em] text-white/85 uppercase">
              Frame 03 / 08
            </span>
          </div>

          <div className="relative mx-auto mt-2.5 aspect-square w-full max-w-[190px] overflow-hidden rounded-xl border border-[#4A2A1C] bg-[radial-gradient(circle_at_50%_42%,rgba(232,60,0,.18),rgba(232,60,0,0)_64%),#160D09] md:max-w-[200px]">
            <span className="absolute top-2 left-2 z-10 size-3 border-t border-l border-signal/50" />
            <span className="absolute top-2 right-2 z-10 size-3 border-t border-r border-signal/50" />
            <span className="absolute bottom-2 left-2 z-10 size-3 border-b border-l border-signal/50" />
            <span className="absolute right-2 bottom-2 z-10 size-3 border-r border-b border-signal/50" />
            <SignHand className="absolute top-1/2 left-1/2 z-10 size-[64%] -translate-x-1/2 -translate-y-1/2 text-signal" />
            <span className="absolute bottom-2.5 left-2.5 z-10 font-mono text-[10px] tracking-[0.08em] text-white/85">
              hello_hi
            </span>
            <span className="absolute top-2.5 right-2.5 z-10 font-mono text-[10px] tracking-[0.08em] text-white/85">
              400 × 400
            </span>
          </div>

          <div className="mt-3 flex items-center gap-1.5">
            <span className="grid size-7 place-items-center rounded-md border border-signal bg-signal text-white">
              <Play className="size-3 fill-current" />
            </span>
            <span className="grid size-7 place-items-center rounded-md border border-white/[0.12] bg-white/[0.04] text-white/85">
              <Pause className="size-3 fill-current" />
            </span>
            <span className="grid size-7 place-items-center rounded-md border border-white/[0.12] bg-white/[0.04] text-white/85">
              <Square className="size-2.5 fill-current" />
            </span>
            <span className="grid size-7 place-items-center rounded-md border border-white/[0.12] bg-white/[0.04] text-white/85">
              <RotateCcw className="size-3" />
            </span>
            <span className="ml-auto font-mono text-[10px] tracking-[0.08em] text-white/85 uppercase">
              ~10 fps
            </span>
          </div>

          <div className="mt-2 h-0.5 w-full overflow-hidden rounded-full bg-white/10">
            <span className="block h-full w-[38%] bg-signal" />
          </div>

          <div className="mt-2.5 flex gap-1 max-sm:hidden">
            {Array.from({ length: 8 }).map((_, index) => (
              <span
                key={index}
                className={
                  index === 2
                    ? "grid h-6 flex-1 place-items-center rounded-[4px] border border-[rgba(232,60,0,.6)] bg-[rgba(232,60,0,.14)] font-mono text-[10px] text-signal-bright"
                    : "grid h-6 flex-1 place-items-center rounded-[4px] border border-white/[0.09] bg-white/[0.015] font-mono text-[10px] text-white/70"
                }
              >
                {String(index + 1).padStart(2, "0")}
              </span>
            ))}
          </div>

          <div className="mt-auto flex items-center justify-between gap-3 border-t border-white/[0.07] pt-3">
            <ConsoleLabel>Fallback</ConsoleLabel>
            <span className="font-mono text-[10px] tracking-[0.1em] text-live uppercase">
              Text card ready
            </span>
          </div>
        </div>
      </div>
    </div>
  );
}
