import type { Metadata, Viewport } from "next";
import {
  Geist_Mono,
  IBM_Plex_Sans,
  Instrument_Sans,
  Noto_Sans_Telugu,
} from "next/font/google";
import { SmoothScroll } from "@/components/smooth-scroll";
import { ThemeProvider } from "@/components/theme-provider";
import { siteConfig, siteUrl } from "@/lib/site";
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
  metadataBase: siteUrl,
  title: siteConfig.title,
  description: siteConfig.description,
  applicationName: siteConfig.name,
  authors: [{ name: siteConfig.author.name, url: siteConfig.author.portfolio }],
  creator: siteConfig.author.name,
  publisher: siteConfig.author.name,
  category: "technology",
  keywords: [
    "VaniSign",
    "Telugu",
    "Indian Sign Language",
    "speech to sign",
    "ISL",
    "accessibility",
    "Res-BiLSTM-AM",
    "speech recognition",
    "Telugu ASR",
  ],
  alternates: {
    canonical: "/",
  },
  robots: {
    index: true,
    follow: true,
    googleBot: {
      index: true,
      follow: true,
      "max-image-preview": "large",
      "max-snippet": -1,
      "max-video-preview": -1,
    },
  },
  openGraph: {
    title: siteConfig.title,
    description:
      "Telugu speech in. Indian Sign Language out. A dictionary-first runtime with a trainable Res-BiLSTM-AM research branch.",
    type: "website",
    url: "/",
    siteName: siteConfig.name,
    locale: "en_IN",
  },
  twitter: {
    card: "summary_large_image",
    title: siteConfig.title,
    description:
      "Telugu speech in. Indian Sign Language out. A dictionary-first runtime with a trainable Res-BiLSTM-AM research branch.",
    images: ["/opengraph-image"],
  },
  appleWebApp: {
    capable: true,
    title: siteConfig.name,
    statusBarStyle: "default",
  },
  formatDetection: {
    email: false,
    address: false,
    telephone: false,
  },
};

export const viewport: Viewport = {
  width: "device-width",
  initialScale: 1,
  viewportFit: "cover",
  colorScheme: "light dark",
  themeColor: [
    { media: "(prefers-color-scheme: light)", color: "#FDFCFC" },
    { media: "(prefers-color-scheme: dark)", color: "#0D0806" },
  ],
};

export default function RootLayout({ children }: LayoutProps<"/">) {
  return (
    <html
      lang="en-IN"
      suppressHydrationWarning
      className={`${instrument.variable} ${plex.variable} ${geistMono.variable} ${notoTelugu.variable}`}
    >
      <body>
        <ThemeProvider
          attribute="class"
          defaultTheme="light"
          enableSystem={false}
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
