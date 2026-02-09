import React from 'react';

export interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  error?: string;
  helperText?: string;
  variant?: 'default' | 'outlined' | 'filled';
  inputSize?: 'sm' | 'md' | 'lg';
}

const Input: React.FC<InputProps> = ({
  label,
  error,
  helperText,
  variant = 'default',
  inputSize = 'md',
  className = '',
  ...props
}) => {
  // Size classes
  const sizeClasses = {
    sm: 'px-2 py-1 text-sm',
    md: 'px-3 py-2 text-sm',
    lg: 'px-4 py-3 text-base',
  };

  // Variant classes
  const variantClasses = {
    default: 'border border-border-color rounded-md shadow-sm focus:ring-accent-primary focus:border-accent-primary',
    outlined: 'border border-border-color rounded-md focus:ring-accent-primary focus:border-accent-primary',
    filled: 'bg-bg-secondary border border-transparent rounded-md focus:ring-accent-primary focus:border-accent-primary',
  };

  const inputClasses = `
    block w-full
    ${sizeClasses[inputSize]}
    ${variantClasses[variant]}
    bg-bg-primary text-text-primary
    placeholder-text-secondary
    focus:outline-none
    ${error ? 'border-red-500' : ''}
    ${className}
  `;

  return (
    <div className="w-full">
      {label && (
        <label className="block text-sm font-medium text-text-primary mb-1 text-body-md">
          {label}
        </label>
      )}
      <input
        className={inputClasses}
        {...props}
      />
      {helperText && !error && (
        <p className="mt-1 text-sm text-text-secondary">{helperText}</p>
      )}
      {error && (
        <p className="mt-1 text-sm text-red-600">{error}</p>
      )}
    </div>
  );
};

export default Input;