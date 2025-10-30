export interface User {
  id: string;
  email: string;
  first_name: string;
  last_name: string;
  role: 'client' | 'provider' | 'admin';
  is_verified: boolean;
  created_at: string;
  updated_at: string;
}

export interface RegisterData {
  email: string;
  password: string;
  first_name: string;
  last_name: string;
  role: 'client' | 'provider';
}

export interface LoginData {
  email: string;
  password: string;
}

export interface AuthResponse {
  access_token: string;
  user: User;
}

export interface AuthState {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  error: string | null;
}
