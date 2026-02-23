import { useState, useCallback } from 'react';
import { apiClient } from '../services/api-client';

interface MessageAction {
  action: string;
  details?: string;
  params?: any;
}

interface Message {
  id: string | number;
  role: 'user' | 'assistant';
  content: string;
  timestamp?: string;
  actionsTaken?: MessageAction[];
}

interface Conversation {
  id: string;
  title: string;
  created_at: string;
}

interface SendMessageResponse {
  success: boolean;
  conversationId?: string;
  actions_taken?: MessageAction[];
  error?: string;
}

interface ChatResponseData {
  response: string;
  conversation_id: string;
  actions_taken?: MessageAction[];
}

interface ApiResponse<T> {
  data: {
    success: boolean;
    data: T;
    message?: string;
  };
}

const useChat = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const [conversations, setConversations] = useState<Conversation[]>([]);
  const [userId, setUserId] = useState<string | null>(null);

  // Get user ID from auth context or wherever it's stored
  const getUserId = () => {
    // This would typically come from your auth context
    // For now, we'll rely on the token being in the apiClient
    return userId;
  };

  const setUserIdLocal = (id: string | null) => {
    setUserId(id);
  };

  const sendMessage = useCallback(async (message: string, conversationId: string | null = null): Promise<SendMessageResponse> => {
    // Extract user ID from the JWT token
    const token = apiClient.getAuthToken();
    if (!token) {
      throw new Error('No authentication token available');
    }

    // Parse the JWT token to extract user ID
    const parseJwt = (token: string): any => {
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
      const response: ApiResponse<ChatResponseData> = await apiClient.post(`/chat/${userId}/chat`, {
        message,
        conversation_id: conversationId
      });

      if (response.data.success) {
        const { response: aiResponse, conversation_id: newConversationId, actions_taken } = response.data.data;

        // Add both user and AI messages to the conversation
        const newUserMessage: Message = {
          id: Date.now().toString(),
          role: 'user',
          content: message,
          timestamp: new Date().toISOString()
        };

        const newAiMessage: Message = {
          id: (Date.now() + 1).toString(),
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
    } catch (err: any) {
      setError(err.response?.data?.detail || err.message || 'An error occurred while sending the message');
      return { success: false, error: err.response?.data?.detail || err.message || 'An error occurred while sending the message' };
    } finally {
      setIsLoading(false);
    }
  }, []);

  const loadConversations = useCallback(async (): Promise<void> => {
    // Extract user ID from the JWT token
    const token = apiClient.getAuthToken();
    if (!token) {
      throw new Error('No authentication token available');
    }

    // Parse the JWT token to extract user ID
    const parseJwt = (token: string): any => {
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
      const response: ApiResponse<{ conversations: Conversation[] }> = await apiClient.get(`/chat/${userId}/conversations`);

      if (response.data.success) {
        setConversations(response.data.data.conversations);
      } else {
        throw new Error(response.data.message || 'Failed to load conversations');
      }
    } catch (err: any) {
      setError(err.response?.data?.detail || err.message || 'An error occurred while loading conversations');
    }
  }, []);

  const loadConversationHistory = useCallback(async (conversationId: string): Promise<void> => {
    // Extract user ID from the JWT token
    const token = apiClient.getAuthToken();
    if (!token) {
      throw new Error('No authentication token available');
    }

    // Parse the JWT token to extract user ID
    const parseJwt = (token: string): any => {
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
      const response: ApiResponse<{ conversation: { messages: { id: string | number; role: 'user' | 'assistant'; content: string; timestamp: string; }[] } }> = await apiClient.get(`/chat/${userId}/conversations/${conversationId}`);

      if (response.data.success) {
        const { messages } = response.data.data.conversation;
        // Convert server messages to our format
        const formattedMessages: Message[] = messages.map(msg => ({
          id: msg.id,
          role: msg.role,
          content: msg.content,
          timestamp: msg.timestamp,
        }));
        setMessages(formattedMessages);
      } else {
        throw new Error(response.data.message || 'Failed to load conversation history');
      }
    } catch (err: any) {
      setError(err.response?.data?.detail || err.message || 'An error occurred while loading conversation history');
    }
  }, []);

  const clearMessages = useCallback((): void => {
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