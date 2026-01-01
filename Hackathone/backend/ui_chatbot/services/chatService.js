/**
 * Chat Service for communicating with backend API
 */

import { API_URL, API_TIMEOUT } from '../utils/constants.js';
import { formatErrorMessage } from '../utils/formatters.js';

/**
 * Send a chat message to the backend API
 *
 * @param {string} query - User's question or message
 * @param {string} [highlightedText] - Optional highlighted text context
 * @returns {Promise<Object>} Response data or throws error
 */
export async function sendMessage(query, highlightedText = null) {
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), API_TIMEOUT);

  try {
    const requestBody = {
      query: query.trim(),
    };

    // Add highlighted text if provided
    if (highlightedText && highlightedText.trim()) {
      requestBody.highlighted_text = highlightedText.trim();
    }

    const response = await fetch(`${API_URL}/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(requestBody),
      signal: controller.signal,
    });

    clearTimeout(timeoutId);

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({
        error: 'UnknownError',
        message: `HTTP ${response.status}: ${response.statusText}`,
        code: 'HTTP_ERROR',
      }));

      throw new Error(errorData.message || 'Failed to get response');
    }

    const data = await response.json();

    // Validate response has required fields
    if (!data.content) {
      throw new Error('Invalid response: missing content');
    }

    return {
      id: data.response_id || generateId(),
      role: 'assistant',
      content: data.content,
      timestamp: data.timestamp || new Date().toISOString(),
      generationTime: data.generation_time || 0,
      confidenceScore: data.confidence_score || 0,
    };
  } catch (error) {
    clearTimeout(timeoutId);

    if (error.name === 'AbortError') {
      throw new Error('Request timed out. Please try again.');
    }

    if (error.name === 'TypeError' && error.message.includes('fetch')) {
      throw new Error('Unable to connect. Please check your internet connection.');
    }

    throw error;
  }
}

/**
 * Check backend health status
 *
 * @returns {Promise<Object>} Health status
 */
export async function checkHealth() {
  try {
    const response = await fetch(`${API_URL}/health`, {
      method: 'GET',
      signal: AbortSignal.timeout(5000), // 5 second timeout for health check
    });

    if (!response.ok) {
      throw new Error(`Health check failed: HTTP ${response.status}`);
    }

    const data = await response.json();
    return data;
  } catch (error) {
    if (error.name === 'AbortError') {
      throw new Error('Health check timed out');
    }
    throw error;
  }
}

/**
 * Send a chat message with context (page URL, title)
 *
 * @param {string} query - User's question
 * @param {string} [highlightedText] - Optional highlighted text
 * @param {string} [pageUrl] - Current page URL
 * @param {string} [pageTitle] - Current page title
 * @returns {Promise<Object>} Response data
 */
export async function sendMessageWithContext(query, highlightedText = null, pageUrl = null, pageTitle = null) {
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), API_TIMEOUT);

  try {
    const requestBody = {
      query: query.trim(),
    };

    // Add highlighted text if provided
    if (highlightedText && highlightedText.trim()) {
      requestBody.highlighted_text = highlightedText.trim();
    }

    // Add page context if provided
    if (pageUrl || pageTitle) {
      requestBody.context = {};
      if (pageUrl) {
        requestBody.context.page_url = pageUrl;
      }
      if (pageTitle) {
        requestBody.context.page_title = pageTitle;
      }
    }

    const response = await fetch(`${API_URL}/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(requestBody),
      signal: controller.signal,
    });

    clearTimeout(timeoutId);

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({
        error: 'UnknownError',
        message: `HTTP ${response.status}: ${response.statusText}`,
        code: 'HTTP_ERROR',
      }));

      throw new Error(errorData.message || 'Failed to get response');
    }

    const data = await response.json();

    // Validate response
    if (!data.content) {
      throw new Error('Invalid response: missing content');
    }

    return {
      id: data.response_id || generateId(),
      role: 'assistant',
      content: data.content,
      timestamp: data.timestamp || new Date().toISOString(),
      generationTime: data.generation_time || 0,
      confidenceScore: data.confidence_score || 0,
    };
  } catch (error) {
    clearTimeout(timeoutId);

    if (error.name === 'AbortError') {
      throw new Error('Request timed out. Please try again.');
    }

    if (error.name === 'TypeError' && error.message.includes('fetch')) {
      throw new Error('Unable to connect. Please check your internet connection.');
    }

    throw error;
  }
}

/**
 * Generate a unique ID (fallback if backend doesn't provide one)
 * @returns {string} UUID
 */
function generateId() {
  return `msg_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
}

/**
 * Retry a failed request with exponential backoff
 *
 * @param {Function} requestFn - Function that returns a Promise
 * @param {number} [maxRetries] - Maximum number of retries
 * @param {number} [baseDelay] - Base delay in ms
 * @returns {Promise<any>} Result of the request
 */
export async function retryRequest(requestFn, maxRetries = 3, baseDelay = 1000) {
  for (let attempt = 0; attempt < maxRetries; attempt++) {
    try {
      return await requestFn();
    } catch (error) {
      const isLastAttempt = attempt === maxRetries - 1;

      if (isLastAttempt) {
        throw error;
      }

      // Calculate delay with exponential backoff
      const delay = baseDelay * Math.pow(2, attempt);
      console.log(`Request failed (attempt ${attempt + 1}/${maxRetries}), retrying in ${delay}ms...`);

      await new Promise((resolve) => setTimeout(resolve, delay));
    }
  }

  throw new Error('Max retries exceeded');
}

export default {
  sendMessage,
  sendMessageWithContext,
  checkHealth,
  retryRequest,
};
