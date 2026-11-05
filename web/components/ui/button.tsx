import * as React from "react"
import { cva, type VariantProps } from "class-variance-authority"
import { cn } from "cn"
import { Slot } from "radix-ui"

const buttonVariants = cva(
  "group/button inline-flex shrink-0 items-center justify-center rounded-lg border border-transparent bg-clip-padding whitespace-nowrap transition-[color,background-color,border-color,box-shadow,transform] duration-150 outline-none select-none focus-visible:ring-3 focus-visible:ring-ring/50 active:scale-[.985] disabled:pointer-events-none disabled:opacity-50 motion-reduce:active:scale-100 aria-invalid:border-destructive aria-invalid:ring-3 aria-invalid:ring-destructive/20 [&_svg]:pointer-events-none [&_svg]:shrink-0 [&_svg:not([class*='size-'])]:size-4",
  {
    variants: {
      variant: {
        default: "bg-primary text-primary-foreground hover:bg-primary/80",
        outline:
          "border-border bg-background hover:bg-muted hover:text-foreground aria-expanded:bg-muted aria-expanded:text-foreground",
        secondary:
          "bg-secondary text-secondary-foreground hover:bg-[color-mix(in_oklch,var(--secondary),var(--foreground)_5%)] aria-expanded:bg-secondary",
        ghost:
          "hover:bg-muted hover:text-foreground aria-expanded:bg-muted aria-expanded:text-foreground",
        destructive:
          "bg-destructive/10 text-destructive hover:bg-destructive/20 focus-visible:border-destructive/40 focus-visible:ring-destructive/20",
        link: "text-primary underline-offset-4 hover:underline",
        ink: "border-white bg-[linear-gradient(169deg,rgba(129,129,129,0),rgba(129,129,129,.2)),linear-gradient(90deg,#22180F,#190E09)] text-white shadow-[0_0_0_1px_#190E09] hover:border-white/80 hover:shadow-[0_0_0_1px_#190E09,0_8px_20px_rgba(120,40,0,.18)] dark:border-foreground dark:bg-foreground dark:bg-none dark:text-background dark:shadow-none dark:hover:border-foreground/80 dark:hover:shadow-none",
        paper:
          "border-border bg-card text-foreground shadow-[0_0_0_1px_rgba(25,14,9,.03)] hover:border-signal/40 dark:shadow-none",
        signal:
          "border-signal-deep bg-signal-deep text-white hover:border-[#9f2b00] hover:bg-[#9f2b00]",
        outlineLight:
          "border-white/20 bg-transparent text-white hover:border-white/40 hover:bg-white/5",
      },
      size: {
        default:
          "h-8 gap-1.5 px-2.5 text-sm font-medium has-data-[icon=inline-end]:pr-2 has-data-[icon=inline-start]:pl-2",
        xs: "h-6 gap-1 rounded-[min(var(--radius-md),10px)] px-2 text-xs font-medium",
        sm: "h-7 gap-1 rounded-[min(var(--radius-md),12px)] px-2.5 text-[0.8rem] font-medium",
        lg: "h-9 gap-1.5 px-2.5 text-sm font-medium",
        cta: "h-11 gap-2.5 rounded-lg py-2 pr-2 pl-3.5 text-[15px] font-normal",
        nav: "h-11 gap-2.5 rounded-lg py-2 pr-1.5 pl-3 text-sm font-normal",
        icon: "size-8",
        "icon-xs": "size-6",
        "icon-sm": "size-7",
        "icon-lg": "size-9",
      },
    },
    defaultVariants: {
      variant: "default",
      size: "default",
    },
  }
)

function Button({
  className,
  variant = "default",
  size = "default",
  asChild = false,
  ...props
}: React.ComponentProps<"button"> &
  VariantProps<typeof buttonVariants> & {
    asChild?: boolean
  }) {
  const Comp = asChild ? Slot.Root : "button"

  return (
    <Comp
      data-slot="button"
      data-variant={variant}
      data-size={size}
      className={cn(buttonVariants({ variant, size, className }))}
      {...props}
    />
  )
}

export { Button, buttonVariants }
