// src/hooks/useNotifications.ts
import { useState, useCallback } from 'react';
import toast from 'react-hot-toast';

export interface Notification {
  id: string | number;
  type: 'success' | 'error' | 'warning' | 'info';
  message: string;
  duration?: number;
}

export const useNotifications = () => {
  const [notifications, setNotifications] = useState<Notification[]>([]);

  const showNotification = useCallback((notification: Omit<Notification, 'id'>) => {
    const id = Date.now(); // Simple ID generation
    const newNotification = { ...notification, id };

    setNotifications(prev => [...prev, newNotification]);

    // Auto-remove notification after duration
    setTimeout(() => {
      setNotifications(prev => prev.filter(n => n.id !== id));
    }, notification.duration || 3000);

    // Also show with toast library
    switch(notification.type) {
      case 'success':
        toast.success(notification.message);
        break;
      case 'error':
        toast.error(notification.message);
        break;
      case 'warning':
        toast(notification.message); // Default toast for warning
        break;
      case 'info':
        toast(notification.message); // Default toast for info
        break;
    }
  }, []);

  const hideNotification = useCallback((id: string | number) => {
    setNotifications(prev => prev.filter(notification => notification.id !== id));
  }, []);

  const showError = useCallback((message: string) => {
    showNotification({ type: 'error', message });
  }, [showNotification]);

  const showSuccess = useCallback((message: string) => {
    showNotification({ type: 'success', message });
  }, [showNotification]);

  const showInfo = useCallback((message: string) => {
    showNotification({ type: 'info', message });
  }, [showNotification]);

  const showWarning = useCallback((message: string) => {
    showNotification({ type: 'warning', message });
  }, [showNotification]);

  return {
    notifications,
    showNotification,
    hideNotification,
    showError,
    showSuccess,
    showInfo,
    showWarning,
  };
};