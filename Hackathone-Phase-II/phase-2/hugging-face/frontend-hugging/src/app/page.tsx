import Link from 'next/link';
import MainLayout from '@/components/layout/MainLayout';

export default function HomePage() {
  return (
    <MainLayout>
      <div className="flex flex-col justify-center py-12 sm:px-6 lg:px-8 min-h-[calc(100vh-200px)]">
        <div className="mt-8 sm:mx-auto sm:w-full sm:max-w-md">
          <div className="bg-white py-8 px-4 shadow-lg sm:rounded-xl sm:px-10 border border-border-color">
            <h1 className="text-3xl font-bold text-center text-text-primary mb-8 text-h1">
              Welcome to Todo App
            </h1>
            <div className="space-y-4">
              <Link href="/login" className="w-full flex justify-center py-2 px-4 border border-border-color rounded-md shadow-md text-sm font-medium text-black bg-accent-primary hover:bg-[color-mix(in_srgb,theme(colors.light.primary)_75%,transparent)] focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-accent-primary transition-all duration-200">
                Sign In
              </Link>
              <Link href="/signup" className="w-full flex justify-center py-2 px-4 border border-border-color rounded-md shadow-md text-sm font-medium text-text-primary bg-bg-secondary hover:bg-[color-mix(in_srgb,theme(colors.light.primary)_75%,theme(colors.gray.200))] focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-accent-primary transition-all duration-200">
                Create Account
              </Link>
            </div>
          </div>
        </div>
      </div>
    </MainLayout>
  );
}
