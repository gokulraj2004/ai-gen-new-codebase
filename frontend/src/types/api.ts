// Re-export from index to avoid duplication
export type { PaginatedResponse } from './index';

export interface ApiError {
  detail: string;
  status_code: number;
}