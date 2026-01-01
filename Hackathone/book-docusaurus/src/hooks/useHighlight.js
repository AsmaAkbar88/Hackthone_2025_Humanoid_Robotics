import { useState, useCallback, useEffect } from 'react';
import { MIN_HIGHLIGHT_LENGTH, MAX_HIGHLIGHT_LENGTH } from '../utils/constants';

export function useHighlight(onAsk) {
  const [selection, setSelection] = useState(null);
  const [buttonPosition, setButtonPosition] = useState({ x: 0, y: 0 });
  const [isValid, setIsValid] = useState(false);

  const handleSelection = useCallback(() => {
    const selectionObj = window.getSelection();
    const text = selectionObj.toString().trim();

    if (text.length === 0) {
      setSelection(null);
      setButtonPosition({ x: 0, y: 0 });
      setIsValid(false);
      return;
    }

    const lengthValid = text.length >= MIN_HIGHLIGHT_LENGTH && text.length <= MAX_HIGHLIGHT_LENGTH;

    if (lengthValid) {
      try {
        const range = selectionObj.getRangeAt(0);
        const rect = range.getBoundingClientRect();
        const scrollX = window.pageXOffset || document.documentElement.scrollLeft;
        const scrollY = window.pageYOffset || document.documentElement.scrollTop;

        setButtonPosition({
          x: rect.left + scrollX + rect.width / 2,
          y: rect.bottom + scrollY + 10,
        });

        setSelection(text);
        setIsValid(true);
      } catch (error) {
        console.error('Error getting selection position:', error);
        clearSelection();
      }
    } else {
      setSelection(null);
      setButtonPosition({ x: 0, y: 0 });
      setIsValid(false);
    }
  }, [onAsk]);

  const clearSelection = useCallback(() => {
    try {
      const selectionObj = window.getSelection();
      selectionObj.removeAllRanges();
    } catch (error) {
      console.warn('Error clearing selection:', error);
    }
    setSelection(null);
    setButtonPosition({ x: 0, y: 0 });
    setIsValid(false);
  }, []);

  const handleAsk = useCallback(() => {
    if (selection && isValid && typeof onAsk === 'function') {
      onAsk(selection);
      clearSelection();
    }
  }, [selection, isValid, onAsk]);

  const handleKeyDown = useCallback(
    (event) => {
      if (event.key === 'Escape') {
        event.preventDefault();
        clearSelection();
      }
    },
    [clearSelection]
  );

  useEffect(() => {
    document.addEventListener('mouseup', handleSelection);
    document.addEventListener('touchend', handleSelection);
    document.addEventListener('keydown', handleKeyDown);

    return () => {
      document.removeEventListener('mouseup', handleSelection);
      document.removeEventListener('touchend', handleSelection);
      document.removeEventListener('keydown', handleKeyDown);
    };
  }, [handleSelection, handleKeyDown]);

  return {
    selection,
    buttonPosition,
    isValid,
    handleAsk,
    clearSelection,
  };
}

export default useHighlight;
