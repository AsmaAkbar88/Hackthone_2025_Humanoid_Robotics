// src/components/ui/Header.tsx
import React from 'react';
import Link from 'next/link';
import { useAuth } from '@/hooks/useAuth';
import { useTheme } from '@/context/ThemeContext';
import ThemeToggle from './ThemeToggle';
import Button from './Button';

const Header: React.FC = () => {
  const { state: authState, logout } = useAuth();
  const { theme } = useTheme();

  const handleLogout = async () => {
    try {
      await logout();
    } catch (error) {
      console.error('Logout error:', error);
    }
  };

  return (
    <header className="bg-bg-secondary shadow-sm border-b border-border-color">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          <div className="flex items-center">
            <Link href="/" className="flex-shrink-0 flex items-center">
              <span className="text-xl font-bold text-accent-primary text-h3">Todo App</span>
            </Link>
          </div>
          <div className="flex items-center space-x-4">
            {/* Theme Toggle */}
            <div className="flex items-center">
              <ThemeToggle />
            </div>

            {authState.isAuthenticated ? (
              <>
                <span className="text-text-primary hidden md:inline">Welcome, {authState.user?.name || authState.user?.email}</span>
                <Button
                  onClick={handleLogout}
                  variant="primary"
                  className="ml-4 bg-white"
                >
                  Logout
                </Button>
              </>
            ) : (
              <>
                <Link
                  href="/login"
                  className="px-4 py-2 text-sm font-medium text-text-primary bg-bg-secondary border border-border-color rounded-md hover:bg-[color-mix(in_srgb,theme(colors.white)_85%,theme(colors.gray.200))] focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-accent-primary"
                >
                  Sign In
                </Link>
                <Link
                  href="/signup"
                  className="ml-2 px-4 py-2 text-sm font-medium text-white bg-accent-primary rounded-md hover:bg-[color-mix(in_srgb,theme(colors.light.primary)_85%,transparent)] focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-accent-primary shadow-sm"
                >
                  Sign Up
                </Link>
              </>
            )}
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;