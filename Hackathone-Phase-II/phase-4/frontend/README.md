# Todo Frontend UI

A responsive Todo web application frontend built with Next.js, TypeScript, and Tailwind CSS.

## Features

- User authentication with secure login and signup
- Create, read, update, and delete tasks
- Task completion toggling
- Task filtering (all, active, completed)
- Responsive design for desktop, tablet, and mobile
- Real-time notifications
- Loading states and error handling
- Accessibility compliant (WCAG AA standards)

## Tech Stack

- **Framework**: Next.js 16+ with App Router
- **Language**: TypeScript 5+
- **Styling**: Tailwind CSS
- **Authentication**: Better Auth
- **State Management**: React Context API
- **UI Components**: Custom components with Tailwind CSS
- **Forms**: React Hook Form
- **Notifications**: React Hot Toast

## Project Structure

```
frontend/
├── public/                 # Static assets
├── src/
│   ├── app/               # Next.js App Router pages
│   │   ├── layout.tsx     # Root layout
│   │   ├── page.tsx       # Home page
│   │   ├── login/page.tsx # Login page
│   │   ├── signup/page.tsx # Signup page
│   │   └── dashboard/
│   │       └── page.tsx   # Task dashboard
│   ├── components/        # Reusable UI components
│   │   ├── ui/           # Generic UI components
│   │   └── auth/         # Authentication components
│   ├── context/           # React Context providers
│   ├── hooks/             # Custom React hooks
│   ├── providers/         # App-wide providers
│   ├── services/          # API and business logic
│   └── styles/            # Global styles
└── tests/                 # Test files
```

## Environment Variables

Create a `.env.local` file in the project root:

```env
NEXT_PUBLIC_API_BASE_URL=http://todo-chatbot-backend:8000/api
NEXT_PUBLIC_BETTER_AUTH_URL=http://todo-chatbot-backend:8000
NEXT_PUBLIC_APP_NAME=Todo App
```

## Getting Started

1. Install dependencies:
   ```bash
   npm install
   ```

2. Run the development server:
   ```bash
   npm run dev
   ```

3. Open [http://localhost:3000](http://localhost:3000) in your browser during development, or access via the Kubernetes service in production.

## Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run start` - Start production server
- `npm run lint` - Run linter

## API Integration

The frontend communicates with the backend API following these contracts:

- Authentication endpoints: `/api/auth/login`, `/api/auth/register`
- Task endpoints: `/api/tasks`, `/api/tasks/:id`, `/api/tasks/:id/toggle`
- All requests include JWT tokens automatically via the API client

## Testing

Run the tests with:

```bash
npm test
```

Unit tests are located in `tests/unit/`, integration tests in `tests/integration/`, and end-to-end tests in `tests/e2e/`.

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request