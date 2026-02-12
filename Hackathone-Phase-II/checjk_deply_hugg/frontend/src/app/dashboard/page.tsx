'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
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
          <div className="bg-white shadow-md overflow-hidden sm:rounded-lg p-6 theme-card">
            <div className="flex justify-between items-center mb-6">
              <h2 className="text-2xl font-bold text-[var(--text-primary)]">Your Tasks</h2>
              <button
                onClick={() => setShowTaskForm(!showTaskForm)}
                className="ml-4 px-4 py-2 text-sm font-medium text-black shadow-md border-2 rounded-md hover:bg-pink-400 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-[var(--primary-500)]"
              >
                {showTaskForm ? 'Cancel' : '+ New Task'}
              </button>
            </div>

            {showTaskForm && (
              <div className="mb-6 p-4 bg-[var(--secondary-50)]">
                <h3 className="text-lg font-medium text-[var(--text-primary)] mb-3">Create New Task</h3>
                <TaskForm
                  onSubmit={handleCreateTask}
                  onCancel={() => setShowTaskForm(false)}
                  submitText="Create Task"
                />
              </div>
            )}

            {tasksState.loading ? (
              <p className="text-[var(--text-secondary)]">Loading tasks...</p>
            ) : tasksState.error ? (
              <div className="bg-red-50 text-red-500  p-4 rounded">
                Error loading tasks: {tasksState.error}
                <button
                  onClick={() => fetchTasks()}
                  className="ml-4 text-[var(--primary-600)] underline"
                >
                  Retry
                </button>
              </div>
            ) : (
              <div>
                <div className="flex space-x-4 mb-4">
                  <button
                    onClick={() => setFilter('all')}
                    className={`px-3 py-1 text-sm ml-4 px-4 py-2 text-sm font-medium text-black shadow-md border-2 rounded-md hover:bg-pink-400 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-[var(--primary-500)] rounded ${
                      tasksState.currentFilter === 'all'
                        ? 'bg-pink-400 shadow-md border-2 text-black'
                        : 'bg-[var(--secondary-200)] text-[var(--text-primary)]'
                    }`}
                  >
                    All ({tasksState.tasks.length})
                  </button>
                  <button
                    onClick={() => setFilter('active')}
                    className={`px-3 py-1 text-sm ml-4 px-4 py-2 text-sm font-medium text-black shadow-md border-2 rounded-md hover:bg-pink-400 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-[var(--primary-500)] rounded ${
                      tasksState.currentFilter === 'active'
                        ? 'bg-[var(--primary-500)] text-black bg-pink-400 shadow-md'
                        : 'bg-[var(--secondary-200)] text-[var(--text-primary)]'
                    }`}
                  >
                    Active ({tasksState.tasks.filter(t => !t.completed).length})
                  </button>
                  <button
                    onClick={() => setFilter('completed')}
                    className={`px-3 py-1 text-sm ml-4 px-4 py-2 text-sm font-medium text-black shadow-md border-2 rounded-md hover:bg-pink-400 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-[var(--primary-500)] rounded ${
                      tasksState.currentFilter === 'completed'
                        ? 'bg-[var(--primary-500)] text-black bg-pink-400 shadow-md'
                        : 'bg-[var(--secondary-200)] text-[var(--text-primary)]'
                    }`}
                  >
                    Completed ({tasksState.tasks.filter(t => t.completed).length})
                  </button>
                </div>

                <p className="text-[var(--text-secondary)] mb-4">
                  Showing {filteredTasks.length} of {tasksState.tasks.length} tasks
                </p>

                {filteredTasks.length > 0 ? (
                  <div>
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
                  <p className="text-[var(--text-secondary)]">No tasks found. {tasksState.tasks.length === 0 ? 'Create your first task!' : 'Try changing the filter.'}</p>
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