import { createContext } from 'react';

export interface User {
  id: string;
  email: string;
  name?: string;
  dateOfBirth?: string;
  createdAt: string;
  lastLoginAt?: string;
  force_password_change?: boolean;
}

export interface AuthContextType {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  loading: boolean;
  login: (email: string, password: string) => Promise<void>;
  logout: () => void;
  register: (email: string, password: string) => Promise<void>;
  checkAuthStatus: () => Promise<boolean>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export { AuthContext };