import { useMutation } from "@tanstack/react-query";
import { api } from "@shared/routes";
import { type RunPipelineRequest, type RunPipelineResponse } from "@shared/routes";

export function useRunPipeline() {
  return useMutation<RunPipelineResponse, Error, RunPipelineRequest>({
    mutationFn: async (data: RunPipelineRequest) => {
      // Validate input before sending (client-side check)
      const validatedInput = api.pipeline.run.input.parse(data);

      const res = await fetch(api.pipeline.run.path, {
        method: api.pipeline.run.method,
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(validatedInput),
      });

      if (!res.ok) {
        const errorData = await res.json().catch(() => ({}));
        throw new Error(errorData.message || "Failed to run pipeline");
      }

      const rawData = await res.json();
      
      // Validate response using the schema from routes
      // We use safeParse here to avoid crashing the UI if the backend sends unexpected data,
      // but ideally this guarantees type safety.
      const parsed = api.pipeline.run.responses[200].safeParse(rawData);
      
      if (!parsed.success) {
        console.error("Pipeline response validation failed:", parsed.error);
        // Fallback to raw data if strict validation fails, or throw
        return rawData as RunPipelineResponse;
      }

      return parsed.data;
    },
  });
}
