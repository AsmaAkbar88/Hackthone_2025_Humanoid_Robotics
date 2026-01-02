<!-- SYNC IMPACT REPORT
Version change: N/A (initial version) → 1.0.0
List of modified principles: N/A (initial creation)
Added sections: All sections (initial constitution creation)
Removed sections: N/A
Templates requiring updates:
  - .specify/templates/plan-template.md ✅ updated
  - .specify/templates/spec-template.md ✅ updated
  - .specify/templates/tasks-template.md ✅ updated
  - .specify/templates/commands/*.md ⚠ pending
Follow-up TODOs: None
-->

# Backend-Only Integrated RAG Chatbot for AI-Spec Driven Book Constitution

## Core Principles

### Zero Hallucination
All responses must be generated exclusively from retrieved book chunks. If no relevant content is retrieved, the system must respond with a safe fallback. This ensures responses are grounded in retrieved content only.

### Context Isolation
Selected-text queries must not access global book knowledge. Selected-text mode must strictly limit context to user-provided text only. This enforces book-only context usage.

### Spec-First Deterministic Behavior
Deterministic behavior through spec-first development. All responses must be generated exclusively from retrieved book chunks. This ensures predictable and testable system behavior.

### Hackathon-Ready Simplicity with Production Alignment
Hackathon-ready simplicity with production-aligned architecture. Scope limited to hackathon timeframe with no unnecessary abstractions. This balances quick implementation with maintainable code practices.

### Free-Tier Service Compatibility
Free-tier compatibility across all services. Backend-only implementation using free-tier services only with no paid APIs. This ensures cost-effective development aligned with hackathon constraints.

### Clear Observability and Reproducibility
Clear observability and reproducibility. Retrieval, prompt construction, and model responses must be traceable. Clear separation between retrieval logic, generation logic, and storage layers.

## Additional Constraints and Requirements

Backend-only implementation with no book authoring, documentation writing, or frontend chatbot UI included in scope. No external knowledge beyond indexed book content. Performance optimized for live demo conditions. Defensive error handling for empty, low-score, or malformed queries.

Technology Stack: Backend Framework: FastAPI (Python), Vector Store: Qdrant Cloud, Relational Database: Neon Serverless Postgres, API Interface: RESTful endpoints with primary endpoint POST /chat. Architecture Style: Stateless where possible, session-aware where required.

AI & Embedding Strategy: Embedding Model: Cohere Embed (Free Tier), Vector Database: Qdrant Cloud (Free Tier), Reasoning Layer: OpenAI Agents / ChatKit SDK, Retrieval Strategy: Semantic similarity search using cosine distance, Prompting: Strict system prompts enforcing book-only context usage.

## Development Workflow and Quality Standards

All responses must be generated exclusively from retrieved book chunks. If no relevant content is retrieved, the system must respond with a safe fallback. Selected-text mode must strictly limit context to user-provided text only. Retrieval, prompt construction, and model responses must be traceable. Clear separation between retrieval logic, generation logic, and storage layers. Defensive error handling for empty, low-score, or malformed queries.

Key Engineering Standards include: All responses generated exclusively from retrieved book chunks, strict context isolation for selected-text mode, traceable retrieval and generation processes, clear architectural separation of concerns, and defensive error handling.

## Governance

This constitution governs all development decisions for the backend RAG chatbot. All implementation must strictly adhere to zero hallucination and context isolation principles. Any deviation from free-tier services requires explicit approval. All code reviews must verify compliance with spec-first development practices. Architecture decisions must align with hackathon-ready simplicity while maintaining production-aligned practices.

**Version**: 1.0.0 | **Ratified**: 2025-12-28 | **Last Amended**: 2025-12-28