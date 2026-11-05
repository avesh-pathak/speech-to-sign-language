import Link from "next/link";
import { ArrowDown, ArrowLeft, ArrowUpRight } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Container } from "@/components/container";
import { Eyebrow } from "@/components/eyebrow";
import { GitHubIcon } from "@/components/github-icon";
import { IconTile } from "@/components/icon-tile";
import { MissingRouteConsole } from "@/components/missing-route-console";
import { ThemeToggle } from "@/components/theme-toggle";
import { VaniSignMark } from "@/components/vanisign-mark";
import { DOCS, GITHUB_URL } from "@/lib/project";

const destinations = [
  { number: "01", label: "The problem", href: "/#problem" },
  { number: "02", label: "How it works", href: "/#how" },
  { number: "03", label: "The model", href: "/#model" },
  { number: "04", label: "The stack", href: "/#stack" },
];

export default function NotFound() {
  return (
    <div className="flex min-h-dvh flex-col bg-background">
      <header className="relative z-20 border-b border-border bg-card/95 backdrop-blur-md">
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
            <span
              className="hidden h-5 w-px bg-border sm:block"
              aria-hidden="true"
            />
            <span className="hidden font-mono text-[10px] font-medium tracking-[0.13em] whitespace-nowrap text-muted-foreground uppercase sm:block">
              404 &middot; Signal lost
            </span>
          </Link>

          <div className="flex items-center gap-2">
            <ThemeToggle className="hidden sm:grid" />
            <Button asChild variant="ink" size="nav">
              <Link href="/" aria-label="Back to home">
                <span className="sm:hidden">Home</span>
                <span className="hidden sm:inline">Back home</span>
                <IconTile>
                  <ArrowLeft className="size-3.5" />
                </IconTile>
              </Link>
            </Button>
          </div>
        </Container>
      </header>

      <main id="main" className="relative flex-1 overflow-hidden">
        <div className="hero-atmosphere" aria-hidden="true" />

        <Container className="relative z-10 py-14 sm:py-20 lg:py-24">
          <div className="grid items-center gap-12 lg:grid-cols-[minmax(0,1.06fr)_minmax(0,.94fr)] lg:gap-16 xl:gap-24">
            <div>
              <Eyebrow>Error 404 &middot; Route not found</Eyebrow>

              <h1 className="mt-4 max-w-[640px] font-display text-[clamp(2.55rem,6.4vw,4.35rem)] leading-[0.99] font-normal tracking-[-0.048em] text-foreground text-balance">
                This page got{" "}
                <span className="highlight-bar">lost in translation</span>.
              </h1>

              <div className="mt-7 flex items-center gap-3.5">
                <span
                  className="h-9 w-px shrink-0 bg-signal"
                  aria-hidden="true"
                />
                <div>
                  <p
                    lang="te"
                    className="font-telugu text-[19px] leading-[1.5] text-foreground"
                  >
                    ఈ పేజీ కనబడలేదు
                  </p>
                  <p className="mt-0.5 font-mono text-[10px] font-medium tracking-[0.1em] text-muted-foreground uppercase">
                    This page was not found
                  </p>
                </div>
              </div>

              <p className="mt-6 max-w-[490px] text-[15px] leading-[1.7] text-muted-foreground">
                The address may be mistyped, moved, or retired. Nothing else
                went missing &mdash; the dictionary, the model notes, and the
                source are all still on air.
              </p>

              <div className="mt-7 flex flex-wrap items-center gap-2.5 max-[520px]:items-stretch">
                <Button
                  asChild
                  variant="ink"
                  size="cta"
                  className="max-[520px]:justify-between"
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
                  className="max-[520px]:justify-between"
                >
                  <Link href="/#how">
                    See how it works
                    <IconTile variant="paper">
                      <ArrowDown className="size-3.5" />
                    </IconTile>
                  </Link>
                </Button>
              </div>

              <div className="mt-10 border-t border-border pt-5">
                <p className="font-mono text-[10px] font-medium tracking-[0.12em] text-muted-foreground uppercase">
                  Recover the signal
                </p>
                <div className="mt-1 grid sm:grid-cols-2 sm:gap-x-8">
                  {destinations.map((destination) => (
                    <Link
                      key={destination.href}
                      href={destination.href}
                      className="group flex min-h-11 items-center gap-3 border-b border-border py-2.5 font-display text-[14px] text-foreground transition-colors hover:text-signal-text"
                    >
                      <span className="font-mono text-[10px] tracking-[0.08em] text-muted-foreground">
                        {destination.number}
                      </span>
                      {destination.label}
                      <ArrowUpRight className="ml-auto size-3.5 text-muted-foreground transition-colors group-hover:text-signal" />
                    </Link>
                  ))}
                </div>
              </div>
            </div>

            <div className="relative">
              <div
                className="pointer-events-none absolute -inset-6 rounded-[32px] bg-[radial-gradient(65%_65%_at_70%_20%,rgba(232,60,0,.14),rgba(232,60,0,0)_72%)] blur-2xl"
                aria-hidden="true"
              />
              <MissingRouteConsole />
              <p className="relative mt-3 flex flex-wrap items-center justify-between gap-2 px-1 font-mono text-[10px] tracking-[0.04em] text-muted-foreground">
                <span>Illustrative trace &middot; no page was harmed</span>
                <span>HTTP 404 &middot; fallback ready</span>
              </p>
            </div>
          </div>
        </Container>
      </main>

      <footer className="relative z-10 border-t border-border bg-card">
        <Container className="flex flex-col gap-3 py-6 pb-[calc(1.5rem+env(safe-area-inset-bottom))] sm:flex-row sm:items-center sm:justify-between">
          <p className="font-mono text-[10px] leading-[1.7] tracking-[0.05em] text-muted-foreground">
            &copy; 2026 VaniSign &middot; Telugu speech to Indian Sign Language
          </p>
          <nav
            aria-label="Footer"
            className="flex flex-wrap items-center gap-x-5 gap-y-2 font-display text-[13px]"
          >
            <Link
              href="/"
              className="inline-flex min-h-11 items-center transition-colors hover:text-signal-text sm:min-h-0"
            >
              Home
            </Link>
            <a
              href={DOCS.readme}
              target="_blank"
              rel="noreferrer"
              className="inline-flex min-h-11 items-center gap-1 transition-colors hover:text-signal-text sm:min-h-0"
            >
              README
              <ArrowUpRight className="size-2.5 opacity-60" />
            </a>
            <a
              href={GITHUB_URL}
              target="_blank"
              rel="noreferrer"
              className="inline-flex min-h-11 items-center gap-1.5 transition-colors hover:text-signal-text sm:min-h-0"
            >
              <GitHubIcon className="size-3.5" />
              GitHub
            </a>
          </nav>
        </Container>
      </footer>
    </div>
  );
}
