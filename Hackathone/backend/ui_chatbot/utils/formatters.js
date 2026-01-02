/**
 * Formatting utilities for chatbot UI
 */

import { v4 as uuidv4 } from 'uuid';

/**
 * Generate a unique ID
 * @returns {string} UUID
 */
export const generateId = () => {
  return uuidv4();
};

/**
 * Format message content for display
 * @param {string} content - Raw message content
 * @returns {string} Formatted content (line breaks preserved)
 */
export const formatMessage = (content) => {
  if (!content) return '';

  // Preserve line breaks
  return content.replace(/\n/g, '<br />');
};

/**
 * Format ISO timestamp to readable time
 * @param {string} isoTimestamp - ISO8601 timestamp
 * @returns {string} Formatted time (e.g., "10:30 AM")
 */
export const formatTimestamp = (isoTimestamp) => {
  if (!isoTimestamp) return '';

  try {
    const date = new Date(isoTimestamp);
    return date.toLocaleTimeString('en-US', {
      hour: 'numeric',
      minute: '2-digit',
      hour12: true
    });
  } catch (error) {
    console.error('Error formatting timestamp:', error);
    return '';
  }
};

/**
 * Format ISO timestamp to readable date and time
 * @param {string} isoTimestamp - ISO8601 timestamp
 * @returns {string} Formatted date/time (e.g., "Dec 30, 2025 at 10:30 AM")
 */
export const formatDateTime = (isoTimestamp) => {
  if (!isoTimestamp) return '';

  try {
    const date = new Date(isoTimestamp);
    return date.toLocaleString('en-US', {
      month: 'short',
      day: 'numeric',
      year: 'numeric',
      hour: 'numeric',
      minute: '2-digit',
      hour12: true
    });
  } catch (error) {
    console.error('Error formatting date/time:', error);
    return '';
  }
};

/**
 * Truncate text to specified length with ellipsis
 * @param {string} text - Text to truncate
 * @param {number} maxLength - Maximum length
 * @returns {string} Truncated text
 */
export const truncateText = (text, maxLength) => {
  if (!text || text.length <= maxLength) return text;
  return text.substring(0, maxLength).trim() + '...';
};

/**
 * Sanitize text to prevent XSS
 * Note: React automatically escapes JSX, but this provides additional safety
 * @param {string} text - Text to sanitize
 * @returns {string} Sanitized text
 */
export const sanitizeText = (text) => {
  if (!text) return '';
  // Basic sanitization - remove script tags and event handlers
  return text
    .replace(/<script[^>]*>.*?<\/script>/gis, '')
    .replace(/on\w+="[^"]*"/gi, '');
};

/**
 * Format error message for display
 * @param {Error} error - Error object
 * @returns {string} User-friendly error message
 */
export const formatErrorMessage = (error) => {
  if (!error) return 'An unknown error occurred';

  // If it's a string error
  if (typeof error === 'string') return error;

  // If it's an Error object
  if (error.message) return error.message;

  // Default fallback
  return 'An error occurred. Please try again.';
};

/**
 * Format user name for message header
 * @param {string} role - Message role ('user' | 'assistant' | 'system')
 * @returns {string} Formatted name
 */
export const formatUserName = (role) => {
  switch (role) {
    case 'user':
      return 'You';
    case 'assistant':
      return 'Book Assistant';
    case 'system':
      return 'System';
    default:
      return 'Unknown';
  }
};
