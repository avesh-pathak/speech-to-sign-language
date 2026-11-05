import { ArrowUpRight, Code2 } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Container } from "@/components/container";
import { Reveal } from "@/components/reveal";
import { SectionHeading } from "@/components/section-heading";
import { DOCS, project } from "@/lib/project";

const architecture = [
  { key: "Input", value: "Dual feature tensor", note: "200 × 143" },
  { key: "Normalise", value: "Layer normalisation", note: "per frame" },
  {
    key: "Context",
    value: "Multi-head attention",
    note: "4 heads",
    tag: "+ residual",
    active: true,
  },
  { key: "Sequence", value: "Bidirectional LSTM", note: "128 × 2" },
  {
    key: "Deepen",
    value: "Residual BiLSTM block",
    note: "skip connection",
    tag: "LN → ReLU → +",
    active: true,
  },
  { key: "Reduce", value: "Global average pooling", note: "sequence → vector" },
  { key: "Classify", value: "Dense + dropout", note: "256 · 0.3" },
  { key: "Output", value: "Softmax over sign classes", note: "N classes" },
];

const training = ["Adam 1e-3", "Sparse categorical CE", "75 / 25 split", "Early stopping"];

export function ModelSection() {
  return (
    <section
      id="model"
      className="relative overflow-hidden border-y border-border bg-muted pt-24 pb-16 text-foreground md:pt-28 lg:pt-[150px] lg:pb-[88px]"
    >
      <div
        className="pointer-events-none absolute inset-0 bg-[radial-gradient(55%_60%_at_88%_6%,rgba(232,60,0,.1),rgba(232,60,0,0)_68%),radial-gradient(45%_40%_at_0%_100%,rgba(255,107,44,.05),rgba(255,107,44,0)_70%)] dark:opacity-100"
        aria-hidden="true"
      />

      <Container className="relative z-10">
        <SectionHeading
          eyebrow="The research branch"
          title="Res-BiLSTM-AM, end to end."
          description="A dual-feature acoustic branch with attention and residual connections, implemented in TensorFlow / Keras and kept separate from the lightweight runtime."
        />

        <div className="grid items-start gap-12 lg:grid-cols-[minmax(0,5fr)_minmax(0,7fr)] lg:gap-[48px] xl:gap-[64px]">
          <Reveal>
            <div className="grid grid-cols-2 gap-2.5">
              {[
                { value: "200 × 143", label: "Model input" },
                { value: "143", label: "Features per frame" },
                { value: "4", label: "Attention heads" },
                { value: "128 × 2", label: "BiLSTM units" },
              ].map((stat) => (
                <div
                  key={stat.label}
                  className="min-h-[91px] rounded-xl border border-border bg-card px-4 py-4"
                >
                  <div className="font-display text-[27px] leading-[1.05] font-normal tracking-[-0.045em] text-foreground tabular-nums max-sm:text-[23px]">
                    {stat.value}
                  </div>
                  <div className="mt-1.5 font-mono text-[10px] tracking-[0.1em] text-muted-foreground uppercase">
                    {stat.label}
                  </div>
                </div>
              ))}
            </div>

            <div className="mt-6">
              <div className="flex items-center justify-between gap-4">
                <span className="font-mono text-[10px] font-medium tracking-[0.12em] text-muted-foreground uppercase">
                  Feature contract
                </span>
                <b className="font-mono text-[10px] font-normal tracking-[0.08em] text-signal-text">
                  143 TOTAL
                </b>
              </div>
              <div className="mt-2.5 flex h-2.5 gap-0.5 overflow-hidden rounded-[3px]">
                <span className="bg-signal" style={{ flex: 120 }} />
                <span className="bg-signal-bright" style={{ flex: 4 }} />
                <span className="bg-[#FFB18A]" style={{ flex: 7 }} />
                <span className="bg-peach-deep" style={{ flex: 12 }} />
              </div>
              <div className="mt-2.5 grid grid-cols-2 gap-x-3.5 gap-y-1.5 max-sm:grid-cols-1">
                {project.model.features.map((feature, index) => (
                  <span
                    key={feature.label}
                    className="flex items-center gap-1.5 font-mono text-[10px] tracking-[0.04em] text-muted-foreground"
                  >
                    <i
                      className={[
                        "size-[5px] shrink-0 rounded-[1px]",
                        index === 0 && "bg-signal",
                        index === 1 && "bg-signal-bright",
                        index === 2 && "bg-[#FFB18A]",
                        index === 3 && "bg-peach-deep",
                      ]
                        .filter(Boolean)
                        .join(" ")}
                    />
                    {feature.label} &middot; {feature.count}
                  </span>
                ))}
              </div>
            </div>

            <div className="mt-5 flex flex-wrap gap-1.5">
              {training.map((item) => (
                <span
                  key={item}
                  className="rounded-[4px] border border-border bg-card px-1.5 py-1 font-mono text-[10px] tracking-[0.06em] text-muted-foreground uppercase"
                >
                  {item}
                </span>
              ))}
            </div>

            <div className="mt-5 flex items-start gap-3 rounded-[9px] border border-amber/25 bg-amber/[0.055] px-3.5 py-3.5">
              <span className="mt-[5px] size-1.5 shrink-0 rounded-full bg-amber" />
              <p className="text-[11.5px] leading-[1.6] text-muted-foreground">
                <b className="font-medium text-foreground">Honest boundary.</b> No
                pretrained checkpoint ships with this repository. The paper
                reports ESTOI 97.2% on its own data; this implementation does not
                reproduce or claim those numbers.
              </p>
            </div>

            <div className="mt-6 flex flex-wrap gap-2.5">
              <Button asChild variant="paper" size="cta">
                <a href={DOCS.paperNotes} target="_blank" rel="noreferrer">
                  Read the paper notes
                  <ArrowUpRight className="size-4" />
                </a>
              </Button>
              <Button asChild variant="paper" size="cta">
                <a href={DOCS.modelCode} target="_blank" rel="noreferrer">
                  View model code
                  <Code2 className="size-4" />
                </a>
              </Button>
            </div>
          </Reveal>

          <Reveal delay={80}>
            <div className="rounded-2xl border border-border bg-card px-5 pt-1 pb-1.5 shadow-[0_30px_60px_rgba(60,20,5,.08)] max-sm:px-3.5">
              <div className="flex items-center justify-between gap-3 border-b border-border py-3">
                <span className="font-mono text-[10px] font-medium tracking-[0.12em] text-muted-foreground uppercase">
                  Forward pass
                </span>
                <span className="flex items-center gap-1.5 font-mono text-[10px] tracking-[0.08em] text-live uppercase">
                  <span className="size-1 rounded-full bg-live" />
                  Trainable
                </span>
              </div>

              <div className="arch-line relative">
                {architecture.map((row) => (
                  <div
                    key={row.key}
                    className="grid grid-cols-[16px_1fr_auto] items-center gap-3 border-b border-border py-2.5 last:border-b-0"
                  >
                    <span
                      className={
                        row.active
                          ? "size-[5px] justify-self-center rounded-full bg-signal shadow-[0_0_0_3px_rgba(232,60,0,.14)]"
                          : "size-[5px] justify-self-center rounded-full bg-muted-foreground/30"
                      }
                    />
                    <div className="min-w-0">
                      <span className="block font-mono text-[10px] tracking-[0.1em] text-muted-foreground uppercase">
                        {row.key}
                      </span>
                      <strong className="flex flex-wrap items-center gap-1.5 font-display text-[13.5px] leading-[1.3] font-normal text-foreground max-sm:text-xs">
                        {row.value}
                        {row.tag ? (
                          <span className="rounded-[3px] border border-signal/30 bg-signal/[0.08] px-1 py-0.5 font-mono text-[10px] tracking-[0.06em] whitespace-nowrap text-signal-text uppercase">
                            {row.tag}
                          </span>
                        ) : null}
                      </strong>
                    </div>
                    <span className="font-mono text-[10px] tracking-[0.04em] whitespace-nowrap text-muted-foreground max-sm:text-[10px]">
                      {row.note}
                    </span>
                  </div>
                ))}
              </div>
            </div>
          </Reveal>
        </div>
      </Container>
    </section>
  );
}
