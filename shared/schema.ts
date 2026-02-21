import { pgTable, text, serial, jsonb, timestamp } from "drizzle-orm/pg-core";
import { createInsertSchema } from "drizzle-zod";
import { z } from "zod";

export const pipelineRuns = pgTable("pipeline_runs", {
  id: serial("id").primaryKey(),
  keyword: text("keyword").notNull(),
  result: jsonb("result").notNull(),
  createdAt: timestamp("created_at").defaultNow(),
});

export const runPipelineRequestSchema = z.object({
  keyword: z.string().min(1, "Keyword is required"),
});

// Zod schemas for the complex response
export const signalSchema = z.object({
  title: z.string(),
  url: z.string(),
  summary: z.string(),
  relevance_score: z.number(),
});

export const scoredSignalSchema = z.object({
  title: z.string(),
  authority: z.number(),
  recency: z.number(),
  relevance: z.number(),
  novelty: z.number(),
  composite: z.number(),
});

export const strategyBriefSchema = z.object({
  chosen_angle: z.string(),
  angle_rationale: z.string(),
  competitive_gap_exploited: z.string(),
  core_positioning_thesis: z.string(),
  platform_distribution_plan: z.object({
    blog: z.string(),
    linkedin: z.string(),
    twitter: z.string(),
  }),
  target_audience: z.string(),
  estimated_authority_score: z.number(),
});

export const blogEvolutionSchema = z.object({
  draft_number: z.number(),
  scores: z.record(z.number()),
});

export const socialAssetsSchema = z.object({
  linkedin: z.string(),
  twitter: z.array(z.string()),
});

export const runPipelineResponseSchema = z.object({
  keyword: z.string().optional(),
  raw_signals: z.array(signalSchema).optional(),
  scored_signals: z.array(scoredSignalSchema).optional(),
  selected_signal: z.any().optional(),
  validated_facts: z.array(z.string()).optional(),
  competitor_angles: z.array(z.string()).optional(),
  identified_gaps: z.array(z.string()).optional(),
  verified_solutions: z.array(z.string()).optional(),
  strategy_brief: strategyBriefSchema.optional(),
  blog_final: z.string().optional(),
  blog_evolution: z.array(blogEvolutionSchema).optional(),
  authority_approved: z.boolean().optional(),
  social_assets: socialAssetsSchema.optional(),
  halt: z.boolean().optional(),
  halt_reason: z.string().optional(),
});
