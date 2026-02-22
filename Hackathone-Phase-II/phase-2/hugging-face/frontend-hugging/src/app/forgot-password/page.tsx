'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import ForgotPasswordForm from '@/components/auth/ForgotPasswordForm';
import Notification from '@/components/ui/Notification';
import { useAuth } from '@/hooks/useAuth';
import { useNotifications } from '@/hooks/useNotifications';

export default function ForgotPasswordPage() {
  const [step, setStep] = useState<'verify' | 'reset'>('verify'); // verify or reset
  const [email, setEmail] = useState('');

  const handleVerificationSuccess = (verifiedEmail: string) => {
    setEmail(verifiedEmail);
    setStep('reset');
  };

  return (
    <div className="min-h-screen bg-[var(--bg-primary)] flex flex-col justify-center py-12 sm:px-6 lg:px-8">
      <div className="sm:mx-auto sm:w-full sm:max-w-md">
        <h2 className="mt-6 text-center text-3xl font-extrabold text-[var(--text-primary)]">
          {step === 'verify' ? 'Verify Your Identity' : 'Reset Your Password'}
        </h2>
        <p className="mt-2 text-center text-sm text-[var(--text-secondary)]">
          {step === 'verify'
            ? 'Enter your email and date of birth to verify your identity'
            : 'Enter your new password'}
        </p>
      </div>

      <div className="bg-white mt-8 sm:mx-auto sm:w-full sm:max-w-md">
        <div className="bg-[var(--bg-card)] py-8 px-4 shadow sm:rounded-lg sm:px-10 theme-card">
          {step === 'verify' ? (
            <ForgotPasswordForm onVerificationSuccess={handleVerificationSuccess} />
          ) : (
            <ResetPasswordForm email={email} />
          )}

          <div className="mt-4 text-sm text-center">
            <Link href="/login" className="w-full flex justify-center py-2 px-4 border border-grey-300 rounded-md shadow-lg text-sm font-medium text-black bg-[var(--btn-primary-bg)] hover:bg-pink-400 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-[var(--btn-primary-bg)] disabled:opacity-50 disabled:cursor-not-allowed">
              Back to login
            </Link>
          </div>
        </div>
      </div>
      <Notification />
    </div>
  );
}

// Separate component for password reset form
function ResetPasswordForm({ email }: { email: string }) {
  const [newPassword, setNewPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const { resetPassword } = useAuth();
  const { showError, showSuccess } = useNotifications();
  const router = useRouter();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');

    if (newPassword !== confirmPassword) {
      setError('Passwords do not match');
      return;
    }

    if (newPassword.length < 6) {
      setError('Password must be at least 6 characters long');
      return;
    }

    setLoading(true);

    try {
      await resetPassword({ email, newPassword });
      showSuccess('Password reset successfully! Please login with your new password.');
      // Redirect to login page after successful password reset
      setTimeout(() => {
        router.push('/login');
      }, 2000); // Wait 2 seconds to show success message before redirecting
    } catch (err: any) {
      const errorMessage = err.message || 'Failed to reset password. Please try again.';
      showError(errorMessage);
      console.error('Password reset error:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <form className="space-y-6" onSubmit={handleSubmit}>
      <div>
        <label htmlFor="email-display" className="block text-sm font-medium text-[var(--text-primary)]">
          Email
        </label>
        <div className="mt-1">
          <input
            id="email-display"
            name="email-display"
            type="email"
            readOnly
            value={email}
            className="appearance-none block w-full px-3 py-2 border border-[var(--border-secondary)] rounded-md shadow-sm placeholder-[var(--text-muted)] bg-[var(--secondary-100)] sm:text-sm theme-input"
          />
        </div>
      </div>

      <div>
        <label htmlFor="newPassword" className="block text-sm font-medium text-[var(--text-primary)]">
          New Password
        </label>
        <div className="mt-1">
          <input
            id="newPassword"
            name="newPassword"
            type="password"
            required
            value={newPassword}
            onChange={(e) => setNewPassword(e.target.value)}
            disabled={loading}
            className="appearance-none block w-full px-3 py-2  rounded-md shadow-sm placeholder-[var(--text-muted)] focus:outline-none border border-grey-300 focus:border-black focus:ring-0 focus:outline-none sm:text-sm disabled:opacity-50 theme-input"
          />
        </div>
      </div>

      <div>
        <label htmlFor="confirmPassword" className="block text-sm font-medium text-[var(--text-primary)]">
          Confirm New Password
        </label>
        <div className="mt-1">
          <input
            id="confirmPassword"
            name="confirmPassword"
            type="password"
            required
            value={confirmPassword}
            onChange={(e) => setConfirmPassword(e.target.value)}
            disabled={loading}
            className="appearance-none block w-full px-3 py-2  rounded-md shadow-sm placeholder-[var(--text-muted)] focus:outline-none border border-grey-300 focus:border-black focus:ring-0 focus:outline-none sm:text-sm disabled:opacity-50 theme-input"
          />
        </div>
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
          className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-lg text-sm font-medium text-black bg-[var(--btn-primary-bg)] hover:bg-pink-400 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-[var(--btn-primary-bg)] disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {loading ? 'Resetting password...' : 'Reset Password'}
        </button>
      </div>
    </form>
  );
}