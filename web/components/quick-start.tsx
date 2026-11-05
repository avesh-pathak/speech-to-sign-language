"use client";

import { useEffect, useState } from "react";
import { ArrowUpRight, BookOpen, Check, Copy } from "lucide-react";
import {
  Tabs,
  TabsContent,
  TabsList,
  TabsTrigger,
} from "@/components/ui/tabs";
import { Button } from "@/components/ui/button";
import { Container } from "@/components/container";
import { Eyebrow } from "@/components/eyebrow";
import { GitHubIcon } from "@/components/github-icon";
import { IconTile } from "@/components/icon-tile";
import { Reveal } from "@/components/reveal";
import { DOCS, GITHUB_URL } from "@/lib/project";

const commands = {
  windows: `git clone https://github.com/avesh-pathak/speech-to-sign-language
cd speech-to-sign-language
py -3.11 -m venv .venv
.\\.venv\\Scripts\\Activate.ps1
pip install -r requirements.txt
python app.py

# inspect what the runtime sees
python app.py --mode info`,
  unix: `git clone https://github.com/avesh-pathak/speech-to-sign-language
cd speech-to-sign-language
python3.11 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py

# inspect what the runtime sees
python app.py --mode info`,
} as const;

type Platform = keyof typeof commands;

function Prompt() {
  return <span className="text-signal-bright">$</span>;
}

function WindowsCommands() {
  return (
    <pre className="overflow-x-auto p-5 font-mono text-[11px] leading-[1.9] text-white max-sm:p-4 max-sm:text-[10px] max-lg:whitespace-pre-wrap max-lg:break-words">
      <span className="block">
        <Prompt /> git clone https://github.com/avesh-pathak/speech-to-sign-language
      </span>
      <span className="block">
        <Prompt /> cd speech-to-sign-language
      </span>
      <span className="block">
        <Prompt /> py -3.11 -m venv .venv
      </span>
      <span className="block">
        <Prompt /> .\.venv\Scripts\Activate.ps1
      </span>
      <span className="block">
        <Prompt /> pip install -r requirements.txt
      </span>
      <span className="block">
        <Prompt /> python app.py
      </span>
      <span className="block">&nbsp;</span>
      <span className="block text-white/50">
        # inspect what the runtime sees
      </span>
      <span className="block">
        <Prompt /> python app.py --mode info
      </span>
    </pre>
  );
}

function UnixCommands() {
  return (
    <pre className="overflow-x-auto p-5 font-mono text-[11px] leading-[1.9] text-white max-sm:p-4 max-sm:text-[10px] max-lg:whitespace-pre-wrap max-lg:break-words">
      <span className="block">
        <Prompt /> git clone https://github.com/avesh-pathak/speech-to-sign-language
      </span>
      <span className="block">
        <Prompt /> cd speech-to-sign-language
      </span>
      <span className="block">
        <Prompt /> python3.11 -m venv .venv
      </span>
      <span className="block">
        <Prompt /> source .venv/bin/activate
      </span>
      <span className="block">
        <Prompt /> pip install -r requirements.txt
      </span>
      <span className="block">
        <Prompt /> python app.py
      </span>
      <span className="block">&nbsp;</span>
      <span className="block text-white/50">
        # inspect what the runtime sees
      </span>
      <span className="block">
        <Prompt /> python app.py --mode info
      </span>
    </pre>
  );
}

