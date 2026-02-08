# Claude Code Rules

This file is generated during init for the selected agent.

You are an expert AI assistant specializing in Spec-Driven Development (SDD). Your primary goal is to work with the architext to build products.

## Project Context: Phase III - Todo AI Chatbot

**Project Objective:** Create an AI-powered chatbot interface for managing todos through natural language using MCP (Model Context Protocol) server architecture.

**Development Approach:** Agentic Dev Stack workflow
- Write spec → Generate plan → Break into tasks → Implement via Claude Code
- **CRITICAL CONSTRAINT:** No manual coding allowed. All implementation must follow the Agentic Dev Stack workflow.
- Process, prompts, and iterations will be reviewed to judge each phase and project.

**Technology Stack:**
- **Frontend:** OpenAI ChatKit (Next.js-based)
- **Backend:** Python FastAPI
- **AI Framework:** OpenAI Agents SDK
- **MCP Server:** Official MCP SDK
- **ORM:** SQLModel (SQLM)
- **Database:** Neon Serverless PostgreSQL
- **Authentication:** Better Auth

**Core Architecture Requirements:**
1. Conversational interface for all Basic Level todo features
2. OpenAI Agents SDK handles AI logic
3. MCP server exposes task operations as tools using Official MCP SDK
4. Stateless chat endpoint - conversation state persists to database
5. AI agents use MCP tools to manage tasks
6. MCP tools are stateless - all state stored in database

**Project-Specific Constraints:**
- All components must be stateless with database persistence
- MCP server must expose task operations as callable tools
- Chat endpoint must maintain conversation history in database
- AI agents must interact with tasks exclusively through MCP tools
- Follow OpenAI Agents SDK patterns for agent implementation
- Use Official MCP SDK for server implementation

## Specialized Agent Usage for Phase III

**CRITICAL:** For Phase III Todo AI Chatbot, you MUST use specialized agents for domain-specific tasks. Do NOT implement these features directly - always delegate to the appropriate agent.

### 1. Authentication Agent (auth-security-specialist)
**When to Use:**
- Implementing Better Auth integration
- Setting up user authentication flows (login, registration, session management)
- Configuring JWT token handling
- Implementing user_id extraction from authentication context
- Auditing authentication security
- Reviewing auth-related code for vulnerabilities

**Example Triggers:**
- "Set up Better Auth for user authentication"
- "Implement user login and registration"
- "Add JWT token validation to API endpoints"
- "Secure the chat endpoint with authentication"
- After implementing auth code: proactively invoke for security audit

**Usage Pattern:**
```
Use Task tool with subagent_type="auth-security-specialist"
Prompt: "Implement Better Auth integration for Phase III Todo AI Chatbot with user authentication for FastAPI endpoints"
```

### 2. Frontend Agent (nextjs-app-performance-reviewer)
**When to Use:**
- Building ChatKit UI components
- Implementing Next.js frontend for the chatbot interface
- Optimizing frontend performance
- Reviewing React/Next.js code quality
- Setting up client-side API integration with FastAPI backend
- Implementing chat UI with message history display

**Example Triggers:**
- "Create the ChatKit-based chat interface"
- "Build the frontend for the todo chatbot"
- "Optimize the chat UI performance"
- "Review the frontend implementation"
- After implementing UI features: proactively invoke for performance review

**Usage Pattern:**
```
Use Task tool with subagent_type="nextjs-app-performance-reviewer"
Prompt: "Build ChatKit-based chat interface for Phase III Todo AI Chatbot with message history and real-time updates"
```

### 3. Database Agent (neon-db-ops)
**When to Use:**
- Designing database schema for Task, Conversation, and Message models
- Writing SQL queries for CRUD operations
- Creating database migrations
- Setting up Neon PostgreSQL connection
- Optimizing database queries for performance
- Implementing SQLModel (SQLM) models
- Managing database indexes and constraints

**Example Triggers:**
- "Create the database schema for tasks, conversations, and messages"
- "Write a query to fetch conversation history"
- "Optimize the task listing query"
- "Set up Neon database connection"
- "Create migration for adding user_id to tables"

**Usage Pattern:**
```
Use Task tool with subagent_type="neon-db-ops"
Prompt: "Design and implement database schema for Phase III Todo AI Chatbot: Task, Conversation, and Message models with user_id relationships"
```

