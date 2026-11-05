"use client";

import { useEffect, useId, useRef, useState, useSyncExternalStore } from "react";
import { useTheme } from "next-themes";
import { cn } from "@/lib/utils";

const subscribeToMobile = (callback: () => void) => {
  const query = window.matchMedia("(max-width: 767px)");
  query.addEventListener("change", callback);
  return () => query.removeEventListener("change", callback);
};

const getMobileSnapshot = () => window.matchMedia("(max-width: 767px)").matches;
const getServerMobileSnapshot = () => false;

export function MermaidDiagram({
  chart,
  mobileChart,
  className,
  label,
}: {
  chart: string;
  mobileChart: string;
  className?: string;
  label: string;
}) {
  const ref = useRef<HTMLDivElement>(null);
  const { resolvedTheme } = useTheme();
  const isMobile = useSyncExternalStore(
    subscribeToMobile,
    getMobileSnapshot,
    getServerMobileSnapshot
  );
  const reactId = useId().replace(/:/g, "");
  const renderCount = useRef(0);
  const [error, setError] = useState(false);

  const isDark = resolvedTheme === "dark";

  useEffect(() => {
    let active = true;
    const source = isMobile ? mobileChart : chart;

    const renderDiagram = async () => {
      const mermaid = (await import("mermaid")).default;
      const palette = isDark
        ? {
            background: "transparent",
            primaryColor: "#150D09",
            primaryTextColor: "#F8F1EC",
            primaryBorderColor: "#33231C",
            secondaryColor: "#2A1710",
            secondaryTextColor: "#F8F1EC",
            tertiaryColor: "#1C120D",
            lineColor: "#FF7A3D",
            textColor: "#F8F1EC",
            mainBkg: "#150D09",
            nodeBorder: "#33231C",
            edgeLabelBackground: "#150D09",
            clusterBkg: "#150D09",
            clusterBorder: "#33231C",
          }
        : {
            background: "transparent",
            primaryColor: "#FFFFFF",
            primaryTextColor: "#100703",
            primaryBorderColor: "#E9E4E2",
            secondaryColor: "#FFF0E8",
            secondaryTextColor: "#100703",
            tertiaryColor: "#F5EEEA",
            lineColor: "#E83C00",
            textColor: "#100703",
            mainBkg: "#FFFFFF",
            nodeBorder: "#E9E4E2",
            edgeLabelBackground: "#FDFCFC",
            clusterBkg: "#FFFFFF",
            clusterBorder: "#E9E4E2",
          };

      mermaid.initialize({
        startOnLoad: false,
        securityLevel: "strict",
        theme: "base",
        themeVariables: {
          ...palette,
          fontFamily: "IBM Plex Sans, sans-serif",
          fontSize: "14px",
        },
        flowchart: {
          curve: "basis",
          htmlLabels: true,
          padding: 14,
          nodeSpacing: 38,
          rankSpacing: 54,
          useMaxWidth: true,
        },
        themeCSS: `
          .node rect, .node circle, .node polygon, .node path { rx: 10px; ry: 10px; filter: none !important; stroke-width: 1px; }
          .node .label { font-family: IBM Plex Sans, sans-serif; }
          .edgeLabel { font-family: ui-monospace, monospace; font-size: 10px; }
          .edgePath .path { stroke-width: 1.4px; }
        `,
      });

      try {
        renderCount.current += 1;
        const { svg } = await mermaid.render(
          `vanisign-mermaid-${reactId}-${renderCount.current}`,
          source
        );
        if (active && ref.current) {
          ref.current.innerHTML = svg;
          setError(false);
        }
      } catch {
        if (active) setError(true);
      }
    };

    renderDiagram();

    return () => {
      active = false;
    };
  }, [chart, mobileChart, isMobile, isDark, reactId]);

  return (
    <div
      role="img"
      aria-label={label}
      className={cn("relative min-h-[220px] w-full", className)}
    >
      <div
        ref={ref}
        className="mermaid-diagram flex w-full items-center justify-center"
      />
      {error ? (
        <p className="absolute inset-0 grid place-items-center font-mono text-[10px] tracking-[0.06em] text-muted-foreground uppercase">
          Diagram unavailable
        </p>
      ) : null}
    </div>
  );
}
