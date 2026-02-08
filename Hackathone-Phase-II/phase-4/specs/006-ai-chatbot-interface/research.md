# Research: AI Chatbot Interface for Todo Application

## Overview
Research conducted to support the implementation of an AI-powered chatbot for the Todo application, focusing on integrating OpenAI Agents SDK and MCP tools while maintaining a stateless architecture with database persistence.

## Decision: MCP Tools Implementation
**Rationale**: MCP (Model Context Protocol) tools are essential for enabling the AI agent to perform specific actions like creating, reading, updating, and deleting tasks. This approach ensures that all task operations go through a standardized interface that can be properly authenticated and authorized.

**Alternatives considered**:
- Direct API calls from AI: Would bypass security and audit trails
- Custom function calling: Would require more custom implementation and maintenance

## Decision: Conversation and Message Models
**Rationale**: To maintain stateless design while preserving conversation history, we need dedicated database models to store conversation threads and individual messages. This allows the AI to have context during interactions without keeping state in server memory.

**Alternatives considered**:
- Client-side storage: Would not persist across devices/sessions
- In-memory cache: Would not survive server restarts and violates stateless constraint

## Decision: Single Stateless Chat Endpoint
**Rationale**: Following the constraint of having a single stateless chat endpoint at POST /api/{user_id}/chat ensures simplicity and scalability. The endpoint will handle all AI interactions while relying on database-stored context.

**Alternatives considered**:
- WebSocket connections: More complex implementation and harder to scale statelessly
- Multiple endpoints: Would violate the specified constraint

## Decision: OpenAI Agents SDK Integration
**Rationale**: The OpenAI Agents SDK provides the necessary infrastructure to connect natural language inputs to specific tool calls (MCP tools), making it ideal for our use case of translating user commands into task operations.

**Alternatives considered**:
- Custom NLP processing: Would require significant development effort and maintenance
- Third-party chatbot services: Would not provide the same level of control and integration

## Decision: Database Schema Extensions
**Rationale**: Extending the existing Neon PostgreSQL database with new tables for conversations and messages maintains consistency with the current architecture while providing the necessary persistence for chat functionality.

**Tables to be added**:
- conversations: Stores conversation threads with user_id foreign key for isolation
- messages: Stores individual messages with conversation_id foreign key and message type (user/assistant)