'use client';

import React, { useState, useEffect, ReactNode } from 'react';
import { AuthContext, type AuthContextType, type User } from './authContext';

export const AuthProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [token, setToken] = useState<string | null>(null);
  const [isAuthenticated, setIsAuthenticated] = useState<boolean>(false);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    // Check if user is already logged in when app loads
    const initAuth = async () => {
      const savedToken = localStorage.getItem('authToken');
      if (savedToken) {
        try {
          // Verify token and get user info
          const isValid = await checkAuthStatus();
          if (isValid) {
            setToken(savedToken);
            setIsAuthenticated(true);
          } else {
            // Token is invalid, clear it
            localStorage.removeItem('authToken');
            setToken(null);
            setIsAuthenticated(false);
          }
        } catch (error) {
          console.error('Error initializing auth:', error);
          localStorage.removeItem('authToken');
          setToken(null);
          setIsAuthenticated(false);
        }
      }
      setLoading(false);
    };

    initAuth();
  }, []);

  const checkAuthStatus = async (): Promise<boolean> => {
    const token = localStorage.getItem('authToken');
    if (!token) return false;

    try {
      const response = await fetch('/api/auth/me', {
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });

      if (response.ok) {
        const userData = await response.json();
        setUser(userData);
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
      const response = await fetch('/api/auth/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password }),
      });

      if (response.ok) {
        const data = await response.json();
        const { token, user } = data;

        // Save token to localStorage
        localStorage.setItem('authToken', token);

        // Set user and auth state
        setUser(user);
        setToken(token);
        setIsAuthenticated(true);
      } else {
        const errorData = await response.json();
        throw new Error(errorData.error || 'Login failed');
      }
    } catch (error) {
      console.error('Login error:', error);
      throw error;
    }
  };

  const register = async (email: string, password: string): Promise<void> => {
    try {
      const response = await fetch('/api/auth/register', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || 'Registration failed');
      }

      // Registration successful, now login
      await login(email, password);
    } catch (error) {
      console.error('Registration error:', error);
      throw error;
    }
  };

  const logout = (): void => {
    // Remove token from localStorage
    localStorage.removeItem('authToken');

    // Reset state
    setUser(null);
    setToken(null);
    setIsAuthenticated(false);
  };

  // Handle token expiration automatically
  useEffect(() => {
    if (!token) return;

    const handleExpiredToken = () => {
      logout();
      window.location.href = '/login'; // Redirect to login page
    };

    // Listen for 401 responses indicating token expiration
    const originalFetch = window.fetch;
    window.fetch = async (...args) => {
      const response = await originalFetch(...args);

      if (response.status === 401) {
        handleExpiredToken();
      }

      return response;
    };

    return () => {
      window.fetch = originalFetch;
    };
  }, [token]);

  if (loading) {
    return <div>Loading...</div>; // Or a spinner component
  }

  return (
    <AuthContext.Provider
      value={{
        user,
        token,
        isAuthenticated,
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