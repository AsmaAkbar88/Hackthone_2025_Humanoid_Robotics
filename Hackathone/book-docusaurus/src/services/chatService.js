import { API_URL, API_TIMEOUT } from '../utils/constants';
import { generateId } from '../utils/formatters';

export async function sendMessage(query, highlightedText = null) {
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), API_TIMEOUT);

  try {
    const requestBody = {
      query: query.trim(),
    };

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
      throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    }

    const data = await response.json();

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

    throw error;
  }
}

export default { sendMessage };
