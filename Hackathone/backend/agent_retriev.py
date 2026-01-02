"""
Qdrant RAG Agent Implementation

This agent connects to Qdrant Cloud to retrieve book content and uses OpenAI Agents SDK
for response generation. The system enforces "answer only from book data" policy to prevent hallucinations.
"""

import os
import logging
import asyncio
import time
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from datetime import datetime
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from qdrant_client.http import models
import cohere
from agents import Agent, Runner ,set_tracing_disabled ,OpenAIChatCompletionsModel
from openai import AsyncOpenAI
import threading


# Load environment variables
from pathlib import Path
load_dotenv(dotenv_path=Path(__file__).parent.parent / ".env")
set_tracing_disabled(True)


class CohereRateLimiter:
    """
    Rate limiter for Cohere API (Trial key: very conservative limits)
    """
    def __init__(self, requests_per_minute=10, concurrent_limit=1):
        self.requests_per_minute = requests_per_minute
        self.concurrent_limit = concurrent_limit
        self.semaphore = threading.Semaphore(concurrent_limit)
        self.last_request_time = 0
        self.min_interval = 60.0 / requests_per_minute  # seconds between requests
        self.lock = threading.Lock()

    def acquire(self):
        """Acquire permission to make a request"""
        # Wait for semaphore (concurrent limit) - BLOCKING
        self.semaphore.acquire()

        # Only wait if we made a request recently (within the rate limit window)
        with self.lock:
            now = time.time()
            elapsed = now - self.last_request_time
            wait_time = max(0, self.min_interval - elapsed)

            if wait_time > 0:
                print(f"Rate limit: waiting {wait_time:.2f}s...")
                time.sleep(wait_time)

            self.last_request_time = time.time()

    def release(self):
        """Release the request slot"""
        self.semaphore.release()


# Global rate limiter for Cohere (Trial key: 1 concurrent request)
cohere_rate_limiter = CohereRateLimiter(requests_per_minute=10, concurrent_limit=1)


# Initialize client inside the functions where it's needed to avoid module-level initialization issues
client = None

def get_openrouter_client():
    """Initialize and return OpenRouter client when needed"""
    global client
    if client is None:
        client = AsyncOpenAI(
            api_key=os.getenv("OPENROUTER_API_KEY"),
            base_url="https://openrouter.ai/api/v1"
        )
    return client

# Initialize the model_qdt inside the function where it's needed
def get_model():
    """Initialize and return the model when needed"""
    return OpenAIChatCompletionsModel(
        model="mistralai/devstral-2512:free",
        openai_client=get_openrouter_client()
    )

# Configure logging
logging.basicConfig(level=logging.WARNING)  # Reduced logging level to hide INFO messages
logger = logging.getLogger(__name__)


@dataclass
class Query:
    """A user's natural language question or request for information from the book content"""
    query_id: str
    text: str
    timestamp: datetime = None  # Will be set when the query is created
    similarity_threshold: float = 0.5  # Lowered threshold to capture more relevant results
    top_k: int = 5


@dataclass
class ContextChunk:
    """A segment of book content retrieved from Qdrant based on vector similarity to the query"""
    chunk_id: str
    content: str
    similarity_score: float
    source_url: Optional[str] = None
    source_title: Optional[str] = None
    rank: Optional[int] = None


@dataclass
class Response:
    """The generated answer created by the OpenAI agent using retrieved context chunks"""
    response_id: str
    query_id: str
    content: str
    context_chunks_used: List[str]
    generation_time: float
    confidence_score: float
    timestamp: datetime = None  # When the response was generated


