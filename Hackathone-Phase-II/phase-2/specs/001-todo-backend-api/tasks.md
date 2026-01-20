---
description: "Task list for Todo Backend API implementation"
---

# Tasks: Todo Backend API

**Input**: Design documents from `/specs/001-todo-backend-api/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: Tests are included as specified in the feature requirements.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Backend project**: `backend/src/`, `backend/tests/` at repository root
- Paths shown below follow the planned structure from plan.md

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Create project structure per implementation plan in backend/
- [X] T002 Initialize Python project with FastAPI, SQLModel, Pydantic v2 dependencies
- [X] T003 [P] Configure linting and formatting tools (black, flake8, mypy)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T004 Setup database schema and migrations framework using SQLModel and Alembic
- [X] T005 [P] Implement JWT authentication utility functions in backend/src/utils/jwt_utils.py
- [X] T006 [P] Setup database connection and session management in backend/src/database/database.py
- [X] T007 Create base models/entities that all stories depend on in backend/src/models/
- [X] T008 Configure centralized error handling and exception handlers in backend/src/utils/error_handlers.py
- [X] T009 Setup environment configuration management with Pydantic settings
- [X] T010 [P] Implement authentication dependency injection in backend/src/api/deps.py

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Create and Manage Personal Tasks (Priority: P1) 🎯 MVP

**Goal**: Allow authenticated users to securely create, view, update, and delete their personal tasks

**Independent Test**: The system can be tested by authenticating a user and performing operations on tasks. The system should only return tasks owned by the authenticated user, and reject attempts to access other users' tasks.

### Tests for User Story 1 (included per requirements) ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [X] T011 [P] [US1] Contract test for GET /api/tasks endpoint in backend/tests/contract/test_api_contracts.py
- [X] T012 [P] [US1] Contract test for POST /api/tasks endpoint in backend/tests/contract/test_api_contracts.py
- [X] T013 [P] [US1] Integration test for user task management flow in backend/tests/integration/test_task_endpoints.py
- [X] T014 [P] [US1] Unit test for Task model validation in backend/tests/unit/test_task_model.py

### Implementation for User Story 1

- [X] T015 [P] [US1] Create Task model in backend/src/models/task.py following data model specification
- [X] T016 [P] [US1] Create User model in backend/src/models/user.py following data model specification
- [X] T017 [US1] Implement TaskService in backend/src/services/task_service.py for business logic
- [X] T018 [US1] Implement GET /api/tasks endpoint in backend/src/api/routes/tasks.py
- [X] T019 [US1] Implement POST /api/tasks endpoint in backend/src/api/routes/tasks.py
- [X] T020 [US1] Add validation and error handling for task creation
- [X] T021 [US1] Add user-based filtering to ensure users only see their own tasks

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Secure Task Operations (Priority: P2)

**Goal**: Allow users to securely update and delete their tasks with proper authentication and authorization checks

**Independent Test**: A user with valid authentication can update or delete their own tasks but receives error responses when attempting to modify tasks belonging to other users.

### Tests for User Story 2 (included per requirements) ⚠️

- [X] T022 [P] [US2] Contract test for PUT /api/tasks/{task_id} endpoint in backend/tests/contract/test_api_contracts.py
- [X] T023 [P] [US2] Contract test for DELETE /api/tasks/{task_id} endpoint in backend/tests/contract/test_api_contracts.py
- [X] T024 [P] [US2] Integration test for secure task operations in backend/tests/integration/test_task_endpoints.py

### Implementation for User Story 2

- [X] T025 [P] [US2] Add PUT /api/tasks/{task_id} endpoint in backend/src/api/routes/tasks.py
- [X] T026 [P] [US2] Add DELETE /api/tasks/{task_id} endpoint in backend/src/api/routes/tasks.py
- [X] T027 [US2] Enhance TaskService to support update and delete operations with user validation
- [X] T028 [US2] Add authorization checks to ensure users can only modify their own tasks
- [X] T029 [US2] Add error handling for unauthorized access attempts

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Error Handling and Status Codes (Priority: P3)

**Goal**: Ensure the system returns appropriate status codes for all operations and provides meaningful error messages when requests fail

**Independent Test**: Invalid requests return appropriate error responses with clear error messages.

### Tests for User Story 3 (included per requirements) ⚠️

- [X] T030 [P] [US3] Contract test for error response formats in backend/tests/contract/test_api_contracts.py
- [X] T031 [P] [US3] Unit test for error handling utilities in backend/tests/unit/test_error_handlers.py
- [X] T032 [P] [US3] Integration test for error scenarios in backend/tests/integration/test_task_endpoints.py

### Implementation for User Story 3

- [X] T033 [P] [US3] Create error response models using Pydantic in backend/src/models/
- [X] T034 [US3] Enhance centralized exception handlers with specific error codes
- [X] T035 [US3] Implement GET /api/tasks/{task_id} endpoint in backend/src/api/routes/tasks.py
- [X] T036 [US3] Implement PATCH /api/tasks/{task_id}/toggle endpoint in backend/src/api/routes/tasks.py
- [X] T037 [US3] Add comprehensive validation for all API endpoints
- [X] T038 [US3] Ensure all endpoints return proper HTTP status codes as specified in contracts

**Checkpoint**: All user stories should now be independently functional

---

[Add more user story phases as needed, following the same pattern]

---

## Phase N: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [X] T039 [P] Documentation updates in backend/docs/
- [X] T040 Code cleanup and refactoring
- [X] T041 Performance optimization across all stories
- [X] T042 [P] Additional unit tests (if requested) in backend/tests/unit/
- [X] T043 Security hardening
- [X] T044 Run quickstart.md validation

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
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - Builds on US1 models and services
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - Builds on US1/US2 endpoints

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
# Launch all tests for User Story 1 together:
Task: "Contract test for GET /api/tasks endpoint in backend/tests/contract/test_api_contracts.py"
Task: "Contract test for POST /api/tasks endpoint in backend/tests/contract/test_api_contracts.py"

# Launch all models for User Story 1 together:
Task: "Create Task model in backend/src/models/task.py"
Task: "Create User model in backend/src/models/user.py"
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
5. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 2
   - Developer C: User Story 3
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