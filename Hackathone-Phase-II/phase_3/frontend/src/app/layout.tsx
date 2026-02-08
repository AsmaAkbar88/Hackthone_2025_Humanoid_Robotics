import '../styles/globals.css';
import type { Metadata } from 'next';
import AppProviders from '@/providers/AppProviders';

export const metadata: Metadata = {
  title: 'Todo App',
  description: 'A simple todo application',
  icons: {
    icon: '/favicon.svg',
  },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>
        <AppProviders> 
          <div className="bg-pink-100 py-8 px-4" >{children}</div>
          
        </AppProviders>
      </body>
    </html>
  );
}