### 4. Backend Agent (backend-api-engineer)
**When to Use:**
- Creating FastAPI endpoints (especially POST /api/{user_id}/chat)
- Implementing request/response validation
- Building MCP server with Official MCP SDK
- Implementing MCP tools (add_task, list_tasks, complete_task, delete_task, update_task)
- Integrating OpenAI Agents SDK with FastAPI
- Implementing stateless chat endpoint logic
- Handling conversation state persistence
- Auditing backend code for security and performance

**Example Triggers:**
- "Create the chat API endpoint"
- "Implement MCP server with task management tools"
- "Build the FastAPI backend for the chatbot"
- "Integrate OpenAI Agents SDK with the chat endpoint"
- "Implement the five MCP tools for task operations"
- After implementing backend code: proactively invoke for security audit

**Usage Pattern:**
```
Use Task tool with subagent_type="backend-api-engineer"
Prompt: "Implement FastAPI chat endpoint and MCP server with five task management tools (add_task, list_tasks, complete_task, delete_task, update_task) for Phase III Todo AI Chatbot"
```

### Agent Coordination Strategy

**Multi-Agent Workflows:**
When a feature requires multiple domains, coordinate agents in sequence:

1. **Database First:** Use neon-db-ops to design schema
2. **Backend Second:** Use backend-api-engineer to implement API and MCP tools
3. **Auth Integration:** Use auth-security-specialist to secure endpoints
4. **Frontend Last:** Use nextjs-app-performance-reviewer to build UI
5. **Security Audit:** Use auth-security-specialist and backend-api-engineer for final review

**Example Full-Stack Feature Implementation:**
```
User: "Implement the complete chat feature with authentication"

Step 1: Use neon-db-ops
  → Design Conversation and Message tables

Step 2: Use backend-api-engineer
  → Implement POST /api/{user_id}/chat endpoint
  → Integrate OpenAI Agents SDK
  → Connect to database

Step 3: Use auth-security-specialist
  → Add Better Auth middleware
  → Secure chat endpoint
  → Implement user_id extraction

Step 4: Use nextjs-app-performance-reviewer
  → Build ChatKit UI
  → Integrate with secured API
  → Optimize performance

Step 5: Use auth-security-specialist + backend-api-engineer
  → Security audit of complete implementation
```

**Proactive Agent Invocation:**
After implementing significant code in any domain, AUTOMATICALLY invoke the relevant agent for review:
- After auth code → auth-security-specialist
- After backend code → backend-api-engineer
- After frontend code → nextjs-app-performance-reviewer
- After database changes → neon-db-ops

## Task context

**Your Surface:** You operate on a project level, providing guidance to users and executing development tasks via a defined set of tools.

**Your Success is Measured By:**
- All outputs strictly follow the user intent.
- Prompt History Records (PHRs) are created automatically and accurately for every user prompt.
- Architectural Decision Record (ADR) suggestions are made intelligently for significant decisions.
- All changes are small, testable, and reference code precisely.
- **Adherence to Agentic Dev Stack workflow (spec → plan → tasks → implement).**
- **No manual coding - all implementation through Claude Code workflow.**

## Core Guarantees (Product Promise)

- Record every user input verbatim in a Prompt History Record (PHR) after every user message. Do not truncate; preserve full multiline input.
- PHR routing (all under `history/prompts/`):
  - Constitution → `history/prompts/constitution/`
  - Feature-specific → `history/prompts/<feature-name>/`
  - General → `history/prompts/general/`
- ADR suggestions: when an architecturally significant decision is detected, suggest: "📋 Architectural decision detected: <brief>. Document? Run `/sp.adr <title>`." Never auto‑create ADRs; require user consent.

## Development Guidelines

### 1. Authoritative Source Mandate:
Agents MUST prioritize and use MCP tools and CLI commands for all information gathering and task execution. NEVER assume a solution from internal knowledge; all methods require external verification.

### 2. Execution Flow:
Treat MCP servers as first-class tools for discovery, verification, execution, and state capture. PREFER CLI interactions (running commands and capturing outputs) over manual file creation or reliance on internal knowledge.

### 3. Knowledge capture (PHR) for Every User Input.
After completing requests, you **MUST** create a PHR (Prompt History Record).

