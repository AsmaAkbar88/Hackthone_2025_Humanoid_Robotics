# Data Model: Docusaurus Content Embedding Pipeline

## Entities

### DocumentationContent
**Description**: Represents text content extracted from documentation pages
- **url** (string): Source URL of the documentation page
- **content** (string): Clean text content extracted from the page
- **title** (string): Title of the documentation page
- **metadata** (object): Additional metadata about the page

### TextChunk
**Description**: Represents a chunk of text content for embedding
- **id** (string): Unique identifier for the chunk
- **content** (string): The text content of the chunk
- **source_url** (string): URL of the original documentation page
- **chunk_index** (integer): Position of the chunk in the original document
- **metadata** (object): Additional metadata for the chunk

### SemanticRepresentation
**Description**: Represents vector representation of text content
- **id** (string): Unique identifier for the representation
- **vector** (array[float]): The embedding vector data
- **text_chunk_id** (string): Reference to the original text chunk
- **metadata** (object): Additional metadata including source information

### VectorRecord
**Description**: Represents stored representations in the vector database
- **id** (string): Unique identifier for the record
- **vector** (array[float]): The embedding vector data
- **payload** (object): Metadata payload including source URL, content, and other information
- **collection_name** (string): Name of the Qdrant collection (new_rag_embedding)

## Relationships
- DocumentationContent contains multiple TextChunks
- TextChunk generates one SemanticRepresentation
- SemanticRepresentation is stored as one VectorRecord

## Validation Rules
- DocumentationContent.url must be a valid URL
- TextChunk.content must not be empty
- SemanticRepresentation.vector must be a valid embedding vector
- VectorRecord.id must be unique within the collection