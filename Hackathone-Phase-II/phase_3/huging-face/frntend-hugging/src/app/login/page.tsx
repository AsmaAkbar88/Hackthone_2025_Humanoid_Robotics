'use client';

import { useRouter } from 'next/navigation';
import Link from 'next/link';
import LoginForm from '@/components/auth/LoginForm';
import Notification from '@/components/ui/Notification';

export default function LoginPage() {
  const router = useRouter();

  const handleLoginSuccess = () => {
    router.push('/dashboard');
  };

  return (
    <div className="min-h-screen bg-pink-100  flex flex-col justify-center py-12 sm:px-6 lg:px-8">
      <div className="sm:mx-auto sm:w-full sm:max-w-md">
        <div className="flex justify-center">
          <div className="bg-pink-200 rounded-full p-3">
            <svg xmlns="http://www.w3.org/2000/svg" className="h-12 w-12 text-pink-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
            </svg>
          </div>
        </div>
        <h2 className="mt-6 text-center text-3xl font-extrabold text-gray-900">
          Welcome Back
        </h2>
        <p className="mt-2 text-center text-sm text-black-600">
          Sign in to your account to continue
        </p>
      </div>

      <div className="mt-8 sm:mx-auto sm:w-full sm:max-w-md">
        <div className="bg-white py-8 px-6 shadow-xl sm:rounded-2xl sm:px-10 border border-pink-100">
          <LoginForm onSuccess={handleLoginSuccess} />

          <div className="mt-6 text-sm text-center space-y-3">
            <div className="border-t border-gray-200 pt-4">
              <Link href="/signup" className="font-medium text-black hover:text-pink-500 inline-flex items-center">
                Don't have an account?
                <span className="ml-1 border border-grey-300 text-blackunderline underline">Sign up</span>
              </Link>
            </div>
            <div>
              <Link href="/forgot-password" className="font-medium text-black hover:text-pink-500 inline-flex items-center">
                <span className="underline">Forgot your password?</span>
              </Link>
            </div>
          </div>
        </div>
      </div>
      <Notification />
    </div>
  );
}