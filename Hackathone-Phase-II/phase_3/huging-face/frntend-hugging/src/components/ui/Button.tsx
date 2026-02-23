import React from 'react';

export interface ButtonProps {
  children: React.ReactNode;
  variant?: 'primary' | 'secondary' | 'danger' | 'success' | 'outline' | 'ghost';
  size?: 'sm' | 'md' | 'lg';
  onClick?: () => void;
  disabled?: boolean;
  className?: string;
  type?: 'button' | 'submit' | 'reset';
}

const Button: React.FC<ButtonProps> = ({
  children,
  variant = 'primary',
  size = 'md',
  onClick,
  disabled = false,
  className = '',
  type = 'button',
}) => {
  // Base classes for all buttons
  const baseClasses = 'inline-flex items-center justify-center rounded-md font-medium transition-all duration-200 ease-in-out focus:outline-none focus:ring-2 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed';

  // Size classes
  const sizeClasses = {
    sm: 'text-xs px-3 py-1.5',
    md: 'text-sm px-4 py-2',
    lg: 'text-base px-6 py-3',
  };

  // Variant classes
  const variantClasses = {
    primary: 'bg-accent-primary border border-border-color text-black dark:text-text-primary hover:bg-[color-mix(in_srgb,theme(colors.light.primary)_85%,transparent)] focus:ring-accent-primary rounded-md shadow-md',
    secondary: 'bg-bg-primary text-text-primary border border-border-color hover:bg-[color-mix(in_srgb,theme(colors.white)_85%,theme(colors.gray.200))] focus:ring-accent-primary',
    danger: 'bg-red-600 text-white hover:bg-red-700 focus:ring-red-500',
    success: 'bg-green-600 text-black hover:bg-green-700 focus:ring-green-500',
    outline: 'border border-border-color text-text-primary bg-transparent hover:bg-bg-secondary focus:ring-accent-primary',
    ghost: 'bg-transparent text-text-primary hover:bg-bg-secondary focus:ring-accent-primary',
  };

  const classes = `${baseClasses} ${sizeClasses[size]} ${variantClasses[variant]} ${className}`;

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

export default Button;