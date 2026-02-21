import { db } from "./db";
import { pipelineRuns } from "@shared/schema";

export interface IStorage {
  logRun(keyword: string, result: any): Promise<void>;
}

export class DatabaseStorage implements IStorage {
  async logRun(keyword: string, result: any): Promise<void> {
    await db.insert(pipelineRuns).values({ keyword, result });
  }
}

export const storage = new DatabaseStorage();
