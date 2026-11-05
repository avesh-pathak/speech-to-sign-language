import type { Metadata, Viewport } from "next";
import {
  Geist_Mono,
  IBM_Plex_Sans,
  Instrument_Sans,
  Noto_Sans_Telugu,
} from "next/font/google";
import { SmoothScroll } from "@/components/smooth-scroll";
import { ThemeProvider } from "@/components/theme-provider";
import "./globals.css";

const instrument = Instrument_Sans({
  subsets: ["latin"],
  variable: "--font-instrument",
  display: "swap",
});

const plex = IBM_Plex_Sans({
  subsets: ["latin"],
  weight: ["300", "400", "500", "600", "700"],
  variable: "--font-plex",
  display: "swap",
});

const geistMono = Geist_Mono({
  subsets: ["latin"],
  variable: "--font-geist-mono",
  display: "swap",
});

const notoTelugu = Noto_Sans_Telugu({
  subsets: ["telugu"],
  variable: "--font-noto-telugu",
  display: "swap",
});

export const metadata: Metadata = {
  metadataBase: new URL(
    process.env.NEXT_PUBLIC_SITE_URL ?? "http://localhost:3000"
  ),
  title: "VaniSign — Telugu speech to Indian Sign Language",
  description:
    "VaniSign is a speech-to-sign translation framework for Telugu. It recognises spoken Telugu, produces an ordered ISL gloss sequence, and plays the matching sign frames — with a text fallback that never drops a word.",
  keywords: [
    "VaniSign",
    "Telugu",
    "Indian Sign Language",
    "speech to sign",
    "ISL",
    "accessibility",
    "Res-BiLSTM-AM",
    "speech recognition",
  ],
  openGraph: {
    title: "VaniSign — Telugu speech to Indian Sign Language",
    description:
      "Telugu speech in. Indian Sign Language out. A dictionary-first runtime with a trainable Res-BiLSTM-AM research branch.",
    type: "website",
  },
};

export const viewport: Viewport = {
  width: "device-width",
  initialScale: 1,
  viewportFit: "cover",
  themeColor: [
    { media: "(prefers-color-scheme: light)", color: "#FDFCFC" },
    { media: "(prefers-color-scheme: dark)", color: "#0D0806" },
  ],
};

export default function RootLayout({ children }: LayoutProps<"/">) {
  return (
    <html
      lang="en"
      suppressHydrationWarning
      className={`${instrument.variable} ${plex.variable} ${geistMono.variable} ${notoTelugu.variable}`}
    >
      <body>
        <ThemeProvider
          attribute="class"
          defaultTheme="system"
          enableSystem
          disableTransitionOnChange
          storageKey="vanisign-theme"
        >
          <SmoothScroll />
          {children}
        </ThemeProvider>
      </body>
    </html>
  );
}
