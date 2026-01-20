import React from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { useAuth } from '@/hooks/useAuth';

const Navigation: React.FC = () => {
  const pathname = usePathname();
  const { state: authState } = useAuth();

  // Navigation items for authenticated users
  const authenticatedNavItems = [
    { name: 'Dashboard', href: '/dashboard' },
    { name: 'Profile', href: '/profile' },
  ];

  // Navigation items for unauthenticated users
  const unauthenticatedNavItems = [
    { name: 'Home', href: '/' },
    { name: 'Login', href: '/login' },
    { name: 'Sign Up', href: '/signup' },
  ];

  const navItems = authState.isAuthenticated ? authenticatedNavItems : unauthenticatedNavItems;

  return (
    <nav className="bg-bg-secondary border-b border-border-color">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex h-16 items-center justify-between">
          <div className="flex items-center">
            <div className="flex-shrink-0">
              <Link href="/" className="text-xl font-bold text-accent-primary text-h3">
                Todo App
              </Link>
            </div>
            <div className="hidden md:block">
              <div className="ml-10 flex items-baseline space-x-4">
                {navItems.map((item) => (
                  <Link
                    key={item.name}
                    href={item.href}
                    className={`px-3 py-2 rounded-md text-sm font-medium ${
                      pathname === item.href
                        ? 'bg-accent-primary text-white'
                        : 'text-text-primary hover:bg-bg-secondary hover:text-text-primary'
                    } transition-colors duration-200`}
                  >
                    {item.name}
                  </Link>
                ))}
              </div>
            </div>
          </div>
          <div className="hidden md:block">
            <div className="ml-4 flex items-center md:ml-6">
              {authState.isAuthenticated && (
                <span className="text-text-primary mr-4 hidden md:inline">
                  Welcome, {authState.user?.name || authState.user?.email.split('@')[0]}
                </span>
              )}
            </div>
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navigation;