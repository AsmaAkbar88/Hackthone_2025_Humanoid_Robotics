'use client';

import { useRouter } from 'next/navigation';
import Link from 'next/link';
import SignupForm from '@/components/auth/SignupForm';
import Notification from '@/components/ui/Notification';

export default function SignupPage() {
  const router = useRouter();

  const handleSignupSuccess = () => {
    router.push('/dashboard');
  };

  return (
    <div className="min-h-screen bg-pink-100  flex flex-col justify-center py-12 sm:px-6 lg:px-8">
      <div className="sm:mx-auto sm:w-full sm:max-w-md">
        <div className="flex justify-center">
          <div className="bg-[var(--primary-100)] rounded-full p-3">
            <svg xmlns="http://www.w3.org/2000/svg" className="h-12 w-12 text-[var(--primary-500)]" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M18 9v3m0 0v3m0-3h3m-3 0h-3m-2-5a4 4 0 11-8 0 4 4 0 018 0zM3 20a6 6 0 0112 0v1H3v-1z" />
            </svg>
          </div>
        </div>
        <h2 className="mt-6 text-center text-3xl font-extrabold text-[var(--text-primary)]">
          Create Your Account
        </h2>
        <p className="mt-2 text-center text-sm text-[var(--text-secondary)]">
          Join us today and start managing your tasks efficiently
        </p>
      </div>

      <div className="mt-8 sm:mx-auto sm:w-full sm:max-w-md">
        <div className=" bg-white bg-[var(--bg-card)] py-8 px-6 shadow-xl sm:rounded-2xl sm:px-10 border border-[var(--primary-100)] theme-card">
          <SignupForm onSuccess={handleSignupSuccess} />

          <div className="mt-6 text-sm text-cente">
            <div className="border-t border-[var(--border-secondary)] pt-4">
              <Link href="/login" className="font-medium hover:text-pink-500 text-[var(--text-link)] hover:text-[var(--primary-700)] inline-flex items-center theme-link">
                Already have an account?
                <span className="ml-1 underline">Sign in</span>
              </Link>
            </div>
          </div>
        </div>
      </div>
      <Notification />
    </div>
  );
}