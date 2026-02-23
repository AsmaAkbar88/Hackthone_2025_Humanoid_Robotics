// src/services/auth-service.ts
import { apiClient } from './api-client';

interface LoginCredentials {
  email: string;
  password: string;
}

interface RegisterData {
  name: string;
  email: string;
  password: string;
  dateOfBirth: string; // Format: YYYY-MM-DD (will be converted to date_of_birth for backend)
}

interface ForgotPasswordData {
  email: string;
  dateOfBirth: string; // Format: YYYY-MM-DD
}


interface ResetPasswordData {
  email: string;
  newPassword: string;
}


export interface User {
  id: string;
  email: string;
  name?: string;
  dateOfBirth?: string;
  createdAt: string;
  lastLoginAt?: string;
  force_password_change?: boolean; // Flag to indicate if user needs to change password
}

class AuthService {
  async login(credentials: LoginCredentials): Promise<{ user: User; token?: string }> {
    console.log('Login attempt with:', credentials);

    try {
      // API call to the backend
      const response: { data: { data: { user: User; access_token: string } } } = await apiClient.post('/auth/login', credentials);

      // Transform the response to match what the frontend expects
      const { data } = response.data; // Extract from the nested data property

      // Ensure force_password_change flag is handled appropriately to prevent unwanted notifications
      const user = {
        ...data.user,
        force_password_change: false  // Override to prevent unwanted notifications
      };

      // Store the token in memory only
      apiClient.setAuthToken(data.access_token);

      return {
        user
      };
    } catch (error: any) {
      if (error.response) {
        if (error.response.status === 401) {
          throw new Error(
            error.response.data?.detail || 'Invalid email or password'
          );
        }

        throw new Error('Login failed. Please try again.');
      }

      // Only here for real network issues
      throw error; // Re-throw the original error instead of a hardcoded message
    }
  }

  async register(userData: RegisterData): Promise<{ user: User; token?: string }> {
    console.log('Register attempt with:', userData);

    // Validate date format before sending to backend
    if (userData.dateOfBirth) {
      // Check if date format is valid (YYYY-MM-DD)
      const dateRegex = /^\d{4}-\d{2}-\d{2}$/;
      if (!dateRegex.test(userData.dateOfBirth)) {
        throw new Error('Invalid date of birth format. Please use YYYY-MM-DD format.');
      }

      // Parse the date to ensure it's valid
      const dateObj = new Date(userData.dateOfBirth);
      if (isNaN(dateObj.getTime())) {
        throw new Error('Invalid date of birth. Please enter a valid date.');
      }

      // Check if the date is reasonable (not in the future and not too far in the past)
      const today = new Date();
      const minDate = new Date('1900-01-01');
      if (dateObj > today || dateObj < minDate) {
        throw new Error('Date of birth must be a realistic past date.');
      }
    }

    try {
      // Transform camelCase to snake_case to match backend expectations
      const transformedData = {
        name: userData.name,
        email: userData.email,
        password: userData.password,
        date_of_birth: userData.dateOfBirth, // Convert camelCase to snake_case
      };

      // API call to the backend
      const response: { data: { data: { user: any; access_token: string } } } = await apiClient.post('/auth/register', transformedData);

      // Transform the response to match what the frontend expects
      const responseData = response.data; // The backend returns data in a nested structure

      // The backend returns: { success: true, data: { user: ..., access_token: ..., token_type: ... } }
      const backendUserData = responseData.data;

      // Map backend snake_case fields to frontend camelCase fields
      const transformedUser = {
        id: backendUserData.user.id,
        email: backendUserData.user.email,
        name: backendUserData.user.name || undefined,
        dateOfBirth: backendUserData.user.date_of_birth, // Map snake_case to camelCase
        createdAt: backendUserData.user.created_at || backendUserData.user.createdAt,
      };

      // Ensure force_password_change flag is handled appropriately to prevent unwanted notifications
      const user = {
        ...transformedUser,
        force_password_change: false  // Override to prevent unwanted notifications
      };

      // Store the token in memory only
      apiClient.setAuthToken(backendUserData.access_token);

      return {
        user: user as User
      };
    } catch (error: any) {
      if (error.response) {
        if (error.response.status === 401) {
          throw new Error(
            error.response.data?.detail || 'Registration failed'
          );
        }

        if (error.response.status === 400) {
          throw new Error(
            error.response.data?.detail || 'Invalid input data'
          );
        }

        throw new Error('Registration failed. Please try again.');
      }

      throw error; // Re-throw the original error instead of a hardcoded message
    }
  }

  async forgotPassword(forgotData: ForgotPasswordData): Promise<boolean> {
    console.log('Forgot password attempt with:', forgotData);

    try {
      // API call to the backend - update to match new backend expectation
      const response: { data: { success: boolean } } = await apiClient.post('/auth/forgot-password', {
        email: forgotData.email,
        date_of_birth: forgotData.dateOfBirth  // Convert to snake_case to match backend
      });
      return response.data.success;
    } catch (error: any) {
      if (error.response) {
        if (error.response.status === 401) {
          throw new Error(
            error.response.data?.detail || 'Verification failed'
          );
        }

        if (error.response.status === 400) {
          throw new Error(
            error.response.data?.detail || 'Verification failed'
          );
        }

        throw new Error('Forgot password request failed. Please try again.');
      }

      throw error; // Re-throw the original error instead of a hardcoded message
    }
  }

  async resetPassword(resetData: ResetPasswordData): Promise<boolean> {
    console.log('Reset password attempt for:', resetData.email);

    try {
      // API call to the backend - update to match new backend expectation
      const response: { data: { success: boolean } } = await apiClient.post('/auth/reset-password', {
        email: resetData.email,
        new_password: resetData.newPassword
      });
      return response.data.success;
    } catch (error: any) {
      if (error.response) {
        if (error.response.status === 401) {
          throw new Error(
            error.response.data?.detail || 'Password reset failed'
          );
        }

        if (error.response.status === 400) {
          throw new Error(
            error.response.data?.detail || 'Password reset failed'
          );
        }

        throw new Error('Password reset failed. Please try again.');
      }

      throw error; // Re-throw the original error instead of a hardcoded message
    }
  }

  async logout(): Promise<void> {
    // Call backend to invalidate session if needed
    try {
      await apiClient.post('/auth/logout');
    } catch (error) {
      // Even if backend logout fails, continue with frontend cleanup
      console.error('Logout error:', error);
    }
    
    // Clear the token from memory
    apiClient.clearAuthToken();
  }

  async getCurrentUser(): Promise<User | null> {
    try {
      // Call the backend to verify authentication status
      const response: { data: { user: User } } = await apiClient.get('/auth/me');
      return response.data.user as User;
    } catch (error: any) {
      // Check if this is a network error vs a 401 unauthorized
      // Only throw network errors, return null for 401s (which is normal when not logged in)
      if (error.response) {
        // If it's a 401 response, it means user is not authenticated, which is normal
        if (error.response.status === 401) {
          return null;
        }
        // For other HTTP errors, we might want to handle them differently
        // but for now, return null as the user is not authenticated
        return null;
      } else {
        // This is a network error (no response received), re-throw it
        // so it can be handled appropriately by the caller
        throw error;
      }
    }
  }
}

export const authService = new AuthService();
export default AuthService;