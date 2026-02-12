// src/components/auth/ForgotPasswordForm.tsx
'use client';

import React, { useState } from 'react';
import { useNotifications } from '@/hooks/useNotifications';
import { authService } from '@/services/auth-service';

interface ForgotPasswordFormProps {
  onVerificationSuccess: (email: string) => void;
}

const ForgotPasswordForm: React.FC<ForgotPasswordFormProps> = ({ onVerificationSuccess }) => {
  const [email, setEmail] = useState('');
  const [dateOfBirth, setDateOfBirth] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const { showError, showSuccess } = useNotifications();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');

    setLoading(true);

    try {
      // Call the auth service to verify identity using email and date of birth
      const success = await authService.forgotPassword({ email, dateOfBirth });
      if (success) {
        showSuccess('Identity verified! Please set your new password.');
        onVerificationSuccess(email);
      }
    } catch (err: any) {
      const errorMessage = err.message || 'Verification failed. Please try again.';
      setError(errorMessage);
      showError(errorMessage);
      console.error('Forgot password error:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <form className="space-y-6" onSubmit={handleSubmit}>
      <div>
        <label htmlFor="email" className="block text-sm font-medium text-[var(--text-primary)]">
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
            className="appearance-none block w-full px-3 py-2 border border-grey-300 focus:border-black focus:ring-0 focus:outline-none rounded-md shadow-sm placeholder-[var(--text-muted)] focus:outline-none  sm:text-sm disabled:opacity-50 theme-input"
          />
        </div>
      </div>

      <div>
        <label htmlFor="dateOfBirth" className="block text-sm font-medium text-[var(--text-primary)]">
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
            className="appearance-none block w-full px-3 py-2  rounded-md shadow-sm placeholder-[var(--text-muted)] focus:outline-none border border-grey-300 focus:border-black focus:ring-0 focus:outline-none sm:text-sm disabled:opacity-50 theme-input"
          />
        </div>
        <p className="mt-1 text-xs text-[var(--text-muted)]">Enter the date of birth you used during registration</p>
      </div>

      {error && (
        <div className="rounded-md bg-red-50 p-4">
          <div className="text-sm text-red-700">{error}</div>
        </div>
      )}

      <div>
        <button
          type="submit"
          disabled={loading}
          className="w-full shadow-lg flex justify-center py-2 px-4 border border-grey-300 rounded-md  text-sm font-medium text-black bg-[var(--btn-primary-bg)] hover:bg-pink-400 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-[var(--btn-primary-bg)] disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {loading ? 'Verifying...' : 'Verify Identity'}
        </button>
      </div>
    </form>
  );
};

export default ForgotPasswordForm;