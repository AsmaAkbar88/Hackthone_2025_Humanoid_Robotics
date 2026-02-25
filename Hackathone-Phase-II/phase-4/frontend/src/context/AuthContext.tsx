// src/context/AuthContext.tsx
'use client';

import React, { createContext, useContext, useReducer, useEffect } from 'react';
import { authService, type User } from '@/services/auth-service';

interface AuthState {
  user: User | null;
  loading: boolean;
  error: string | null;
  isAuthenticated: boolean;
}

type AuthAction =
  | { type: 'LOGIN_START' }
  | { type: 'LOGIN_SUCCESS'; payload: User }
  | { type: 'LOGIN_FAILURE'; payload: string }
  | { type: 'REGISTER_START' }
  | { type: 'REGISTER_SUCCESS'; payload: User }
  | { type: 'REGISTER_FAILURE'; payload: string }
  | { type: 'LOGOUT' }
  | { type: 'SET_ERROR'; payload: string | null }
  | { type: 'CHECK_AUTH_STATUS_START' }
  | { type: 'CHECK_AUTH_STATUS_SUCCESS'; payload: User | null }
  | { type: 'CHECK_AUTH_STATUS_FAILURE'; payload: string };

const initialState: AuthState = {
  user: null,
  loading: true,
  error: null,
  isAuthenticated: false,
};

const AuthContext = createContext<{
  state: AuthState;
  login: (email: string, password: string) => Promise<User>;
  register: (name: string, email: string, password: string, dateOfBirth: string) => Promise<User>;
  logout: () => Promise<void>;
  clearError: () => void;
  resetPassword: (data: { email: string; newPassword: string }) => Promise<void>;
} | undefined>(undefined);

const authReducer = (state: AuthState, action: AuthAction): AuthState => {
  switch (action.type) {
    case 'LOGIN_START':
    case 'REGISTER_START':
    case 'CHECK_AUTH_STATUS_START':
      return {
        ...state,
        loading: true,
        error: null,
      };
    case 'LOGIN_SUCCESS':
    case 'REGISTER_SUCCESS':
    case 'CHECK_AUTH_STATUS_SUCCESS':
      return {
        ...state,
        user: action.payload,
        loading: false,
        error: null,
        isAuthenticated: !!action.payload,
      };
    case 'LOGIN_FAILURE':
    case 'REGISTER_FAILURE':
    case 'CHECK_AUTH_STATUS_FAILURE':
      return {
        ...state,
        user: null,
        loading: false,
        error: action.payload,
        isAuthenticated: false,
      };
    case 'LOGOUT':
      return {
        ...state,
        user: null,
        loading: false,
        error: null,
        isAuthenticated: false,
      };
    case 'SET_ERROR':
      return {
        ...state,
        error: action.payload,
      };
    default:
      return state;
  }
};

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [state, dispatch] = useReducer(authReducer, initialState);
  const timeoutRef = React.useRef<NodeJS.Timeout | null>(null);

  // Cleanup timeout on unmount
  React.useEffect(() => {
    return () => {
      if (timeoutRef.current) {
        clearTimeout(timeoutRef.current);
      }
    };
  }, []);

  React.useEffect(() => {
    // Set a timeout to stop loading after 5 seconds if auth check takes too long
    timeoutRef.current = setTimeout(() => {
      if (state.loading) {
        // Stop loading but keep the initial state (no user, not authenticated)
        dispatch({
          type: 'CHECK_AUTH_STATUS_FAILURE',
          payload: 'Authentication check timed out. Please refresh the page.'
        });
      }
    }, 5000); // 5 seconds timeout

    // Add a small delay to allow the app to initialize before checking auth status
    // This helps prevent race conditions during startup
    const authCheckTimer = setTimeout(() => {
      checkAuthStatus();
    }, 100); // Small delay to ensure initialization

    // Cleanup the auth check timer
    return () => {
      clearTimeout(authCheckTimer);
    };
  }, []);

  const checkAuthStatus = async () => {
    dispatch({ type: 'CHECK_AUTH_STATUS_START' });

    // Clear the timeout since we're now getting a response
    if (timeoutRef.current) {
      clearTimeout(timeoutRef.current);
      timeoutRef.current = null;
    }

    try {
      const user = await authService.getCurrentUser();
      dispatch({ type: 'CHECK_AUTH_STATUS_SUCCESS', payload: user });
    } catch (err: any) {
      if (err && typeof err === 'object' && err.response?.status === 401) {
        dispatch({ type: 'CHECK_AUTH_STATUS_SUCCESS', payload: null }); // NORMAL
        return;
      }
      // For other errors (real network issues), handle accordingly
      dispatch({
        type: 'CHECK_AUTH_STATUS_SUCCESS',
        payload: null // No user is authenticated, which is normal
      });
    }
  };

  const login = async (email: string, password: string) => {
    dispatch({ type: 'LOGIN_START' });
    try {
      const { user } = await authService.login({ email, password });

      dispatch({ type: 'LOGIN_SUCCESS', payload: user });
      return user;
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'Login failed';
      dispatch({ type: 'LOGIN_FAILURE', payload: errorMessage });
      throw error;
    }
  };

  const register = async (name: string, email: string, password: string, dateOfBirth: string) => {
    dispatch({ type: 'REGISTER_START' });
    try {
      const { user } = await authService.register({ name, email, password, dateOfBirth }); // The authService will handle the field name transformation

      dispatch({ type: 'REGISTER_SUCCESS', payload: user });
      return user;
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'Registration failed';
      dispatch({ type: 'REGISTER_FAILURE', payload: errorMessage });
      throw error;
    }
  };

  const logout = async () => {
    try {
      await authService.logout();
      dispatch({ type: 'LOGOUT' });
    } catch (error) {
      console.error('Logout error:', error);
    }
  };

  const resetPassword = async (data: { email: string; newPassword: string }) => {
    try {
      await authService.resetPassword(data);
      return;
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'Password reset failed';
      dispatch({ type: 'SET_ERROR', payload: errorMessage });
      throw error;
    }
  };

  const clearError = () => {
    dispatch({ type: 'SET_ERROR', payload: null });
  };

  return (
    <AuthContext.Provider value={{ state, login, register, logout, clearError, resetPassword }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};