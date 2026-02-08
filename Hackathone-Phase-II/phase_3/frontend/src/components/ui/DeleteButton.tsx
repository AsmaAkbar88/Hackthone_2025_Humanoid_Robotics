import React from 'react';
import Button, { ButtonProps } from './Button';

const DeleteButton: React.FC<Omit<ButtonProps, 'variant'>> = ({
  children,
  size = 'md',
  onClick,
  disabled = false,
  className = '',
  type = 'button',
}) => {
  // Base classes for delete button with danger styling
  const baseClasses = 'inline-flex items-center justify-center rounded-md font-medium transition-all duration-200 ease-in-out focus:outline-none focus:ring-2 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transform hover:scale-105';

  // Size classes
  const sizeClasses = {
    sm: 'text-xs px-3 py-1.5',
    md: 'text-sm px-4 py-2',
    lg: 'text-base px-6 py-3',
  };

  // Danger variant classes
  const dangerClasses = 'bg-red-600 text-white hover:bg-red-700 focus:ring-red-500 shadow-md';

  const classes = `${baseClasses} ${sizeClasses[size]} ${dangerClasses} ${className}`;

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

export default DeleteButton;