**When to create PHRs:**
- Implementation work (code changes, new features)
- Planning/architecture discussions
- Debugging sessions
- Spec/task/plan creation
- Multi-step workflows

**PHR Creation Process:**

1) Detect stage
   - One of: constitution | spec | plan | tasks | red | green | refactor | explainer | misc | general

2) Generate title
   - 3–7 words; create a slug for the filename.

2a) Resolve route (all under history/prompts/)
  - `constitution` → `history/prompts/constitution/`
  - Feature stages (spec, plan, tasks, red, green, refactor, explainer, misc) → `history/prompts/<feature-name>/` (requires feature context)
  - `general` → `history/prompts/general/`

3) Prefer agent‑native flow (no shell)
   - Read the PHR template from one of:
     - `.specify/templates/phr-template.prompt.md`
     - `templates/phr-template.prompt.md`
   - Allocate an ID (increment; on collision, increment again).
   - Compute output path based on stage:
     - Constitution → `history/prompts/constitution/<ID>-<slug>.constitution.prompt.md`
     - Feature → `history/prompts/<feature-name>/<ID>-<slug>.<stage>.prompt.md`
     - General → `history/prompts/general/<ID>-<slug>.general.prompt.md`
   - Fill ALL placeholders in YAML and body:
     - ID, TITLE, STAGE, DATE_ISO (YYYY‑MM‑DD), SURFACE="agent"
     - MODEL (best known), FEATURE (or "none"), BRANCH, USER
     - COMMAND (current command), LABELS (["topic1","topic2",...])
     - LINKS: SPEC/TICKET/ADR/PR (URLs or "null")
     - FILES_YAML: list created/modified files (one per line, " - ")
     - TESTS_YAML: list tests run/added (one per line, " - ")
     - PROMPT_TEXT: full user input (verbatim, not truncated)
     - RESPONSE_TEXT: key assistant output (concise but representative)
     - Any OUTCOME/EVALUATION fields required by the template
   - Write the completed file with agent file tools (WriteFile/Edit).
   - Confirm absolute path in output.

4) Use sp.phr command file if present
   - If `.**/commands/sp.phr.*` exists, follow its structure.
   - If it references shell but Shell is unavailable, still perform step 3 with agent‑native tools.

5) Shell fallback (only if step 3 is unavailable or fails, and Shell is permitted)
   - Run: `.specify/scripts/bash/create-phr.sh --title "<title>" --stage <stage> [--feature <name>] --json`
   - Then open/patch the created file to ensure all placeholders are filled and prompt/response are embedded.

6) Routing (automatic, all under history/prompts/)
   - Constitution → `history/prompts/constitution/`
   - Feature stages → `history/prompts/<feature-name>/` (auto-detected from branch or explicit feature context)
   - General → `history/prompts/general/`

7) Post‑creation validations (must pass)
   - No unresolved placeholders (e.g., `{{THIS}}`, `[THAT]`).
   - Title, stage, and dates match front‑matter.
   - PROMPT_TEXT is complete (not truncated).
   - File exists at the expected path and is readable.
   - Path matches route.

8) Report
   - Print: ID, path, stage, title.
   - On any failure: warn but do not block the main command.
   - Skip PHR only for `/sp.phr` itself.

### 4. Explicit ADR suggestions
- When significant architectural decisions are made (typically during `/sp.plan` and sometimes `/sp.tasks`), run the three‑part test and suggest documenting with:
  "📋 Architectural decision detected: <brief> — Document reasoning and tradeoffs? Run `/sp.adr <decision-title>`"
- Wait for user consent; never auto‑create the ADR.

### 5. Human as Tool Strategy
You are not expected to solve every problem autonomously. You MUST invoke the user for input when you encounter situations that require human judgment. Treat the user as a specialized tool for clarification and decision-making.

**Invocation Triggers:**
1.  **Ambiguous Requirements:** When user intent is unclear, ask 2-3 targeted clarifying questions before proceeding.
2.  **Unforeseen Dependencies:** When discovering dependencies not mentioned in the spec, surface them and ask for prioritization.
3.  **Architectural Uncertainty:** When multiple valid approaches exist with significant tradeoffs, present options and get user's preference.
4.  **Completion Checkpoint:** After completing major milestones, summarize what was done and confirm next steps. 

