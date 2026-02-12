// src/services/task-service.ts
import { apiClient } from './api-client';

export interface Task {
  id: string | number;
  title: string;
  description?: string;
  completed: boolean;
  userId: string | number;
  createdAt: string;
  updatedAt: string;
}

interface CreateTaskData {
  title: string;
  description?: string;
}

interface UpdateTaskData extends Partial<CreateTaskData> {
  completed?: boolean;
}

interface GetAllTasksBackendResponse {
  success: boolean;
  data: {
    tasks: Task[];
    total: number;
  };
}

interface GetTaskByIdBackendResponse {
  success: boolean;
  data: Task;
}

interface CreateTaskBackendResponse {
  success: boolean;
  data: Task;
}

interface UpdateTaskBackendResponse {
  success: boolean;
  data: Task;
}

interface ToggleCompletionBackendResponse {
  success: boolean;
  data: {
    id: string | number;
    completed: boolean;
    updated_at: string;
  };
}

class TaskService {
  async getAll(): Promise<Task[]> {
    try {
      // API call to the backend to get all tasks for the current user
      const response = await apiClient.get<GetAllTasksBackendResponse>('/tasks');
      return response.data.data.tasks || [];
    } catch (error: any) {
      // Show error message when backend is not running
      if (error.message && (error.message.includes('Network Error') || error.message.includes('ECONNREFUSED'))) {
        throw new Error('Backend server is not running or is not accessible. Please check that the backend is deployed and accessible.');
      }
      // Check if it's a mixed content error
      if (error.message && error.message.includes('mixed-content')) {
        throw new Error('Mixed content error: The frontend is trying to access the backend via HTTP instead of HTTPS. Please check your API URL configuration.');
      }
      console.error('Error fetching tasks:', error);
      throw error;
    }
  }

  async getById(id: string | number): Promise<Task> {
    try {
      // API call to the backend to get a specific task
      const response = await apiClient.get<GetTaskByIdBackendResponse>(`/tasks/${id}`);
      return response.data.data; // Backend returns task in data property
    } catch (error: any) {
      if (error.message && (error.message.includes('Network Error') || error.message.includes('ECONNREFUSED'))) {
        throw new Error('Backend server is not running or is not accessible. Please check that the backend is deployed and accessible.');
      }
      // Check if it's a mixed content error
      if (error.message && error.message.includes('mixed-content')) {
        throw new Error('Mixed content error: The frontend is trying to access the backend via HTTP instead of HTTPS. Please check your API URL configuration.');
      }
      console.error(`Error fetching task ${id}:`, error);
      throw error;
    }
  }

  async create(taskData: CreateTaskData): Promise<Task> {
    try {
      // API call to the backend to create a new task
      const response = await apiClient.post<CreateTaskBackendResponse>('/tasks', taskData);
      return response.data.data; // Backend returns task in data property
    } catch (error: any) {
      if (error.message && (error.message.includes('Network Error') || error.message.includes('ECONNREFUSED'))) {
        throw new Error('Backend server is not running or is not accessible. Please check that the backend is deployed and accessible.');
      }
      // Check if it's a mixed content error
      if (error.message && error.message.includes('mixed-content')) {
        throw new Error('Mixed content error: The frontend is trying to access the backend via HTTP instead of HTTPS. Please check your API URL configuration.');
      }
      console.error('Error creating task:', error);
      throw error;
    }
  }

  async update(id: string | number, taskData: UpdateTaskData): Promise<Task> {
    try {
      // API call to the backend to update a task
      const response = await apiClient.put<UpdateTaskBackendResponse>(`/tasks/${id}`, taskData);
      return response.data.data; // Backend returns task in data property
    } catch (error: any) {
      if (error.message && (error.message.includes('Network Error') || error.message.includes('ECONNREFUSED'))) {
        throw new Error('Backend server is not running or is not accessible. Please check that the backend is deployed and accessible.');
      }
      // Check if it's a mixed content error
      if (error.message && error.message.includes('mixed-content')) {
        throw new Error('Mixed content error: The frontend is trying to access the backend via HTTP instead of HTTPS. Please check your API URL configuration.');
      }
      console.error(`Error updating task ${id}:`, error);
      throw error;
    }
  }

  async toggleCompletion(id: string | number): Promise<Task> {
    try {
      // API call to the backend to toggle task completion
      const response = await apiClient.patch<ToggleCompletionBackendResponse>(`/tasks/${id}/toggle`);

      // The toggle endpoint returns limited data, so we need to fetch the full task
      // Or we can update based on the response we get
      const toggleResponse = response.data.data;

      // For now, let's fetch the full task after toggling to get complete data
      return await this.getById(id);
    } catch (error: any) {
      if (error.message && (error.message.includes('Network Error') || error.message.includes('ECONNREFUSED'))) {
        throw new Error('Backend server is not running or is not accessible. Please check that the backend is deployed and accessible.');
      }
      // Check if it's a mixed content error
      if (error.message && error.message.includes('mixed-content')) {
        throw new Error('Mixed content error: The frontend is trying to access the backend via HTTP instead of HTTPS. Please check your API URL configuration.');
      }
      console.error(`Error toggling task ${id}:`, error);
      throw error;
    }
  }

  async delete(id: string | number): Promise<void> {
    try {
      // API call to the backend to delete a task
      await apiClient.delete(`/tasks/${id}`);
    } catch (error: any) {
      if (error.message && (error.message.includes('Network Error') || error.message.includes('ECONNREFUSED'))) {
        throw new Error('Backend server is not running or is not accessible. Please check that the backend is deployed and accessible.');
      }
      // Check if it's a mixed content error
      if (error.message && error.message.includes('mixed-content')) {
        throw new Error('Mixed content error: The frontend is trying to access the backend via HTTP instead of HTTPS. Please check your API URL configuration.');
      }
      console.error(`Error deleting task ${id}:`, error);
      throw error;
    }
  }
}

export const taskService = new TaskService();
export default TaskService;