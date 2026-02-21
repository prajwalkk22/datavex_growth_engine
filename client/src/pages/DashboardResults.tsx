import { type RunPipelineResponse } from "@shared/routes";
import { MetricCard } from "@/components/MetricCard";
import { StatusBadge } from "@/components/StatusBadge";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { Separator } from "@/components/ui/separator";
import { 
  AlertTriangle, 
  CheckCircle, 
  Copy, 
  ExternalLink, 
  Lightbulb, 
  LineChart, 
  MessageSquare, 
  Share2, 
  Target,
  FileText,
  Linkedin,
  Twitter
} from "lucide-react";
import ReactMarkdown from "react-markdown";
import { useToast } from "@/hooks/use-toast";
import { motion } from "framer-motion";

interface DashboardResultsProps {
  data: RunPipelineResponse;
}

export default function DashboardResults({ data }: DashboardResultsProps) {
  const { toast } = useToast();

  const copyToClipboard = (text: string, label: string) => {
    navigator.clipboard.writeText(text);
    toast({
      title: "Copied!",
      description: `${label} copied to clipboard.`,
    });
  };

  if (data.halt) {
    return (
      <div className="max-w-3xl mx-auto mt-12 text-center p-12 border-2 border-dashed border-destructive/30 bg-destructive/5 rounded-3xl">
        <div className="inline-flex items-center justify-center w-16 h-16 rounded-full bg-destructive/10 mb-6">
          <AlertTriangle className="w-8 h-8 text-destructive" />
        </div>
        <h2 className="text-2xl font-bold text-destructive mb-4">Pipeline Halted</h2>
        <p className="text-lg text-muted-foreground max-w-lg mx-auto mb-8">
          {data.halt_reason || "The pipeline determined that no valid strategy could be formed for this keyword."}
        </p>
      </div>
    );
  }

  // Calculate some aggregate metrics for display
  const signalCount = data.raw_signals?.length || 0;
  const authorityScore = data.strategy_brief?.estimated_authority_score || 0;
  const blogWordCount = data.blog_final?.split(/\s+/).length || 0;

  return (
    <div className="space-y-8 animate-in fade-in slide-in-from-bottom-8 duration-700">
      
      {/* Top Metrics Row */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <MetricCard 
          label="Signals Analyzed" 
          value={signalCount} 
          icon={<LineChart className="w-4 h-4" />}
          delay={0}
        />
        <MetricCard 
          label="Authority Score" 
          value={`${authorityScore}/100`}
          subValue={authorityScore > 70 ? "Excellent" : "Good"} 
          trend={authorityScore > 70 ? "up" : "neutral"}
          icon={<Target className="w-4 h-4" />}
          delay={1}
        />
        <MetricCard 
          label="Content Length" 
          value={`${blogWordCount} words`}
          icon={<FileText className="w-4 h-4" />}
          delay={2}
        />
        <MetricCard 
          label="Status" 
          value={data.authority_approved ? "Approved" : "Pending"}
          subValue={data.authority_approved ? "Ready to publish" : "Needs review"}
          trend={data.authority_approved ? "up" : "neutral"}
          icon={data.authority_approved ? <CheckCircle className="w-4 h-4 text-green-500" /> : <AlertTriangle className="w-4 h-4 text-amber-500" />}
          delay={3}
        />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        
        {/* Main Content Area (Left 2/3) */}
        <div className="lg:col-span-2 space-y-8">
          
          {/* Strategy Brief */}
          <Card className="border-l-4 border-l-primary shadow-sm hover:shadow-md transition-shadow">
            <CardHeader>
              <div className="flex items-center gap-2">
                <Lightbulb className="w-5 h-5 text-primary" />
                <CardTitle>Strategy Brief</CardTitle>
              </div>
              <CardDescription>
                Core positioning and angle derived from competitor analysis
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
              <div>
                <h4 className="text-sm font-semibold text-muted-foreground uppercase tracking-wider mb-2">Chosen Angle</h4>
                <p className="text-lg font-medium text-foreground">{data.strategy_brief?.chosen_angle}</p>
              </div>
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div className="bg-secondary/30 p-4 rounded-lg border border-border/50">
                  <h4 className="text-sm font-semibold text-muted-foreground mb-2">Gap Exploited</h4>
                  <p className="text-sm leading-relaxed">{data.strategy_brief?.competitive_gap_exploited}</p>
                </div>
                <div className="bg-secondary/30 p-4 rounded-lg border border-border/50">
                  <h4 className="text-sm font-semibold text-muted-foreground mb-2">Target Audience</h4>
                  <p className="text-sm leading-relaxed">{data.strategy_brief?.target_audience}</p>
                </div>
              </div>

              <div>
                <h4 className="text-sm font-semibold text-muted-foreground uppercase tracking-wider mb-2">Positioning Thesis</h4>
                <p className="italic text-muted-foreground border-l-2 border-primary/20 pl-4 py-1">
                  "{data.strategy_brief?.core_positioning_thesis}"
                </p>
              </div>
            </CardContent>
          </Card>

          {/* Tabbed Detailed View */}
          <Tabs defaultValue="blog" className="w-full">
            <div className="flex items-center justify-between mb-4">
              <TabsList className="grid w-full max-w-md grid-cols-3">
                <TabsTrigger value="blog">Content</TabsTrigger>
                <TabsTrigger value="signals">Signals</TabsTrigger>
                <TabsTrigger value="gaps">Gap Analysis</TabsTrigger>
              </TabsList>
            </div>

            {/* Blog Content Tab */}
            <TabsContent value="blog" className="space-y-4">
              <Card>
                <CardHeader className="flex flex-row items-center justify-between">
                  <div>
                    <CardTitle>Generated Article</CardTitle>
                    <CardDescription>
                      Final draft based on authority analysis
                    </CardDescription>
                  </div>
                  <Button variant="outline" size="sm" onClick={() => copyToClipboard(data.blog_final || "", "Article")}>
                    <Copy className="w-4 h-4 mr-2" /> Copy
                  </Button>
                </CardHeader>
                <CardContent>
                  <div className="prose prose-sm md:prose-base dark:prose-invert max-w-none bg-background p-6 rounded-lg border border-border/50">
                    <ReactMarkdown>{data.blog_final || "*No content generated*"}</ReactMarkdown>
                  </div>
                </CardContent>
              </Card>

              {/* Evolution History */}
              {data.blog_evolution && data.blog_evolution.length > 0 && (
                <Card className="bg-muted/30">
                  <CardHeader>
                    <CardTitle className="text-base">Draft Evolution</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-4">
                      {data.blog_evolution.map((evo) => (
                        <div key={evo.draft_number} className="flex items-center gap-4 text-sm">
                          <span className="font-mono font-bold text-muted-foreground">v{evo.draft_number}.0</span>
                          <div className="flex-1">
                            <div className="flex justify-between mb-1">
                              <span>Critique Score</span>
                              <span className="font-medium">{Object.values(evo.scores).reduce((a, b) => a + b, 0) / Object.values(evo.scores).length}/10</span>
                            </div>
                            <Progress value={(Object.values(evo.scores).reduce((a, b) => a + b, 0) / Object.values(evo.scores).length) * 10} className="h-2" />
                          </div>
                        </div>
                      ))}
                    </div>
                  </CardContent>
                </Card>
              )}
            </TabsContent>

            {/* Signals Tab */}
            <TabsContent value="signals">
              <div className="space-y-4">
                {data.scored_signals?.map((signal, idx) => (
                  <Card key={idx} className={cn("overflow-hidden transition-all", idx === 0 ? "border-primary/50 shadow-md ring-1 ring-primary/20" : "")}>
                    <CardHeader className="pb-2">
                      <div className="flex justify-between items-start gap-4">
                        <CardTitle className="text-base leading-tight">
                          {signal.title}
                          {idx === 0 && <StatusBadge status="success" className="ml-3">Selected</StatusBadge>}
                        </CardTitle>
                        <div className="text-right">
                          <div className="text-2xl font-bold text-primary">{signal.composite.toFixed(1)}</div>
                          <div className="text-xs text-muted-foreground">Composite</div>
                        </div>
                      </div>
                    </CardHeader>
                    <CardContent>
                      <div className="grid grid-cols-4 gap-2 text-xs text-center mt-2">
                        <div className="bg-secondary p-2 rounded">
                          <div className="font-bold">{signal.authority}</div>
                          <div className="text-muted-foreground">Auth</div>
                        </div>
                        <div className="bg-secondary p-2 rounded">
                          <div className="font-bold">{signal.recency}</div>
                          <div className="text-muted-foreground">Recency</div>
                        </div>
                        <div className="bg-secondary p-2 rounded">
                          <div className="font-bold">{signal.relevance}</div>
                          <div className="text-muted-foreground">Rel</div>
                        </div>
                        <div className="bg-secondary p-2 rounded">
                          <div className="font-bold">{signal.novelty}</div>
                          <div className="text-muted-foreground">Novelty</div>
                        </div>
                      </div>
                    </CardContent>
                  </Card>
                ))}
              </div>
            </TabsContent>

            {/* Gaps Tab */}
            <TabsContent value="gaps" className="space-y-6">
               <Card>
                <CardHeader>
                  <CardTitle>Identified Market Gaps</CardTitle>
                </CardHeader>
                <CardContent>
                  <ul className="space-y-3">
                    {data.identified_gaps?.map((gap, i) => (
                      <li key={i} className="flex gap-3 items-start p-3 rounded-lg bg-indigo-50 dark:bg-indigo-900/10 border border-indigo-100 dark:border-indigo-800">
                        <Target className="w-5 h-5 text-indigo-600 dark:text-indigo-400 mt-0.5 shrink-0" />
                        <span className="text-sm text-foreground">{gap}</span>
                      </li>
                    ))}
                  </ul>
                </CardContent>
               </Card>

               <Card>
                <CardHeader>
                  <CardTitle>Competitor Angles</CardTitle>
                </CardHeader>
                <CardContent>
                  <ul className="space-y-2">
                    {data.competitor_angles?.map((angle, i) => (
                      <li key={i} className="flex gap-2 items-center text-sm text-muted-foreground">
                        <div className="w-1.5 h-1.5 rounded-full bg-slate-300" />
                        {angle}
                      </li>
                    ))}
                  </ul>
                </CardContent>
               </Card>
            </TabsContent>
          </Tabs>
        </div>

        {/* Sidebar (Right 1/3) */}
        <div className="space-y-8">
          
          {/* Authority Status */}
          <Card>
            <CardHeader className="pb-3">
              <CardTitle className="text-sm font-medium uppercase tracking-wider text-muted-foreground">
                Approval Status
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="flex flex-col items-center text-center p-4">
                {data.authority_approved ? (
                  <>
                    <div className="w-12 h-12 rounded-full bg-green-100 text-green-600 flex items-center justify-center mb-3">
                      <CheckCircle className="w-6 h-6" />
                    </div>
                    <h3 className="font-bold text-lg text-green-700">Authority Approved</h3>
                    <p className="text-sm text-muted-foreground mt-1">Content meets quality standards.</p>
                  </>
                ) : (
                  <>
                    <div className="w-12 h-12 rounded-full bg-amber-100 text-amber-600 flex items-center justify-center mb-3">
                      <AlertTriangle className="w-6 h-6" />
                    </div>
                    <h3 className="font-bold text-lg text-amber-700">Review Needed</h3>
                    <p className="text-sm text-muted-foreground mt-1">Manual edits required before publishing.</p>
                  </>
                )}
              </div>
            </CardContent>
          </Card>

          {/* Validated Facts */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <CheckCircle2 className="w-4 h-4 text-primary" />
                Validated Facts
              </CardTitle>
            </CardHeader>
            <CardContent>
              <ul className="space-y-3">
                {data.validated_facts?.slice(0, 4).map((fact, i) => (
                  <li key={i} className="text-xs text-muted-foreground border-b border-border/50 last:border-0 pb-2 last:pb-0">
                    {fact}
                  </li>
                ))}
              </ul>
            </CardContent>
          </Card>

          {/* Social Assets */}
          <Card className={cn("transition-opacity", !data.authority_approved && "opacity-60 grayscale pointer-events-none")}>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Share2 className="w-4 h-4" />
                Social Assets
              </CardTitle>
              {!data.authority_approved && (
                <CardDescription className="text-xs text-amber-600 font-medium">
                  Approve content to unlock social assets
                </CardDescription>
              )}
            </CardHeader>
            <CardContent className="space-y-6">
              
              {/* LinkedIn */}
              <div className="space-y-2">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2 text-sm font-semibold text-[#0077b5]">
                    <Linkedin className="w-4 h-4" /> LinkedIn
                  </div>
                  <Button variant="ghost" size="icon" className="h-6 w-6" onClick={() => copyToClipboard(data.social_assets?.linkedin || "", "LinkedIn Post")}>
                    <Copy className="w-3 h-3" />
                  </Button>
                </div>
                <Textarea 
                  readOnly 
                  value={data.social_assets?.linkedin} 
                  className="min-h-[120px] text-xs font-mono bg-muted/20 resize-none focus-visible:ring-0"
                />
              </div>

              <Separator />

              {/* Twitter */}
              <div className="space-y-2">
                 <div className="flex items-center gap-2 text-sm font-semibold text-black dark:text-white mb-2">
                    <Twitter className="w-4 h-4" /> Twitter Thread
                  </div>
                  <div className="space-y-3">
                    {data.social_assets?.twitter.slice(0, 3).map((tweet, i) => (
                      <div key={i} className="group relative bg-muted/20 p-3 rounded-lg border border-border/50 hover:border-border transition-colors">
                        <p className="text-xs text-muted-foreground">{tweet}</p>
                        <Button 
                          variant="ghost" 
                          size="icon" 
                          className="absolute top-1 right-1 h-5 w-5 opacity-0 group-hover:opacity-100 transition-opacity"
                          onClick={() => copyToClipboard(tweet, `Tweet ${i+1}`)}
                        >
                          <Copy className="w-3 h-3" />
                        </Button>
                      </div>
                    ))}
                    {data.social_assets?.twitter && data.social_assets.twitter.length > 3 && (
                      <div className="text-xs text-center text-muted-foreground italic">
                        + {data.social_assets.twitter.length - 3} more tweets
                      </div>
                    )}
                  </div>
              </div>

            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
}
