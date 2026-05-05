// Re-export from index to avoid duplication
export type { User, LoginRequest, RegisterRequest } from './index';

export interface TokenResponse {
  access_token: string;
  refresh_token: string;
  token_type: string;
  expires_in: number;
}

export interface UpdateProfileRequest {
  first_name?: string;
  last_name?: string;
}