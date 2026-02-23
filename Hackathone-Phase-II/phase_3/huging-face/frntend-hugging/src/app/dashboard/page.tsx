'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import Header from '@/components/ui/Header';
import TaskCard from '@/components/ui/TaskCard';
import TaskForm from '@/components/ui/TaskForm';
import { useAuth } from '@/hooks/useAuth';
import { useTasks } from '@/hooks/useTasks';
import { useNotifications } from '@/hooks/useNotifications';
import Notification from '@/components/ui/Notification';

export default function DashboardPage() {
  const router = useRouter();
  const { state: authState } = useAuth();
  const { state: tasksState, fetchTasks, createTask, updateTask, deleteTask, toggleTaskCompletion, setFilter } = useTasks();
  const { showError, showSuccess } = useNotifications();
  const [showTaskForm, setShowTaskForm] = useState(false);

  useEffect(() => {
    if (!authState.loading && !authState.isAuthenticated) {
      router.push('/login');
    } else if (authState.isAuthenticated) {
      fetchTasks();
    }
  }, [authState.loading, authState.isAuthenticated, router, fetchTasks]);

  if (authState.loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-lg">Loading...</div>
      </div>
    );
  }

  if (!authState.isAuthenticated) {
    return null; // Redirect is happening in useEffect
  }

  const handleCreateTask = async (data: { title: string; description?: string }) => {
    try {
      await createTask(data);
      showSuccess('Task created successfully!');
      setShowTaskForm(false);
    } catch (error) {
      showError('Failed to create task. Please try again.');
      console.error('Create task error:', error);
    }
  };

  const handleToggleTask = async (id: string | number) => {
    try {
      await toggleTaskCompletion(id);
      showSuccess('Task updated successfully!');
    } catch (error) {
      showError('Failed to update task. Please try again.');
      console.error('Toggle task error:', error);
    }
  };

  const handleDeleteTask = async (id: string | number) => {
    if (window.confirm('Are you sure you want to delete this task?')) {
      try {
        await deleteTask(id);
        showSuccess('Task deleted successfully!');
      } catch (error) {
        showError('Failed to delete task. Please try again.');
        console.error('Delete task error:', error);
      }
    }
  };

  const filteredTasks = tasksState.tasks.filter(task => {
    switch(tasksState.currentFilter) {
      case 'active':
        return !task.completed;
      case 'completed':
        return task.completed;
      default:
        return true;
    }
  });

  return (
    <div className="min-h-screen ">
      <Header />

      <main className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        <div className="px-4 py-6 sm:px-0">
          <div className="glass-container max-w-4xl mx-auto p-8">
            <div className="flex justify-between items-center mb-8">
              <h2 className="text-3xl font-bold text-text-primary theme-typography-h2">Your Tasks</h2>
              <div className="flex space-x-4">
                <Link href="/chat">
                  <button
                    className="theme-btn-secondary text-black"
                  >
                    AI Assistant
                  </button>
                </Link>
                <button
                  onClick={() => setShowTaskForm(!showTaskForm)}
                  className="theme-btn-primary text-black"
                >
                  {showTaskForm ? 'Cancel' : '+ New Task'}
                </button>
              </div>
            </div>

            {showTaskForm && (
              <div className="mb-8 p-6 glass-container">
                <h3 className="text-xl font-semibold text-text-primary theme-typography-h3 mb-4">Create New Task</h3>
                <TaskForm
                  onSubmit={handleCreateTask}
                  onCancel={() => setShowTaskForm(false)}
                  submitText="Create Task"
                />
              </div>
            )}

            {tasksState.loading ? (
              <div className="flex justify-center items-center py-12">
                <div className="relative">
                  <div className="w-12 h-12 border-4 border-turquoise border-opacity-50 rounded-full animate-spin"></div>
                  <div className="absolute inset-0 w-12 h-12 border-4 border-transparent border-r-turquoise border-t-turquoise rounded-full animate-spin-reverse"></div>
                </div>
              </div>
            ) : tasksState.error ? (
              <div className="p-6 rounded-xl glass-container border border-red-200">
                <div className="text-red-500 theme-typography-body">
                  <p className="font-medium">Error loading tasks:</p>
                  <p className="mt-1">{tasksState.error}</p>
                </div>
                <div className="mt-4">
                  <button
                    onClick={() => fetchTasks()}
                    className="theme-btn-secondary"
                  >
                    Retry
                  </button>
                </div>
              </div>
            ) : (
            ) : (
              <div>
                <div className="flex space-x-4 mb-6">
                  <button
                    onClick={() => setFilter('all')}
                    className={`filter-button ${
                      tasksState.currentFilter === 'all' ? 'active' : ''
                    }`}
                  >
                    All ({tasksState.tasks.length})
                    <span className="ml-2 status-badge status-pending">{tasksState.tasks.length}</span>
                  </button>
                  <button
                    onClick={() => setFilter('active')}
                    className={`filter-button ${
                      tasksState.currentFilter === 'active' ? 'active' : ''
                    }`}
                  >
                    Active ({tasksState.tasks.filter(t => !t.completed).length})
                    <span className="ml-2 status-badge status-pending">{tasksState.tasks.filter(t => !t.completed).length}</span>
                  </button>
                  <button
                    onClick={() => setFilter('completed')}
                    className={`filter-button ${
                      tasksState.currentFilter === 'completed' ? 'active' : ''
                    }`}
                  >
                    Completed ({tasksState.tasks.filter(t => t.completed).length})
                    <span className="ml-2 status-badge status-completed">{tasksState.tasks.filter(t => t.completed).length}</span>
                  </button>
                </div>

                <p className="text-text-secondary mb-6 theme-typography-body">
                  Showing {filteredTasks.length} of {tasksState.tasks.length} tasks
                </p>

                {filteredTasks.length > 0 ? (
                  <div className="space-y-4">
                    {filteredTasks.map((task) => (
                      <TaskCard
                        key={task.id}
                        task={task}
                        onToggle={handleToggleTask}
                        onDelete={handleDeleteTask}
                        onUpdate={async (id, data) => {
                          try {
                            await updateTask(id, data);
                            showSuccess('Task updated successfully!');
                          } catch (error) {
                            showError('Failed to update task. Please try again.');
                            console.error('Update task error:', error);
                          }
                        }}
                      />
                    ))}
                  </div>
                ) : (
                  <div className="text-center py-12 glass-container">
                    <p className="text-text-secondary theme-typography-body mb-4">No tasks found.</p>
                    <p className="text-text-muted theme-typography-body">{tasksState.tasks.length === 0 ? 'Create your first task!' : 'Try changing the filter.'}</p>
                  </div>
                )}
              </div>
            )}
          </div>
        </div>
      </main>
      <Notification />
    </div>
  );
}