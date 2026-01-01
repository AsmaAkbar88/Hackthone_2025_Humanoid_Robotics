/**
 * HighlightButton - Floating "Ask about this" button for selected text
 * Appears when user selects text on page
 */

import React, { useEffect, useRef } from 'react';
import './responsive.css';

/**
 * HighlightButton component
 * @param {Object} props - Component props
 * @param {string} props.text - Selected text to ask about
 * @param {Object} props.position - Button position {x, y}
 * @param {boolean} props.isValid - Whether selection is valid
 * @param {Function} props.onAsk - Handler when button is clicked
 * @param {Function} props.onClear - Handler to clear selection
 */
function HighlightButton({ text, position, isValid, onAsk, onClear }) {
  const buttonRef = useRef(null);

  // Focus button when it appears
  useEffect(() => {
    if (buttonRef.current && isValid) {
      buttonRef.current.focus();
    }
  }, [position, isValid]);

  if (!text || !position) {
    return null;
  }

  const handleClick = () => {
    if (isValid && typeof onAsk === 'function') {
      onAsk(text);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' || e.key === ' ') {
      e.preventDefault();
      handleClick();
    } else if (e.key === 'Escape') {
      e.preventDefault();
      if (typeof onClear === 'function') {
        onClear();
      }
    }
  };

  const truncatedText = text.length > 50 ? `${text.substring(0, 50)}...` : text;

  return (
    <button
      ref={buttonRef}
      type="button"
      className="highlight-button"
      onClick={handleClick}
      onKeyDown={handleKeyDown}
      aria-label={`Ask about selected text: ${truncatedText}`}
      aria-pressed={false}
      tabIndex={0}
      style={{
        left: `${position.x}px`,
        top: `${position.y}px`,
      }}
    >
      Ask about this
    </button>
  );
}

HighlightButton.displayName = 'HighlightButton';

export default HighlightButton;
