/**
 * useHighlight - Custom React hook for text selection handling
 * Manages highlight detection, button positioning, and selection state
 */

import { useState, useCallback, useEffect } from 'react';
import {
  MIN_HIGHLIGHT_LENGTH,
  MAX_HIGHLIGHT_LENGTH,
} from '../utils/constants.js';

/**
 * Custom hook for managing text selection state
 * @returns {Object} Highlight state and functions
 */
export function useHighlight(onAsk) {
  const [selection, setSelection] = useState(null);
  const [buttonPosition, setButtonPosition] = useState({ x: 0, y: 0 });
  const [isValid, setIsValid] = useState(false);

  /**
   * Handle text selection changes
   * Validates selection length and updates button position
   */
  const handleSelection = useCallback(() => {
    const selectionObj = window.getSelection();
    const text = selectionObj.toString().trim();

    if (text.length === 0) {
      // No selection - clear state
      setSelection(null);
      setButtonPosition({ x: 0, y: 0 });
      setIsValid(false);
      return;
    }

    // Validate selection length
    const lengthValid = text.length >= MIN_HIGHLIGHT_LENGTH && text.length <= MAX_HIGHLIGHT_LENGTH;

    if (lengthValid) {
      // Calculate button position
      try {
        const range = selectionObj.getRangeAt(0);
        const rect = range.getBoundingClientRect();

        // Get scroll position
        const scrollX = window.pageXOffset || document.documentElement.scrollLeft;
        const scrollY = window.pageYOffset || document.documentElement.scrollTop;

        setButtonPosition({
          x: rect.left + scrollX + rect.width / 2,
          y: rect.bottom + scrollY + 10,
        });

        setSelection(text);
        setIsValid(true);
      } catch (error) {
        // Range error - likely selection is collapsed
        console.error('Error getting selection position:', error);
        clearSelection();
      }
    } else {
      // Selection too short or too long
      setSelection(null);
      setButtonPosition({ x: 0, y: 0 });
      setIsValid(false);
    }
  }, [onAsk]);

  /**
   * Clear the current selection
   */
  const clearSelection = useCallback(() => {
    try {
      const selectionObj = window.getSelection();
      selectionObj.removeAllRanges();
    } catch (error) {
      // Selection already cleared or invalid
      console.warn('Error clearing selection:', error);
    }
    setSelection(null);
    setButtonPosition({ x: 0, y: 0 });
    setIsValid(false);
  }, []);

  /**
   * Handle "Ask about this" button click
   */
  const handleAsk = useCallback(() => {
    if (selection && isValid && typeof onAsk === 'function') {
      onAsk(selection);
      clearSelection();
    }
  }, [selection, isValid, onAsk]);

  /**
   * Handle Escape key to clear selection
   */
  const handleKeyDown = useCallback(
    (event) => {
      if (event.key === 'Escape') {
        event.preventDefault();
        clearSelection();
      }
    },
    [clearSelection]
  );

  // Add/remove event listeners for text selection
  useEffect(() => {
    // Use mouseup and touchend events for selection completion
    document.addEventListener('mouseup', handleSelection);
    document.addEventListener('touchend', handleSelection);
    document.addEventListener('keydown', handleKeyDown);

    return () => {
      document.removeEventListener('mouseup', handleSelection);
      document.removeEventListener('touchend', handleSelection);
      document.removeEventListener('keydown', handleKeyDown);
    };
  }, [handleSelection, handleKeyDown]);

  // Clear selection on page navigation or window blur
  useEffect(() => {
    const handleVisibilityChange = () => {
      if (document.hidden) {
        clearSelection();
      }
    };

    const handlePageUnload = () => {
      clearSelection();
    };

    document.addEventListener('visibilitychange', handleVisibilityChange);
    window.addEventListener('beforeunload', handlePageUnload);

    return () => {
      document.removeEventListener('visibilitychange', handleVisibilityChange);
      window.removeEventListener('beforeunload', handlePageUnload);
    };
  }, [clearSelection]);

  return {
    selection,
    buttonPosition,
    isValid,
    handleAsk,
    clearSelection,
  };
}

export default useHighlight;
