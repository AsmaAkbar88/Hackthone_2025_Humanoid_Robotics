# Quickstart: Qdrant Retrieval Testing

## Prerequisites
- Python 3.11+
- pip package manager
- Access to Qdrant Cloud instance with vectors already stored
- Existing vector collection named "new_rag_embedding"

## Setup

1. **Install dependencies**:
   ```bash
   pip install -r requirements-test.txt
   ```

2. **Set up environment variables**:
   Create a `.env` file with the following:
   ```
   QDRANT_URL=your_qdrant_cloud_url
   QDRANT_API_KEY=your_qdrant_api_key
   ```

3. **Run retrieval tests**:
   ```bash
   python test_retrieval.py
   ```

## Configuration
- The tests will query the Qdrant collection named "new_rag_embedding"
- Default top-k value is 5, but can be configured
- Tests verify content accuracy, metadata integrity, and JSON output format

## Expected Output
- All queries return correct top-k matches based on semantic similarity
- Retrieved chunks match original text content exactly
- Metadata (URL, chunk ID) is returned correctly
- JSON responses follow the expected format
- Test results indicate pass/fail status for each validation