/**
 * ChatWidgetIcon - Floating chat icon button component
 * Displays unread badge and toggles chat panel
 */

import React, { forwardRef, useRef, useEffect } from 'react';
import './chatWidget.css';

/**
 * ChatWidgetIcon component
 * @param {Object} props - Component props
 * @param {boolean} props.isOpen - Whether chat panel is currently open
 * @param {number} props.unreadCount - Number of unread messages
 * @param {Function} props.onClick - Click handler to toggle chat
 * @param {Function} props.onFocus - Focus handler
 * @param {React.Ref} ref - Forward ref
 */
const ChatWidgetIcon = forwardRef(({ isOpen, unreadCount, onClick, onFocus }, ref) => {
  const buttonRef = useRef(null);

  // Forward ref to internal button ref
  useEffect(() => {
    if (typeof ref === 'function') {
      ref(buttonRef.current);
    } else if (ref) {
      ref.current = buttonRef.current;
    }
  }, [ref]);

  // Handle keyboard interactions (Enter or Space to toggle)
  const handleKeyDown = (e) => {
    if (e.key === 'Enter' || e.key === ' ') {
      e.preventDefault();
      onClick();
    }
  };

  return (
    <button
      ref={buttonRef}
      className={`chat-widget-icon ${isOpen ? 'open' : ''} ${unreadCount > 0 ? 'has-new-messages' : ''}`}
      onClick={onClick}
      onFocus={onFocus}
      onKeyDown={handleKeyDown}
      aria-label={isOpen ? 'Close chat' : 'Open chat'}
      aria-expanded={isOpen}
      aria-live="polite"
      type="button"
      tabIndex={0}
    >
      <svg
        className="chat-icon"
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
        strokeWidth="2"
        strokeLinecap="round"
        strokeLinejoin="round"
        aria-hidden="true"
        focusable="false"
      >
        <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2v10l-4 4H7l4-4V5a2 2 0 0 1-2-2z" />
        <path d="M12 3v10" />
        <path d="M17 9l-5 5" />
        <path d="M7 9l5 5" />
      </svg>

      {unreadCount > 0 && (
        <span
          className={`chat-unread-badge ${unreadCount > 9 ? 'double-digit' : ''}`}
          aria-label={`${unreadCount} unread message${unreadCount !== 1 ? 's' : ''}`}
        >
          {unreadCount > 99 ? '99+' : unreadCount}
        </span>
      )}
    </button>
  );
});

ChatWidgetIcon.displayName = 'ChatWidgetIcon';

export default ChatWidgetIcon;
