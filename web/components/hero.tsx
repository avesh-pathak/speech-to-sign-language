import { ArrowDown } from "lucide-react";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Container } from "@/components/container";
import { GitHubIcon } from "@/components/github-icon";
import { IconTile } from "@/components/icon-tile";
import { ProductConsole } from "@/components/product-console";
import { GITHUB_URL } from "@/lib/project";

function HeroBadge({ children }: { children: React.ReactNode }) {
  return (
    <Badge
      variant="outline"
      className="h-auto gap-2 rounded-[7px] border-foreground/[0.08] bg-foreground/5 px-2.5 py-1 font-display text-xs font-normal text-foreground"
    >
      <span
        className="size-[7px] rounded-full bg-signal shadow-[0_0_0_3px_rgba(232,60,0,.12)]"
        aria-hidden="true"
      />
      {children}
    </Badge>
  );
}

export function Hero() {
  return (
    <section
      id="top"
      className="relative overflow-hidden pt-[calc(90px+env(safe-area-inset-top))]"
    >
      <div className="hero-atmosphere" aria-hidden="true" />

      <Container className="relative z-10">
        <div className="mb-6 flex flex-wrap justify-center gap-2 max-sm:gap-1.5">
          <HeroBadge>Telugu-first speech recognition</HeroBadge>
          <HeroBadge>214-entry ISL mapping</HeroBadge>
          <HeroBadge>Res-BiLSTM-AM research branch</HeroBadge>
        </div>

        <h1 className="mx-auto max-w-[1060px] text-center font-display text-[clamp(2.125rem,7.8vw,3.5rem)] leading-[1.05] font-normal tracking-[-0.032em] text-foreground text-balance">
          Telugu speech in.
          <br />
          <span className="highlight-bar">Indian Sign Language</span> out.
        </h1>

        <p className="mx-auto mt-6 max-w-[660px] text-center font-display text-[17.5px] leading-[1.58] text-muted-foreground max-sm:text-[15.5px] max-sm:leading-[1.6]">
          Telugu speech becomes an ordered ISL gloss sequence and matching sign
          frames &mdash; with a text fallback that never drops a word.
        </p>

        <div className="mt-6 flex flex-wrap items-center justify-center gap-2.5 max-[520px]:mx-auto max-[520px]:max-w-[270px] max-[520px]:flex-col max-[520px]:items-stretch">
          <Button asChild variant="ink" size="cta" className="max-[520px]:justify-between">
            <a href={GITHUB_URL} target="_blank" rel="noreferrer">
              View on GitHub
              <IconTile>
                <GitHubIcon className="size-3.5" />
              </IconTile>
            </a>
          </Button>
          <Button asChild variant="paper" size="cta" className="max-[520px]:justify-between">
            <a href="#how">
              See how it works
              <IconTile variant="paper">
                <ArrowDown className="size-3.5" />
              </IconTile>
            </a>
          </Button>
        </div>

        <p className="mt-3.5 text-center font-mono text-[10px] font-medium tracking-[0.06em] text-muted-foreground max-sm:leading-[1.9]">
          VaniSign &middot; academic capstone &middot; implementation of the
          ICSCSA 2025 paper &middot;{" "}
          <a
            href="#model"
            className="inline-block border-b border-foreground/30 py-2 -my-2 transition-colors hover:border-signal hover:text-signal-text"
          >
            read the research notes
          </a>
        </p>

        <ProductConsole />

        <div className="mx-auto mt-3 flex max-w-[1040px] items-center justify-between gap-4 font-mono text-[10px] tracking-[0.04em] text-muted-foreground max-sm:hidden xl:max-w-[1080px] 2xl:max-w-[1120px]">
          <span>Illustrative runtime &middot; sign frames require a corpus</span>
          <span>Telugu ASR &middot; ISL gloss &middot; sign playback</span>
        </div>

        <div className="h-16 max-sm:h-6" aria-hidden="true" />
      </Container>
    </section>
  );
}
