// src/components/ui/TaskForm.tsx
import React, { useState } from 'react';
import { useForm } from 'react-hook-form';
import { Task } from '@/services/task-service';
import Button from './Button';
import EditButton from './EditButton';

interface TaskFormProps {
  initialData?: Partial<Task>;
  onSubmit: (data: { title: string; description?: string }) => void;
  onCancel?: () => void;
  submitText?: string;
  cancelText?: string;
}

interface FormData {
  title: string;
  description?: string;
}

const TaskForm: React.FC<TaskFormProps> = ({
  initialData,
  onSubmit,
  onCancel,
  submitText = 'Save Task',
  cancelText = 'Cancel',
}) => {
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
    reset,
  } = useForm<FormData>({
    defaultValues: {
      title: initialData?.title || '',
      description: initialData?.description || '',
    },
  });

  const [isExpanded, setIsExpanded] = useState(!!initialData?.description);

  const toggleExpand = () => {
    setIsExpanded(!isExpanded);
  };

  const onSubmitHandler = async (data: FormData) => {
    try {
      await onSubmit(data);
      reset();
      if (!initialData) {
        setIsExpanded(false);
      }
    } catch (error) {
      console.error('Error submitting task:', error);
    }
  };

  return (
    <form onSubmit={handleSubmit(onSubmitHandler)} className="space-y-4">
      <div>
        <label htmlFor="title" className="block text-sm font-medium text-text-primary text-body-md">
          Title *
        </label>
        <div className="mt-1">
          <input
            id="title"
            {...register('title', { required: 'Title is required', minLength: { value: 1, message: 'Title cannot be empty' } })}
            className={`block w-full px-3 py-2 border ${
              errors.title ? 'border-red-300' : 'border-border-color'
            } rounded-md shadow-sm focus:outline-none focus:border-black focus:border-accent-primary sm:text-sm theme-input bg-bg-primary text-text-primary`}
            placeholder="Task title"
          />
          {errors.title && (
            <p className="mt-1 text-sm text-red-600">{errors.title.message}</p>
          )}
        </div>
      </div>

      <div>
        <div className="flex items-center ">
          <label htmlFor="description" className=" block text-sm font-medium text-text-primary mr-8 text-body-md">
            Description
          </label>
          <EditButton
            type="button"
            onClick={toggleExpand}
            className="text-sm hover:bg-pink-400 shadow-md "
          >
            {isExpanded ? 'Hide' : 'Show'} description
          </EditButton>
        </div>
        {isExpanded && (
          <div className="mt-1">
            <textarea
              id="description"
              {...register('description')}
              rows={3}
              className="shadow-sm focus:ring-0 focus:border-black focus:outline-none mt-1 block w-full sm:text-sm border border-border-color rounded-md p-2 theme-input bg-bg-primary text-text-primary"
              placeholder="Task description (optional)"
            />
          </div>
        )}
      </div>

      <div className="flex space-x-3 pt-2 ">
        <Button
          type="submit"
          disabled={isSubmitting}
          variant="primary"
        >
          {isSubmitting ? 'Saving...' : submitText}
        </Button>
        <div className=' hover:bg-pink-400'>
        {onCancel && (
          <Button
            type="button"
            variant="outline"
            onClick={onCancel}
          >
            {cancelText}
          </Button>
        )}
        </div>
      </div>
    </form>
  );
};

export default TaskForm;