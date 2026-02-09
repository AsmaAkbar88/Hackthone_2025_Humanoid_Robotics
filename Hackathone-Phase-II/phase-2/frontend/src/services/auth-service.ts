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


interface LoginBackendResponse {
  data: {
    user: User;
    access_token: string;
  };
}

interface RegisterBackendResponse {
  success: boolean;
  data: {
    user: {
      id: string;
      email: string;
      name?: string;
      date_of_birth?: string; // Snake_case from backend
      created_at: string; // Snake_case from backend
    };
    access_token: string;
    token_type: string;
  };
}

interface ForgotPasswordBackendResponse {
  success: boolean;
}

interface ResetPasswordBackendResponse {
  success: boolean;
}

class AuthService {
  async login(credentials: LoginCredentials): Promise<{ user: User; token: string }> {
    console.log('Login attempt with:', credentials);

    try {
      // API call to the backend
      const response = await apiClient.post<LoginBackendResponse>('/auth/login', credentials);

      // Transform the response to match what the frontend expects
      const { data } = response.data; // Extract from the nested data property

      // Ensure force_password_change flag is handled appropriately to prevent unwanted notifications
      const user = {
        ...data.user,
        force_password_change: false  // Override to prevent unwanted notifications
      };

      return {
        user,
        token: data.access_token
      };
    } catch (error: any) {
      if (error.message && (error.message.includes('Network Error') || error.message.includes('ECONNREFUSED'))) {
        throw new Error('Backend server is not running. Please start the backend server on port 8000.');
      }

      // Handle 401 errors specifically
      if (error.response?.status === 401) {
        const errorDetail = error.response.data?.detail || 'Invalid email or password';
        throw new Error(errorDetail);
      }

      console.error('Login error:', error);
      throw error;
    }
  }

  async register(userData: RegisterData): Promise<{ user: User; token: string }> {
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
      const response = await apiClient.post<RegisterBackendResponse>('/auth/register', transformedData);

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
        createdAt: backendUserData.user.created_at,
      };

      // Ensure force_password_change flag is handled appropriately to prevent unwanted notifications
      const user = {
        ...transformedUser,
        force_password_change: false  // Override to prevent unwanted notifications
      };

      return {
        user: user as User,
        token: backendUserData.access_token
      };
    } catch (error: any) {
      if (error.message && (error.message.includes('Network Error') || error.message.includes('ECONNREFUSED'))) {
        throw new Error('Backend server is not running. Please start the backend server on port 8000.');
      }

      // Handle 401 errors specifically
      if (error.response?.status === 401) {
        const errorDetail = error.response.data?.detail || 'Registration failed';
        throw new Error(errorDetail);
      }

      // Handle 400 errors (validation errors)
      if (error.response?.status === 400) {
        const errorDetail = error.response.data?.detail || 'Invalid input data';
        throw new Error(errorDetail);
      }

      console.error('Registration error:', error);
      throw error;
    }
  }

  async forgotPassword(forgotData: ForgotPasswordData): Promise<boolean> {
    console.log('Forgot password attempt with:', forgotData);

    try {
      // API call to the backend - update to match new backend expectation
      const response = await apiClient.post<ForgotPasswordBackendResponse>('/auth/forgot-password', {
        email: forgotData.email,
        date_of_birth: forgotData.dateOfBirth  // Convert to snake_case to match backend
      });
      return response.data.success;
    } catch (error: any) {
      if (error.message && (error.message.includes('Network Error') || error.message.includes('ECONNREFUSED'))) {
        throw new Error('Backend server is not running. Please start the backend server on port 8000.');
      }

      // Handle 401 errors specifically
      if (error.response?.status === 401) {
        const errorDetail = error.response.data?.detail || 'Verification failed';
        throw new Error(errorDetail);
      } else if (error.response?.status === 400) {
        const errorDetail = error.response.data?.detail || 'Verification failed';
        throw new Error(errorDetail);
      }

      console.error('Forgot password error:', error);
      throw error;
    }
  }

  async resetPassword(resetData: ResetPasswordData): Promise<boolean> {
    console.log('Reset password attempt for:', resetData.email);

    try {
      // API call to the backend - update to match new backend expectation
      const response = await apiClient.post<ResetPasswordBackendResponse>('/auth/reset-password', {
        email: resetData.email,
        new_password: resetData.newPassword
      });
      return response.data.success;
    } catch (error: any) {
      if (error.message && (error.message.includes('Network Error') || error.message.includes('ECONNREFUSED'))) {
        throw new Error('Backend server is not running. Please start the backend server on port 8000.');
      }

      // Handle 401 errors specifically
      if (error.response?.status === 401) {
        const errorDetail = error.response.data?.detail || 'Password reset failed';
        throw new Error(errorDetail);
      } else if (error.response?.status === 400) {
        const errorDetail = error.response.data?.detail || 'Password reset failed';
        throw new Error(errorDetail);
      }

      console.error('Reset password error:', error);
      throw error;
    }
  }

  async logout(): Promise<void> {
    // Clear authentication state
    if (typeof window !== 'undefined') {
      localStorage.removeItem('auth-token');
      localStorage.removeItem('user');
    }
  }

  async getCurrentUser(): Promise<User | null> {
    if (typeof window !== 'undefined') {
      const userStr = localStorage.getItem('user');
      const user = userStr ? JSON.parse(userStr) : null;

      // Ensure force_password_change flag is handled appropriately to prevent unwanted notifications
      if (user && user.hasOwnProperty('force_password_change')) {
        return {
          ...user,
          force_password_change: false  // Override to prevent unwanted notifications
        };
      }

      return user;
    }
    return null;
  }
}

export const authService = new AuthService();
export default AuthService;