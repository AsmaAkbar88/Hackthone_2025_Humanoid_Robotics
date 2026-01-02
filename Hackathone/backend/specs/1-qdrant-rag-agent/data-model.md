# Data Model: Qdrant RAG Agent

**Feature**: 1-qdrant-rag-agent
**Date**: 2025-12-28
**Status**: Complete

## Entities

### Query
**Description**: A user's natural language question or request for information from the book content

**Fields**:
- query_id: Unique identifier for the query (string/UUID)
- text: The actual query text (string, required, max 1000 characters)
- timestamp: When the query was submitted (datetime, required)
- similarity_threshold: Minimum similarity score for context retrieval (float, default 0.7)
- top_k: Number of context chunks to retrieve (integer, default 5)

**Validation Rules**:
- Text must be non-empty
- Text length must be between 5 and 1000 characters
- Similarity threshold must be between 0.0 and 1.0
- Top_k must be between 1 and 20

### Context Chunk
**Description**: A segment of book content retrieved from Qdrant based on vector similarity to the query

**Fields**:
- chunk_id: Unique identifier for the chunk (string)
- content: The actual content text (string, required)
- similarity_score: How similar this chunk is to the query (float, 0.0-1.0)
- source_url: URL or reference to the original source (string, optional)
- source_title: Title of the source document (string, optional)
- rank: Position in the ranked list of results (integer)

**Validation Rules**:
- Content must be non-empty
- Similarity score must be between 0.0 and 1.0
- Rank must be positive integer

### Response
**Description**: The generated answer created by the OpenAI agent using retrieved context chunks

**Fields**:
- response_id: Unique identifier for the response (string/UUID)
- query_id: Reference to the original query (string, required)
- content: The generated response text (string, required)
- context_chunks_used: List of chunk IDs used to generate the response (array of strings)
- generation_time: How long it took to generate the response (float, seconds)
- confidence_score: Estimated confidence in the response accuracy (float, 0.0-1.0)
- timestamp: When the response was generated (datetime, required)

**Validation Rules**:
- Content must be non-empty
- Confidence score must be between 0.0 and 1.0
- Generation time must be positive

### Qdrant Collection
**Description**: A stored vector database containing embedded book content for retrieval

**Fields**:
- collection_name: Name of the Qdrant collection (string, required)
- vector_size: Dimension of the embedded vectors (integer, required)
- total_points: Number of vectors in the collection (integer)
- creation_date: When the collection was created (datetime)

**Validation Rules**:
- Collection name must follow Qdrant naming conventions
- Vector size must match the embedding model used

### Agent Configuration
**Description**: Settings that define how the RAG agent connects to Qdrant and OpenAI services

**Fields**:
- agent_id: Unique identifier for the agent (string/UUID)
- qdrant_url: URL for Qdrant Cloud instance (string, required)
- qdrant_api_key: API key for Qdrant Cloud access (string, required)
- openai_api_key: API key for OpenAI access (string, required)
- cohere_api_key: API key for Cohere embeddings (string, required)
- collection_name: Name of the Qdrant collection to query (string, required)
- default_top_k: Default number of results to retrieve (integer, default 5)
- default_similarity_threshold: Default minimum similarity (float, default 0.7)
- timeout_seconds: Request timeout value (integer, default 30)

**Validation Rules**:
- All API keys must be non-empty
- URLs must be valid
- Default values must be within valid ranges

## Relationships

- Query → Response (1:1): Each query generates one response
- Query → Context Chunk (1:M): Each query can retrieve multiple context chunks
- Response → Context Chunk (M:N): A response can reference multiple chunks
- Agent Configuration → Query (1:M): One configuration serves multiple queries