"use client";

import { usePathname } from "next/navigation";
import { ArrowRight } from "lucide-react";
import { Badge } from "@/components/ui/badge";
import { SignHand } from "@/components/sign-hand";

function ConsoleLabel({ children }: { children: React.ReactNode }) {
  return (
    <span className="font-mono text-[10px] font-medium tracking-[0.12em] text-white/85 uppercase">
      {children}
    </span>
  );
}

const trace = [
  { label: "Speech decoder", value: "te-IN ready", ok: true },
  { label: "Gloss dictionary", value: "214 entries", ok: true },
  { label: "Route lookup", value: "no match", ok: false },
];

export function MissingRouteConsole() {
  const pathname = usePathname();

  return (
    <div
      role="img"
      aria-label={`Route trace for ${pathname}: the speech decoder and gloss dictionary are ready, but the page lookup failed with HTTP 404. No sign frame is indexed for this route, so the text fallback is active.`}
      className="hero-console relative overflow-hidden rounded-[18px] border border-white/10 text-white"
    >
      <div className="relative z-10 flex items-center gap-3 border-b border-white/[0.08] px-4 py-3 sm:px-5">
        <div className="flex gap-1.5" aria-hidden="true">
          <span className="size-[7px] rounded-full bg-signal" />
          <span className="size-[7px] rounded-full bg-white/20" />
          <span className="size-[7px] rounded-full bg-white/20" />
        </div>
        <span className="font-display text-sm tracking-[-0.02em] whitespace-nowrap">
          VaniSign · route trace
        </span>
        <span className="ml-auto flex items-center gap-1.5 font-mono text-[10px] tracking-[0.12em] text-signal-bright uppercase">
          <span className="size-1.5 rounded-[1px] bg-signal" />
          Signal lost
        </span>
      </div>

      <div className="relative z-10 p-4 sm:p-5" aria-hidden="true">
        <div className="flex items-center justify-between gap-3">
          <ConsoleLabel>Requested route</ConsoleLabel>
          <span className="font-mono text-[10px] tracking-[0.1em] text-signal-bright uppercase">
            HTTP 404
          </span>
        </div>

        <div className="mt-2 flex min-w-0 items-center gap-2.5 rounded-lg border border-white/[0.09] bg-black/30 px-3 py-2.5 font-mono text-[11px]">
          <span className="flex-none text-white/40">GET</span>
          <span className="truncate text-white/90">{pathname}</span>
          <span className="ml-auto flex-none rounded-[3px] border border-signal/30 bg-signal/10 px-1.5 py-0.5 text-[9px] tracking-[0.08em] text-signal-bright uppercase">
            miss
          </span>
        </div>

        <div className="mt-5">
          <ConsoleLabel>Decode trace</ConsoleLabel>
          <ul className="mt-2 space-y-1.5">
            {trace.map((step) => (
              <li
                key={step.label}
                className={
                  step.ok
                    ? "flex items-center gap-2.5 rounded-md px-2 py-1.5 font-mono text-[11px]"
                    : "flex items-center gap-2.5 rounded-md border border-signal/25 bg-signal/[0.09] px-2 py-1.5 font-mono text-[11px]"
                }
              >
                <span
                  className={
                    step.ok
                      ? "text-live"
                      : "text-signal-bright"
                  }
                >
                  {step.ok ? "✓" : "✕"}
                </span>
                <span className={step.ok ? "text-white/70" : "text-white"}>
                  {step.label}
                </span>
                <span
                  className={
                    step.ok
                      ? "ml-auto text-[10px] tracking-[0.06em] text-white/40 uppercase"
                      : "ml-auto text-[10px] tracking-[0.06em] text-signal-bright uppercase"
                  }
                >
                  {step.value}
                </span>
              </li>
            ))}
          </ul>
        </div>

        <div className="mt-4">
          <ConsoleLabel>Closest gloss</ConsoleLabel>
          <div className="mt-2 flex flex-wrap items-center gap-2">
            <Badge
              variant="outline"
              className="h-auto gap-2 rounded-md border-[rgba(232,60,0,.34)] bg-[rgba(232,60,0,.12)] px-2.5 py-1.5 font-mono text-[10px] font-normal tracking-[0.03em] text-[#FFD9C8]"
            >
              <b className="font-normal text-white">route_unknown</b>
              <em className="font-mono text-[10px] tracking-[0.1em] text-signal-bright uppercase not-italic">
                miss
              </em>
            </Badge>
            <ArrowRight className="size-3 text-white/85" />
            <Badge
              variant="outline"
              className="h-auto gap-2 rounded-md border-[rgba(61,186,117,.3)] bg-[rgba(61,186,117,.1)] px-2.5 py-1.5 font-mono text-[10px] font-normal tracking-[0.03em] text-[#C8F5DC]"
            >
              <b className="font-normal text-white">text_card</b>
              <em className="font-mono text-[10px] tracking-[0.1em] text-live uppercase not-italic">
                fallback
              </em>
            </Badge>
          </div>
        </div>

        <div className="mt-5 grid grid-cols-[minmax(0,1fr)_auto] items-center gap-4 border-t border-white/[0.08] pt-4">
          <div className="min-w-0">
            <ConsoleLabel>Sign frame</ConsoleLabel>
            <p className="mt-1.5 font-display text-[13px] leading-[1.55] text-white/70">
              No frame is indexed for this route.
            </p>
            <p
              lang="te"
              className="mt-1 font-telugu text-[17px] leading-[1.5] text-white/85"
            >
              సంజ్ఞ లేదు
            </p>
            <p className="font-mono text-[9px] tracking-[0.1em] text-white/40 uppercase">
              no sign
            </p>
          </div>

          <div className="relative size-[112px] shrink-0 overflow-hidden rounded-xl border border-[#4A2A1C] bg-[radial-gradient(circle_at_50%_42%,rgba(232,60,0,.18),rgba(232,60,0,0)_64%),#160D09] sm:size-[124px]">
            <span className="absolute top-2 left-2 z-10 size-3 border-t border-l border-signal/50" />
            <span className="absolute top-2 right-2 z-10 size-3 border-t border-r border-signal/50" />
            <span className="absolute bottom-2 left-2 z-10 size-3 border-b border-l border-signal/50" />
            <span className="absolute right-2 bottom-2 z-10 size-3 border-r border-b border-signal/50" />
            <SignHand className="absolute top-1/2 left-1/2 z-10 size-[58%] -translate-x-1/2 -translate-y-1/2 text-signal/30" />
            <span className="absolute inset-x-0 top-1/2 z-20 h-px bg-signal/30" />
            <span className="absolute bottom-2.5 left-2.5 z-20 font-mono text-[9px] tracking-[0.08em] text-white/55">
              no_frame
            </span>
            <span className="absolute top-2.5 right-2.5 z-20 font-mono text-[9px] tracking-[0.08em] text-white/55">
              404
            </span>
          </div>
        </div>

        <div className="mt-4 flex flex-wrap items-center justify-between gap-2 border-t border-white/[0.07] pt-3">
          <span className="inline-flex items-center gap-1.5 font-mono text-[10px] tracking-[0.1em] text-live uppercase">
            <span className="size-1 rounded-full bg-live" />
            Fallback active
          </span>
          <span className="font-mono text-[10px] tracking-[0.08em] text-white/55 uppercase">
            HTTP/1.1 404 Not Found
          </span>
        </div>
      </div>
    </div>
  );
}
