// src/services/api-client.ts
import axios, { AxiosInstance, AxiosRequestConfig, AxiosResponse } from 'axios';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'https://asmaakbar-phase-iii.hf.space/api';

class ApiClient {
  private client: AxiosInstance;
  private authToken: string | null = null;

  constructor() {
    // Initialize token from sessionStorage on startup
    if (typeof window !== 'undefined') {
      this.authToken = sessionStorage.getItem('authToken');
    }

    this.client = axios.create({
      baseURL: API_BASE_URL,
      headers: {
        'Content-Type': 'application/json',
      },
      // Enable sending cookies with requests (for session-based auth if implemented later)
      withCredentials: true
    });

    // Request interceptor to add JWT token from a secure source
    this.client.interceptors.request.use(
      (config) => {
        const token = this.getAuthToken(); // Use getter to ensure token is read from sessionStorage if needed
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
        const url = error.config?.url || '';

        // ✅ SILENTLY ignore auth check when user is not logged in
        if (error.response?.status === 401 && url.includes('/auth/me')) {
          return Promise.reject(error);
        }

        // ✅ SILENTLY handle network errors - let calling code handle errors
        // No console.error here to avoid spam during initial auth check

        return Promise.reject(error);
      }
    );
  }

  public setAuthToken(token: string | null): void {
    // Set the token in memory and sessionStorage to persist across page refreshes
    this.authToken = token;
    if (typeof window !== 'undefined') {
      if (token) {
        sessionStorage.setItem('authToken', token);
      } else {
        sessionStorage.removeItem('authToken');
      }
    }
  }

  public getAuthToken(): string | null {
    // Check both memory and sessionStorage to ensure consistency
    if (!this.authToken && typeof window !== 'undefined') {
      this.authToken = sessionStorage.getItem('authToken');
    }
    return this.authToken;
  }

  public clearAuthToken(): void {
    // Clear the token from memory and sessionStorage
    this.authToken = null;
    if (typeof window !== 'undefined') {
      sessionStorage.removeItem('authToken');
    }
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
