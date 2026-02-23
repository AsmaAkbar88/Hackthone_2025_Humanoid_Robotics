'use client';

import React, { useState, useEffect, ReactNode } from 'react';
import { AuthContext, type AuthContextType, type User } from './authContext';
import { apiClient } from '../services/api-client';
import { authService } from '../services/auth-service';

export const AuthProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [token, setToken] = useState<string | null>(null);
  const [isAuthenticated, setIsAuthenticated] = useState<boolean>(false);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    // Check if user is already logged in when app loads
    const initAuth = async () => {
      try {
        // Verify token and get user info
        const currentUser = await authService.getCurrentUser();
        if (currentUser) {
          setUser(currentUser);
          setIsAuthenticated(true);
        }
      } catch (error) {
        console.error('Error initializing auth:', error);
        // Clear any invalid tokens
        apiClient.clearAuthToken();
        setToken(null);
        setIsAuthenticated(false);
      }
      setLoading(false);
    };

    initAuth();
  }, []);

  const checkAuthStatus = async (): Promise<boolean> => {
    try {
      const currentUser = await authService.getCurrentUser();
      if (currentUser) {
        setUser(currentUser);
        return true;
      } else {
        return false;
      }
    } catch (error) {
      console.error('Error checking auth status:', error);
      return false;
    }
  };

  const login = async (email: string, password: string): Promise<void> => {
    try {
      const result = await authService.login({ email, password });
      const { user } = result;

      // Token is now handled by apiClient internally
      setUser(user);
      setIsAuthenticated(true);
    } catch (error) {
      console.error('Login error:', error);
      throw error;
    }
  };

  const register = async (email: string, password: string): Promise<void> => {
    try {
      const result = await authService.register({ email, password, name: '', dateOfBirth: '' });
      const { user } = result;

      // Token is now handled by apiClient internally
      setUser(user);
      setIsAuthenticated(true);
    } catch (error) {
      console.error('Registration error:', error);
      throw error;
    }
  };

  const logout = (): void => {
    // Clear token from memory via apiClient
    apiClient.clearAuthToken();

    // Reset state
    setUser(null);
    setToken(null);
    setIsAuthenticated(false);
  };

  // Handle token expiration automatically
  useEffect(() => {
    // Token handling is now centralized in apiClient
  }, []);

  if (loading) {
    return <div>Loading...</div>; // Or a spinner component
  }

  return (
    <AuthContext.Provider
      value={{
        user,
        token: apiClient.getAuthToken(),
        isAuthenticated,
        loading,
        login,
        logout,
        register,
        checkAuthStatus,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};