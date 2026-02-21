import { z } from 'zod';
import { runPipelineRequestSchema, runPipelineResponseSchema } from './schema';

export const errorSchemas = {
  validation: z.object({
    message: z.string(),
    field: z.string().optional(),
  }),
  internal: z.object({
    message: z.string(),
  }),
};

export const api = {
  pipeline: {
    run: {
      method: 'POST' as const,
      // Prefix with /api to match Replit fullstack standard
      path: '/api/run-pipeline' as const,
      input: runPipelineRequestSchema,
      responses: {
        200: runPipelineResponseSchema,
        400: errorSchemas.validation,
      },
    },
  },
};

export function buildUrl(path: string, params?: Record<string, string | number>): string {
  let url = path;
  if (params) {
    Object.entries(params).forEach(([key, value]) => {
      if (url.includes(`:${key}`)) {
        url = url.replace(`:${key}`, String(value));
      }
    });
  }
  return url;
}

export type RunPipelineRequest = z.infer<typeof api.pipeline.run.input>;
export type RunPipelineResponse = z.infer<typeof api.pipeline.run.responses[200]>;
