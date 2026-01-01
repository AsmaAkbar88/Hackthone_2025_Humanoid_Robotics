/**
 * useChat - Updated custom React hook for chat state management
 * Manages chat messages, API calls, loading states, errors, and highlighted text
 */

import { useState, useCallback, useRef, useEffect } from 'react';
import { sendMessage } from '../services/chatService.js';
import { generateId, formatDateTime } from '../utils/formatters.js';
import {
  MIN_QUERY_LENGTH,
  MAX_QUERY_LENGTH,
  MAX_HIGHLIGHT_LENGTH,
  MAX_MESSAGES_PER_SESSION,
} from '../utils/constants.js';

/**
 * Custom hook for managing chat functionality with highlight support
 * @returns {Object} Chat state and functions
 */
export function useChat() {
  // Chat session state
  const [messages, setMessages] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [isOpen, setIsOpen] = useState(false);
  const [unreadCount, setUnreadCount] = useState(0);
  const [highlightedText, setHighlightedText] = useState(null);

  // Refs for managing focus and previous state
  const messagesEndRef = useRef(null);
  const chatInputRef = useRef(null);
  const widgetIconRef = useRef(null);
  const wasOpenRef = useRef(false);

  /**
   * Auto-scroll to bottom of messages when new messages arrive
   */
  const scrollToBottom = useCallback(() => {
    if (messagesEndRef.current) {
      messagesEndRef.current.scrollTop = messagesEndRef.current.scrollHeight;
    }
  }, []);

  /**
   * Send a message to the chat API
   * @param {string} query - User's question or message
   * @param {string} [highlightedContext] - Optional highlighted text context
   */
  const sendMessage = useCallback(
    async (query, highlightedContext = null) => {
      // Validate query length
      if (!query || query.trim().length < MIN_QUERY_LENGTH) {
        setError(`Query must be at least ${MIN_QUERY_LENGTH} characters long`);
        return;
      }

      if (query.trim().length > MAX_QUERY_LENGTH) {
        setError(`Query must not exceed ${MAX_QUERY_LENGTH} characters`);
        return;
      }

      // Validate highlighted text length
      if (highlightedContext && highlightedContext.length > MAX_HIGHLIGHT_LENGTH) {
        setError(`Highlighted text must not exceed ${MAX_HIGHLIGHT_LENGTH} characters`);
        return;
      }

      // Clear any previous error
      setError(null);

      // Create user message
      const userMessage = {
        id: generateId(),
        role: 'user',
        content: query.trim(),
        timestamp: new Date().toISOString(),
        highlightedContext: highlightedContext || null,
      };

      // Add user message to chat history
      setMessages((prev) => {
        const newMessages = [...prev, userMessage];
        // Limit to max messages per session
        if (newMessages.length > MAX_MESSAGES_PER_SESSION) {
          return newMessages.slice(newMessages.length - MAX_MESSAGES_PER_SESSION);
        }
        return newMessages;
      });

      // Set loading state
      setIsLoading(true);

      try {
        // Send to backend API with highlighted context
        const responseData = await sendMessage(
          userMessage.content,
          highlightedContext || null
        );

        // Create assistant message from response
        const assistantMessage = {
          id: responseData.id || generateId(),
          role: 'assistant',
          content: responseData.content,
          timestamp: responseData.timestamp || new Date().toISOString(),
          generationTime: responseData.generationTime,
          confidenceScore: responseData.confidenceScore,
        };

        // Add assistant message to chat history
        setMessages((prev) => {
          const newMessages = [...prev, assistantMessage];
          // Limit to max messages per session
          if (newMessages.length > MAX_MESSAGES_PER_SESSION) {
            return newMessages.slice(newMessages.length - MAX_MESSAGES_PER_SESSION);
          }
          return newMessages;
        });

        // Update unread count if chat is closed
        if (!isOpen) {
          setUnreadCount((prev) => prev + 1);
        }
      } catch (err) {
        // Create system error message
        const errorMessage = {
          id: generateId(),
          role: 'system',
          content: err.message || 'Failed to send message. Please try again.',
          timestamp: new Date().toISOString(),
          error: err.message,
        };

        setMessages((prev) => {
          const newMessages = [...prev, errorMessage];
          if (newMessages.length > MAX_MESSAGES_PER_SESSION) {
            return newMessages.slice(newMessages.length - MAX_MESSAGES_PER_SESSION);
          }
          return newMessages;
        });

        setError(err.message || 'Failed to send message. Please try again.');
      } finally {
        setIsLoading(false);
      }
    },
    [isOpen, MIN_QUERY_LENGTH, MAX_QUERY_LENGTH, MAX_HIGHLIGHT_LENGTH, MAX_MESSAGES_PER_SESSION]
  );

  /**
   * Clear all messages from chat
   */
  const clearChat = useCallback(() => {
    setMessages([]);
    setError(null);
    setUnreadCount(0);
  }, []);

  /**
   * Toggle chat panel open/closed
   */
  const toggleChat = useCallback(() => {
    setIsOpen((prev) => {
      const newState = !prev;
      wasOpenRef.current = prev;

      // Reset unread count when opening chat
      if (newState && !prev) {
        setUnreadCount(0);

        // Focus input when opening
        setTimeout(() => {
          if (chatInputRef.current) {
            chatInputRef.current.focus();
          }
        }, 100);
      }

      // Return focus to widget icon when closing
      if (!newState && prev && widgetIconRef.current) {
        setTimeout(() => {
          widgetIconRef.current.focus();
        }, 300);
      }

      return newState;
    });
  }, []);

  /**
   * Set highlighted text for context
   * @param {string} text - Highlighted text
   */
  const setHighlighted = useCallback((text) => {
    setHighlightedText(text);
  }, []);

  /**
   * Clear highlighted text
   */
  const clearHighlighted = useCallback(() => {
    setHighlightedText(null);
  }, []);

  /**
   * Handle keyboard shortcuts
   * @param {KeyboardEvent} event - Keyboard event
   */
  const handleKeyDown = useCallback(
    (event) => {
      if (!isOpen) return;

      // Escape key closes chat
      if (event.key === 'Escape') {
        toggleChat();
      }
    },
    [isOpen, toggleChat]
  );

  // Auto-scroll to bottom when messages change
  useEffect(() => {
    if (messages.length > 0) {
      scrollToBottom();
    }
  }, [messages, scrollToBottom]);

  // Add/remove keyboard event listener
  useEffect(() => {
    if (isOpen) {
      document.addEventListener('keydown', handleKeyDown);
    }

    return () => {
      document.removeEventListener('keydown', handleKeyDown);
    };
  }, [isOpen, handleKeyDown]);

  // Update unread count when chat closes with new messages
  useEffect(() => {
    if (wasOpenRef.current && !isOpen && messages.length > 0) {
      // Count messages added after last close
      // This is a simple implementation - could be enhanced
    }
  }, [isOpen, messages.length]);

  return {
    // Chat state
    messages,
    isLoading,
    error,
    isOpen,
    unreadCount,
    highlightedText,

    // Actions
    sendMessage,
    clearChat,
    toggleChat,
    setHighlighted,
    clearHighlighted,

    // Refs
    messagesEndRef,
    chatInputRef,
    widgetIconRef,
  };
}

export default useChat;
