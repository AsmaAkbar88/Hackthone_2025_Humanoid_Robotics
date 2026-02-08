'use client';

import React from 'react';
import { useTheme } from '@/context/ThemeContext';
import Header from '@/components/ui/Header';

interface MainLayoutProps {
  children: React.ReactNode;
}

const MainLayout: React.FC<MainLayoutProps> = ({ children }) => {
  const { theme } = useTheme();

  return (
    <div className={`min-h-screen flex flex-col bg-bg-primary text-text-primary transition-colors duration-300`} data-theme={theme}>
      <Header />
      <main className="flex-grow container mx-auto px-4 py-6">
        {children}
      </main>
      <footer className="py-4 text-center text-text-secondary text-sm">
        © {new Date().getFullYear()} Todo App. All rights reserved.
      </footer>
    </div>
  );
};

export default MainLayout;