// src/components/ui/Notification.tsx
import React, { useEffect } from 'react';
import { Toaster } from 'react-hot-toast';

interface NotificationProps {
  position?: 'top-left' | 'top-right' | 'bottom-left' | 'bottom-right' | 'top-center' | 'bottom-center';
}

const Notification: React.FC<NotificationProps> = ({
  position = 'top-right'
}) => {
  return (
    <Toaster
      position={position}
      toastOptions={{
        style: {
          fontSize: '14px',
        },
        success: {
          style: {
            background: 'var(--secondary-100)',
            color: 'var(--text-primary)',
            border: '1px solid var(--primary-200)',
          },
        },
        error: {
          style: {
            background: '#fee2e2',
            color: '#b91c1c',
          },
        },
        loading: {
          style: {
            background: 'var(--secondary-200)',
            color: 'var(--text-primary)',
          },
        },
      }}
    />
  );
};

export default Notification;