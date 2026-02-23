// src/components/ui/TaskCard.tsx
import React, { useState } from 'react';
import { Task } from '@/services/task-service';
import TaskForm from './TaskForm';
import EditButton from './EditButton';
import DeleteButton from './DeleteButton';

interface TaskCardProps {
  task: Task;
  onToggle?: (id: string | number) => void;
  onDelete?: (id: string | number) => void;
  onUpdate?: (id: string | number, data: Partial<Task>) => void;
}

const TaskCard: React.FC<TaskCardProps> = ({ task, onToggle, onDelete, onUpdate }) => {
  const [isEditing, setIsEditing] = useState(false);

  const handleToggle = () => {
    onToggle?.(task.id);
  };

  const handleDelete = () => {
    onDelete?.(task.id);
  };

  const handleEdit = () => {
    setIsEditing(true);
  };

  const handleSave = async (data: { title: string; description?: string }) => {
    if (onUpdate) {
      await onUpdate(task.id, data);
      setIsEditing(false);
    }
  };

  const handleCancel = () => {
    setIsEditing(false);
  };

  return (
    <div
      className={`task-item ${task.completed ? 'completed' : ''} p-5 mb-4 glass-container card-hover`}
      role="listitem"
      aria-labelledby={`task-title-${task.id}`}
    >
      {isEditing ? (
        <div className="edit-mode">
          <h3 className="text-lg font-medium text-text-primary mb-3 text-h3 theme-typography-h3">Edit Task</h3>
          <TaskForm
            initialData={task}
            onSubmit={handleSave}
            onCancel={handleCancel}
            submitText="Update Task"
          />
        </div>
      ) : (
        <div className="view-mode">
          <div className="flex items-start">
            <input
              type="checkbox"
              id={`task-checkbox-${task.id}`}
              checked={task.completed}
              onChange={handleToggle}
              className="theme-checkbox h-5 w-5 mt-1 focus:ring-0"
              aria-describedby={`task-desc-${task.id}`}
            />
            <div className="ml-4 flex-1 min-w-0">
              <h3
                id={`task-title-${task.id}`}
                className={`task-title font-medium ${task.completed ? 'line-through text-text-secondary' : 'text-text-primary'}`}
              >
                {task.title}
              </h3>
              {task.description && (
                <p
                  id={`task-desc-${task.id}`}
                  className={`task-description mt-1 text-sm ${task.completed ? 'text-text-secondary' : 'text-text-secondary'}`}
                >
                  {task.description}
                </p>
              )}
              <div className="mt-2 flex items-center text-xs text-text-secondary">
                <span className="task-date">Created: {new Date(task.createdAt).toLocaleDateString()}</span>
                {task.updatedAt !== task.createdAt && (
                  <span className="task-date ml-2">Updated: {new Date(task.updatedAt).toLocaleDateString()}</span>
                )}
              </div>
            </div>
            <div className="flex space-x-2">
              <EditButton
                onClick={handleEdit}
                aria-label={`Edit task: ${task.title}`}
                size="sm"
                className="opacity-80 hover:opacity-100 transition-opacity"
              >
                <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4" viewBox="0 0 20 20" fill="currentColor">
                  <path d="M13.586 3.586a2 2 0 112.828 2.828l-.793.793-2.828-2.828.793-.793zM11.379 5.793L3 14.172V17h2.828l8.38-8.379-2.83-2.828z" />
                </svg>
              </EditButton>
              <DeleteButton
                onClick={handleDelete}
                aria-label={`Delete task: ${task.title}`}
                size="sm"
                className="opacity-80 hover:opacity-100 transition-opacity"
              >
                <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4" viewBox="0 0 20 20" fill="currentColor">
                  <path
                    fillRule="evenodd"
                    d="M9 2a1 1 0 00-.894.553L7.382 4H4a1 1 0 000 2v10a2 2 0 002 2h8a2 2 0 002-2V6a1 1 0 100-2h-3.382l-.724-1.447A1 1 0 0011 2H9zM7 8a1 1 0 012 0v6a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v6a1 1 0 102 0V8a1 1 0 00-1-1z"
                    clipRule="evenodd"
                  />
                </svg>
              </DeleteButton>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default TaskCard; 
