# Quickstart Guide: Qdrant RAG Agent

**Feature**: 1-qdrant-rag-agent
**Date**: 2025-12-28

## Prerequisites

- Python 3.9+
- Qdrant Cloud account with existing vector collection
- OpenAI API key
- Cohere API key
- Git

## Setup

### 1. Clone Repository
```bash
git clone <repository-url>
cd <repository-directory>
```

### 2. Install Dependencies
```bash
pip install openai qdrant-client cohere python-dotenv fastapi uvicorn
```

### 3. Environment Configuration
Create a `.env` file with the following variables:
```env
QDRANT_URL=your_qdrant_cloud_url
QDRANT_API_KEY=your_qdrant_api_key
QDRANT_COLLECTION=your_collection_name
OPENAI_API_KEY=your_openai_api_key
COHERE_API_KEY=your_cohere_api_key
```

### 4. Run the Agent
```bash
python agent_retriev.py
```

## Usage

### Basic Query
```python
from agent_retriev import RAGAgent

agent = RAGAgent()
response = agent.query("Your question here")
print(response.answer)
```

### API Usage
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your_api_key" \
  -d '{
    "query": "What is artificial intelligence?",
    "top_k": 5,
    "similarity_threshold": 0.7
  }'
```

## Configuration

The agent can be configured via environment variables or by passing parameters to the constructor:

```python
agent = RAGAgent(
    qdrant_url="your_url",
    collection_name="your_collection",
    top_k=5,
    similarity_threshold=0.7
)
```

## Troubleshooting

### Common Issues

1. **Authentication Errors**: Verify API keys are correctly set in environment variables
2. **Connection Issues**: Check Qdrant Cloud URL and network connectivity
3. **Empty Results**: Verify that your collection contains indexed content
4. **Rate Limits**: Check if API usage limits have been reached

### Verification Steps

1. Test Qdrant connection: `python -c "from agent_retriev import test_qdrant_connection; test_qdrant_connection()"`
2. Verify API keys: `python -c "from agent_retriev import verify_apis; verify_apis()"`
3. Run basic query: `python -c "from agent_retriev import basic_test; basic_test()"`