class RAGAgent:
    """
    RAG (Retrieval-Augmented Generation) agent that connects to Qdrant Cloud to retrieve
    book content and uses OpenAI for response generation.
    """

    def __init__(
        self,
        qdrant_url: Optional[str] = None,
        qdrant_api_key: Optional[str] = None,
        collection_name: Optional[str] = None,
        openai_api_key: Optional[str] = None,
        cohere_api_key: Optional[str] = None,
        default_top_k: int = 5,
        default_similarity_threshold: float = 0.5  # Lowered threshold to capture more relevant results
    ):
        """
        Initialize the RAG Agent with configuration parameters.

        Args:
            qdrant_url: URL for Qdrant Cloud instance
            qdrant_api_key: API key for Qdrant Cloud access
            collection_name: Name of the Qdrant collection to query
            openai_api_key: API key for OpenAI access
            cohere_api_key: API key for Cohere embeddings
            default_top_k: Default number of results to retrieve
            default_similarity_threshold: Default minimum similarity
        """
        self.qdrant_url = qdrant_url or os.getenv("QDRANT_URL")
        self.qdrant_api_key = qdrant_api_key or os.getenv("QDRANT_API_KEY")
        self.collection_name = collection_name or os.getenv("QDRANT_COLLECTION", "default_collection")
        self.openai_api_key = openai_api_key or os.getenv("OPENAI_API_KEY")
        self.cohere_api_key = cohere_api_key or os.getenv("COHERE_API_KEY")
        self.default_top_k = default_top_k
        self.default_similarity_threshold = default_similarity_threshold

        # Initialize clients
        self.qdrant_client = self._setup_qdrant_client()
        self.cohere_client = self._setup_cohere_client()

    def _setup_qdrant_client(self) -> QdrantClient:
        """Setup Qdrant client with connection parameters"""
        try:
            if self.qdrant_url and self.qdrant_api_key:
                client = QdrantClient(
                    url=self.qdrant_url,
                    api_key=self.qdrant_api_key,
                    timeout=30
                )
            else:
                # For local development
                client = QdrantClient(host="localhost", port=6333)

            # Validate connection by attempting to list collections
            client.get_collections()
            logger.info(f"Connected to Qdrant at {self.qdrant_url}")
            return client
        except Exception as e:
            logger.error(f"Failed to connect to Qdrant: {str(e)}")
            raise


    def validate_qdrant_connection(self) -> bool:
        """
        Validate Qdrant collection connection by attempting to access the collection

        Returns:
            bool: True if connection is valid, False otherwise
        """
        try:
            # Try to get information about the collection to verify access
            collection_info = self.qdrant_client.get_collection(self.collection_name)
            logger.info(f"Successfully validated connection to collection: {self.collection_name}")
            return True
        except Exception as e:
            logger.error(f"Failed to validate connection to collection {self.collection_name}: {str(e)}")
            return False


    def get_agent_config(self) -> Dict[str, Any]:
        """
        Get the current agent configuration for MCP Server compatibility

        Returns:
            Dict containing agent configuration parameters
        """
        return {
            "qdrant_url": self.qdrant_url,
            "collection_name": self.collection_name,
            "default_top_k": self.default_top_k,
            "default_similarity_threshold": self.default_similarity_threshold,
            "has_openai_key": bool(self.openai_api_key),
            "has_cohere_key": bool(self.cohere_api_key),
            "has_qdrant_key": bool(self.qdrant_api_key)
        }

    def update_agent_config(self, config: Dict[str, Any]) -> bool:
        """
        Update agent configuration for MCP Server compatibility

        Args:
            config: Dictionary with configuration parameters to update

        Returns:
            bool: True if update was successful, False otherwise
        """
        try:
            if "qdrant_url" in config:
                self.qdrant_url = config["qdrant_url"]
            if "collection_name" in config:
                self.collection_name = config["collection_name"]
            if "default_top_k" in config:
                self.default_top_k = config["default_top_k"]
            if "default_similarity_threshold" in config:
                self.default_similarity_threshold = config["default_similarity_threshold"]

            # Reinitialize clients if needed
            if "qdrant_url" in config or "collection_name" in config:
                self.qdrant_client = self._setup_qdrant_client()

            logger.info("Agent configuration updated successfully")
            return True
        except Exception as e:
            logger.error(f"Failed to update agent configuration: {str(e)}")
            return False

    def _setup_cohere_client(self):
        """Setup Cohere client"""
        if self.cohere_api_key:
            client = cohere.Client(self.cohere_api_key)
        else:
            client = None
        return client

    def health_check(self) -> Dict[str, bool]:
        """
        Perform health check for monitoring and service discovery

        Returns:
            Dict with service status for each dependency
        """
        status = {
            "qdrant": False,
            "openai": False,
            "cohere": False,
            "overall": False
        }

        try:
            # Check Qdrant connection
            if hasattr(self, 'qdrant_client'):
                try:
                    self.qdrant_client.get_collections()
                    status["qdrant"] = True
                except:
                    status["qdrant"] = False

            # Check if API keys are configured (basic check)
            status["openai"] = bool(self.openai_api_key)
            status["cohere"] = bool(self.cohere_api_key)

            # Overall status - all essential services should be available
            status["overall"] = status["qdrant"] and status["openai"] and status["cohere"]

        except Exception as e:
            logger.error(f"Health check error: {str(e)}")
            status["overall"] = False

        return status

    def _generate_embedding(self, text: str) -> List[float]:
        """
        Generate embedding for text using Cohere API

        Args:
            text: Input text to generate embeddings for

        Returns:
            List of embedding values
        """
        embedding = self._safe_cohere_embedding(text)
        if embedding is None:
            raise ValueError("Failed to generate embedding with Cohere API")
        return embedding

    def _retrieve_context(self, query_embedding: List[float], top_k: int = 5,
                         similarity_threshold: float = 0.7) -> List[ContextChunk]:
        """
        Retrieve relevant context chunks from Qdrant based on query embedding

        Args:
            query_embedding: Embedding vector for the query
            top_k: Number of results to retrieve
            similarity_threshold: Minimum similarity score threshold

        Returns:
            List of relevant context chunks
        """
        try:
            # Perform search in Qdrant using query_points method (newer API)
            search_results = self.qdrant_client.query_points(
                collection_name=self.collection_name,
                query=query_embedding,
                limit=top_k,
                score_threshold=similarity_threshold,
                with_payload=True,
                with_vectors=False
            ).points

            # Convert results to ContextChunk objects
            context_chunks = []
            for i, result in enumerate(search_results):
                if result.score >= similarity_threshold:
                    # Extract content from payload - try different possible field names
                    content = (result.payload.get("content") or
                              result.payload.get("text") or
                              result.payload.get("document") or
                              result.payload.get("page_content") or
                              "")

                    # Extract URL - try different possible field names
                    url = (result.payload.get("url") or
                           result.payload.get("source_url") or
                           result.payload.get("source") or
                           result.payload.get("link") or
                           "")

                    # Extract title - try different possible field names
                    title = (result.payload.get("title") or
                             result.payload.get("heading") or
                             result.payload.get("header") or
                             result.payload.get("name") or
                             "")

                    chunk = ContextChunk(
                        chunk_id=str(result.id),
                        content=content,
                        similarity_score=result.score,
                        source_url=url,
                        source_title=title,
                        rank=i + 1
                    )
                    context_chunks.append(chunk)

            logger.info(f"Retrieved {len(context_chunks)} context chunks from Qdrant")
            return context_chunks
        except Exception as e:
            logger.error(f"Error retrieving context from Qdrant: {str(e)}")
            # Return empty list in case of error
            return []

    def _generate_response(self, query: str, context_chunks: List[ContextChunk]) -> str:
        """
        Generate response using OpenAI based on query and context chunks

        Args:
            query: Original user query
            context_chunks: Retrieved context chunks to use as input

        Returns:
            Generated response string
        """
        # Check if the query is a greeting or casual conversation
        query_lower = query.lower().strip()
        greetings = ["hello", "hi", "hey", "greetings", "good morning", "good afternoon", "good evening", "how are you", "how are you?", "hru", "hru?", "what's up", "what's up?", "whats up", "whats up?"]

        for greeting in greetings:
            if greeting in query_lower:
                if "hello" in query_lower or "hi" in query_lower or "hey" in query_lower:
                    return "Hello! I'm your AI assistant for the Physical AI & Humanoid Robotics book. How can I help you with information from the book today?"
                elif "how are you" in query_lower or "hru" in query_lower:
                    return "I'm doing well, thank you for asking! I'm here to help you with information from the Physical AI & Humanoid Robotics book. What would you like to know?"
                elif "what's up" in query_lower:
                    return "Not much! I'm here to assist you with questions about Physical AI & Humanoid Robotics. Feel free to ask anything about the book content!"

        if not context_chunks:
            return "I couldn't find relevant information in the book content to answer your question. Please ask something related to Physical AI, Humanoid Robotics, ROS2, Gazebo, NVIDIA Isaac, or Vision-Language-Action models."

        # Format context for the prompt
        context_text = "\n\n".join([chunk.content for chunk in context_chunks if chunk.content])

        # Create a prompt that enforces using only the provided context
        prompt = f"""
        Answer the following question based ONLY on the provided context.
        Do not use any knowledge outside of the provided context.

        Context:
        {context_text}

        Question: {query}

        Answer:"""

        # For now, using the traditional OpenAI API call as a fallback
        # since the main query method is synchronous
        try:
            from openai import OpenAI

            client = OpenAI(
                api_key=os.getenv("OPENROUTER_API_KEY") or self.openai_api_key,
                base_url="https://openrouter.ai/api/v1"
            )

            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that only uses information provided in the context to answer questions. Do not use any external knowledge."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=500
            )

            return response.choices[0].message.content.strip()
        except Exception as e:
            logger.error(f"Error in OpenAI API call: {str(e)}")
            return "Sorry, I encountered an error while generating the response. Please try again."

    def create_rag_agent(self):
        """
        Create an OpenAI Agent specifically for RAG operations using the Agent SDK
        """
        from agents import Agent

        # Create an agent with instructions for RAG operations
        agent = Agent(
            name="RAG Assistant",
            instructions="""
            You are a RAG (Retrieval-Augmented Generation) assistant.
            Use only the information provided in the context to answer the user's question.
            Do not use any external knowledge or make up information.
            If the context doesn't contain relevant information, clearly state that.
            Be helpful but factual based only on the provided context.
            """,
            model=get_model()
        )

        return agent

    def query_with_agent(self, query_text: str, top_k: Optional[int] = None,
                        similarity_threshold: Optional[float] = None) -> Response:
        """
        Query method that uses the OpenAI Agent SDK for response generation
        """
        import time

        start_time = time.time()

        # Use defaults if not provided
        top_k = top_k or self.default_top_k
        similarity_threshold = similarity_threshold or self.default_similarity_threshold

        # Validate input
        if not query_text or len(query_text.strip()) < 5:
            raise ValueError("Query must be at least 5 characters long")

        # Create query object
        query = Query(
            query_id=f"query_{int(time.time())}",
            text=query_text,
            timestamp=datetime.now(),
            top_k=top_k,
            similarity_threshold=similarity_threshold
        )

        # Generate embedding for the query
        query_embedding = self._generate_embedding(query_text)

        # Retrieve relevant context
        context_chunks = self._retrieve_context(
            query_embedding,
            top_k=query.top_k,
            similarity_threshold=query.similarity_threshold
        )

        # Format context for the agent
        if not context_chunks:
            response_text = "I couldn't find relevant information in the book content to answer your question."
        else:
            # Format context for the agent
            context_text = "\n\n".join([chunk.content for chunk in context_chunks if chunk.content])

            # Create a prompt that enforces using only the provided context
            full_prompt = f"""
            Context:
            {context_text}

            Question: {query_text}

            Answer:"""

            # Create and run the RAG agent
            agent = self.create_rag_agent()
            try:
                result = Runner.run_sync(agent, full_prompt)
                response_text = result.final_output
            except Exception as e:
                logger.error(f"Error in OpenAI Agent call: {str(e)}")
                response_text = "Sorry, I encountered an error while generating the response. Please try again."

        # Calculate generation time
        generation_time = time.time() - start_time

        # Create response object
        response = Response(
            response_id=f"response_{int(time.time())}",
            query_id=query.query_id,
            content=response_text,
            context_chunks_used=[chunk.chunk_id for chunk in context_chunks],
            generation_time=generation_time,
            confidence_score=min(1.0, len(context_chunks) / top_k),  # Simple confidence based on retrieved chunks
            timestamp=datetime.now()
        )

        logger.info(f"Processed query in {generation_time:.2f}s")
        logger.info(f"Response confidence: {response.confidence_score:.2f}, "
                   f"chunks used: {len(context_chunks)}")
        return response

    def _safe_cohere_embedding(self, text: str) -> Optional[List[float]]:
        """
        Safely generate embedding using Cohere API with error handling
        Includes rate limiting for Trial API with fast retries

        Args:
            text: Input text to generate embeddings for

        Returns:
            List of embedding values or None if error occurs
        """
        max_retries = 3
        retry_delays = [2, 4]  # Fast retries - total max 6s

        for attempt in range(max_retries):
            try:
                if not self.cohere_client:
                    logger.error("Cohere client not initialized")
                    return None

                # Apply rate limiting for Trial API
                cohere_rate_limiter.acquire()

                try:
                    response = self.cohere_client.embed(
                        texts=[text],
                        model="embed-english-v3.0",
                        input_type="search_query"
                    )
                    return response.embeddings[0]
                finally:
                    # Always release the semaphore
                    cohere_rate_limiter.release()

            except Exception as e:
                error_str = str(e)
                # Check if it's a rate limit error
                if "429" in error_str or "Too Many Requests" in error_str or "Please wait" in error_str:
                    if attempt < max_retries - 1:
                        wait_time = retry_delays[attempt]
                        logger.warning(f"Cohere rate limit, retry in {wait_time}s...")
                        time.sleep(wait_time)
                        continue
                    else:
                        logger.error(f"Cohere rate limit max retries exceeded")
                        return None
                else:
                    logger.error(f"Cohere error: {error_str[:100]}")
                return None

        return None

    async def _safe_agent_call(self, prompt: str) -> str:
        """
        Safely call OpenAI Agent SDK with comprehensive error handling

        Args:
            prompt: The prompt to send to the OpenAI Agent

        Returns:
            Generated response string or error message
        """
        try:
            # Create an agent with instructions to only use provided context
            agent = Agent(
                name="RAG Agent",
                instructions="You are a helpful assistant that only uses information provided in the context to answer questions. Do not use any external knowledge. Answer the user's question based only on the provided context.",
            )

            # Run the agent with the prompt
            result = await Runner.run(agent, prompt)
            return result.final_output

        except Exception as e:
            logger.error(f"Error in OpenAI Agent call: {str(e)}")
            return "Sorry, I encountered an error while generating the response. Please try again."

    def query(self, query_text: str, top_k: Optional[int] = None,
              similarity_threshold: Optional[float] = None) -> Response:
        """
        Process a user query and return a context-grounded response

        Args:
            query_text: The user's query text
            top_k: Number of context chunks to retrieve (optional)
            similarity_threshold: Minimum similarity score threshold (optional)

        Returns:
            Response object with answer and metadata
        """
        import time
        start_time = time.time()

        # Use defaults if not provided
        top_k = top_k or self.default_top_k
        similarity_threshold = similarity_threshold or self.default_similarity_threshold

        # Validate input
        if not query_text or len(query_text.strip()) < 5:
            raise ValueError("Query must be at least 5 characters long")

        # Check if the query is a greeting or casual conversation first
        query_lower = query_text.lower().strip()
        greetings = ["hello", "hi", "hey", "greetings", "good morning", "good afternoon", "good evening", "how are you", "how are you?", "hru", "hru?", "what's up", "what's up?", "whats up", "whats up?"]

        for greeting in greetings:
            if greeting in query_lower:
                if "hello" in query_lower or "hi" in query_lower or "hey" in query_lower:
                    response_text = "Hello! I'm your AI assistant for the Physical AI & Humanoid Robotics book. How can I help you with information from the book today?"
                elif "how are you" in query_lower or "hru" in query_lower:
                    response_text = "I'm doing well, thank you for asking! I'm here to help you with information from the Physical AI & Humanoid Robotics book. What would you like to know?"
                elif "what's up" in query_lower:
                    response_text = "Not much! I'm here to assist you with questions about Physical AI & Humanoid Robotics. Feel free to ask anything about the book content!"

                # Return a response without generating embeddings or querying Qdrant
                generation_time = time.time() - start_time
                response = Response(
                    response_id=f"response_{int(time.time())}",
                    query_id=f"query_{int(time.time())}",
                    content=response_text,
                    context_chunks_used=[],
                    generation_time=generation_time,
                    confidence_score=1.0,  # High confidence for predefined responses
                    timestamp=datetime.now()
                )
                return response

        # Create query object
        query = Query(
            query_id=f"query_{int(time.time())}",
            text=query_text,
            timestamp=datetime.now(),
            top_k=top_k,
            similarity_threshold=similarity_threshold
        )

        # Generate embedding for the query
        query_embedding = self._generate_embedding(query_text)

        # Retrieve relevant context
        context_chunks = self._retrieve_context(
            query_embedding,
            top_k=query.top_k,
            similarity_threshold=query.similarity_threshold
        )

        # Generate response based on context
        response_text = self._generate_response(query_text, context_chunks)

        # Calculate generation time
        generation_time = time.time() - start_time

        # Create response object
        response = Response(
            response_id=f"response_{int(time.time())}",
            query_id=query.query_id,
            content=response_text,
            context_chunks_used=[chunk.chunk_id for chunk in context_chunks],
            generation_time=generation_time,
            confidence_score=min(1.0, len(context_chunks) / top_k),  # Simple confidence based on retrieved chunks
            timestamp=datetime.now()
        )

        logger.info(f"Processed query in {generation_time:.2f}s")
        logger.info(f"Response confidence: {response.confidence_score:.2f}, "
                   f"chunks used: {len(context_chunks)}")
        return response


