import { cn } from "@/lib/utils"
import { forwardRef } from "react"

export interface BadgeProps extends React.HTMLAttributes<HTMLDivElement> {
  variant?: "default" | "secondary" | "destructive" | "outline"
}

const Badge = forwardRef<HTMLDivElement, BadgeProps>(
  ({ className, variant = "default", ...props }, ref) => (
    <div
      ref={ref}
      className={cn(
        "inline-flex items-center rounded-full border px-2.5 py-0.5 text-xs font-semibold transition-colors focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2",
        variant === "default" && "border-transparent bg-primary text-primary-foreground",
        variant === "secondary" && "border-transparent bg-secondary text-secondary-foreground",
        variant === "destructive" && "border-transparent bg-destructive text-destructive-foreground",
        variant === "outline" && "text-foreground",
        className
      )}
      {...props}
    />
  )
)
Badge.displayName = "Badge"

export { Badge }
