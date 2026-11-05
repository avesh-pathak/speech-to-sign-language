import Link from "next/link";
import { ArrowLeft, ArrowRight } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Container } from "@/components/container";
import { Eyebrow } from "@/components/eyebrow";
import { IconTile } from "@/components/icon-tile";
import { ThemeToggle } from "@/components/theme-toggle";
import { VaniSignMark } from "@/components/vanisign-mark";

export default function NotFound() {
  return (
    <div className="flex min-h-dvh flex-col bg-background">
      <header className="border-b border-border">
        <Container className="flex h-[calc(4rem+env(safe-area-inset-top))] items-center justify-between gap-4 pt-[env(safe-area-inset-top)]">
          <Link
            href="/"
            className="flex min-h-11 min-w-0 items-center gap-2.5"
            aria-label="VaniSign home"
          >
            <VaniSignMark className="size-[30px] text-foreground" />
            <span className="font-display text-[22px] leading-none font-semibold tracking-[-0.045em]">
              VaniSign
            </span>
          </Link>

          <ThemeToggle />
        </Container>
      </header>

      <main
        id="main"
        className="flex flex-1 items-center justify-center px-6 py-20"
      >
        <div className="w-full max-w-[520px] text-center">
          <Eyebrow>Error 404</Eyebrow>

          <h1 className="mt-5 font-display text-[clamp(2.5rem,7vw,3.75rem)] leading-[1.02] font-normal tracking-[-0.045em] text-foreground text-balance">
            This page doesn&apos;t exist.
          </h1>

          <p
            lang="te"
            className="mt-6 font-telugu text-[19px] leading-[1.6] text-muted-foreground"
          >
            ఈ పేజీ కనబడలేదు
          </p>

          <p className="mx-auto mt-2 max-w-[380px] text-[15px] leading-[1.7] text-muted-foreground">
            The link may be broken, or the page may have moved.
          </p>

          <div className="mt-8 flex flex-col items-center justify-center gap-2.5 sm:flex-row">
            <Button
              asChild
              variant="ink"
              size="cta"
              className="w-full justify-between sm:w-auto"
            >
              <Link href="/">
                Back to home
                <IconTile>
                  <ArrowLeft className="size-3.5" />
                </IconTile>
              </Link>
            </Button>
            <Button
              asChild
              variant="paper"
              size="cta"
              className="w-full justify-between sm:w-auto"
            >
              <Link href="/#how">
                See how it works
                <IconTile variant="paper">
                  <ArrowRight className="size-3.5" />
                </IconTile>
              </Link>
            </Button>
          </div>
        </div>
      </main>

      <footer className="border-t border-border">
        <Container className="py-6 pb-[calc(1.5rem+env(safe-area-inset-bottom))] text-center font-mono text-[10px] tracking-[0.05em] text-muted-foreground">
          &copy; 2026 VaniSign &middot; Telugu speech to Indian Sign Language
        </Container>
      </footer>
    </div>
  );
}
