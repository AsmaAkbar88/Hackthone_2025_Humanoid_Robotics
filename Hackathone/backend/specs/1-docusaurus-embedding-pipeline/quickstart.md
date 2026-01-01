# Quickstart: Docusaurus Content Embedding Pipeline

## Prerequisites
- Python 3.11+
- pip package manager
- Cohere API key
- Qdrant Cloud account and API key

## Setup

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up environment variables**:
   Create a `.env` file with the following:
   ```
   COHERE_API_KEY=your_cohere_api_key_here
   QDRANT_URL=your_qdrant_cloud_url_here
   QDRANT_API_KEY=your_qdrant_api_key_here
   ```

   Or copy the example file:
   ```bash
   cp .env.example .env
   # Then edit .env with your actual API keys
   ```

3. **Run the pipeline**:
   ```bash
   python main.py
   ```

## Configuration
- The pipeline will crawl the documentation site at https://book-three-eta.vercel.app/
- Embeddings will be stored in a Qdrant collection named "new_rag_embedding"
- Text will be chunked for optimal embedding generation
- The pipeline includes comprehensive logging for observability
- Error handling and retry logic for network requests

## Expected Output
- All pages from the documentation site will be crawled and processed
- Embeddings will be generated for all content using Cohere
- Data will be stored in Qdrant vector database with metadata
- Processing logs will be displayed during execution
- The pipeline will continue processing even if individual URLs fail