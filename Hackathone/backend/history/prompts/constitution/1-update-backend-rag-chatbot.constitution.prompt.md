---
id: 1
title: Update Backend RAG Chatbot Constitution
stage: constitution
date: 2025-12-28
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: 1-qdrant-retrieval-testing
user: Claude
command: sp.constitution
labels: [constitution,rag,backend,hackathon]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - .specify/memory/constitution.md
tests:
 -
---

## Prompt

```
Project:
Backend-Only Integrated RAG Chatbot for AI-Spec Driven Book

Project Scope Clarification:
The AI / Spec-driven book built with Docusaurus has already been completed and deployed.
This constitution applies strictly to the BACKEND development of the RAG chatbot.
No book authoring, documentation writing, or frontend chatbot UI is included in this scope.

Purpose:
To design and implement a reliable, spec-driven RAG chatbot backend that can answer
user questions grounded strictly in the published book content, including
context-limited answers based only on user-selected text.

Core Principles:
- Zero hallucination: responses must be grounded in retrieved content only
- Context isolation: selected-text queries must not access global book knowledge
- Deterministic behavior through spec-first development
- Hackathon-ready simplicity with production-aligned architecture
- Free-tier compatibility across all services
- Clear observability and reproducibility

AI & Embedding Strategy:
- Embedding Model: Cohere Embed (Free Tier)
  - Justification: Claude does not provide native embedding models
  - Chosen for cost-free semantic search capability
- Vector Database: Qdrant Cloud (Free Tier)
- Reasoning Layer: OpenAI Agents / ChatKit SDK
- Retrieval Strategy: Semantic similarity search using cosine distance
- Prompting: Strict system prompts enforcing book-only context usage

Backend Technology Stack:
- Backend Framework: FastAPI (Python)
- Vector Store: Qdrant Cloud
- Relational Database: Neon Serverless Postgres
  - Stores chat history, sessions, and selected-text payloads
- API Interface: RESTful endpoints
  - Primary endpoint: POST /chat
- Architecture Style: Stateless where possible, session-aware where required

Key Engineering Standards:
- All responses must be generated exclusively from retrieved book chunks
- If no relevant content is retrieved, the system must respond with a safe fallback
- Selected-text mode must strictly limit context to user-provided text only
- Retrieval, prompt construction, and model responses must be traceable
- Clear separation between retrieval logic, generation logic, and storage layers
- Defensive error handling for empty, low-score, or malformed queries

Constraints:
- Backend-only implementation
- Free-tier services only (no paid APIs)
- No external knowledge beyond indexed book content
- Performance optimized for live demo conditions
- Scope limited to hackathon timeframe (no unnecessary abstractions)

Success Criteria:
- Accurate, book-grounded answers during live demo
- Correct enforcement of selected-text-only answering mode
- Stable backend performance under repeated queries
- Clear documentation of RAG pipeline and data flow
- Full alignment with hackathon requirements and judging rubric
```

## Response snapshot

Successfully updated the project constitution with the provided specifications for the Backend-Only Integrated RAG Chatbot for AI-Spec Driven Book. The updated constitution includes:

1. Six core principles:
   - Zero Hallucination: All responses must be generated exclusively from retrieved book chunks
   - Context Isolation: Selected-text queries must not access global book knowledge
   - Spec-First Deterministic Behavior: Deterministic behavior through spec-first development
   - Hackathon-Ready Simplicity: Hackathon-ready simplicity with production-aligned architecture
   - Free-Tier Service Compatibility: Free-tier compatibility across all services
   - Clear Observability: Clear observability and reproducibility

2. Additional sections for constraints, technology stack, development workflow standards, and governance

3. Version 1.0.0 with today's date (2025-12-28) as both ratification and last amended dates

The constitution now properly reflects the requirements for a backend-only RAG chatbot with zero hallucination, context isolation, and free-tier service compatibility.

## Outcome

- ✅ Impact: Updated constitution file with comprehensive principles for RAG chatbot backend
- 🧪 Tests: N/A
- 📁 Files: Updated .specify/memory/constitution.md with new project principles
- 🔁 Next prompts: Ready for spec, plan, and task creation based on this constitution
- 🧠 Reflection: Constitution now properly defines the project scope and constraints

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Begin spec creation based on constitution