export function QuickStart() {
  const [platform, setPlatform] = useState<Platform>("windows");
  const [copied, setCopied] = useState(false);

  useEffect(() => {
    if (!copied) return;
    const timeout = window.setTimeout(() => setCopied(false), 1600);
    return () => window.clearTimeout(timeout);
  }, [copied]);

  const copyCommands = async () => {
    const fallbackCopy = () => {
      const field = document.createElement("textarea");
      field.value = commands[platform];
      field.setAttribute("readonly", "");
      field.style.position = "fixed";
      field.style.left = "-9999px";
      document.body.appendChild(field);
      field.select();
      const copied = document.execCommand("copy");
      document.body.removeChild(field);
      if (copied) setCopied(true);
    };

    if (!navigator.clipboard) {
      fallbackCopy();
      return;
    }

    try {
      await navigator.clipboard.writeText(commands[platform]);
      setCopied(true);
    } catch {
      fallbackCopy();
    }
  };

  return (
    <section
      id="start"
      className="relative pt-20 pb-16 md:pt-24 lg:pt-[150px] lg:pb-[88px]"
    >
      <Container>
        <Reveal>
          <div className="relative overflow-hidden rounded-[22px] border border-border bg-card px-6 py-10 shadow-[0_30px_70px_rgba(60,20,5,.1)] sm:px-10 lg:grid lg:grid-cols-[minmax(0,5fr)_minmax(0,7fr)] lg:items-center lg:gap-10 lg:px-10 lg:py-10 xl:gap-14 xl:px-14 xl:py-14">
            <div
              className="pointer-events-none absolute inset-0 bg-[radial-gradient(50%_70%_at_78%_0%,rgba(232,60,0,.13),rgba(232,60,0,0)_70%),radial-gradient(40%_60%_at_0%_100%,rgba(255,107,44,.05),rgba(255,107,44,0)_70%)]"
              aria-hidden="true"
            />

            <div className="relative z-10">
              <Eyebrow>Run it locally</Eyebrow>
              <h2 className="mt-4 font-display text-[clamp(2rem,3.4vw,2.75rem)] leading-[1.04] font-normal tracking-[-0.045em] text-foreground text-balance">
                From clone to a running app.
              </h2>
              <p className="mt-4 max-w-[420px] text-[14.5px] leading-[1.65] text-muted-foreground">
                Install the runtime, launch the Tkinter window, and speak or type
                Telugu. Add a word-level ISL corpus when you have one &mdash;
                without it, every sign becomes a readable text card.
              </p>

              <div className="mt-6 flex flex-wrap gap-2.5 max-sm:flex-col max-sm:items-stretch">
                <Button
                  asChild
                  variant="signal"
                  size="cta"
                  className="max-sm:justify-between"
                >
                  <a href={GITHUB_URL} target="_blank" rel="noreferrer">
                    Open the repository
                    <IconTile className="bg-signal-deep">
                      <GitHubIcon className="size-3.5" />
                    </IconTile>
                  </a>
                </Button>
                <Button
                  asChild
                  variant="paper"
                  size="cta"
                  className="max-sm:justify-between"
                >
                  <a href={DOCS.setup} target="_blank" rel="noreferrer">
                    Read setup guide
                    <IconTile variant="paper">
                      <BookOpen className="size-3.5" />
                    </IconTile>
                  </a>
                </Button>
              </div>

              <p className="mt-5 font-mono text-[10px] tracking-[0.06em] text-muted-foreground">
                Python 3.10+ &middot; no GPU &middot; Google ASR for live speech
              </p>
            </div>

            <div className="relative z-10 mt-8 lg:mt-0">
              <Tabs
                value={platform}
                onValueChange={(value) => setPlatform(value as Platform)}
                className="gap-0 overflow-hidden rounded-xl border border-white/10 bg-[#0B0604] shadow-[0_20px_50px_rgba(0,0,0,.3)]"
              >
                <div className="flex items-center gap-2.5 border-b border-white/[0.08] px-3.5 py-2.5">
                  <div className="flex gap-1.5" aria-hidden="true">
                    <span className="size-[7px] rounded-full bg-signal" />
                    <span className="size-[7px] rounded-full bg-white/20" />
                    <span className="size-[7px] rounded-full bg-white/20" />
                  </div>
                  <span className="ml-0.5 hidden font-mono text-[10px] tracking-[0.1em] text-white/50 uppercase sm:inline">
                    quick start
                  </span>
                  <TabsList className="ml-auto h-auto gap-0.5 bg-transparent p-0">
                    <TabsTrigger
                      value="windows"
                      className="h-10 rounded-[4px] px-2 py-1 font-mono text-[10px] tracking-[0.06em] text-white/50 uppercase data-[state=active]:bg-white/10 data-[state=active]:text-white"
                    >
                      Windows
                    </TabsTrigger>
                    <TabsTrigger
                      value="unix"
                      className="h-10 rounded-[4px] px-2 py-1 font-mono text-[10px] tracking-[0.06em] text-white/50 uppercase data-[state=active]:bg-white/10 data-[state=active]:text-white"
                    >
                      macOS / Linux
                    </TabsTrigger>
                  </TabsList>
                  <button
                    type="button"
                    onClick={copyCommands}
                    aria-label={copied ? "Commands copied" : "Copy commands"}
                    title={copied ? "Copied" : "Copy commands"}
                    className="grid size-8 shrink-0 place-items-center rounded-[4px] text-white/50 transition-colors hover:bg-white/10 hover:text-white"
                  >
                    {copied ? (
                      <Check className="size-3.5 text-live" />
                    ) : (
                      <Copy className="size-3.5" />
                    )}
                  </button>
                  <span className="sr-only" aria-live="polite">
                    {copied ? "Commands copied to clipboard" : ""}
                  </span>
                </div>

                <TabsContent
                  value="windows"
                  className="mt-0 data-[state=active]:animate-in data-[state=active]:fade-in-0 data-[state=active]:slide-in-from-bottom-1 data-[state=active]:duration-150 motion-reduce:animate-none"
                >
                  <WindowsCommands />
                </TabsContent>
                <TabsContent
                  value="unix"
                  className="mt-0 data-[state=active]:animate-in data-[state=active]:fade-in-0 data-[state=active]:slide-in-from-bottom-1 data-[state=active]:duration-150 motion-reduce:animate-none"
                >
                  <UnixCommands />
                </TabsContent>

                <div className="flex flex-wrap items-center justify-between gap-2 border-t border-white/[0.08] px-3.5 py-2.5 font-mono text-[10px] tracking-[0.04em] text-white/50">
                  <span>Mappings &middot; signs &middot; frames &middot; ASR backend</span>
                  <b className="font-normal text-live">Fallback ready</b>
                </div>
              </Tabs>
            </div>
          </div>
        </Reveal>

        <Reveal className="mt-4 flex flex-col justify-between gap-2.5 px-1 font-mono text-[10px] tracking-[0.06em] text-muted-foreground sm:flex-row sm:items-center">
          <span>No ISL corpus? The app still starts in text-fallback mode.</span>
          <a
            href={DOCS.corpus}
            target="_blank"
            rel="noreferrer"
            className="inline-flex w-fit items-center gap-1.5 border-b border-foreground/25 pb-0.5 text-foreground transition-colors hover:border-signal hover:text-signal-text"
          >
            Corpus layout
            <ArrowUpRight className="size-2.5" />
          </a>
        </Reveal>
      </Container>
    </section>
  );
}
