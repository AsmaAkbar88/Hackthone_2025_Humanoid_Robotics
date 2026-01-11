#  uvicorn api:app --reload
# uvicorn api.index:app_instance --reload

# uvicorn api.index:app_instance --port 8000 --host 127.0.0.1
import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import cohere
from qdrant_client import QdrantClient
from qdrant_client.http import models
from dotenv import load_dotenv
import logging
import time
from typing import List, Dict, Any
import uuid

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def get_all_urls(base_url: str, max_depth: int = 1) -> List[str]:
    """
    Crawl the documentation site and return all accessible URLs.

    Args:
        base_url: The base URL of the documentation site
        max_depth: Maximum depth to crawl (currently only supports 1 level)

    Returns:
        List of URLs found on the site
    """
    urls = set()
    urls.add(base_url)

    try:
        response = requests.get(base_url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all links on the page
        for link in soup.find_all('a', href=True):
            href = link['href']
            full_url = urljoin(base_url, href)

            # Only add URLs from the same domain
            if urlparse(full_url).netloc == urlparse(base_url).netloc:
                urls.add(full_url)

        logger.info(f"Found {len(urls)} URLs from {base_url}")
        return list(urls)

    except requests.RequestException as e:
        logger.error(f"Error crawling {base_url}: {str(e)}")
        return [base_url]  # Return the base URL as fallback


def extract_text_from_url(url: str) -> Dict[str, Any]:
    """
    Extract clean text content from a URL.

    Args:
        url: The URL to extract text from

    Returns:
        Dictionary with 'url', 'title', and 'content' keys
    """
    try:
        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()

        # Get title
        title_tag = soup.find('title')
        title = title_tag.get_text().strip() if title_tag else "No Title"

        # Try to find main content area (common selectors for documentation sites)
        content_selectors = [
            'main',  # Most common for modern sites
            '.main-content',  # Common class
            '.content',  # Common class
            '.doc-content',  # Documentation sites
            '.documentation-content',  # Documentation sites
            '.article-content',  # Article-style content
            'article',  # HTML5 article tag
            '.post-content',  # Blog-style content
            'body'  # Fallback
        ]

        content = ""
        for selector in content_selectors:
            element = soup.select_one(selector)
            if element:
                content = element.get_text(separator=' ', strip=True)
                break

        # If no content found with selectors, get from body
        if not content:
            body = soup.find('body')
            if body:
                content = body.get_text(separator=' ', strip=True)

        # Clean up the content
        lines = (line.strip() for line in content.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        content = ' '.join(chunk for chunk in chunks if chunk)

        logger.info(f"Extracted content from {url} (title: {title[:50]}...)")

        return {
            'url': url,
            'title': title,
            'content': content
        }

    except requests.RequestException as e:
        logger.error(f"Error extracting content from {url}: {str(e)}")
        return {
            'url': url,
            'title': "Error",
            'content': ""
        }
    except Exception as e:
        logger.error(f"Unexpected error extracting content from {url}: {str(e)}")
        return {
            'url': url,
            'title': "Error",
            'content': ""
        }


def chunk_text(text: str, chunk_size: int = 1000, overlap: int = 100) -> List[Dict[str, Any]]:
    """
    Split text into chunks of specified size with overlap.

    Args:
        text: The text to chunk
        chunk_size: Maximum size of each chunk
        overlap: Number of characters to overlap between chunks

    Returns:
        List of dictionaries with 'id', 'content', 'chunk_index', and 'metadata'
    """
    if not text:
        return []

    chunks = []
    start = 0
    chunk_index = 0

    while start < len(text):
        end = start + chunk_size

        # If this is the last chunk, include the rest
        if end >= len(text):
            end = len(text)
        else:
            # Try to break at sentence boundary
            while end > start + chunk_size - overlap and end < len(text) and text[end] not in '.!?':
                end += 1
            if end == start + chunk_size - overlap:  # If no sentence boundary found, just cut at chunk_size
                end = start + chunk_size

        chunk_content = text[start:end].strip()

        if chunk_content:  # Only add non-empty chunks
            chunk = {
                'id': str(uuid.uuid4()),
                'content': chunk_content,
                'chunk_index': chunk_index,
                'metadata': {}
            }
            chunks.append(chunk)

        start = end - overlap if end < len(text) else end
        chunk_index += 1

    logger.info(f"Text chunked into {len(chunks)} pieces")
    return chunks


def embed(texts: List[str]) -> List[List[float]]:
    """
    Generate embeddings for a list of texts using Cohere.

    Args:
        texts: List of texts to embed

    Returns:
        List of embedding vectors
    """
    cohere_api_key = os.getenv('COHERE_API_KEY')
    if not cohere_api_key:
        raise ValueError("COHERE_API_KEY environment variable is not set")

    co = cohere.Client(cohere_api_key)

    try:
        response = co.embed(
            texts=texts,
            model="embed-english-v3.0",  # Using a common Cohere embedding model
            input_type="search_document"  # Appropriate for document search
        )

        logger.info(f"Generated embeddings for {len(texts)} text chunks")
        return [embedding for embedding in response.embeddings]

    except Exception as e:
        logger.error(f"Error generating embeddings: {str(e)}")
        raise


def create_collection(client: QdrantClient, collection_name: str = "new_rag_embedding"):
    """
    Create a Qdrant collection for storing embeddings.

    Args:
        client: Qdrant client instance
        collection_name: Name of the collection to create
    """
    try:
        # Check if collection already exists
        collections = client.get_collections()
        collection_names = [col.name for col in collections.collections]

        if collection_name in collection_names:
            logger.info(f"Collection '{collection_name}' already exists")
            return

        # Create the collection
        client.create_collection(
            collection_name=collection_name,
            vectors_config=models.VectorParams(
                size=1024,  # Cohere embeddings are typically 1024 dimensions
                distance=models.Distance.COSINE
            )
        )

        logger.info(f"Created collection '{collection_name}' successfully")

    except Exception as e:
        logger.error(f"Error creating collection '{collection_name}': {str(e)}")
        raise


def save_chunk_to_qdrant(client: QdrantClient, chunk: Dict[str, Any], embedding: List[float],
                        collection_name: str = "new_rag_embedding"):
    """
    Save a text chunk with its embedding to Qdrant.

    Args:
        client: Qdrant client instance
        chunk: Dictionary containing chunk information
        embedding: Embedding vector for the chunk
        collection_name: Name of the collection to save to
    """
    try:
        # Prepare the payload
        payload = {
            'content': chunk['content'],
            'url': chunk.get('source_url', ''),
            'title': chunk.get('title', ''),
            'chunk_index': chunk['chunk_index'],
            'metadata': chunk.get('metadata', {}),
            'created_at': time.time()
        }

        # Prepare the point to be inserted
        point = models.PointStruct(
            id=chunk['id'],
            vector=embedding,
            payload=payload
        )

        # Upsert the point
        client.upsert(
            collection_name=collection_name,
            points=[point]
        )

        logger.info(f"Saved chunk {chunk['id']} to Qdrant collection '{collection_name}'")

    except Exception as e:
        logger.error(f"Error saving chunk {chunk['id']} to Qdrant: {str(e)}")
        raise


def setup_cohere_client():
    """
    Set up and return a Cohere client.

    Returns:
        Cohere client instance
    """
    cohere_api_key = os.getenv('COHERE_API_KEY')
    if not cohere_api_key:
        raise ValueError("COHERE_API_KEY environment variable is not set")

    return cohere.Client(cohere_api_key)


def setup_qdrant_client():
    """
    Set up and return a Qdrant client.

    Returns:
        Qdrant client instance
    """
    qdrant_url = os.getenv('QDRANT_URL')
    qdrant_api_key = os.getenv('QDRANT_API_KEY')

    if not qdrant_url:
        raise ValueError("QDRANT_URL environment variable is not set")

    if not qdrant_api_key:
        raise ValueError("QDRANT_API_KEY environment variable is not set")

    return QdrantClient(
        url=qdrant_url,
        api_key=qdrant_api_key
    )


def main():
    """
    Main function to execute the complete pipeline:
    1. Crawl documentation site
    2. Extract and clean text content
    3. Chunk the text
    4. Generate embeddings
    5. Store in Qdrant
    """
    logger.info("Starting Docusaurus Content Embedding Pipeline")

    # Target documentation site
    target_url = "https://book-three-eta.vercel.app/"

    try:
        # Setup clients
        logger.info("Setting up Cohere and Qdrant clients...")
        qdrant_client = setup_qdrant_client()

        # Create collection
        logger.info("Creating Qdrant collection...")
        create_collection(qdrant_client, "new_rag_embedding")

        # Get all URLs from the documentation site
        logger.info(f"Crawling documentation site: {target_url}")
        urls = get_all_urls(target_url)
        logger.info(f"Found {len(urls)} URLs to process")

        # Process each URL
        processed_count = 0
        for url in urls:
            try:
                logger.info(f"Processing URL: {url}")

                # Extract text content from the URL
                content_data = extract_text_from_url(url)

                if not content_data['content']:
                    logger.warning(f"No content extracted from {url}, skipping...")
                    continue

                # Chunk the text
                chunks = chunk_text(content_data['content'])

                if not chunks:
                    logger.warning(f"No chunks created from {url}, skipping...")
                    continue

                # Add source URL to each chunk
                for chunk in chunks:
                    chunk['source_url'] = url
                    chunk['title'] = content_data['title']

                # Process chunks in batches to handle API limits
                batch_size = 5  # Conservative batch size for Cohere API
                for i in range(0, len(chunks), batch_size):
                    batch = chunks[i:i + batch_size]

                    # Extract text content for embedding
                    texts_to_embed = [chunk['content'] for chunk in batch]

                    # Generate embeddings
                    logger.info(f"Generating embeddings for batch {i//batch_size + 1}...")
                    embeddings = embed(texts_to_embed)

                    # Save each chunk with its embedding to Qdrant
                    for chunk, embedding in zip(batch, embeddings):
                        save_chunk_to_qdrant(qdrant_client, chunk, embedding)

                processed_count += 1
                logger.info(f"Successfully processed {url}")

            except Exception as e:
                logger.error(f"Error processing {url}: {str(e)}")
                continue  # Continue with next URL even if one fails

        logger.info(f"Pipeline completed successfully. Processed {processed_count}/{len(urls)} URLs.")

    except Exception as e:
        logger.error(f"Pipeline failed with error: {str(e)}")
        raise


if __name__ == "__main__":
    main()