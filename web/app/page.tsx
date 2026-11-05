import { SiteHeader } from "@/components/site-header";
import { Hero } from "@/components/hero";
import { StackStrip } from "@/components/stack-strip";
import { ProblemSection } from "@/components/problem-section";
import { PipelineSection } from "@/components/pipeline-section";
import { LanguageSection } from "@/components/language-section";
import { BuildSection } from "@/components/build-section";
import { ModelSection } from "@/components/model-section";
import { StackSection } from "@/components/stack-section";
import { QuickStart } from "@/components/quick-start";
import { SiteFooter } from "@/components/site-footer";
import { siteConfig, siteUrl } from "@/lib/site";

const websiteId = new URL("/#website", siteUrl).toString();
const personId = new URL("/#person", siteUrl).toString();

const jsonLd = {
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "WebSite",
      "@id": websiteId,
      url: siteUrl.toString(),
      name: siteConfig.name,
      description: siteConfig.description,
      inLanguage: "en-IN",
      publisher: { "@id": personId },
    },
    {
      "@type": "Person",
      "@id": personId,
      name: siteConfig.author.name,
      url: siteConfig.author.portfolio,
      sameAs: [siteConfig.author.github, siteConfig.author.linkedin],
    },
    {
      "@type": "SoftwareApplication",
      name: siteConfig.name,
      applicationCategory: "AccessibilityApplication",
      operatingSystem: "Windows, macOS, Linux",
      description: siteConfig.description,
      url: siteUrl.toString(),
      codeRepository: "https://github.com/avesh-pathak/speech-to-sign-language",
      author: { "@id": personId },
      offers: {
        "@type": "Offer",
        price: "0",
        priceCurrency: "INR",
      },
      featureList: [
        "Telugu speech recognition",
        "Telugu to Indian Sign Language gloss translation",
        "Ordered ISL frame playback",
        "Text-card fallback for missing signs",
        "Res-BiLSTM-AM research branch",
      ],
    },
  ],
};

export default function Home() {
  return (
    <>
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{
          __html: JSON.stringify(jsonLd).replace(/</g, "\\u003c"),
        }}
      />
      <a
        href="#main"
        className="sr-only focus:not-sr-only focus:fixed focus:top-3 focus:left-4 focus:z-[100] focus:rounded-lg focus:bg-surface-dark focus:px-3.5 focus:py-2.5 focus:font-display focus:text-sm focus:text-white"
      >
        Skip to content
      </a>

      <SiteHeader />

      <main id="main">
        <Hero />
        <StackStrip />
        <ProblemSection />
        <PipelineSection />
        <LanguageSection />
        <BuildSection />
        <ModelSection />
        <StackSection />
        <QuickStart />
      </main>

      <SiteFooter />
    </>
  );
}
