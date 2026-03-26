/** User roles in the system. */
export type UserRole = 'admin' | 'user';

/** User profile returned from the API. */
export interface User {
  id: string;
  email: string;
  full_name: string;
  role: UserRole;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

/** Request body for POST /api/auth/register. */
export interface RegisterRequest {
  email: string;
  password: string;
  full_name: string;
}

/** Request body for POST /api/auth/login. */
export interface LoginRequest {
  email: string;
  password: string;
}

/** Response from POST /api/auth/login. */
export interface LoginResponse {
  access_token: string;
  token_type: string;
}

/** Request body for PATCH /api/auth/me. */
export interface UserUpdateRequest {
  full_name?: string;
  password?: string;
  current_password?: string;
}
