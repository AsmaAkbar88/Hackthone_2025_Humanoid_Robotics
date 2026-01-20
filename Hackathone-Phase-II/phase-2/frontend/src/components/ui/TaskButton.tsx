import React from 'react';
import Button, { ButtonProps } from './Button';

const TaskButton: React.FC<Omit<ButtonProps, 'variant'>> = ({
  children,
  size = 'md',
  onClick,
  disabled = false,
  className = '',
  type = 'button',
}) => {
  // Base classes for task button with premium non-danger styling
  const baseClasses = 'inline-flex items-center justify-center rounded-md font-medium transition-all duration-200 ease-in-out focus:outline-none focus:ring-2 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed hover:shadow-md';

  // Size classes
  const sizeClasses = {
    sm: 'text-xs px-3 py-1.5',
    md: 'text-sm px-4 py-2',
    lg: 'text-base px-6 py-3',
  };

  // Premium non-danger variant classes
  const taskClasses = 'bg-accent-primary text-black hover:bg-[color-mix(in_srgb,theme(colors.light.primary)_85%,transparent)] focus:ring-accent-primary';

  const classes = `${baseClasses} ${sizeClasses[size]} ${taskClasses} ${className}`;

  return (
    <button
      type={type}
      className={classes}
      onClick={onClick}
      disabled={disabled}
    >
      {children}
    </button>
  );
};

export default TaskButton;