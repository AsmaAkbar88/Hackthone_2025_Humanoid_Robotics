// src/context/TasksContext.tsx
'use client';

import React, { createContext, useContext, useReducer, useEffect, useCallback } from 'react';
import { taskService, type Task } from '@/services/task-service';

interface TasksState {
  tasks: Task[];
  loading: boolean;
  error: string | null;
  currentFilter: 'all' | 'active' | 'completed';
}

type TasksAction =
  | { type: 'FETCH_TASKS_START' }
  | { type: 'FETCH_TASKS_SUCCESS'; payload: Task[] }
  | { type: 'FETCH_TASKS_FAILURE'; payload: string }
  | { type: 'CREATE_TASK_START' }
  | { type: 'CREATE_TASK_SUCCESS'; payload: Task }
  | { type: 'CREATE_TASK_FAILURE'; payload: string }
  | { type: 'UPDATE_TASK_START' }
  | { type: 'UPDATE_TASK_SUCCESS'; payload: Task }
  | { type: 'UPDATE_TASK_FAILURE'; payload: string }
  | { type: 'DELETE_TASK_START' }
  | { type: 'DELETE_TASK_SUCCESS'; payload: string | number }
  | { type: 'DELETE_TASK_FAILURE'; payload: string }
  | { type: 'TOGGLE_TASK_START' }
  | { type: 'TOGGLE_TASK_SUCCESS'; payload: Task }
  | { type: 'TOGGLE_TASK_FAILURE'; payload: string }
  | { type: 'SET_FILTER'; payload: 'all' | 'active' | 'completed' }
  | { type: 'SET_ERROR'; payload: string | null };

const initialState: TasksState = {
  tasks: [],
  loading: false,
  error: null,
  currentFilter: 'all',
};

const TasksContext = createContext<{
  state: TasksState;
  fetchTasks: () => Promise<void>;
  createTask: (taskData: { title: string; description?: string }) => Promise<void>;
  updateTask: (id: string | number, taskData: Partial<Task>) => Promise<void>;
  deleteTask: (id: string | number) => Promise<void>;
  toggleTaskCompletion: (id: string | number) => Promise<void>;
  setFilter: (filter: 'all' | 'active' | 'completed') => void;
  clearError: () => void;
} | undefined>(undefined);

const tasksReducer = (state: TasksState, action: TasksAction): TasksState => {
  switch (action.type) {
    case 'FETCH_TASKS_START':
      return {
        ...state,
        loading: true,
        error: null,
      };
    case 'FETCH_TASKS_SUCCESS':
      return {
        ...state,
        tasks: action.payload,
        loading: false,
        error: null,
      };
    case 'FETCH_TASKS_FAILURE':
      return {
        ...state,
        loading: false,
        error: action.payload,
      };
    case 'CREATE_TASK_START':
      return {
        ...state,
        loading: true,
        error: null,
      };
    case 'CREATE_TASK_SUCCESS':
      return {
        ...state,
        tasks: [...state.tasks, action.payload],
        loading: false,
        error: null,
      };
    case 'CREATE_TASK_FAILURE':
      return {
        ...state,
        loading: false,
        error: action.payload,
      };
    case 'UPDATE_TASK_START':
      return {
        ...state,
        loading: true,
        error: null,
      };
    case 'UPDATE_TASK_SUCCESS':
      return {
        ...state,
        tasks: state.tasks.map(task =>
          task.id === action.payload.id ? action.payload : task
        ),
        loading: false,
        error: null,
      };
    case 'UPDATE_TASK_FAILURE':
      return {
        ...state,
        loading: false,
        error: action.payload,
      };
    case 'DELETE_TASK_START':
      return {
        ...state,
        loading: true,
        error: null,
      };
    case 'DELETE_TASK_SUCCESS':
      return {
        ...state,
        tasks: state.tasks.filter(task => task.id !== action.payload),
        loading: false,
        error: null,
      };
    case 'DELETE_TASK_FAILURE':
      return {
        ...state,
        loading: false,
        error: action.payload,
      };
    case 'TOGGLE_TASK_START':
      return {
        ...state,
        loading: true,
        error: null,
      };
    case 'TOGGLE_TASK_SUCCESS':
      return {
        ...state,
        tasks: state.tasks.map(task =>
          task.id === action.payload.id ? action.payload : task
        ),
        loading: false,
        error: null,
      };
    case 'TOGGLE_TASK_FAILURE':
      return {
        ...state,
        loading: false,
        error: action.payload,
      };
    case 'SET_FILTER':
      return {
        ...state,
        currentFilter: action.payload,
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

export const TasksProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [state, dispatch] = useReducer(tasksReducer, initialState);

  const fetchTasks = useCallback(async () => {
    dispatch({ type: 'FETCH_TASKS_START' });
    try {
      const tasks = await taskService.getAll();
      dispatch({ type: 'FETCH_TASKS_SUCCESS', payload: tasks });
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'Failed to fetch tasks';
      dispatch({ type: 'FETCH_TASKS_FAILURE', payload: errorMessage });
    }
  }, []);

  const createTask = useCallback(async (taskData: { title: string; description?: string }) => {
    dispatch({ type: 'CREATE_TASK_START' });
    try {
      const newTask = await taskService.create(taskData);
      dispatch({ type: 'CREATE_TASK_SUCCESS', payload: newTask });
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'Failed to create task';
      dispatch({ type: 'CREATE_TASK_FAILURE', payload: errorMessage });
      throw error;
    }
  }, []);

  const updateTask = useCallback(async (id: string | number, taskData: Partial<Task>) => {
    dispatch({ type: 'UPDATE_TASK_START' });
    try {
      const updatedTask = await taskService.update(id, taskData);
      dispatch({ type: 'UPDATE_TASK_SUCCESS', payload: updatedTask });
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'Failed to update task';
      dispatch({ type: 'UPDATE_TASK_FAILURE', payload: errorMessage });
      throw error;
    }
  }, []);

  const deleteTask = useCallback(async (id: string | number) => {
    dispatch({ type: 'DELETE_TASK_START' });
    try {
      await taskService.delete(id);
      dispatch({ type: 'DELETE_TASK_SUCCESS', payload: id });
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'Failed to delete task';
      dispatch({ type: 'DELETE_TASK_FAILURE', payload: errorMessage });
      throw error;
    }
  }, []);

  const toggleTaskCompletion = useCallback(async (id: string | number) => {
    dispatch({ type: 'TOGGLE_TASK_START' });
    try {
      const updatedTask = await taskService.toggleCompletion(id);
      dispatch({ type: 'TOGGLE_TASK_SUCCESS', payload: updatedTask });
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'Failed to toggle task';
      dispatch({ type: 'TOGGLE_TASK_FAILURE', payload: errorMessage });
      throw error;
    }
  }, []);

  const setFilter = useCallback((filter: 'all' | 'active' | 'completed') => {
    dispatch({ type: 'SET_FILTER', payload: filter });
  }, []);

  const clearError = useCallback(() => {
    dispatch({ type: 'SET_ERROR', payload: null });
  }, []);

  return (
    <TasksContext.Provider
      value={{
        state,
        fetchTasks,
        createTask,
        updateTask,
        deleteTask,
        toggleTaskCompletion,
        setFilter,
        clearError,
      }}
    >
      {children}
    </TasksContext.Provider>
  );
};

export const useTasks = () => {
  const context = useContext(TasksContext);
  if (context === undefined) {
    throw new Error('useTasks must be used within a TasksProvider');
  }
  return context;
};