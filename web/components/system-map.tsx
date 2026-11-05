import { Eyebrow } from "@/components/eyebrow";
import { MermaidDiagram } from "@/components/mermaid-diagram";

const runtimeChart = `flowchart LR
  A["Telugu speech<br/>mic · file · text"] --> B["Telugu ASR<br/>Google · te-IN"]
  B --> C["Translator<br/>214 entries · pivot · stem"]
  C --> D["ISL gloss<br/>ordered sequence"]
  D --> E["Frame corpus<br/>ordered frames"]
  E --> F["Playback<br/>400 × 400 · ~10 fps"]
  E -.->|no frames| G["TEXT_&lt;word&gt;<br/>text card"]`;

const runtimeChartMobile = `flowchart TB
  A["Telugu speech<br/>mic · file · text"] --> B["Telugu ASR<br/>Google · te-IN"]
  B --> C["Translator<br/>214 entries · pivot · stem"]
  C --> D["ISL gloss<br/>ordered sequence"]
  D --> E["Frame corpus<br/>ordered frames"]
  E --> F["Playback<br/>400 × 400 · ~10 fps"]
  E -.->|no frames| G["TEXT_&lt;word&gt;<br/>text card"]`;

const researchChart = `flowchart LR
  A["Telugu audio<br/>16 kHz mono"] --> B["Dual features<br/>200 × 143"]
  F["Feature contract<br/>MFCC 120 · spectral 23"] --> B
  B --> C["Res-BiLSTM-AM<br/>attention + residual"]
  C --> D["Sign class<br/>softmax · N classes"]`;

const researchChartMobile = `flowchart TB
  A["Telugu audio<br/>16 kHz mono"] --> B["Dual features<br/>143-D · 200 frames"]
  B --> C["Res-BiLSTM-AM<br/>attention + residual"]
  C --> D["Sign class<br/>softmax · N classes"]`;

function DiagramCard({
  eyebrow,
  title,
  chart,
  mobileChart,
  note,
}: {
  eyebrow: string;
  title: string;
  chart: string;
  mobileChart: string;
  note: string;
}) {
  return (
    <div className="relative overflow-hidden rounded-2xl border border-border bg-card p-5 sm:p-6">
      <div className="flex flex-wrap items-start justify-between gap-3">
        <div>
          <Eyebrow>{eyebrow}</Eyebrow>
          <h3 className="mt-2 font-display text-[19px] font-medium tracking-[-0.02em] text-foreground">
            {title}
          </h3>
        </div>
        <span className="rounded-[4px] border border-border bg-muted px-2 py-1 font-mono text-[9px] tracking-[0.08em] text-muted-foreground uppercase">
          Mermaid · from docs
        </span>
      </div>

      <div className="mt-5 overflow-hidden rounded-xl border border-border bg-background/40 px-2 py-4 sm:px-4">
        <MermaidDiagram
          chart={chart}
          mobileChart={mobileChart}
          label={`${title} — Mermaid flowchart`}
        />
      </div>

      <div className="mt-4 border-t border-border pt-3 font-mono text-[10px] leading-[1.55] tracking-[0.04em] text-muted-foreground">
        {note}
      </div>
    </div>
  );
}

export function SystemMap() {
  return (
    <div className="mt-4 grid gap-4">
      <DiagramCard
        eyebrow="Runtime map"
        title="Speech to sign, end to end"
        chart={runtimeChart}
        mobileChart={runtimeChartMobile}
        note="README.md · runtime path · fallback is a first-class branch"
      />
      <DiagramCard
        eyebrow="Research map"
        title="Audio to a sign class"
        chart={researchChart}
        mobileChart={researchChartMobile}
        note="PAPER_NOTES.md · dual features · Res-BiLSTM-AM · softmax"
      />
    </div>
  );
}
