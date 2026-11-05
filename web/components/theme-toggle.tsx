"use client";

import { useSyncExternalStore } from "react";
import { Moon, Sun } from "lucide-react";
import { useTheme } from "next-themes";
import { cn } from "@/lib/utils";

const subscribe = () => () => {};
const getClientSnapshot = () => true;
const getServerSnapshot = () => false;

export function ThemeToggle({
  variant = "header",
  className,
}: {
  variant?: "header" | "menu";
  className?: string;
}) {
  const { resolvedTheme, setTheme } = useTheme();
  const mounted = useSyncExternalStore(
    subscribe,
    getClientSnapshot,
    getServerSnapshot
  );

  const isDark = mounted && resolvedTheme === "dark";
  const nextTheme = isDark ? "light" : "dark";
  const label = isDark ? "Switch to light mode" : "Switch to dark mode";

  if (variant === "menu") {
    return (
      <button
        type="button"
        onClick={() => setTheme(nextTheme)}
        aria-label={label}
        className={cn(
          "flex min-h-14 w-full items-center justify-between border-b border-border py-3.5 font-display text-base text-muted-foreground transition-colors hover:text-foreground",
          className
        )}
      >
        <span>Appearance</span>
        <span className="flex items-center gap-2 font-mono text-[10px] tracking-[0.1em] text-muted-foreground uppercase">
          {mounted ? (isDark ? "Dark" : "Light") : "Theme"}
          {isDark ? <Sun className="size-4" /> : <Moon className="size-4" />}
        </span>
      </button>
    );
  }

  return (
    <button
      type="button"
      onClick={() => setTheme(nextTheme)}
      aria-label={label}
      title={label}
      className={cn(
        "grid size-11 place-items-center rounded-lg border border-border bg-card text-foreground transition-colors hover:bg-muted",
        className
      )}
    >
      {mounted ? (
        isDark ? (
          <Sun className="size-4" />
        ) : (
          <Moon className="size-4" />
        )
      ) : (
        <Moon className="size-4 opacity-0" />
      )}
    </button>
  );
}
