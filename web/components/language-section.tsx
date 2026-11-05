import { Container } from "@/components/container";
import { Eyebrow } from "@/components/eyebrow";
import { Reveal } from "@/components/reveal";

const layers = [
  {
    number: "01",
    title: "Direct mapping",
    copy: "214 curated Telugu → ISL pairs. Deterministic, fast, and fully offline for entries in the dictionary.",
  },
  {
    number: "02",
    title: "English pivot",
    copy: "When the dictionary misses, the Telugu token is translated to English and matched against the corpus vocabulary. Broader reach, with some meaning loss.",
  },
  {
    number: "03",
    title: "Fuzzy & stem matching",
    copy: (
      <>
        <code className="rounded border border-foreground/10 bg-foreground/5 px-1 py-0.5 font-mono text-[11px] text-foreground">
          going
        </code>{" "}
        →{" "}
        <code className="rounded border border-foreground/10 bg-foreground/5 px-1 py-0.5 font-mono text-[11px] text-foreground">
          go
        </code>
        ,{" "}
        <code className="rounded border border-foreground/10 bg-foreground/5 px-1 py-0.5 font-mono text-[11px] text-foreground">
          happily
        </code>{" "}
        →{" "}
        <code className="rounded border border-foreground/10 bg-foreground/5 px-1 py-0.5 font-mono text-[11px] text-foreground">
          happy
        </code>
        , plus conservative substring matching for near-misses.
      </>
    ),
  },
];

export function LanguageSection() {
  return (
    <section
      id="language"
      className="border-y border-border bg-muted pt-24 pb-16 md:pt-28 lg:pt-[150px] lg:pb-[88px]"
    >
      <Container>
        <div className="grid items-center gap-12 lg:grid-cols-[minmax(0,5fr)_minmax(0,7fr)] lg:gap-[56px] xl:gap-[72px]">
          <Reveal className="mx-auto w-full min-w-0 max-w-[640px] lg:mx-0 lg:max-w-none">
            <Eyebrow>Language layer</Eyebrow>
            <h2 className="mt-4 max-w-[540px] font-display text-[clamp(2rem,3.4vw,2.6rem)] leading-[1.06] font-normal tracking-[-0.04em] text-foreground text-balance">
              Dictionary first. Coverage second.
            </h2>
            <p className="mt-5 max-w-[540px] font-display text-[16px] leading-[1.65] text-muted-foreground">
              The translator is deliberately inspectable. Every token records how
              it was resolved, so the UI can distinguish a direct hit from a
              guess and a fallback.
            </p>

            <div className="mt-7">
              {layers.map((layer) => (
                <div
                  key={layer.number}
                  className="grid grid-cols-[34px_1fr] gap-3 border-t border-foreground/10 py-4 last:border-b"
                >
                  <span className="pt-0.5 font-mono text-[10px] tracking-[0.1em] text-signal-text">
                    {layer.number}
                  </span>
                  <div>
                    <h3 className="font-display text-[17px] font-medium tracking-[-0.02em] text-foreground">
                      {layer.title}
                    </h3>
                    <p className="mt-1 max-w-[440px] text-[13.5px] leading-[1.56] text-muted-foreground">
                      {layer.copy}
                    </p>
                  </div>
                </div>
              ))}
            </div>

            <div className="mt-6 flex items-start gap-2.5 rounded-[10px] border border-signal/15 bg-signal/[0.055] px-3.5 py-3 text-[12.5px] leading-[1.55] text-foreground">
              <span className="mt-[5px] size-[5px] shrink-0 rounded-[1px] bg-signal" />
              <div>
                No match at all? The token becomes{" "}
                <code className="rounded border border-foreground/10 bg-foreground/5 px-1 py-0.5 font-mono text-[11px]">
                  TEXT_&lt;word&gt;
                </code>{" "}
                and renders as a text card. The sentence stays readable &mdash;
                that is the contract.
              </div>
            </div>
          </Reveal>

          <Reveal delay={80} className="mx-auto w-full min-w-0 max-w-[820px] lg:mx-0 lg:max-w-none">
            <div className="min-w-0 max-w-full overflow-hidden rounded-2xl border border-[#3A2118] bg-surface-dark shadow-[0_30px_60px_rgba(60,20,5,.18)]">
              <div className="flex items-center gap-2.5 border-b border-white/[0.08] bg-white/[0.02] px-4 py-3">
                <div className="flex gap-1.5" aria-hidden="true">
                  <span className="size-[7px] rounded-full bg-signal" />
                  <span className="size-[7px] rounded-full bg-white/20" />
                  <span className="size-[7px] rounded-full bg-white/20" />
                </div>
                <span className="ml-1 font-mono text-[10px] tracking-[0.1em] text-white/55 uppercase">
                  translate &middot; te &rarr; isl
                </span>
                <span className="ml-auto flex items-center gap-1.5 font-mono text-[10px] tracking-[0.08em] text-live uppercase">
                  <span className="size-1 rounded-full bg-live" />
                  Offline OK
                </span>
              </div>

              <pre className="w-full max-w-full overflow-x-auto p-5 font-mono text-[11.5px] leading-[1.95] text-white/80 tabular-nums max-sm:text-[10px]">
                <span className="text-white/50">$</span>{" "}
                <span className="text-white">
                  python app.py --translate &quot;నమస్కారం ధన్యవాదాలు&quot;
                </span>
                {"\n\n"}
                <span className="text-white/50">Telugu → ISL</span>
                {"\n"}
                <span className="text-white/50">Input:</span>{" "}
                <span className="text-[#FFC9AC]">నమస్కారం ధన్యవాదాలు</span>
                {"\n\n"}
                {"  "}
                <span className="text-[#FFC9AC]">నమస్కారం</span>
                {"        "}
                <span className="text-signal-bright">→</span>{" "}
                <span className="text-white">hello_hi</span>
                {"    "}
                <span className="text-live">[✓ direct]</span>
                {"\n"}
                {"  "}
                <span className="text-[#FFC9AC]">ధన్యవాదాలు</span>
                {"      "}
                <span className="text-signal-bright">→</span>{" "}
                <span className="text-white">thank</span>
                {"       "}
                <span className="text-live">[✓ direct]</span>
                {"\n\n"}
                <span className="text-white/50">Gloss:</span>{" "}
                <span className="text-white">hello_hi</span>{" "}
                <span className="text-signal-bright">→</span>{" "}
                <span className="text-white">thank</span>
                {"\n"}
                <span className="text-white/50">Animation:</span>{" "}
                <span className="text-white">0 ready, 2 text fallback(s)</span>
                {"\n"}
                {"           "}
                <span className="text-white/50">
                  add a corpus to play the signs
                </span>
              </pre>

              <div className="flex flex-wrap items-center justify-between gap-3 border-t border-white/[0.08] px-4 py-2.5 font-mono text-[10px] tracking-[0.06em] text-white/50 uppercase">
                <span>16 kHz mono &middot; UTF-8 Telugu</span>
                <span>214 curated entries</span>
              </div>
            </div>
          </Reveal>
        </div>
      </Container>
    </section>
  );
}
