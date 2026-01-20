<!--
Sync Impact Report:
Version change: N/A -> 1.0.0
Modified principles: N/A (new constitution)
Added sections: Core Principles (6), Additional Constraints, Development Workflow
Removed sections: None
Templates requiring updates:
  - .specify/templates/plan-template.md ✅ updated (Constitution Check section)
  - .specify/templates/spec-template.md ✅ updated (Scope/Requirements alignment)
  - .specify/templates/tasks-template.md ✅ updated (Task categorization)
Templates not requiring updates: None
Follow-up TODOs: None
-->

# Phase II – Todo Full-Stack Web Application Constitution

## Core Principles

### User-Centric Design
Each user sees only their own tasks; security enforced via JWT tokens. This ensures data privacy and personalization for every user of the application.

### Accuracy and Specification Compliance
REST API endpoints match specifications exactly. All implementations must conform to the defined API contracts without deviation.

### Maintainability and Separation of Concerns
Clear separation of frontend (Next.js) and backend (FastAPI). Codebase must maintain clean architectural boundaries between client and server components.

### Security and JWT Authentication
JWT authentication ensures stateless, secure, token-based access. All authentication must be implemented using Better Auth JWT tokens with proper security practices.

### Performance and Optimization
Database queries optimized for Neon Serverless PostgreSQL. All database interactions must be efficient and follow best practices for performance.

### Responsive and Intuitive Frontend
Frontend must be fully responsive and intuitive across all device sizes. User experience must be consistent and accessible on desktop, tablet, and mobile.

### Spec-Driven Development
All development guided by Claude Code + Spec-Kit Plus workflow. Implementation must follow the established spec-driven development methodology.

## Technology Stack Constraints
Tech stack: Next.js 16+ (App Router), FastAPI, SQLModel, Neon PostgreSQL, Better Auth. No manual coding allowed: Implementation only via Claude Code + Spec-Kit Plus. Authentication must be JWT-based and stateless. Tasks filtered per authenticated user only. JWT secret shared via environment variable `BETTER_AUTH_SECRET`.

Additional requirements:
- RESTful API conforms to all listed endpoints and HTTP methods
- Authentication enforced on all endpoints using Better Auth JWT tokens
- Database schema designed with SQLModel and PostgreSQL best practices
- Frontend responsive on desktop, tablet, and mobile
- Codebase modular with separation of concerns (frontend/backend)
- Error handling implemented on API and frontend
- API returns proper HTTP status codes (200, 201, 401, 404, 500, etc.)

## Development Workflow and Quality Standards
All 5 basic level features fully implemented as web app. All API endpoints functional, secure, and tested. Frontend responsive and intuitive. Persistent storage working in Neon PostgreSQL. Authentication fully functional; unauthorized access blocked. Passes automated QA/spec verification using Spec-Kit Plus. All development follows the Claude Code + Spec-Kit Plus workflow with proper PHR (Prompt History Record) creation for every significant change.

## Governance

All implementations must comply with these constitutional principles. Changes to this constitution require proper documentation, approval, and migration planning. All pull requests and code reviews must verify compliance with these principles. Complexity must be justified against these core principles. Development teams must follow the guidance provided in the Claude Code documentation and Spec-Kit Plus workflows.

**Version**: 1.0.0 | **Ratified**: 2026-01-17 | **Last Amended**: 2026-01-17
