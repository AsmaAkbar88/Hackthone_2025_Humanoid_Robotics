import { useState, useCallback } from 'react';
import { apiClient } from '../services/api-client';

const useChat = () => {
  const [messages, setMessages] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [conversations, setConversations] = useState([]);
  const [userId, setUserId] = useState(null);

  // Get user ID from auth context or wherever it's stored
  const getUserId = () => {
    // This would typically come from your auth context
    // For now, we'll rely on the token being in the apiClient
    return userId;
  };

  const setUserIdLocal = (id) => {
    setUserId(id);
  };

  const sendMessage = useCallback(async (message, conversationId = null) => {
    // Extract user ID from the JWT token
    const token = apiClient.getAuthToken();
    if (!token) {
      throw new Error('No authentication token available');
    }

    // Parse the JWT token to extract user ID
    const parseJwt = (token) => {
      try {
        const base64Url = token.split('.')[1];
        const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
        const jsonPayload = decodeURIComponent(
          atob(base64)
            .split('')
            .map(c => '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2))
            .join('')
        );
        return JSON.parse(jsonPayload);
      } catch (error) {
        console.error('Error parsing JWT:', error);
        return null;
      }
    };

    const tokenPayload = parseJwt(token);
    if (!tokenPayload) {
      throw new Error('Invalid authentication token');
    }

    const userId = tokenPayload.sub || tokenPayload.userId;
    if (!userId) {
      throw new Error('User ID not found in token');
    }

    setIsLoading(true);
    setError(null);

    try {
      const response = await apiClient.post(`/chat/${userId}/chat`, {
        message,
        conversation_id: conversationId
      });

      if (response.data.success) {
        const { response: aiResponse, conversation_id: newConversationId, actions_taken } = response.data.data;

        // Add both user and AI messages to the conversation
        const newUserMessage = {
          id: Date.now(),
          role: 'user',
          content: message,
          timestamp: new Date().toISOString()
        };

        const newAiMessage = {
          id: Date.now() + 1,
          role: 'assistant',
          content: aiResponse,
          timestamp: new Date().toISOString(),
          actionsTaken: actions_taken || []  // Ensure this is always an array
        };

        setMessages(prev => [...prev, newUserMessage, newAiMessage]);

        // Return the conversation ID and actions taken for continued conversation
        return {
          success: true,
          conversationId: newConversationId,
          actions_taken: actions_taken || []
        };
      } else {
        throw new Error(response.data.message || 'Failed to process message');
      }
    } catch (err) {
      setError(err.response?.data?.detail || err.message || 'An error occurred while sending the message');
      return { success: false, error: err.response?.data?.detail || err.message || 'An error occurred while sending the message' };
    } finally {
      setIsLoading(false);
    }
  }, []);

  const loadConversations = useCallback(async () => {
    // Extract user ID from the JWT token
    const token = apiClient.getAuthToken();
    if (!token) {
      throw new Error('No authentication token available');
    }

    // Parse the JWT token to extract user ID
    const parseJwt = (token) => {
      try {
        const base64Url = token.split('.')[1];
        const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
        const jsonPayload = decodeURIComponent(
          atob(base64)
            .split('')
            .map(c => '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2))
            .join('')
        );
        return JSON.parse(jsonPayload);
      } catch (error) {
        console.error('Error parsing JWT:', error);
        return null;
      }
    };

    const tokenPayload = parseJwt(token);
    if (!tokenPayload) {
      throw new Error('Invalid authentication token');
    }

    const userId = tokenPayload.sub || tokenPayload.userId;
    if (!userId) {
      throw new Error('User ID not found in token');
    }

    try {
      const response = await apiClient.get(`/chat/${userId}/conversations`);

      if (response.data.success) {
        setConversations(response.data.data.conversations);
      } else {
        throw new Error(response.data.message || 'Failed to load conversations');
      }
    } catch (err) {
      setError(err.response?.data?.detail || err.message || 'An error occurred while loading conversations');
    }
  }, []);

  const loadConversationHistory = useCallback(async (conversationId) => {
    // Extract user ID from the JWT token
    const token = apiClient.getAuthToken();
    if (!token) {
      throw new Error('No authentication token available');
    }

    // Parse the JWT token to extract user ID
    const parseJwt = (token) => {
      try {
        const base64Url = token.split('.')[1];
        const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
        const jsonPayload = decodeURIComponent(
          atob(base64)
            .split('')
            .map(c => '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2))
            .join('')
        );
        return JSON.parse(jsonPayload);
      } catch (error) {
        console.error('Error parsing JWT:', error);
        return null;
      }
    };

    const tokenPayload = parseJwt(token);
    if (!tokenPayload) {
      throw new Error('Invalid authentication token');
    }

    const userId = tokenPayload.sub || tokenPayload.userId;
    if (!userId) {
      throw new Error('User ID not found in token');
    }

    try {
      const response = await apiClient.get(`/chat/${userId}/conversations/${conversationId}`);

      if (response.data.success) {
        const { messages } = response.data.data.conversation;
        // Convert server messages to our format
        const formattedMessages = messages.map(msg => ({
          id: msg.id,
          role: msg.role,
          content: msg.content,
          timestamp: msg.timestamp,
        }));
        setMessages(formattedMessages);
      } else {
        throw new Error(response.data.message || 'Failed to load conversation history');
      }
    } catch (err) {
      setError(err.response?.data?.detail || err.message || 'An error occurred while loading conversation history');
    }
  }, []);

  const clearMessages = useCallback(() => {
    setMessages([]);
    setError(null);
  }, []);

  return {
    messages,
    isLoading,
    error,
    conversations,
    userId,
    setUserId: setUserIdLocal,
    sendMessage,
    loadConversations,
    loadConversationHistory,
    clearMessages,
  };
};

export default useChat;