/**
 * Chat Service - API communication layer for chat functionality
 * Connects to the backend API for RAG-powered chat responses
 *
 * To run the backend:
 * 1. Navigate to the backend directory: cd ../backend
 * 2. Install dependencies: pip install -r requirements.txt
 * 3. Set up environment variables in a .env file
 * 4. Run the server: uvicorn api.index:app --reload --port 3000
 */

// Update the API_BASE_URL to point to your deployed backend
// Using window.env or default fallback since Docusaurus doesn't have process.env
const API_BASE_URL =
  (typeof window !== 'undefined' && window.env && window.env.REACT_APP_API_URL) ||
  (typeof process !== 'undefined' && process.env.REACT_APP_API_URL) ||
  'http://localhost:8000';  // Default to local development server (backend routes are at root level)

/**
 * Sends a message to the backend API
 * @param {string} message - The user's message
 * @param {string|null} highlightedContext - Optional highlighted text context
 * @param {Object|null} context - Optional page context metadata
 * @returns {Promise<Object>} Response from the backend API
 */
export async function sendMessage(message, highlightedContext = null, context = null) {
  // Validate message length (minimum 5 characters as required by backend)
  if (!message || message.trim().length < 5) {
    throw new Error('Message must be at least 5 characters long');
  }

  try {
    const response = await fetch(`${API_BASE_URL}/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        query: message.trim(),
        highlighted_text: highlightedContext || null,
        context: context || null
      }),
    });

    if (!response.ok) {
      // Check if response is HTML (indicates server error page)
      const contentType = response.headers.get('content-type');
      if (contentType && contentType.includes('text/html')) {
        const htmlText = await response.text();
        console.error('Received HTML error page:', htmlText);
        throw new Error('Backend server returned an error page instead of JSON response');
      }

      const error = await response.json();
      throw new Error(error.message || 'Failed to get response');
    }

    // Check if response is HTML (indicates server error page)
    const contentType = response.headers.get('content-type');
    if (contentType && contentType.includes('text/html')) {
      const htmlText = await response.text();
      console.error('Received HTML instead of JSON:', htmlText);
      throw new Error('Backend server returned HTML instead of JSON response');
    }

    const data = await response.json();

    return {
      id: data.response_id,
      content: data.content,
      timestamp: data.timestamp,
      generationTime: data.generation_time,
      confidenceScore: data.confidence_score
    };
  } catch (error) {
    console.error('Chat API error:', error);
    // Fallback response when backend is not available
    if (error.name === 'TypeError' && error.message.includes('fetch')) {
      return {
        id: Date.now().toString(),
        content: "Backend API is not available. Please check that your backend is deployed and the API URL is configured correctly.",
        timestamp: new Date().toISOString(),
        generationTime: 0,
        confidenceScore: 0
      };
    }
    // Handle JSON parsing errors (like "Unexpected token '<'")
    if (error instanceof SyntaxError && error.message.includes('Unexpected token')) {
      return {
        id: Date.now().toString(),
        content: "Backend API returned invalid response format. The server might be down or misconfigured.",
        timestamp: new Date().toISOString(),
        generationTime: 0,
        confidenceScore: 0
      };
    }
    // Handle service unavailable errors (like rate limiting)
    if (error.message && error.message.includes('503')) {
      return {
        id: Date.now().toString(),
        content: "The service is temporarily busy. Please wait a few seconds and try again. This may be due to API rate limits.",
        timestamp: new Date().toISOString(),
        generationTime: 0,
        confidenceScore: 0
      };
    }
    throw error;
  }
}

/**
 * Health check function to verify backend connectivity
 * @returns {Promise<Object>} Health check response
 */
export async function healthCheck() {
  try {
    const response = await fetch(`${API_BASE_URL}/health`);

    // Check if response is HTML (indicates server error page)
    const contentType = response.headers.get('content-type');
    if (contentType && contentType.includes('text/html')) {
      const htmlText = await response.text();
      console.error('Health check received HTML error page:', htmlText);
      return { status: 'unhealthy', details: { error: 'Server returned HTML instead of JSON' } };
    }

    return await response.json();
  } catch (error) {
    console.error('Health check failed:', error);
    return { status: 'unhealthy', details: {} };
  }
}

// Additional API functions could be added here:
// export async function getChatHistory(sessionId) { ... }
// export async function createNewSession() { ... }
// export async function deleteMessage(messageId) { ... }