# Data Model: Qdrant Retrieval Testing

## Entities

### QueryRequest
**Description**: Represents a retrieval request containing the input query text and parameters
- **query_text** (string): The input query text to search for
- **top_k** (integer): Number of top results to retrieve
- **query_id** (string): Unique identifier for the query request
- **parameters** (object): Additional search parameters (e.g., filters, weights)

### RetrievalResult
**Description**: Represents a single retrieved text chunk with similarity score and metadata
- **chunk_id** (string): Unique identifier for the text chunk
- **content** (string): The retrieved text content
- **similarity_score** (float): Similarity score between query and chunk
- **metadata** (object): Metadata including source URL, chunk index, etc.
- **rank** (integer): Position in the retrieval results (1 for top match)

### QueryResponse
**Description**: Represents the complete response containing multiple retrieval results
- **query_id** (string): Identifier linking to the original query request
- **results** (array[RetrievalResult]): Array of retrieved results
- **query_time** (float): Time taken to process the query in seconds
- **status** (string): Status of the query (success, error, timeout)
- **total_results** (integer): Total number of results returned

## Relationships
- QueryRequest generates one QueryResponse
- QueryResponse contains multiple RetrievalResult items

## Validation Rules
- QueryRequest.query_text must not be empty
- QueryRequest.top_k must be a positive integer
- RetrievalResult.similarity_score must be between 0 and 1
- RetrievalResult.content must not be empty
- QueryResponse.results must contain at least one item when status is success