"""
Utility functions for the In-Memory Python Console Todo Application.

This module provides helper functions for validation, formatting, and other
common operations used across the application.
"""


def validate_title(title: str, max_length: int = 500) -> bool:
    """
    Validate a todo title based on length and content.

    Args:
        title (str): The title to validate
        max_length (int): Maximum allowed length (default: 500)

    Returns:
        bool: True if title is valid, False otherwise
    """
    if not title or not title.strip():
        return False

    if len(title) > max_length:
        return False

    return True


def format_task_status(completed: bool) -> str:
    """
    Format the completion status for display.

    Args:
        completed (bool): The completion status

    Returns:
        str: Formatted status string
    """
    return "[x]" if completed else "[ ]"


def clean_input(user_input: str) -> str:
    """
    Clean user input by stripping whitespace.

    Args:
        user_input (str): Raw user input

    Returns:
        str: Cleaned input string
    """
    return user_input.strip()


def is_positive_integer(value: int) -> bool:
    """
    Check if a value is a positive integer.

    Args:
        value (int): The value to check

    Returns:
        bool: True if value is a positive integer, False otherwise
    """
    return isinstance(value, int) and value > 0


def truncate_text(text: str, max_length: int = 50) -> str:
    """
    Truncate text to a maximum length with ellipsis.

    Args:
        text (str): The text to truncate
        max_length (int): Maximum length (default: 50)

    Returns:
        str: Truncated text with ellipsis if needed
    """
    if len(text) <= max_length:
        return text
    return text[:max_length-3] + "..."


def pluralize(word: str, count: int, plural_form: str = None) -> str:
    """
    Return the appropriate form of a word based on count.

    Args:
        word (str): The singular form of the word
        count (int): The count to determine form
        plural_form (str): Optional custom plural form

    Returns:
        str: Singular or plural form of the word
    """
    if count == 1:
        return word

    if plural_form:
        return plural_form

    if word.endswith('y'):
        return word[:-1] + 'ies'
    elif word.endswith(('s', 'ss', 'sh', 'ch', 'x', 'z')):
        return word + 'es'
    else:
        return word + 's'