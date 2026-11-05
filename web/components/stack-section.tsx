import { Card } from "@/components/ui/card";
import { Container } from "@/components/container";
import { Reveal } from "@/components/reveal";
import { SectionHeading } from "@/components/section-heading";
import { project } from "@/lib/project";

const contracts = [
  "16 kHz mono audio",
  "200 × 143 input",
  "214 curated mappings",
  "~10 fps playback",
  "400 × 400 display",
  "Text fallback",
];

export function StackSection() {
  return (
    <section id="stack" className="relative pt-24 pb-16 md:pt-28 lg:pt-[150px] lg:pb-[88px]">
      <Container>
        <SectionHeading
          eyebrow="The stack"
          title="Runs on a laptop. Trains on a GPU."
          description="The desktop runtime needs no TensorFlow and no GPU. The research stack is optional — installed only when you want to train or classify with the acoustic model."
        />

        <div className="grid gap-4 md:grid-cols-3">
          {project.stack.map((group, index) => (
            <Reveal key={group.group} delay={index * 60} className="h-full">
              <Card
                className={[
                  "flex h-full flex-col gap-0 rounded-2xl border border-border py-0 ring-0 shadow-[0_1px_2px_rgba(25,14,9,.03)]",
                  index === 2
                    ? "bg-[linear-gradient(150deg,var(--accent)_0%,var(--card)_70%)]"
                    : "bg-card",
                ].join(" ")}
              >
                <div className="flex items-center justify-between gap-3 border-b border-border px-5 py-4">
                  <h3 className="font-display text-base font-medium tracking-[-0.02em] text-foreground">
                    {group.group}
                  </h3>
                  <span className="font-mono text-[10px] tracking-[0.1em] text-muted-foreground uppercase">
                    {group.note}
                  </span>
                </div>

                <div className="flex flex-1 flex-col px-5 py-1">
                  {group.items.map((item) => (
                    <div
                      key={item.name}
                      className="flex items-center justify-between gap-3 border-b border-foreground/[0.055] py-2.5 last:border-b-0"
                    >
                      <div className="min-w-0">
                        <b className="block font-display text-[13.5px] leading-[1.35] font-medium tracking-[-0.01em] text-foreground">
                          {item.name}
                        </b>
                        <span className="block text-[10px] leading-[1.4] text-muted-foreground">
                          {item.role}
                        </span>
                      </div>
                      <span className="text-right font-mono text-[10px] tracking-[0.04em] whitespace-nowrap text-muted-foreground">
                        {item.version}
                      </span>
                    </div>
                  ))}
                </div>
              </Card>
            </Reveal>
          ))}
        </div>

        <Reveal className="mt-6 flex flex-wrap gap-1.5">
          {contracts.map((contract) => (
            <span
              key={contract}
              className="inline-flex items-center gap-1.5 rounded-[4px] border border-border bg-card px-1.5 py-1.5 font-mono text-[10px] tracking-[0.06em] text-muted-foreground uppercase"
            >
              <span className="size-1 rounded-[1px] bg-signal" aria-hidden="true" />
              {contract}
            </span>
          ))}
        </Reveal>
      </Container>
    </section>
  );
}
