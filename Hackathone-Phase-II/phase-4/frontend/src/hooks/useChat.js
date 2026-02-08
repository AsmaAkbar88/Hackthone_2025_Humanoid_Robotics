import { useState, useCallback } from 'react';
import axios from 'axios';

const useChat = () => {
  const [messages, setMessages] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [conversations, setConversations] = useState([]);

  // Get user ID from auth context or wherever it's stored
  const getUserId = () => {
    // This would typically come from your auth context
    const user = typeof window !== 'undefined' ? JSON.parse(localStorage.getItem('user') || '{}') : {};
    return user.id || null;
  };

  const sendMessage = useCallback(async (message, conversationId = null) => {
    const userId = getUserId();
    if (!userId) {
      setError('User not authenticated');
      return;
    }

    setIsLoading(true);
    setError(null);

    try {
      const response = await axios.post(`${process.env.NEXT_PUBLIC_API_BASE_URL}/chat/${userId}`, {
        message,
        conversation_id: conversationId
      }, {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('auth-token')}`,
          'Content-Type': 'application/json'
        }
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
          actionsTaken: actions_taken
        };

        setMessages(prev => [...prev, newUserMessage, newAiMessage]);
        
        // Return the conversation ID for continued conversation
        return { success: true, conversationId: newConversationId };
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
    const userId = getUserId();
    if (!userId) {
      setError('User not authenticated');
      return;
    }

    try {
      const response = await axios.get(`${process.env.NEXT_PUBLIC_API_BASE_URL}/chat/${userId}/conversations`, {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('auth-token')}`
        }
      });

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
    const userId = getUserId();
    if (!userId) {
      setError('User not authenticated');
      return;
    }

    try {
      const response = await axios.get(`${process.env.NEXT_PUBLIC_API_BASE_URL}/chat/${userId}/conversations/${conversationId}`, {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('auth-token')}`
        }
      });

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
    sendMessage,
    loadConversations,
    loadConversationHistory,
    clearMessages,
  };
};

export default useChat;