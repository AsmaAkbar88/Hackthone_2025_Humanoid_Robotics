# Quickstart Guide: Todo Frontend UI

## Overview
This guide provides instructions for setting up and running the Todo Frontend UI locally.

## Prerequisites
- Node.js 18+ (or 20+)
- npm or yarn package manager
- Access to the backend API (from Todo Backend API implementation)
- Environment variables configured

## Setup Instructions

### 1. Clone and Navigate
```bash
git clone <repository-url>
cd <repository-directory>
# Navigate to frontend directory if needed
```

### 2. Install Dependencies
```bash
# Using npm
npm install

# Or using yarn
yarn install
```

### 3. Environment Configuration
Create a `.env.local` file in the project root:
```env
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000/api
NEXT_PUBLIC_BETTER_AUTH_URL=http://localhost:8000
NEXT_PUBLIC_APP_NAME=Todo App
```

### 4. Run the Application
```bash
# Development mode with hot reloading
npm run dev
# or
yarn dev
```

The application will be available at `http://localhost:3000`

## Key Components

### Project Structure
```
frontend/
├── public/                 # Static assets
├── src/
│   ├── app/               # Next.js App Router pages
│   │   ├── layout.tsx     # Root layout
│   │   ├── page.tsx       # Home page
│   │   ├── login/page.tsx # Login page
│   │   └── dashboard/
│   │       └── page.tsx   # Task dashboard
│   ├── components/        # Reusable UI components
│   │   ├── ui/           # Generic UI components
│   │   └── auth/         # Authentication components
│   ├── services/          # API and business logic
│   │   ├── api-client.ts # API client with JWT handling
│   │   └── auth-service.ts # Authentication service
│   ├── hooks/             # Custom React hooks
│   │   ├── useAuth.ts    # Authentication state
│   │   └── useTasks.ts   # Task management
│   └── styles/            # Styling
│       └── globals.css    # Global styles
└── tests/                 # Test files
```

### Authentication
The application uses Better Auth for authentication. Key features:
- Secure JWT token management
- Automatic token inclusion in API requests
- Session management
- Protected routes

### API Integration
- All API calls include JWT tokens automatically
- Standardized response format handling
- Error handling and notifications
- Loading states management

### State Management
- React Context for global state (auth, tasks)
- Custom hooks for specific state logic
- Proper separation of concerns

## Development

### Adding New Pages
1. Create new page in `src/app/` directory following Next.js App Router conventions
2. Add necessary layout and component imports
3. Implement proper loading and error states

### Adding New Components
1. Create component in `src/components/ui/` for reusable components
2. Use appropriate TypeScript interfaces
3. Implement proper accessibility attributes
4. Add tests for new components

### API Service Integration
1. Add new endpoints to `src/services/api-client.ts`
2. Implement proper error handling
3. Update TypeScript types as needed
4. Add loading/error states to UI

## Testing

### Running Tests
```bash
# Run all tests
npm test

# Run unit tests
npm run test:unit

# Run integration tests
npm run test:integration

# Run end-to-end tests
npm run test:e2e
```

### Test Structure
- Unit tests in `tests/unit/` for components and services
- Integration tests in `tests/integration/` for API integration
- E2E tests in `tests/e2e/` for full user flows

## Build and Deployment

### Build for Production
```bash
npm run build
```

### Run Production Build
```bash
npm start
```

## Troubleshooting

### Common Issues
1. **API Connection Errors**: Verify backend API is running and URL is correct in environment variables
2. **Authentication Issues**: Check that Better Auth is properly configured and running
3. **Styling Problems**: Ensure Tailwind CSS is properly configured
4. **TypeScript Errors**: Run `npm run type-check` to identify issues

### Environment Variables
- `NEXT_PUBLIC_API_BASE_URL`: Backend API base URL
- `NEXT_PUBLIC_BETTER_AUTH_URL`: Better Auth instance URL
- `NEXT_PUBLIC_APP_NAME`: Application name for display

### Debugging Tips
- Enable React DevTools for component inspection
- Use browser network tab to inspect API requests
- Check console for error messages and warnings
- Use Next.js built-in error overlay for development

## Next Steps
1. Customize UI components to match design requirements
2. Add additional pages and features as needed
3. Implement more comprehensive error handling
4. Add accessibility enhancements
5. Optimize performance for production