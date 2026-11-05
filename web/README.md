# VaniSign — web

The product landing page for **VaniSign**, built with Next.js, React, Tailwind CSS, and shadcn/ui.

## Run

```bash
npm install
npm run dev
```

Open [http://localhost:3000](http://localhost:3000).

## Stack

- **Next.js 16** (App Router, Turbopack)
- **React 19** + **TypeScript**
- **Tailwind CSS 4**
- **shadcn/ui** primitives (Button, Card, Badge, Tabs, Separator)
- **next-themes** light/dark theme toggle with light as the default
- **Mermaid** flowcharts rendered from the repository docs
- **lucide-react** icons
- **Lenis** smooth scrolling (native fallback for reduced motion)
- **next/font** — Instrument Sans, IBM Plex Sans, Geist Mono, Noto Sans Telugu

## Structure

```text
app/
  page.tsx                 # landing page composition
  layout.tsx               # fonts + metadata + theme provider
  globals.css              # Vobiz tokens, light/dark themes, atmosphere
  icon.svg                 # VaniSign favicon
  apple-icon.png           # Apple touch icon
  opengraph-image.tsx      # 1200×630 Open Graph image
  sitemap.ts               # sitemap.xml
  robots.ts                # robots.txt
  manifest.ts              # web app manifest
  api/
    project/route.ts       # typed project overview (JSON)
    health/route.ts        # lightweight service health
components/
  site-header.tsx          # nav + mobile menu + GitHub link
  hero.tsx                 # headline, CTAs, product console
  product-console.tsx      # illustrative runtime surface
  problem-section.tsx      # problem statement + before/after
  pipeline-section.tsx     # five-step runtime + Mermaid system maps
  language-section.tsx     # dictionary / pivot / stem layers
  build-section.tsx        # what is in the repository
  model-section.tsx        # Res-BiLSTM-AM research branch
  stack-section.tsx        # runtime and research dependencies
  quick-start.tsx          # platform tabs + commands
  site-footer.tsx
lib/
  project.ts               # typed source of truth for page + API
```

## API

- `GET /api/project` — typed project overview, runtime facts, model contract, stack, and links.
- `GET /api/health` — service status and timestamp.

## Environment

`NEXT_PUBLIC_SITE_URL` is optional. On Vercel the app falls back to the provided production/deployment host; for a custom or stable domain set:

```text
NEXT_PUBLIC_SITE_URL=https://your-production-domain.com
```

## Design

The UI follows the Vobiz design-language capture: warm paper, ink-black console surfaces, signal orange, mono telemetry labels, 8px buttons with trailing icon tiles, and 150px section rhythm. Light and dark themes are driven by the semantic tokens in `app/globals.css`.
