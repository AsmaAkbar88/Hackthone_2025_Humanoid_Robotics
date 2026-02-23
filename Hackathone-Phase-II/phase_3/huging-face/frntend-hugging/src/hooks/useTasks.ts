// src/hooks/useTasks.ts
import { useTasks as useTasksContext } from '@/context/TasksContext';

export const useTasks = () => {
  const context = useTasksContext();
  if (!context) {
    throw new Error('useTasks must be used within a TasksProvider');
  }
  return context;
};