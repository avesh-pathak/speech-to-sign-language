"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { Menu, X } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Container } from "@/components/container";
import { GitHubIcon } from "@/components/github-icon";
import { VaniSignMark } from "@/components/vanisign-mark";
import { IconTile } from "@/components/icon-tile";
import { ThemeToggle } from "@/components/theme-toggle";
import { GITHUB_URL } from "@/lib/project";

const links = [
  { href: "#problem", label: "Problem" },
  { href: "#how", label: "How it works" },
  { href: "#build", label: "What I built" },
  { href: "#model", label: "The model" },
  { href: "#stack", label: "Stack" },
];

const mobileLinks = [
  { href: "#problem", label: "The problem", number: "01" },
  { href: "#how", label: "How it works", number: "02" },
  { href: "#language", label: "Translation", number: "03" },
  { href: "#build", label: "What I built", number: "04" },
  { href: "#model", label: "The model", number: "05" },
  { href: "#stack", label: "Stack", number: "06" },
];

export function SiteHeader() {
  const [open, setOpen] = useState(false);

  useEffect(() => {
    const onKeyDown = (event: KeyboardEvent) => {
      if (event.key === "Escape") setOpen(false);
    };

    const onResize = () => {
      if (window.innerWidth >= 1024) setOpen(false);
    };

    document.addEventListener("keydown", onKeyDown);
    window.addEventListener("resize", onResize);

    return () => {
      document.removeEventListener("keydown", onKeyDown);
      window.removeEventListener("resize", onResize);
    };
  }, []);

  useEffect(() => {
    if (!open) return;
    const previous = document.body.style.overflow;
    document.body.style.overflow = "hidden";
    return () => {
      document.body.style.overflow = previous;
    };
  }, [open]);

  return (
    <header className="fixed inset-x-0 top-0 z-50 h-[calc(4rem+env(safe-area-inset-top))] border-b border-border bg-card/[0.96] pt-[env(safe-area-inset-top)] backdrop-blur-md">
      <Container className="grid h-full grid-cols-[1fr_auto] items-center gap-4 lg:grid-cols-[1fr_auto_1fr] lg:gap-6">
        <Link
          href="#top"
          className="flex min-h-11 min-w-0 items-center gap-2.5"
          aria-label="VaniSign home"
          onClick={() => setOpen(false)}
        >
          <VaniSignMark className="size-[30px] text-foreground" />
          <span className="font-display text-[22px] leading-none font-semibold tracking-[-0.045em]">
            VaniSign
          </span>
          <span className="hidden h-5 w-px bg-border xl:block" aria-hidden="true" />
          <span className="hidden font-mono text-[10px] font-medium tracking-[0.13em] whitespace-nowrap text-muted-foreground uppercase xl:block">
            Telugu &rarr; ISL
          </span>
        </Link>

        <nav className="hidden items-center gap-0.5 lg:flex" aria-label="Primary">
          {links.map((link) => (
            <a
              key={link.href}
              href={link.href}
              className="inline-flex min-h-11 items-center rounded-lg px-3 py-2.5 font-display text-[13.5px] text-foreground transition-colors hover:bg-foreground/5 hover:text-signal-text"
            >
              {link.label}
            </a>
          ))}
        </nav>

        <div className="flex items-center justify-self-end gap-2">
          <ThemeToggle className="hidden sm:grid" />
          <Button
            asChild
            variant="ink"
            size="nav"
            className="max-lg:px-2.5"
          >
            <a
              href={GITHUB_URL}
              target="_blank"
              rel="noreferrer"
              aria-label="View the VaniSign source on GitHub"
            >
              <span className="hidden sm:inline">GitHub</span>
              <IconTile className="size-[22px]">
                <GitHubIcon className="size-3.5" />
              </IconTile>
            </a>
          </Button>

          <button
            type="button"
            className="grid size-11 place-items-center rounded-lg border border-border bg-card text-foreground transition-colors hover:bg-muted lg:hidden"
            aria-label={open ? "Close menu" : "Open menu"}
            aria-expanded={open}
            aria-controls="mobile-menu"
            onClick={() => setOpen((value) => !value)}
          >
            {open ? <X className="size-4" /> : <Menu className="size-4" />}
          </button>
        </div>
      </Container>

      {open ? (
        <div
          id="mobile-menu"
          className="menu-enter absolute inset-x-0 top-full max-h-[calc(100dvh-4rem-env(safe-area-inset-top))] overflow-y-auto overscroll-contain border-b border-border bg-card px-5 pt-2 pb-6 text-foreground shadow-[0_24px_60px_rgba(60,20,5,.16)] sm:px-8 lg:hidden"
          data-lenis-prevent
        >
          <nav aria-label="Mobile" className="mx-auto max-w-[560px]">
            {mobileLinks.map((link) => (
              <a
                key={link.href}
                href={link.href}
                onClick={() => setOpen(false)}
                className="flex min-h-14 items-center justify-between border-b border-border py-3.5 font-display text-base text-muted-foreground transition-colors hover:text-foreground"
              >
                {link.label}
                <span className="font-mono text-[10px] tracking-[0.1em] text-muted-foreground">
                  {link.number}
                </span>
              </a>
            ))}
            <ThemeToggle variant="menu" />
            <Button
              asChild
              variant="signal"
              size="cta"
              className="mt-5 w-full justify-between"
            >
              <a href={GITHUB_URL} target="_blank" rel="noreferrer">
                View on GitHub
                <IconTile className="bg-signal-deep">
                  <GitHubIcon className="size-3.5" />
                </IconTile>
              </a>
            </Button>
          </nav>
        </div>
      ) : null}
    </header>
  );
}
