# RAG Chatbot Integration Development Guidelines

Auto-generated from all feature plans. Last updated: 2025-12-29

## Active Technologies

- JavaScript/TypeScript (frontend)
- Python 3.11 (backend)
- Docusaurus (documentation framework)
- React (frontend component library)
- FastAPI (Python web framework)
- Qdrant (vector database)
- Cohere (embeddings)
- OpenAI/OpenRouter (response generation)
- HTML/CSS (markup and styling)

## Project Structure

```text
backend/
├── api.py               # FastAPI endpoint for chatbot
├── agent_retriev.py     # RAG agent for retrieving book content
└── requirements.txt     # Python dependencies

book-docusaurus/
├── src/
│   ├── components/
│   │   └── Chatbot/    # Chat UI components
│   ├── theme/
│   │   └── Root.js     # Inject UI components globally
│   └── css/
│       └── chatbot.css # Chat UI styling
└── static/
    └── chatbot.js      # Handle frontend JS for text selection
```

## Commands

### Backend Commands
```bash
# Start the backend API server
cd backend
uvicorn api:app --reload --port 8000

# Install backend dependencies
pip install fastapi uvicorn python-dotenv cohere qdrant-client openai agents

# Test the RAG agent directly
python -c "from agent_retriev import RAGAgent; agent = RAGAgent(); print(agent.query('test query').content)"
```

### Frontend Commands
```bash
# Start the Docusaurus development server
cd book-docusaurus
npm start

# Build the Docusaurus site
npm run build

# Install frontend dependencies
npm install
```

## Code Style

### Python
- Follow PEP 8 guidelines
- Use type hints for all function parameters and return values
- Use descriptive variable names
- Keep functions focused on a single responsibility

### JavaScript/React
- Use functional components with hooks
- Follow React best practices for state management
- Use consistent naming conventions (camelCase)
- Implement proper error boundaries and loading states

### CSS
- Use BEM methodology for class naming
- Write mobile-first responsive styles
- Use CSS variables for consistent theming
- Follow accessibility best practices

## Recent Changes

### Feature: RAG Chatbot Integration (4-rag-chatbot-docusaurus)
- Added FastAPI backend with chat endpoints
- Implemented React chat UI components for Docusaurus
- Integrated highlight-to-answer functionality
- Connected frontend to existing RAG agent system

### Feature: Qdrant RAG Agent (1-qdrant-rag-agent)
- Implemented RAG agent with Qdrant vector search
- Added Cohere embeddings for semantic search
- Created response generation with OpenAI

### Feature: Docusaurus Embedding Pipeline (1-docusaurus-embedding-pipeline)
- Set up Docusaurus documentation site
- Created embedding pipeline for book content
- Integrated with Qdrant vector database

<!-- MANUAL ADDITIONS START -->
<!-- MANUAL ADDITIONS END -->