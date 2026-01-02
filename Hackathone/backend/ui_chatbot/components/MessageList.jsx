/**
 * MessageList - Display all messages in the chat
 * Renders user, assistant, and system messages with proper styling
 */

import React, { forwardRef } from 'react';
import { formatMessage, formatDateTime, formatUserName } from '../utils/formatters';
import './chatPanel.css';

/**
 * MessageList component
 * @param {Object} props - Component props
 * @param {Array} props.messages - Array of message objects
 * @param {React.Ref} ref - Forward ref for scroll container
 */
const MessageList = forwardRef(({ messages }, ref) => {
  if (!messages || messages.length === 0) {
    return (
      <div className="chat-empty-state">
        <svg
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          strokeWidth="1.5"
          aria-hidden="true"
          focusable="false"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.97-4.03 9-9 9-9a9.863 9.863 0 0018-6 016-6s-1.005-1.12-1.417-1.077.267.956 3.61 2.617 3.607 6.994-.002 3.38-6.996 3.376-6.024-1.606-2.088-2.276-4.247-3.228-6.015-.006-.403-.011-.806-.018-1.21l-.003.212c-.004.354-.011.707-.022 1.064l.007 2.12c1.658 3.097 6.886 2.997 10.887-.089.752-.417 1.491-.648 2.228-1.048 2.833-2.418 1.679-.949-.969-.335-2.118-.262-2.817l-.715-.142c-.386-.056-.597-.211-.836-.445l-.093.23c-.363.107.75.232 1.142.821 1.404l-.234.615c-.076.197-.113.43-.113.657 0 .46-.037.896-.112 1.3-.245 1.4z"
          />
        </svg>
        <h3>No messages yet</h3>
        <p>Ask a question about the book content to get started!</p>
      </div>
    );
  }

  return (
    <div
      ref={ref}
      className="chat-message-list"
      role="log"
      aria-live="polite"
      aria-label="Chat messages"
    >
      {messages.map((message) => (
        <div
          key={message.id}
          className={`chat-message ${message.role}`}
          role="article"
          aria-labelledby={`message-${message.id}-role`}
        >
          <div className="chat-message-header">
            <span
              id={`message-${message.id}-role`}
              className="chat-message-role"
            >
              {formatUserName(message.role)}
            </span>
            <time className="chat-timestamp" dateTime={message.timestamp}>
              {formatDateTime(message.timestamp)}
            </time>
          </div>

          {message.highlightedContext && (
            <blockquote className="chat-highlighted-context">
              <span className="chat-highlighted-context-label">Context:</span>
              <p className="chat-highlighted-text">{message.highlightedContext}</p>
            </blockquote>
          )}

          <div
            className="chat-message-content"
            dangerouslySetInnerHTML={{ __html: formatMessage(message.content) }}
            role="presentation"
          />

          {message.generationTime && message.role === 'assistant' && (
            <div
              className="chat-message-timestamp"
              style={{ fontSize: '0.7rem', color: '#6b7280' }}
              aria-live="polite"
            >
              Generated in {message.generationTime.toFixed(2)}s with{' '}
              {Math.round(message.confidenceScore * 100)}% confidence
            </div>
          )}
        </div>
      ))}
    </div>
  );
});

MessageList.displayName = 'MessageList';

export default MessageList;
