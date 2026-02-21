import { useState } from "react";
import { useLocation } from "wouter";
import { useRunPipeline } from "@/hooks/use-pipeline";
import { useToast } from "@/hooks/use-toast";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Loader2, Search, Zap, BarChart3, FileText, CheckCircle2 } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";
import DashboardResults from "./DashboardResults";

export default function Home() {
  const [keyword, setKeyword] = useState("");
  const [isResultsVisible, setIsResultsVisible] = useState(false);
  const { mutate, isPending, data, reset } = useRunPipeline();
  const { toast } = useToast();

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!keyword.trim()) return;

    setIsResultsVisible(false); // Reset view if running again
    
    mutate({ keyword }, {
      onError: (err) => {
        toast({
          title: "Pipeline Failed",
          description: err.message,
          variant: "destructive",
        });
      },
      onSuccess: () => {
        setIsResultsVisible(true);
      }
    });
  };

  const handleReset = () => {
    setKeyword("");
    reset();
    setIsResultsVisible(false);
  };

  return (
    <div className="min-h-screen bg-background text-foreground font-sans">
      {/* Header */}
      <header className="border-b border-border bg-background/80 backdrop-blur-sm sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 rounded-lg bg-primary flex items-center justify-center">
              <Zap className="w-5 h-5 text-primary-foreground" />
            </div>
            <span className="font-bold text-lg tracking-tight">DataVex</span>
          </div>
          <nav className="flex items-center gap-6 text-sm font-medium text-muted-foreground">
            <a href="#" className="hover:text-foreground transition-colors">Documentation</a>
            <a href="#" className="hover:text-foreground transition-colors">Support</a>
            <div className="w-px h-4 bg-border"></div>
            <div className="flex items-center gap-2">
              <div className="w-6 h-6 rounded-full bg-gradient-to-br from-primary to-accent"></div>
              <span className="text-foreground">Workspace</span>
            </div>
          </nav>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {/* Search / Input Section */}
        <div className={`transition-all duration-500 ease-in-out ${isResultsVisible ? 'mb-8' : 'min-h-[60vh] flex flex-col justify-center items-center'}`}>
          <div className={`w-full max-w-2xl ${isResultsVisible ? '' : 'text-center space-y-8'}`}>
            
            {!isResultsVisible && (
              <motion.div 
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5 }}
              >
                <h1 className="text-4xl md:text-5xl font-bold tracking-tight mb-4 bg-clip-text text-transparent bg-gradient-to-r from-foreground to-foreground/70">
                  Growth Engine
                </h1>
                <p className="text-lg text-muted-foreground max-w-xl mx-auto">
                  Generate data-backed content strategies. Enter a keyword to analyze signals, identify gaps, and produce high-authority content.
                </p>
              </motion.div>
            )}

            <motion.form 
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5, delay: 0.1 }}
              onSubmit={handleSubmit}
              className="relative w-full"
            >
              <div className="relative group">
                <div className="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
                  <Search className="h-5 w-5 text-muted-foreground group-focus-within:text-primary transition-colors" />
                </div>
                <Input
                  type="text"
                  placeholder="Enter a keyword (e.g., 'SaaS marketing', 'Vector Databases')"
                  className="pl-11 pr-32 h-14 text-lg rounded-2xl border-2 border-border shadow-sm focus-visible:ring-4 focus-visible:ring-primary/10 transition-all hover:border-primary/50"
                  value={keyword}
                  onChange={(e) => setKeyword(e.target.value)}
                  disabled={isPending}
                />
                <div className="absolute inset-y-0 right-2 flex items-center">
                  <Button 
                    type="submit" 
                    disabled={isPending || !keyword}
                    className="h-10 px-6 rounded-xl font-semibold shadow-lg shadow-primary/20 hover:shadow-primary/30 transition-all"
                  >
                    {isPending ? (
                      <>
                        <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                        Analyzing...
                      </>
                    ) : (
                      "Generate"
                    )}
                  </Button>
                </div>
              </div>
              {!isResultsVisible && (
                <div className="mt-4 flex flex-wrap justify-center gap-2">
                  <span className="text-sm text-muted-foreground">Try:</span>
                  {["Product Growth", "AI Agents", "Remote Work"].map((k) => (
                    <button
                      key={k}
                      type="button"
                      onClick={() => setKeyword(k)}
                      className="text-sm px-3 py-1 bg-secondary/50 hover:bg-secondary text-secondary-foreground rounded-full transition-colors border border-transparent hover:border-border"
                    >
                      {k}
                    </button>
                  ))}
                </div>
              )}
            </motion.form>
          </div>
        </div>

        {/* Results Section */}
        <AnimatePresence>
          {isResultsVisible && data && (
            <motion.div
              initial={{ opacity: 0, y: 40 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: 20 }}
              transition={{ duration: 0.5 }}
            >
              <div className="flex justify-between items-center mb-8">
                <div>
                  <h2 className="text-2xl font-bold tracking-tight">Analysis Results</h2>
                  <p className="text-muted-foreground">
                    Intelligence report for <span className="font-semibold text-foreground">"{data.keyword}"</span>
                  </p>
                </div>
                <Button variant="outline" onClick={handleReset} className="gap-2">
                  <Search className="w-4 h-4" /> New Search
                </Button>
              </div>

              <DashboardResults data={data} />
            </motion.div>
          )}
        </AnimatePresence>
      </main>
    </div>
  );
}
