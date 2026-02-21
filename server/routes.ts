import type { Express } from "express";
import type { Server } from "http";
import { storage } from "./storage";
import { api } from "@shared/routes";
import { z } from "zod";

export async function registerRoutes(
  httpServer: Server,
  app: Express
): Promise<Server> {
  
  app.post(api.pipeline.run.path, async (req, res) => {
    try {
      const input = api.pipeline.run.input.parse(req.body);
      
      // Simulate backend processing delay
      await new Promise(resolve => setTimeout(resolve, 2500));

      let mockResponse: z.infer<typeof api.pipeline.run.responses[200]>;

      // If keyword includes 'halt', we'll simulate the backend rejecting it
      if (input.keyword.toLowerCase().includes('halt')) {
        mockResponse = {
          keyword: input.keyword,
          halt: true,
          halt_reason: "Authority rejected blog due to insufficient depth on the topic."
        };
      } else {
        mockResponse = {
          keyword: input.keyword,
          raw_signals: [
            {
              title: "The Future of Databases in 2024",
              url: "https://example.com/future-db",
              summary: "Discusses vector and graph databases.",
              relevance_score: 8.5
            },
            {
              title: "Scaling RevOps with AI",
              url: "https://example.com/revops",
              summary: "How AI impacts revenue operations.",
              relevance_score: 7.2
            }
          ],
          scored_signals: [
            {
              title: "The Future of Databases in 2024",
              authority: 8.0,
              recency: 9.0,
              relevance: 8.5,
              novelty: 7.0,
              composite: 8.1
            }
          ],
          selected_signal: {
            title: "The Future of Databases in 2024",
            url: "https://example.com/future-db"
          },
          validated_facts: [
            "Signal URL reachable",
            "Primary source confirmed"
          ],
          competitor_angles: [
            "What is an AI-native database?",
            "The rise of the AI-native database"
          ],
          identified_gaps: [
            "Operational impact not discussed",
            "Missing RevOps execution layer"
          ],
          verified_solutions: [
            "Real-time vector search for RevOps signals",
            "Unified semantic + transactional intelligence"
          ],
          strategy_brief: {
            chosen_angle: "Operationalizing AI databases for RevOps",
            angle_rationale: "Competitors focus on architecture, ignoring business value.",
            competitive_gap_exploited: "Missing RevOps execution layer",
            core_positioning_thesis: "AI-native databases must bridge the gap between semantic search and transactional revenue operations.",
            platform_distribution_plan: {
              blog: "Deep-dive technical post",
              linkedin: "Actionable summary for RevOps leaders",
              twitter: "Thread on semantic vs transactional tradeoffs"
            },
            target_audience: "RevOps Leaders and Data Engineers",
            estimated_authority_score: 92
          },
          blog_final: "# Operationalizing AI Databases for RevOps\n\nTraditional databases are struggling to keep up with the demands of modern revenue operations. In this post, we explore how AI-native databases can bridge the gap.\n\n## The Missing Execution Layer\n\nMost discussions around AI databases focus on vector embeddings. But what about the operational impact?\n\nBy uniting semantic search with robust transactional integrity, you can seamlessly feed intelligence straight into automated RevOps systems.",
          blog_evolution: [
            {
              draft_number: 1,
              scores: {
                "Hook Strength": 7,
                "Clarity": 7,
                "Authority Tone": 9
              }
            },
            {
              draft_number: 2,
              scores: {
                "Hook Strength": 9,
                "Clarity": 8,
                "Authority Tone": 9
              }
            }
          ],
          authority_approved: true,
          social_assets: {
            linkedin: "Are you struggling to scale RevOps with traditional databases? It's time to look at AI-native solutions that bridge the gap between semantic search and transactional intelligence. #RevOps #AI",
            twitter: [
              "1/ Traditional databases are struggling to keep up with modern revenue operations.",
              "2/ Enter the AI-native database: bridging semantic search and transactional intelligence.",
              "3/ Read our full deep-dive here. 👇"
            ]
          }
        };
      }

      // Log the run in the database asynchronously
      storage.logRun(input.keyword, mockResponse).catch(console.error);

      res.status(200).json(mockResponse);
    } catch (err) {
      if (err instanceof z.ZodError) {
        return res.status(400).json({
          message: err.errors[0].message,
          field: err.errors[0].path.join('.'),
        });
      }
      res.status(500).json({ message: "Internal server error" });
    }
  });

  return httpServer;
}
