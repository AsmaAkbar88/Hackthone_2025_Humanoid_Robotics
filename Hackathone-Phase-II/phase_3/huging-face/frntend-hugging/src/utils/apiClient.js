import axios from 'axios';
import { apiClient as mainApiClient } from '../services/api-client'; // Import the main API client

// Create an Axios instance
const apiClient = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_BASE_URL || '/api', // Use NEXT_PUBLIC_API_BASE_URL or default to /api
  timeout: 10000, // 10 seconds timeout
});

// Request interceptor to add auth headers
apiClient.interceptors.request.use(
  (config) => {
    const token = mainApiClient.getAuthToken(); // Use the main API client's token

    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }

    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor to handle responses
apiClient.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    // Handle 401 Unauthorized responses (token expired or invalid)
    if (error.response && error.response.status === 401) {
      // Token might be expired or invalid
      
      // Clear token using main API client
      mainApiClient.clearAuthToken();

      // Redirect to login page using window.location
      if (typeof window !== 'undefined') {
        window.location.href = '/login';
      }
    }

    // Handle other errors
    return Promise.reject(error);
  }
);

// Function to handle API calls with automatic token management
const apiCall = async (method, url, data = null, options = {}) => {
  try {
    // Check if token is still valid before making the request
    const token = mainApiClient.getAuthToken();
    if (!token) {
      // Token is not available, redirect to login
      if (typeof window !== 'undefined') {
        window.location.href = '/login';
        return Promise.reject(new Error('Not authenticated'));
      }
    }

    let response;

    switch (method.toLowerCase()) {
      case 'get':
        response = await apiClient.get(url, options);
        break;
      case 'post':
        response = await apiClient.post(url, data, options);
        break;
      case 'put':
        response = await apiClient.put(url, data, options);
        break;
      case 'patch':
        response = await apiClient.patch(url, data, options);
        break;
      case 'delete':
        response = await apiClient.delete(url, options);
        break;
      default:
        throw new Error(`Unsupported method: ${method}`);
    }

    return response.data;
  } catch (error) {
    // Handle specific error cases
    if (error.response) {
      // Server responded with error status
      const { status, data } = error.response;

      if (status === 401) {
        // Unauthorized - token expired or invalid
        mainApiClient.clearAuthToken();

        if (typeof window !== 'undefined') {
          window.location.href = '/login';
        }

        throw new Error('Session expired. Please log in again.');
      } else if (status >= 500) {
        // Server error
        throw new Error('Server error occurred. Please try again later.');
      } else {
        // Client error
        throw new Error(data?.message || `Request failed with status ${status}`);
      }
    } else if (error.request) {
      // Request was made but no response received
      throw new Error('Network error occurred. Please check your connection.');
    } else {
      // Something else happened
      throw new Error(error.message || 'An error occurred during the request.');
    }
  }
};

// Export individual methods for convenience
export const apiGet = (url, options = {}) => apiCall('GET', url, null, options);
export const apiPost = (url, data = null, options = {}) => apiCall('POST', url, data, options);
export const apiPut = (url, data = null, options = {}) => apiCall('PUT', url, data, options);
export const apiPatch = (url, data = null, options = {}) => apiCall('PATCH', url, data, options);
export const apiDelete = (url, options = {}) => apiCall('DELETE', url, null, options);

// Export the apiClient instance and the helper functions
export default apiClient;
export { apiCall };