def test_qdrant_connection():
    """Test function to verify Qdrant connection"""
    try:
        agent = RAGAgent()
        # Try to list collections to test connection
        collections = agent.qdrant_client.get_collections()
        print(f"Connected successfully! Available collections: {[c.name for c in collections.collections]}")
        return True
    except Exception as e:
        print(f"Connection failed: {str(e)}")
        return False


def verify_apis():
    """Test function to verify API keys are working"""
    print("API verification not fully implemented in this template")
    # In a real implementation, we would test the actual APIs
    pass


def basic_test():
    """Basic test function"""
    print("Basic test not fully implemented in this template")
    # In a real implementation, we would run a simple query
    pass


if __name__ == "__main__":
    # Example usage
    agent = RAGAgent()

    # Example query using the traditional method
    print("--- Traditional Method ---")
    response = agent.query("What is ros2??")
    print(f"Answer: {response.content}")
    print(f"Generation time: {response.generation_time:.2f}s")
    print(f"Confidence: {response.confidence_score:.2f}")
    print(f"Context chunks used: {len(response.context_chunks_used)}")

    # Example query using the OpenAI Agent SDK method
    print("\n--- Using OpenAI Agent SDK (RAG from Qdrant) ---")
    response_agent = agent.query_with_agent("What is ros2??")
    print(f"Answer: {response_agent.content}")
    print(f"Generation time: {response_agent.generation_time:.2f}s")
    print(f"Confidence: {response_agent.confidence_score:.2f}")
    print(f"Context chunks used: {len(response_agent.context_chunks_used)}")