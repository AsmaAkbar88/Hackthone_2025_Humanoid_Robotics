'use client';

import React from 'react';
import { useRouter, usePathname } from 'next/navigation';
import { useAuth } from '@/hooks/useAuth'; // Use the hook instead of importing context directly

const ProtectedRoute = ({ children }) => {
  const { state } = useAuth();
  const { isAuthenticated, loading } = state;
  const router = useRouter();
  const pathname = usePathname();

  // While loading, show a loading indicator
  if (loading) {
    return (
      <div className="flex justify-center items-center h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-gray-900"></div>
      </div>
    );
  }

  // If not authenticated, redirect to login
  if (!isAuthenticated) {
    // Redirect to login with the current path as a query parameter
    router.push(`/login?redirect=${encodeURIComponent(pathname)}`);
    return null; // Render nothing while redirecting
  }

  // If authenticated, render the protected content
  return <>{children}</>;
};

export default ProtectedRoute;