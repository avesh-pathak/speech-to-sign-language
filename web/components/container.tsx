import { cn } from "@/lib/utils";

export function Container({
  className,
  children,
  ...props
}: React.ComponentProps<"div">) {
  return (
    <div
      className={cn(
        "mx-auto w-full max-w-[1456px] px-5 sm:px-8 lg:px-[72px]",
        className
      )}
      {...props}
    >
      {children}
    </div>
  );
}
