// src/components/auth/LoginForm.tsx
'use client';

import React, { useState } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/hooks/useAuth';
import { useNotifications } from '@/hooks/useNotifications';
import Button from '@/components/ui/Button';

interface LoginFormProps {
  onSuccess?: () => void;
}

const LoginForm: React.FC<LoginFormProps> = ({ onSuccess }) => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const router = useRouter();
  const { login } = useAuth();
  const { showError, showSuccess } = useNotifications();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const user = await login(email, password);
      showSuccess(`Welcome back, ${user.name || user.email.split('@')[0]}!`);

      if (onSuccess) {
        onSuccess();
      } else {
        router.push('/dashboard');
      }
    } catch (error: any) {
      let errorMessage = 'An error occurred during login.';

      // Handle specific error responses from the backend
      if (error.response?.data?.message) {
        errorMessage = error.response.data.message;
      } else if (error.response?.data?.error) {
        // Handle different error types from the backend
        const errorType = error.response.data.error;

        switch(errorType) {
          case 'EMAIL_NOT_FOUND':
            errorMessage = 'No account found with this email address. Please check your email and try again.';
            break;
          case 'INVALID_PASSWORD':
            errorMessage = 'Incorrect password. Please try again.';
            break;
          case 'AUTH_FAILED':
            errorMessage = 'Invalid email or password. Please check your credentials and try again.';
            break;
          default:
            errorMessage = error.response.data.message || 'Authentication failed. Please try again.';
        }
      } else if (error.message) {
        errorMessage = error.message;
      }

      setError(errorMessage);
      showError(errorMessage);
      console.error('Login error:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <form className="space-y-6" onSubmit={handleSubmit}>
      <div>
        <label htmlFor="email" className=" block text-sm font-medium text-text-primary text-body-md">
          Email address
        </label>
        <div className="mt-1">
          <input
            id="email"
            name="email"
            type="email"
            autoComplete="email"
            required
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            disabled={loading}
            className="block w-full px-3 py-2 border border-border-color rounded-md shadow-sm placeholder-text-secondary focus:outline-none focus:ring-accent-primary focus:border-black sm:text-sm disabled:opacity-50 bg-bg-primary text-text-primary"
          />
        </div>
      </div>

      <div>
        <label htmlFor="password" className="block text-sm font-medium text-text-primary text-body-md">
          Password
        </label>
        <div className="mt-1">
          <input
            id="password"
            name="password"
            type="password"
            autoComplete="current-password"
            required
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            disabled={loading}
            className="block w-full px-3 py-2 border border-border-color rounded-md shadow-sm placeholder-text-secondary focus:outline-none focus:ring-accent-primary focus:border-black sm:text-sm disabled:opacity-50 bg-bg-primary text-text-primary"
          />
        </div>
      </div>

      {error && (
        <div className="rounded-md bg-red-50 p-4 bg-[color-mix(in_srgb,theme(colors.red.100)_50%,theme(colors.red.500))]">
          <div className="flex">
            <div className="flex-shrink-0">
              <svg className="h-5 w-5 text-red-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
              </svg>
            </div>
            <div className="ml-3">
              <h3 className="text-sm font-medium text-red-800 text-text-primary">{error}</h3>
            </div>
          </div>
        </div>
      )}

      <div>
        <Button
          type="submit"
          variant="primary"
          className="w-full"
          disabled={loading}
        >
          {loading ? 'Signing in...' : 'Sign in'}
        </Button>
      </div>
    </form>
  );
};

export default LoginForm;