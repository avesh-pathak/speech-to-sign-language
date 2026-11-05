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

export default function Home() {
  return (
    <>
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
