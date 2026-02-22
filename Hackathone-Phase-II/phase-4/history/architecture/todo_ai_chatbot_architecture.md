# Todo AI Chatbot - Project Architecture Documentation

## Overview
The Todo AI Chatbot is a full-stack application that combines a traditional todo management system with an AI-powered conversational interface. Users can manage their tasks using natural language commands through an AI assistant that leverages MCP (Model Context Protocol) tools.

## Technology Stack
- **Backend**: Python 3.11, FastAPI, SQLModel, PostgreSQL/Neon
- **Frontend**: Next.js 16, React 19, TypeScript, Tailwind CSS
- **AI Integration**: OpenAI Agents SDK, MCP SDK
- **Authentication**: JWT-based authentication
- **Database**: PostgreSQL (with Neon for serverless)

## Backend Architecture

### 1. Models Layer
- **Task Model**: Represents individual tasks with title, description, completion status, and user association
- **User Model**: Stores user information including email, password (hashed), name, and date of birth
- **Conversation Model**: Tracks AI conversation threads between users and the AI assistant
- **Message Model**: Stores individual messages within conversations with role (user/assistant) and content

### 2. Services Layer
- **TaskService**: Handles all task-related operations (CRUD) with proper user authorization
- **ConversationService**: Manages conversations and associated messages
- **AuthService**: Handles user authentication, registration, and session management
- **AIService**: Implements MCP tools for AI interactions with the task system

### 3. Database Layer
- Uses SQLModel for ORM operations
- Async SQLAlchemy sessions for database connectivity
- PostgreSQL/Neon for persistent storage
- Migration scripts for schema management

### 4. API Layer
- FastAPI with proper routing and middleware
- Authentication middleware for protected endpoints
- Chat endpoint supporting conversation history
- Task management endpoints with proper validation

### 5. AI/MCP Integration
- OpenAI Agents SDK for natural language processing
- MCP (Model Context Protocol) server implementation
- Five core MCP tools:
  - `add_task`: Create new tasks
  - `list_tasks`: Retrieve tasks with filtering options
  - `complete_task`: Mark tasks as complete/incomplete
  - `delete_task`: Remove tasks
  - `update_task`: Modify task properties

## Frontend Architecture

### 1. UI Components
- **Task Cards**: Visual representation of individual tasks
- **Task Forms**: Creation and editing interfaces
- **Chat Interface**: Conversational UI for AI interactions
- **Authentication Forms**: Login and signup components

### 2. State Management
- Context API for authentication state management
- Context API for task management state
- Custom hooks for encapsulating business logic
- Proper error handling and loading states

### 3. Service Layer
- API client using Axios with interceptors
- Authentication service with token management
- Task service with CRUD operations
- Chat service for conversation management

### 4. Pages
- **Home Page**: Entry point with login/signup options
- **Login/Signup Pages**: Authentication flows
- **Dashboard**: Traditional task management interface
- **Chat Page**: AI-powered task management interface

## Key Features

### 1. Authentication System
- JWT-based authentication with proper token lifecycle
- User registration with validation
- Protected routes and authorization checks
- Secure password handling with hashing

### 2. Task Management
- Complete CRUD operations for tasks
- Filtering capabilities (all, active, completed)
- User data isolation to prevent cross-user access
- Persistent task state in database

### 3. AI Chat Interface
- Natural language processing for task management
- MCP tools integration for secure AI actions
- Conversation history persistence
- Context-aware responses from the AI assistant

### 4. Security Measures
- User data isolation through proper authorization checks
- Input validation and sanitization
- Secure password storage with bcrypt
- JWT token validation and expiration

## Architecture Patterns

### 1. Stateless Design
- All application state is persisted to the database
- No in-memory state retention between requests
- Scalable architecture that supports horizontal scaling

### 2. Separation of Concerns
- Clear distinction between presentation, business logic, and data layers
- Dedicated services for specific functionality
- Proper API design with consistent response formats

### 3. MCP-First Design
- All AI actions go through standardized MCP tools
- Ensures proper authorization and validation for all operations
- Maintains security boundaries between AI and data

## Data Flow

### Task Creation via AI
1. User sends natural language command to AI assistant
2. AI processes the command and identifies intent to create a task
3. AI calls the `add_task` MCP tool with extracted parameters
4. MCP tool validates user authorization and creates the task
5. Response is returned to the AI assistant
6. AI assistant responds to the user with confirmation

### Traditional Task Management
1. User interacts with UI components in the dashboard
2. Frontend calls appropriate API endpoints
3. Backend validates user authorization
4. Backend performs requested operation on the database
5. Response is returned to the frontend
6. UI updates to reflect the changes

## Security Considerations

### 1. Authentication
- All API endpoints require valid JWT tokens
- User ID validation to prevent unauthorized access
- Token expiration and refresh mechanisms

### 2. Authorization
- Each operation verifies the user owns the requested resource
- Database queries include user ID filters
- MCP tools validate user permissions before executing actions

### 3. Data Validation
- Input validation at both frontend and backend
- SQL injection prevention through parameterized queries
- Proper error handling without information disclosure

## Deployment Considerations

### Backend
- Containerizable with Docker
- Environment variable configuration
- Database connection pooling
- Proper logging and monitoring

### Frontend
- Static asset optimization
- Client-side caching strategies
- Environment-specific API endpoint configuration
- Bundle size optimization

## Future Enhancements

### 1. AI Capabilities
- Enhanced natural language understanding
- Contextual conversation memory
- Advanced task management operations

### 2. Performance
- Caching strategies for improved response times
- Database query optimization
- Frontend performance enhancements

### 3. Security
- Rate limiting for API endpoints
- Enhanced input validation
- Additional authentication factors

This architecture provides a solid foundation for an AI-powered task management system with proper security, scalability, and maintainability considerations.