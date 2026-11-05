import Link from "next/link";
import { ArrowUpRight, BookOpen, Globe } from "lucide-react";
import { Separator } from "@/components/ui/separator";
import { Container } from "@/components/container";
import { GitHubIcon } from "@/components/github-icon";
import { LinkedInIcon } from "@/components/linkedin-icon";
import { VaniSignMark } from "@/components/vanisign-mark";
import { DOCS, GITHUB_URL } from "@/lib/project";

const columns = [
  {
    heading: "Explore",
    links: [
      { label: "The problem", href: "#problem" },
      { label: "How it works", href: "#how" },
      { label: "The model", href: "#model" },
      { label: "The stack", href: "#stack" },
    ],
  },
  {
    heading: "Documentation",
    links: [
      { label: "README", href: DOCS.readme, external: true },
      { label: "Architecture", href: DOCS.architecture, external: true },
      { label: "Setup guide", href: DOCS.setup, external: true },
      { label: "Paper notes", href: DOCS.paperNotes, external: true },
    ],
  },
  {
    heading: "Source",
    links: [
      { label: "Repository", href: GITHUB_URL, external: true },
      { label: "Mapping JSON", href: DOCS.mapping, external: true },
      { label: "Tests", href: DOCS.tests, external: true },
      { label: "Issues", href: DOCS.issues, external: true },
    ],
  },
  {
    heading: "Connect",
    links: [
      { label: "LinkedIn", href: "https://www.linkedin.com/in/avesh-pathak/", external: true },
      { label: "Portfolio", href: "https://avesh.tech", external: true },
    ],
  },
];

export function SiteFooter() {
  return (
    <footer className="relative overflow-hidden border-t border-border bg-card pt-24 text-foreground">
      <div
        className="pointer-events-none absolute inset-0 bg-[radial-gradient(50%_45%_at_12%_0%,rgba(232,60,0,.08),rgba(232,60,0,0)_70%)] dark:opacity-100"
        aria-hidden="true"
      />

      <Container className="relative z-10">
        <div className="grid gap-12 lg:grid-cols-[1.2fr_2fr] lg:gap-20">
          <div>
            <Link
              href="#top"
              className="flex min-h-11 w-fit items-center gap-2.5"
              aria-label="VaniSign home"
            >
              <VaniSignMark className="size-[29px] text-foreground" />
              <span className="font-display text-[22px] leading-none font-semibold tracking-[-0.045em] text-foreground">
                VaniSign
              </span>
            </Link>
            <p className="mt-4 max-w-[330px] text-[13.5px] leading-[1.7] text-foreground/55">
              Telugu speech to Indian Sign Language. A dictionary-first runtime
              with a trainable acoustic branch, built as an academic capstone.
            </p>
            <p className="mt-3 max-w-[330px] font-mono text-[10px] leading-[1.7] tracking-[0.04em] text-foreground/55">
              Based on Mahalakshmi &amp; Anuradha, ICSCSA 2025.{" "}
              <a
                href={DOCS.paper}
                target="_blank"
                rel="noreferrer"
                className="border-b border-foreground/25 pb-px transition-colors hover:border-signal-bright hover:text-foreground"
              >
                DOI
              </a>
            </p>
            <div className="mt-6 grid max-w-[300px] grid-cols-4 gap-2">
              {[
                { label: "GitHub", href: GITHUB_URL, icon: GitHubIcon },
                {
                  label: "LinkedIn",
                  href: "https://www.linkedin.com/in/avesh-pathak/",
                  icon: LinkedInIcon,
                },
                {
                  label: "Portfolio",
                  href: "https://avesh.tech",
                  icon: Globe,
                },
                {
                  label: "Docs",
                  href: DOCS.architecture,
                  icon: BookOpen,
                },
              ].map(({ label, href, icon: Icon }) => (
                <a
                  key={label}
                  href={href}
                  target="_blank"
                  rel="noreferrer"
                  aria-label={
                    label === "Portfolio"
                      ? "Avesh Pathak's portfolio"
                      : label === "Docs"
                        ? "Architecture documentation"
                        : `${label}${label === "LinkedIn" ? " — Avesh Pathak" : ""}`
                  }
                  className="group flex flex-col items-center gap-2 rounded-lg py-1"
                >
                  <span className="grid size-11 place-items-center rounded-full border border-border bg-muted text-foreground/70 transition-colors group-hover:border-signal/50 group-hover:bg-signal group-hover:text-white">
                    <Icon className="size-[15px]" />
                  </span>
                  <span className="font-mono text-[9px] font-medium tracking-[0.07em] text-foreground/60 uppercase transition-colors group-hover:text-foreground/90">
                    {label}
                  </span>
                </a>
              ))}
            </div>
          </div>

          <div className="grid grid-cols-2 gap-8 sm:grid-cols-4">
            {columns.map((column) => (
              <div key={column.heading}>
                <h3 className="mb-3.5 font-mono text-[10px] font-semibold tracking-[0.13em] text-foreground/65 uppercase">
                  {column.heading}
                </h3>
                {column.links.map((link) => (
                  <a
                    key={link.label}
                    href={link.href}
                    {...("external" in link && link.external
                      ? { target: "_blank", rel: "noreferrer" }
                      : {})}
                    className="flex min-h-11 items-center gap-1.5 py-1 font-display text-[13.5px] font-medium text-foreground/80 transition-colors hover:text-foreground sm:min-h-0"
                  >
                    {link.label}
                    {"external" in link && link.external ? (
                      <ArrowUpRight className="size-2.5 opacity-50" />
                    ) : null}
                  </a>
                ))}
              </div>
            ))}
          </div>
        </div>

        <div
          className="pointer-events-none mt-16 mb-[-0.09em] select-none overflow-hidden text-center font-display text-[clamp(4rem,18vw,15rem)] leading-[.78] font-semibold tracking-[-0.07em] whitespace-nowrap text-foreground/5"
          aria-hidden="true"
        >
          VaniSign
        </div>

        <Separator className="bg-border" />

        <div className="flex flex-col items-start justify-between gap-2 py-5 pb-[calc(1.25rem+env(safe-area-inset-bottom))] font-mono text-[10px] tracking-[0.05em] text-foreground/55 sm:flex-row sm:items-center">
          <span>
            &copy; 2026 VaniSign &middot; academic capstone &middot; built by{" "}
            <a
              href="https://github.com/avesh-pathak"
              target="_blank"
              rel="noreferrer"
              className="border-b border-foreground/25 pb-px text-foreground/65 transition-colors hover:border-signal-bright hover:text-foreground"
            >
              Avesh Pathak
            </a>
          </span>
          <span>Telugu speech to Indian Sign Language</span>
        </div>
      </Container>
    </footer>
  );
}