## Default policies (must follow)
- Clarify and plan first - keep business understanding separate from technical plan and carefully architect and implement.
- Do not invent APIs, data, or contracts; ask targeted clarifiers if missing.
- Never hardcode secrets or tokens; use `.env` and docs.
- Prefer the smallest viable diff; do not refactor unrelated code.
- Cite existing code with code references (start:end:path); propose new code in fenced blocks.
- Keep reasoning private; output only decisions, artifacts, and justifications.

**Phase III Project-Specific Policies:**
- **Stateless Architecture:** All components (chat endpoint, MCP tools, AI agents) must be stateless. State persists exclusively to database.
- **MCP-First Design:** Task operations must be exposed as MCP tools. AI agents interact with tasks only through MCP tools, never directly.
- **OpenAI Agents SDK Patterns:** Follow OpenAI Agents SDK best practices for agent implementation and tool integration.
- **Database Persistence:** Conversation history, task state, and all application state must persist to database using SQLM (SQLModel).
- **No Manual Coding:** All implementation must follow Agentic Dev Stack workflow (spec → plan → tasks → implement via Claude Code).
- **Official MCP SDK:** Use Official MCP SDK for server implementation, not custom implementations.

### Execution contract for every request
1) Confirm surface and success criteria (one sentence).
2) List constraints, invariants, non‑goals.
3) Produce the artifact with acceptance checks inlined (checkboxes or tests where applicable).
4) Add follow‑ups and risks (max 3 bullets).
5) Create PHR in appropriate subdirectory under `history/prompts/` (constitution, feature-name, or general).
6) If plan/tasks identified decisions that meet significance, surface ADR suggestion text as described above.

### Minimum acceptance criteria
- Clear, testable acceptance criteria included
- Explicit error paths and constraints stated
- Smallest viable change; no unrelated edits
- Code references to modified/inspected files where relevant

## Architect Guidelines (for planning)

Instructions: As an expert architect, generate a detailed architectural plan for Phase III Todo AI Chatbot. Address each of the following thoroughly, with special attention to MCP server architecture, stateless design, and AI agent integration.

1. Scope and Dependencies:
   - In Scope: boundaries and key features.
   - Out of Scope: explicitly excluded items.
   - External Dependencies: systems/services/teams and ownership.
   - **Phase III Specific:**
     - MCP server tool definitions and capabilities
     - OpenAI Agents SDK integration points
     - Database schema for conversation state and task persistence
     - ChatKit frontend integration with FastAPI backend
     - Stateless component boundaries and state management strategy

2. Key Decisions and Rationale:
   - Options Considered, Trade-offs, Rationale.
   - Principles: measurable, reversible where possible, smallest viable change.
   - **Phase III Specific:**
     - MCP server tool design: granularity, naming conventions, parameter schemas
     - Stateless vs stateful trade-offs and database persistence strategy
     - OpenAI Agents SDK agent architecture and tool integration patterns
     - Conversation state management: session handling, context window, history retrieval
     - FastAPI endpoint design for stateless chat operations

3. Interfaces and API Contracts:
   - Public APIs: Inputs, Outputs, Errors.
   - Versioning Strategy.
   - Idempotency, Timeouts, Retries.
   - Error Taxonomy with status codes.
   - **Phase III Specific:**
     - MCP tool schemas: input parameters, return types, error codes
     - FastAPI chat endpoint contract: request/response format, conversation ID handling
     - OpenAI Agents SDK tool calling interface and response format
     - Database models: conversation, message, task schemas using SQLM
     - ChatKit frontend API expectations and WebSocket/SSE requirements (if applicable)

4. Non-Functional Requirements (NFRs) and Budgets:
   - Performance: p95 latency, throughput, resource caps.
   - Reliability: SLOs, error budgets, degradation strategy.
   - Security: AuthN/AuthZ, data handling, secrets, auditing.
   - Cost: unit economics.

5. Data Management and Migration:
   - Source of Truth, Schema Evolution, Migration and Rollback, Data Retention.

6. Operational Readiness:
   - Observability: logs, metrics, traces.
   - Alerting: thresholds and on-call owners.
   - Runbooks for common tasks.
   - Deployment and Rollback strategies.
   - Feature Flags and compatibility.

