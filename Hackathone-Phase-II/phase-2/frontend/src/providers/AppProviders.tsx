// src/providers/AppProviders.tsx
'use client';

import React from 'react';
import { AuthProvider } from '@/context/AuthContext';
import { TasksProvider } from '@/context/TasksContext';
import { ThemeProvider } from '@/context/ThemeContext';

interface AppProvidersProps {
  children: React.ReactNode;
}

const AppProviders: React.FC<AppProvidersProps> = ({ children }) => {
  return (
    <ThemeProvider>
      <AuthProvider>
        <TasksProvider>
          {children}
        </TasksProvider>
      </AuthProvider>
    </ThemeProvider>
  );
};

export default AppProviders;