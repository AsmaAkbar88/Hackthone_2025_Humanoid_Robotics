'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import Header from '@/components/ui/Header';
import ChatInterface from '@/components/chat/ChatInterface';
import { useAuth } from '@/hooks/useAuth';
import { useNotifications } from '@/hooks/useNotifications';
import Notification from '@/components/ui/Notification';

export default function ChatPage() {
  const router = useRouter();
  const { state: authState } = useAuth();
  const { showError, showSuccess } = useNotifications();

  useEffect(() => {
    if (!authState.loading && !authState.isAuthenticated) {
      router.push('/login');
    }
  }, [authState.loading, authState.isAuthenticated, router]);

  if (authState.loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-lg">Loading...</div>
      </div>
    );
  }

  if (!authState.isAuthenticated) {
    return null; // Redirect is happening in useEffect
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <Header />

      <main className="max-w-4xl mx-auto py-6 sm:px-6 lg:px-8">
        <div className="px-4 py-6 sm:px-0">
          <div className="bg-white shadow-md overflow-hidden sm:rounded-lg p-6">
            <div className="mb-6">
              <h2 className="text-2xl font-bold text-gray-800">AI Task Assistant</h2>
              <p className="text-gray-600 mt-1">Manage your tasks using natural language commands</p>
            </div>

            <div className="h-[600px] flex flex-col">
              <ChatInterface />
            </div>
          </div>
        </div>
      </main>
      <Notification />
    </div>
  );
}