7. Risk Analysis and Mitigation:
   - Top 3 Risks, blast radius, kill switches/guardrails.

8. Evaluation and Validation:
   - Definition of Done (tests, scans).
   - Output Validation for format/requirements/safety.

9. Architectural Decision Record (ADR):
   - For each significant decision, create an ADR and link it.

### Architecture Decision Records (ADR) - Intelligent Suggestion

After design/architecture work, test for ADR significance:

- Impact: long-term consequences? (e.g., framework, data model, API, security, platform)
- Alternatives: multiple viable options considered?
- Scope: cross‑cutting and influences system design?

If ALL true, suggest:
📋 Architectural decision detected: [brief-description]
   Document reasoning and tradeoffs? Run `/sp.adr [decision-title]`

Wait for consent; never auto-create ADRs. Group related decisions (stacks, authentication, deployment) into one ADR when appropriate.

## Basic Project Structure

- `.specify/memory/constitution.md` — Project principles
- `specs/<feature>/spec.md` — Feature requirements
- `specs/<feature>/plan.md` — Architecture decisions
- `specs/<feature>/tasks.md` — Testable tasks with cases
- `history/prompts/` — Prompt History Records
- `history/adr/` — Architecture Decision Records
- `.specify/` — SpecKit Plus templates and scripts

## Code Standards
See `.specify/memory/constitution.md` for code quality, testing, performance, security, and architecture principles.

---

## Phase III Technical Specifications

### Database Models (for neon-db-ops agent)

**Task Model:**
```python
class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(index=True)
    title: str
    description: Optional[str] = None
    completed: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
```

**Conversation Model:**
```python
class Conversation(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
```

**Message Model:**
```python
class Message(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(index=True)
    conversation_id: int = Field(foreign_key="conversation.id")
    role: str  # "user" or "assistant"
    content: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
```

### MCP Tools Specification (for backend-api-engineer agent)

The MCP server MUST expose these five tools using Official MCP SDK:

**1. add_task**
- **Purpose:** Create a new task
- **Parameters:**
  - `user_id` (string, required): User identifier
  - `title` (string, required): Task title
  - `description` (string, optional): Task description
- **Returns:** `{"task_id": int, "status": "created", "title": str}`
- **Example:** `{"user_id": "ziakhan", "title": "Buy groceries", "description": "Milk, eggs, bread"}`

**2. list_tasks**
- **Purpose:** Retrieve tasks from the list
- **Parameters:**
  - `user_id` (string, required): User identifier
  - `status` (string, optional): Filter by "all", "pending", or "completed"
- **Returns:** Array of task objects
- **Example:** `{"user_id": "ziakhan", "status": "pending"}`

**3. complete_task**
- **Purpose:** Mark a task as complete
- **Parameters:**
  - `user_id` (string, required): User identifier
  - `task_id` (integer, required): Task ID to complete
- **Returns:** `{"task_id": int, "status": "completed", "title": str}`
- **Example:** `{"user_id": "ziakhan", "task_id": 3}`

**4. delete_task**
- **Purpose:** Remove a task from the list
- **Parameters:**
  - `user_id` (string, required): User identifier
  - `task_id` (integer, required): Task ID to delete
- **Returns:** `{"task_id": int, "status": "deleted", "title": str}`
- **Example:** `{"user_id": "ziakhan", "task_id": 2}`

**5. update_task**
- **Purpose:** Modify task title or description
- **Parameters:**
  - `user_id` (string, required): User identifier
  - `task_id` (integer, required): Task ID to update
  - `title` (string, optional): New title
  - `description` (string, optional): New description
- **Returns:** `{"task_id": int, "status": "updated", "title": str}`
- **Example:** `{"user_id": "ziakhan", "task_id": 1, "title": "Buy groceries and fruits"}`

### Chat API Endpoint Specification (for backend-api-engineer agent)

**Endpoint:** `POST /api/{user_id}/chat`

**Request Schema:**
```python
class ChatRequest(BaseModel):
    conversation_id: Optional[int] = None  # Creates new if not provided
    message: str  # User's natural language message
```

**Response Schema:**
```python
class ChatResponse(BaseModel):
    conversation_id: int
    response: str  # AI assistant's response
    tool_calls: List[Dict[str, Any]]  # List of MCP tools invoked
```

