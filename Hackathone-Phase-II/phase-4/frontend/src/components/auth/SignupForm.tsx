// src/components/auth/SignupForm.tsx
'use client';

import React, { useState } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/hooks/useAuth';
import { useNotifications } from '@/hooks/useNotifications';
import Button from '@/components/ui/Button';

interface SignupFormProps {
  onSuccess?: () => void;
}

const SignupForm: React.FC<SignupFormProps> = ({ onSuccess }) => {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [dateOfBirth, setDateOfBirth] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const router = useRouter();
  const { register } = useAuth();
  const { showError, showSuccess } = useNotifications();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    // Frontend validation before submitting
    if (dateOfBirth) {
      // Check if date format is valid (YYYY-MM-DD)
      const dateRegex = /^\d{4}-\d{2}-\d{2}$/;
      if (!dateRegex.test(dateOfBirth)) {
        setError('Invalid date of birth format. Please use YYYY-MM-DD format.');
        showError('Invalid date of birth format. Please use YYYY-MM-DD format.');
        setLoading(false);
        return;
      }

      // Parse the date to ensure it's valid
      const dateObj = new Date(dateOfBirth);
      if (isNaN(dateObj.getTime())) {
        setError('Invalid date of birth. Please enter a valid date.');
        showError('Invalid date of birth. Please enter a valid date.');
        setLoading(false);
        return;
      }

      // Check if the date is reasonable (not in the future and not too far in the past)
      const today = new Date();
      const minDate = new Date('1900-01-01');
      if (dateObj > today || dateObj < minDate) {
        setError('Date of birth must be a realistic past date between 1900 and today.');
        showError('Date of birth must be a realistic past date between 1900 and today.');
        setLoading(false);
        return;
      }
    }

    try {
      // Prepare signup data with current date as signup_date
      const signupData = {
        name,
        email,
        password,
        date_of_birth: dateOfBirth,
        signup_date: new Date().toISOString() // Send signup date to backend
      };

      const user = await register(signupData.name, signupData.email, signupData.password, signupData.date_of_birth);
      showSuccess(`Account created successfully! Welcome, ${user.name || user.email.split('@')[0]}. You can now login.`);

      if (onSuccess) {
        onSuccess();
      } else {
        router.push('/login');
      }
    } catch (error: any) {
      let errorMessage = 'Registration failed. Please try again.';

      // Handle specific error responses from the backend
      if (error.response?.data?.message) {
        errorMessage = error.response.data.message;
      } else if (error.response?.data?.error) {
        // Handle different error types from the backend
        const errorType = error.response.data.error;

        switch(errorType) {
          case 'EMAIL_EXISTS':
            errorMessage = 'A user with this email already exists. Please use a different email address.';
            break;
          case 'INVALID_EMAIL_FORMAT':
            errorMessage = 'Invalid email address. Please check your email and try again.';
            break;
          case 'WEAK_PASSWORD':
            errorMessage = 'Password is too weak. Please use a stronger password.';
            break;
          case 'INVALID_SIGNUP_DATE':
            errorMessage = 'Invalid signup date provided. Please try again.';
            break;
          default:
            errorMessage = error.response.data.message || 'Registration failed. Please try again.';
        }
      } else if (error.message) {
        errorMessage = error.message;
      }

      setError(errorMessage);
      showError(errorMessage);
      console.error('Signup error:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <form className="space-y-6" onSubmit={handleSubmit}>
      <div>
        <label htmlFor="name" className="block text-sm font-medium text-text-primary text-body-md">
          Full Name
        </label>
        <div className="mt-1">
          <input
            id="name"
            name="name"
            type="text"
            required
            value={name}
            onChange={(e) => setName(e.target.value)}
            disabled={loading}
            className="block w-full px-3 py-2 border border-border-color rounded-md shadow-sm placeholder-text-secondary focus:outline-none focus:ring-accent-primary focus:border-black sm:text-sm disabled:opacity-50 bg-bg-primary text-text-primary"
          />
        </div>
      </div>

      <div>
        <label htmlFor="email" className="block text-sm font-medium text-text-primary text-body-md">
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
            autoComplete="new-password"
            required
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            disabled={loading}
            className="block w-full px-3 py-2 border border-border-color rounded-md shadow-sm placeholder-text-secondary focus:outline-none focus:border-black focus:border-black sm:text-sm disabled:opacity-50 bg-bg-primary text-text-primary"
          />
        </div>
      </div>

      <div>
        <label htmlFor="dateOfBirth" className="block text-sm font-medium text-text-primary text-body-md">
          Date of Birth
        </label>
        <div className="mt-1">
          <input
            id="dateOfBirth"
            name="dateOfBirth"
            type="date"
            required
            value={dateOfBirth}
            onChange={(e) => setDateOfBirth(e.target.value)}
            disabled={loading}
            className="block w-full px-3 py-2 border border-border-color rounded-md shadow-sm placeholder-text-secondary focus:outline-none focus:border-black focus:border-accent-primary sm:text-sm disabled:opacity-50 bg-bg-primary text-text-primary"
          />
        </div>
        <p className="mt-1 text-xs text-text-secondary">Format: YYYY-MM-DD</p>
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
          {loading ? 'Creating account...' : 'Sign up'}
        </Button>
      </div>
    </form>
  );
};

export default SignupForm;