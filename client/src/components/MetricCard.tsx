import { cn } from "@/lib/utils";
import { motion } from "framer-motion";

interface MetricCardProps {
  label: string;
  value: string | number;
  subValue?: string;
  icon?: React.ReactNode;
  trend?: "up" | "down" | "neutral";
  className?: string;
  delay?: number;
}

export function MetricCard({ label, value, subValue, icon, trend, className, delay = 0 }: MetricCardProps) {
  return (
    <motion.div 
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4, delay: delay * 0.1 }}
      className={cn(
        "bg-card border border-border p-5 rounded-xl shadow-sm hover:shadow-md transition-all duration-200",
        className
      )}
    >
      <div className="flex justify-between items-start mb-2">
        <span className="text-sm font-medium text-muted-foreground">{label}</span>
        {icon && <div className="text-primary/70">{icon}</div>}
      </div>
      <div className="flex items-baseline gap-2">
        <span className="text-2xl font-bold tracking-tight text-foreground">{value}</span>
        {subValue && (
          <span className={cn("text-xs font-medium", {
            "text-green-600": trend === "up",
            "text-red-600": trend === "down",
            "text-muted-foreground": !trend || trend === "neutral"
          })}>
            {subValue}
          </span>
        )}
      </div>
    </motion.div>
  );
}
