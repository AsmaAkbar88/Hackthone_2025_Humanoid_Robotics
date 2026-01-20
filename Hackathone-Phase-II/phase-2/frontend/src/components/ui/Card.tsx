import React from 'react';

interface CardProps {
  children: React.ReactNode;
  className?: string;
  title?: string;
  shadow?: 'sm' | 'md' | 'lg' | 'xl';
  rounded?: 'none' | 'sm' | 'md' | 'lg' | 'xl' | 'full';
}

const Card: React.FC<CardProps> = ({
  children,
  className = '',
  title,
  shadow = 'md',
  rounded = 'lg'
}) => {
  const shadowClasses = {
    sm: 'shadow-sm',
    md: 'shadow-md',
    lg: 'shadow-lg',
    xl: 'shadow-xl'
  };

  const roundedClasses = {
    none: 'rounded-none',
    sm: 'rounded-sm',
    md: 'rounded-md',
    lg: 'rounded-lg',
    xl: 'rounded-xl',
    full: 'rounded-full'
  };

  return (
    <div
      className={`bg-bg-secondary border border-border-color ${shadowClasses[shadow]} ${roundedClasses[rounded]} p-6 ${className}`}
    >
      {title && (
        <h3 className="text-lg font-medium text-text-primary mb-4 text-h3">{title}</h3>
      )}
      {children}
    </div>
  );
};

export default Card;