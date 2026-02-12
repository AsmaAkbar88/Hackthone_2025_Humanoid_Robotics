// src/services/api-client.ts
import axios, { AxiosInstance, AxiosRequestConfig, AxiosResponse } from 'axios';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'https://asmaakbar-web-app.hf.space/api';

// Ensure we're always using HTTPS for production
const isProduction = typeof window !== 'undefined' ? window.location.protocol === 'https:' : true;
const finalApiBaseUrl = API_BASE_URL.replace('http://', 'https://'); // Always enforce HTTPS regardless of environment

class ApiClient {
  private client: AxiosInstance;

  constructor() {
    this.client = axios.create({
      baseURL: finalApiBaseUrl,
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
          console.error('Backend server is not running. Please start the backend server on port 8000.');
          alert('Backend server is not running. Please start the backend server on port 8000.\n\nTo start the backend:\n1. Open a new terminal\n2. Navigate to the backend directory\n3. Run: npm run dev (or python -m uvicorn src.api.main:app --port 8000)');
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
    // Use the same token key as authService.js
    if (typeof window !== 'undefined') {
      return localStorage.getItem('authToken');
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