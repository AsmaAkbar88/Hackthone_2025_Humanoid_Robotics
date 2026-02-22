// src/services/api-client.ts
import axios, { AxiosInstance, AxiosRequestConfig, AxiosResponse } from 'axios';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'https://asmaakbar-phase-ll.hf.space/api';

class ApiClient {
  private client: AxiosInstance;

  constructor() {
    this.client = axios.create({
      baseURL: API_BASE_URL,
      headers: {
        'Content-Type': 'application/json',
      },
    });

    // Request interceptor to add JWT token
    this.client.interceptors.request.use(
      (config) => {
        const token = this.getAuthToken();
        if (token) {
          config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
      },
      (error) => {
        return Promise.reject(error);
      }
    );

    // Response interceptor to handle authentication errors
    this.client.interceptors.response.use(
      (response) => response,
      (error) => {
        if (error.code === 'ECONNREFUSED' || error.code === 'ENOTFOUND') {
          // Show a user-friendly message when backend is not running
          console.error('Backend server is not running. Please start the backend server at https://asmaakbar-phase-ll.hf.space.');
          alert('Backend server is not accessible. Please ensure the backend is deployed at https://asmaakbar-phase-ll.hf.space.\n\nFor local development:\n1. Open a new terminal\n2. Navigate to the backend directory\n3. Run: npm run dev (or python -m uvicorn src.api.main:app --port 8000)');
        } else if (error.response?.status === 401) {
          // Handle unauthorized access - maybe redirect to login
          console.error('Unauthorized access - token may have expired or is invalid');

          // Check if this is a login/register request - if so, don't redirect
          const requestUrl = error.config?.url || '';
          if (!requestUrl.includes('/auth/login') && !requestUrl.includes('/auth/register')) {
            // For non-auth requests, remove auth token and potentially redirect
            if (typeof window !== 'undefined') {
              localStorage.removeItem('auth-token');
              localStorage.removeItem('user');
            }
          }
        }
        return Promise.reject(error);
      }
    );
  }

  private getAuthToken(): string | null {
    // In a real implementation, this would retrieve the token from Better Auth
    // For now, we'll look for it in localStorage as a placeholder
    if (typeof window !== 'undefined') {
      return localStorage.getItem('auth-token');
    }
    return null;
  }

  public async get<T>(url: string, config?: AxiosRequestConfig): Promise<AxiosResponse<T>> {
    return this.client.get<T>(url, config);
  }

  public async post<T>(url: string, data?: any, config?: AxiosRequestConfig): Promise<AxiosResponse<T>> {
    return this.client.post<T>(url, data, config);
  }

  public async put<T>(url: string, data?: any, config?: AxiosRequestConfig): Promise<AxiosResponse<T>> {
    return this.client.put<T>(url, data, config);
  }

  public async patch<T>(url: string, data?: any, config?: AxiosRequestConfig): Promise<AxiosResponse<T>> {
    return this.client.patch<T>(url, data, config);
  }

  public async delete<T>(url: string, config?: AxiosRequestConfig): Promise<AxiosResponse<T>> {
    return this.client.delete<T>(url, config);
  }
}

export const apiClient = new ApiClient();
export default ApiClient;