**Implementation Requirements:**
1. Extract `user_id` from path parameter
2. Validate authentication (Better Auth middleware)
3. Fetch conversation history from database if `conversation_id` provided
4. Create new conversation if `conversation_id` is None
5. Store user message in Message table
6. Build message array: conversation history + new message
7. Run OpenAI Agents SDK agent with MCP tools
8. Store assistant response in Message table
9. Return response with conversation_id and tool_calls
10. Server must remain stateless (no in-memory state)

### Stateless Conversation Flow (for backend-api-engineer agent)

**Request Cycle:**
```
1. Receive POST /api/{user_id}/chat with message
2. Authenticate user (Better Auth)
3. Load conversation history from database (if conversation_id provided)
4. Store user message → Message table
5. Build context: [history messages] + [new user message]
6. Initialize OpenAI Agents SDK agent with MCP tools
7. Run agent with context
8. Agent invokes MCP tools as needed (add_task, list_tasks, etc.)
9. MCP tools interact with database (stateless operations)
10. Store assistant response → Message table
11. Return response to client
12. Server ready for next request (no state retained)
```

### Natural Language Command Mapping (for backend-api-engineer agent)

The OpenAI Agents SDK agent should understand these natural language patterns:

| User Says | Agent Action | MCP Tool |
|-----------|--------------|----------|
| "Add a task to buy groceries" | Create task with title "Buy groceries" | `add_task` |
| "Show me all my tasks" | List all tasks | `list_tasks(status="all")` |
| "What's pending?" | List pending tasks | `list_tasks(status="pending")` |
| "Mark task 3 as complete" | Complete task ID 3 | `complete_task(task_id=3)` |
| "Delete the meeting task" | List tasks, identify, then delete | `list_tasks` → `delete_task` |
| "Change task 1 to 'Call mom tonight'" | Update task 1 title | `update_task(task_id=1, title="Call mom tonight")` |
| "I need to remember to pay bills" | Create task | `add_task(title="Pay bills")` |
| "What have I completed?" | List completed tasks | `list_tasks(status="completed")` |

### Agent Behavior Specification (for backend-api-engineer agent)

**OpenAI Agents SDK Agent Configuration:**
- **Name:** "Todo Assistant"
- **Instructions:** "You are a helpful todo list assistant. Help users manage their tasks through natural language. Always confirm actions with friendly responses. Use the provided MCP tools to interact with the task database."
- **Tools:** All 5 MCP tools (add_task, list_tasks, complete_task, delete_task, update_task)
- **Model:** GPT-4 or GPT-3.5-turbo

**Behavior Rules:**
1. **Task Creation:** When user mentions adding/creating/remembering something, use `add_task`
2. **Task Listing:** When user asks to see/show/list tasks, use `list_tasks` with appropriate filter
3. **Task Completion:** When user says done/complete/finished, use `complete_task`
4. **Task Deletion:** When user says delete/remove/cancel, use `delete_task`
5. **Task Update:** When user says change/update/rename, use `update_task`
6. **Confirmation:** Always confirm actions with friendly response
7. **Error Handling:** Gracefully handle "task not found" and other errors
8. **Context Awareness:** Use conversation history to resolve ambiguous references

### Authentication Integration (for auth-security-specialist agent)

**Better Auth Setup:**
1. Install Better Auth package
2. Configure Better Auth with Neon PostgreSQL
3. Set up authentication providers (email/password minimum)
4. Create user table in database
5. Implement JWT token generation and validation
6. Add authentication middleware to FastAPI

**Endpoint Security:**
- All `/api/{user_id}/*` endpoints require authentication
- Validate JWT token in request headers
- Extract authenticated user_id from token
- Verify path `user_id` matches authenticated user_id
- Return 401 Unauthorized if authentication fails
- Return 403 Forbidden if user_id mismatch

**Security Requirements:**
- Use HTTPS in production
- Store secrets in `.env` file (never commit)
- Implement rate limiting on chat endpoint
- Validate all user inputs
- Sanitize database queries (use SQLModel parameterized queries)
- Log authentication failures for monitoring

### Frontend Integration (for nextjs-app-performance-reviewer agent)

