---
description: "Task list for Todo Web App Security implementation"
---

# Tasks: Todo Web App Security, Validation & Quality Assurance

**Input**: Design documents from `/specs/003-todo-security/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: The examples below include test tasks. Tests are OPTIONAL - only include them if explicitly requested in the feature specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `backend/src/`, `frontend/src/`

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Create backend directory structure: backend/src/models/, backend/src/services/, backend/src/api/, backend/src/middleware/
- [X] T002 Create frontend directory structure: frontend/src/components/, frontend/src/pages/, frontend/src/services/, frontend/src/utils/
- [X] T003 [P] Initialize backend with FastAPI, SQLModel, Better Auth dependencies in backend/requirements.txt
- [X] T004 [P] Initialize frontend with Next.js, React 19+, Better Auth dependencies in frontend/package.json

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T005 Setup JWT authentication middleware in backend/src/middleware/auth.py
- [X] T006 [P] Configure BETTER_AUTH_SECRET environment variable handling in backend/src/config.py
- [X] T007 [P] Create User model in backend/src/models/user.py
- [X] T008 Create Task model in backend/src/models/task.py with userId foreign key
- [X] T009 Create authentication service in backend/src/services/auth_service.py
- [X] T010 Create task authorization service in backend/src/services/task_service.py
- [X] T011 Configure database connection with Neon PostgreSQL in backend/src/database.py
- [X] T012 Setup API routing structure in backend/src/api/main.py
- [X] T013 Configure error handling and logging infrastructure in backend/src/utils/errors.py
- [X] T014 Create frontend authentication context in frontend/src/context/authContext.ts

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Secure Task Access (Priority: P1) 🎯 MVP

**Goal**: Authenticated users can only access, modify, or delete their own tasks, with unauthorized access attempts properly blocked and logged.

**Independent Test**: Can be fully tested by attempting to access tasks owned by different users and verifying that unauthorized access is blocked with appropriate 401 responses.

### Tests for User Story 1 (OPTIONAL - only if tests requested) ⚠️

> **NOTE: Write these tests first, ensure they fail before implementation**

- [X] T015 [P] [US1] Contract test for GET /api/tasks/{taskId} in backend/tests/contract/test_task_auth.py
- [X] T016 [P] [US1] Integration test for cross-user access denial in backend/tests/integration/test_task_authorization.py

### Implementation for User Story 1

- [X] T017 [P] [US1] Implement task ownership verification in backend/src/services/task_service.py
- [X] T018 [US1] Create GET /api/tasks/{taskId} endpoint with user ownership check in backend/src/api/routes/tasks.py
- [X] T019 [US1] Create GET /api/tasks endpoint returning only user's tasks in backend/src/api/routes/tasks.py
- [X] T020 [US1] Create PUT /api/tasks/{taskId} endpoint with user ownership check in backend/src/api/routes/tasks.py
- [X] T021 [US1] Create DELETE /api/tasks/{taskId} endpoint with user ownership check in backend/src/api/routes/tasks.py
- [X] T022 [US1] Add logging for task access attempts in backend/src/utils/logger.py
- [X] T023 [US1] Add 401 Unauthorized responses for failed ownership checks

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - JWT Authentication Enforcement (Priority: P1)

**Goal**: All API endpoints require valid JWT authentication tokens, with requests lacking proper authentication returning 401 Unauthorized.

**Independent Test**: Can be fully tested by making requests to various endpoints without authentication and verifying 401 responses.

### Tests for User Story 2 (OPTIONAL - only if tests requested) ⚠️

- [X] T024 [P] [US2] Contract test for authentication enforcement on all endpoints in backend/tests/contract/test_auth_enforcement.py
- [X] T025 [P] [US2] Integration test for missing JWT requests in backend/tests/integration/test_auth_validation.py

### Implementation for User Story 2

- [X] T026 [P] [US2] Enhance JWT middleware to validate token presence in backend/src/middleware/auth.py
- [X] T027 [US2] Add authentication decorator for API routes in backend/src/api/decorators.py
- [X] T028 [US2] Apply authentication middleware to all task endpoints in backend/src/api/routes/tasks.py
- [X] T029 [US2] Create POST /api/tasks endpoint with authentication and user ownership validation in backend/src/api/routes/tasks.py
- [X] T030 [US2] Implement token expiration validation in backend/src/services/auth_service.py
- [X] T031 [US2] Add standardized 401 Unauthorized error responses in backend/src/utils/errors.py

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Session Expiration Handling (Priority: P2)

**Goal**: Frontend application gracefully handles JWT token expiration by redirecting users to login and clearing any sensitive cached data.

**Independent Test**: Can be fully tested by simulating token expiration and verifying proper redirection and data clearing.

### Tests for User Story 3 (OPTIONAL - only if tests requested) ⚠️

- [X] T032 [P] [US3] Integration test for frontend token expiration handling in frontend/tests/integration/test_session_handling.js
- [X] T033 [P] [US3] Unit test for auth state management in frontend/tests/unit/test_auth_context.js

### Implementation for User Story 3

- [X] T034 [P] [US3] Create frontend authentication service in frontend/src/services/authService.js
- [X] T035 [US3] Implement token expiration check in frontend/src/utils/tokenUtils.js
- [X] T036 [US3] Create interceptor for API requests with auth headers in frontend/src/utils/apiClient.js
- [X] T037 [US3] Implement 401 response handler for redirect to login in frontend/src/utils/apiClient.js
- [X] T038 [US3] Add logout functionality that clears tokens and sensitive data in frontend/src/services/authService.js
- [X] T039 [US3] Create protected route component in frontend/src/components/ProtectedRoute.js
- [X] T040 [US3] Update frontend pages to use protected routes in frontend/src/pages/*

**Checkpoint**: All user stories should now be independently functional

---

## Phase 6: User Story 4 - Consistent JWT Secret Configuration (Priority: P2)

**Goal**: Backend and frontend applications use the same JWT secret for token validation, ensuring seamless authentication flow.

**Independent Test**: Can be fully tested by verifying that tokens generated by the backend can be validated by the frontend and vice versa.

### Tests for User Story 4 (OPTIONAL - only if tests requested) ⚠️

- [X] T041 [P] [US4] Integration test for JWT consistency between backend and frontend in backend/tests/integration/test_jwt_consistency.py

### Implementation for User Story 4

- [X] T042 [P] [US4] Create JWT utility functions in backend/src/utils/jwt_utils.py
- [X] T043 [US4] Implement standardized JWT token generation with BETTER_AUTH_SECRET in backend/src/services/auth_service.py
- [X] T044 [US4] Ensure frontend properly handles tokens from backend in frontend/src/services/authService.js
- [X] T045 [US4] Add configuration validation for JWT settings in backend/src/config.py
- [X] T046 [US4] Document JWT configuration requirements in backend/docs/authentication.md

**Checkpoint**: All user stories should now be independently functional

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [X] T047 [P] Update documentation for security implementation in backend/docs/security.md and frontend/docs/security.md
- [X] T048 Add comprehensive error logging for security events in backend/src/utils/logger.py
- [X] T049 Security hardening: input validation, SQL injection protection, XSS prevention
- [X] T050 [P] Add security headers to API responses in backend/src/middleware/security.py
- [X] T051 Run quickstart.md validation to ensure all security features work correctly
- [X] T052 Perform end-to-end security testing for all user stories
- [X] T053 Update environment configuration to ensure secure JWT secret handling

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P1)**: Can start after Foundational (Phase 2) - May integrate with US1 but should be independently testable
- **User Story 3 (P2)**: Can start after Foundational (Phase 2) - May integrate with US1/US2 but should be independently testable
- **User Story 4 (P2)**: Can start after Foundational (Phase 2) - May integrate with previous stories but should be independently testable

### Within Each User Story

- Tests (if included) MUST be written and FAIL before implementation
- Models before services
- Services before endpoints
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- All tests for a user story marked [P] can run in parallel
- Models within a story marked [P] can run in parallel
- Different user stories can be worked on in parallel by different team members

---

## Parallel Example: User Story 1

```bash
# Launch all tests for User Story 1 together (if tests requested):
Task: "Contract test for GET /api/tasks/{taskId} in backend/tests/contract/test_task_auth.py"
Task: "Integration test for cross-user access denial in backend/tests/integration/test_task_authorization.py"

# Launch all implementation for User Story 1 together:
Task: "Implement task ownership verification in backend/src/services/task_service.py"
Task: "Create GET /api/tasks/{taskId} endpoint with user ownership check in backend/src/api/routes/tasks.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Add User Story 4 → Test independently → Deploy/Demo
6. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 2
   - Developer C: User Story 3
   - Developer D: User Story 4
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence