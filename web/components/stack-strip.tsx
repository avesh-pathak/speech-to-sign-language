import { Fragment } from "react";
import { Container } from "@/components/container";

const proof = [
  ["214", "mapping entries"],
  ["143", "acoustic features"],
  ["6", "test modules"],
  ["~10 fps", "frame playback"],
  ["0 GPU", "runtime"],
] as const;

export function StackStrip() {
  return (
    <div className="border-y border-border bg-card py-4">
      <Container className="flex flex-wrap items-center gap-3.5 sm:gap-7">
        <span className="flex shrink-0 items-center gap-2 font-mono text-[10px] font-medium tracking-[0.12em] text-muted-foreground uppercase">
          <span className="size-[5px] rounded-[1px] bg-signal" aria-hidden="true" />
          Project snapshot
        </span>
        <div className="flex flex-wrap items-center gap-x-4 gap-y-2 sm:gap-x-5">
          {proof.map(([value, label], index) => (
            <Fragment key={label}>
              {index > 0 ? (
                <span
                  className="size-[3px] rounded-full bg-border"
                  aria-hidden="true"
                />
              ) : null}
              <span className="font-display text-[13px] text-foreground">
                <span className="font-medium tabular-nums">{value}</span>
                <span className="ml-1 font-mono text-[10px] tracking-[0.06em] text-muted-foreground">
                  {label}
                </span>
              </span>
            </Fragment>
          ))}
        </div>
      </Container>
    </div>
  );
}
