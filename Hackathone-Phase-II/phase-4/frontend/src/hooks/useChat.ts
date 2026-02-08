import { useState, useCallback } from 'react';
import axios from 'axios';

interface Message {
  id: string | number;
  role: 'user' | 'assistant';
  content: string;
  timestamp: string;
  actionsTaken?: Array<{ action: string; details: string }>;
}

interface Conversation {
  id: string;
  title: string;
  created_at: string;
}

interface SendMessageResponse {
  success: boolean;
  conversationId?: string;
  error?: string;
}

const useChat = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [conversations, setConversations] = useState<Conversation[]>([]);

  // Get user ID from auth context or wherever it's stored
  const getUserId = (): string | null => {
    // This would typically come from your auth context
    if (typeof window !== 'undefined') {
      const userStr = localStorage.getItem('user');
      if (userStr) {
        try {
          const user = JSON.parse(userStr);
          return user.id || null;
        } catch (e) {
          console.error('Error parsing user from localStorage:', e);
          return null;
        }
      }
    }
    return null;
  };

  const sendMessage = useCallback(async (message: string, conversationId: string | null = null): Promise<SendMessageResponse> => {
    const userId = getUserId();
    if (!userId) {
      setError('User not authenticated');
      return { success: false, error: 'User not authenticated' };
    }

    setIsLoading(true);
    setError(null);

    try {
      const response = await axios.post(`${process.env.NEXT_PUBLIC_API_BASE_URL}/chat/${userId}`, {
        message,
        conversation_id: conversationId
      }, {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('auth-token') || ''}`,
          'Content-Type': 'application/json'
        }
      });

      if (response.data.success) {
        const { response: aiResponse, conversation_id: newConversationId, actions_taken } = response.data.data;

        // Add both user and AI messages to the conversation
        const newUserMessage: Message = {
          id: Date.now(),
          role: 'user',
          content: message,
          timestamp: new Date().toISOString()
        };

        const newAiMessage: Message = {
          id: Date.now() + 1,
          role: 'assistant',
          content: aiResponse,
          timestamp: new Date().toISOString(),
          actionsTaken: actions_taken
        };

        setMessages(prev => [...prev, newUserMessage, newAiMessage]);

        // Return the conversation ID for continued conversation
        return { success: true, conversationId: newConversationId };
      } else {
        const errorMsg = response.data.message || 'Failed to process message';
        throw new Error(errorMsg);
      }
    } catch (err: any) {
      const errorMessage = err.response?.data?.detail || err.message || 'An error occurred while sending the message';
      setError(errorMessage);
      return { success: false, error: errorMessage };
    } finally {
      setIsLoading(false);
    }
  }, []);

  const loadConversations = useCallback(async () => {
    const userId = getUserId();
    if (!userId) {
      setError('User not authenticated');
      return;
    }

    try {
      const response = await axios.get(`${process.env.NEXT_PUBLIC_API_BASE_URL}/chat/${userId}/conversations`, {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('auth-token') || ''}`
        }
      });

      if (response.data.success) {
        setConversations(response.data.data.conversations);
      } else {
        throw new Error(response.data.message || 'Failed to load conversations');
      }
    } catch (err: any) {
      const errorMessage = err.response?.data?.detail || err.message || 'An error occurred while loading conversations';
      setError(errorMessage);
    }
  }, []);

  const loadConversationHistory = useCallback(async (conversationId: string) => {
    const userId = getUserId();
    if (!userId) {
      setError('User not authenticated');
      return;
    }

    try {
      const response = await axios.get(`${process.env.NEXT_PUBLIC_API_BASE_URL}/chat/${userId}/conversations/${conversationId}`, {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('auth-token') || ''}`
        }
      });

      if (response.data.success) {
        const { messages } = response.data.data.conversation;
        // Convert server messages to our format
        const formattedMessages: Message[] = messages.map((msg: any) => ({
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
      const errorMessage = err.response?.data?.detail || err.message || 'An error occurred while loading conversation history';
      setError(errorMessage);
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
    sendMessage,
    loadConversations,
    loadConversationHistory,
    clearMessages,
  };
};

export default useChat;