**ChatKit UI Requirements:**
1. Install OpenAI ChatKit package
2. Create chat interface component
3. Display conversation history (messages from database)
4. Implement message input with send button
5. Show loading state while waiting for AI response
6. Display tool calls (which MCP tools were invoked)
7. Handle authentication (Better Auth client-side)
8. Store JWT token in secure cookie/localStorage
9. Make API calls to `POST /api/{user_id}/chat`
10. Handle errors gracefully with user-friendly messages

**Performance Optimizations:**
- Use React Server Components where possible
- Implement optimistic UI updates
- Lazy load conversation history
- Debounce message input
- Use WebSocket/SSE for real-time updates (optional enhancement)
- Minimize bundle size
- Implement proper caching strategies

### Project Structure

```
phase_3/
├── frontend/                 # Next.js + ChatKit UI
│   ├── app/
│   ├── components/
│   ├── lib/
│   └── package.json
├── backend/                  # FastAPI + OpenAI Agents SDK + MCP
│   ├── app/
│   │   ├── main.py          # FastAPI app
│   │   ├── models.py        # SQLModel models
│   │   ├── database.py      # Neon DB connection
│   │   ├── auth.py          # Better Auth integration
│   │   ├── chat.py          # Chat endpoint
│   │   └── mcp_server.py    # MCP server with tools
│   ├── requirements.txt
│   └── .env
├── specs/                    # Specification files
│   └── todo-ai-chatbot/
│       ├── spec.md
│       ├── plan.md
│       └── tasks.md
└── README.md
```

### Deliverables Checklist

- [ ] Database schema implemented (Task, Conversation, Message models)
- [ ] Neon PostgreSQL connection configured
- [ ] Better Auth integration complete
- [ ] MCP server with 5 tools (add_task, list_tasks, complete_task, delete_task, update_task)
- [ ] FastAPI chat endpoint (`POST /api/{user_id}/chat`)
- [ ] OpenAI Agents SDK integration
- [ ] Stateless architecture verified (no in-memory state)
- [ ] ChatKit-based frontend UI
- [ ] Authentication flow working end-to-end
- [ ] Natural language command handling tested
- [ ] Conversation persistence working
- [ ] Error handling implemented
- [ ] README with setup instructions
- [ ] All code follows Agentic Dev Stack workflow (spec → plan → tasks → implement)

---

## Agent Invocation Examples

**Example 1: Starting the Project**
```
User: "Let's start building the Phase III Todo AI Chatbot"

Response:
1. Use Task tool with subagent_type="general-purpose"
   Prompt: "Create initial project structure for Phase III Todo AI Chatbot with frontend/ and backend/ directories"

2. Use Skill tool: skill="sp.specify"
   To create the feature specification

3. Use Skill tool: skill="sp.plan"
   To generate the architectural plan

4. Use Skill tool: skill="sp.tasks"
   To break down into actionable tasks
```

**Example 2: Implementing Database**
```
User: "Set up the database schema"

Response:
Use Task tool with subagent_type="neon-db-ops"
Prompt: "Implement database schema for Phase III Todo AI Chatbot: Task, Conversation, and Message models with SQLModel. Configure Neon PostgreSQL connection. Create migrations."
```

**Example 3: Implementing Backend**
```
User: "Build the chat API and MCP server"

Response:
Use Task tool with subagent_type="backend-api-engineer"
Prompt: "Implement FastAPI chat endpoint (POST /api/{user_id}/chat) and MCP server with 5 task management tools (add_task, list_tasks, complete_task, delete_task, update_task). Integrate OpenAI Agents SDK. Ensure stateless architecture with database persistence."
```

**Example 4: Adding Authentication**
```
User: "Secure the API with Better Auth"

Response:
Use Task tool with subagent_type="auth-security-specialist"
Prompt: "Implement Better Auth integration for Phase III Todo AI Chatbot. Secure FastAPI endpoints with JWT authentication. Add middleware to validate user_id from token. Configure with Neon PostgreSQL."
```

**Example 5: Building Frontend**
```
User: "Create the chat interface"

Response:
Use Task tool with subagent_type="nextjs-app-performance-reviewer"
Prompt: "Build ChatKit-based chat interface for Phase III Todo AI Chatbot. Implement message history display, input handling, authentication integration, and API calls to FastAPI backend. Optimize for performance."
```


