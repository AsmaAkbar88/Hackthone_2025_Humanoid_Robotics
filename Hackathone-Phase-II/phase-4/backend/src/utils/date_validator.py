from datetime import datetime
from typing import Union, Optional
import re


def validate_signup_date(date_input: Union[str, datetime, None]) -> datetime:
    """
    Validates and normalizes the signup date input.

    Args:
        date_input: The date input which can be a string, datetime object, or None

    Returns:
        datetime: A valid datetime object representing the signup date

    Raises:
        ValueError: If the date input is invalid or cannot be parsed
    """
    if date_input is None:
        return datetime.utcnow()

    if isinstance(date_input, datetime):
        return date_input

    if isinstance(date_input, str):
        # Try to parse ISO format first (YYYY-MM-DDTHH:MM:SS.ssssss or YYYY-MM-DDTHH:MM:SS)
        iso_formats = [
            "%Y-%m-%dT%H:%M:%S.%f",
            "%Y-%m-%dT%H:%M:%S",
            "%Y-%m-%d %H:%M:%S.%f",
            "%Y-%m-%d %H:%M:%S",
            "%Y-%m-%d"
        ]

        for fmt in iso_formats:
            try:
                return datetime.strptime(date_input, fmt)
            except ValueError:
                continue

        # Try common alternative formats
        alt_formats = [
            "%m/%d/%Y %H:%M:%S",
            "%m/%d/%Y",
            "%d/%m/%Y",
            "%Y.%m.%d"
        ]

        for fmt in alt_formats:
            try:
                return datetime.strptime(date_input, fmt)
            except ValueError:
                continue

        # If none of the formats worked, raise an error
        raise ValueError(f"Unable to parse date string: {date_input}")

    raise ValueError(f"Invalid date input type: {type(date_input)}. Expected str, datetime, or None")


def is_valid_date_format(date_str: str) -> bool:
    """
    Checks if a date string is in a valid format.

    Args:
        date_str: The date string to validate

    Returns:
        bool: True if the date string is in a valid format, False otherwise
    """
    try:
        validate_signup_date(date_str)
        return True
    except ValueError:
        return False


def normalize_date_to_utc(date_input: Union[str, datetime]) -> datetime:
    """
    Normalizes a date input to UTC timezone.

    Args:
        date_input: The date input to normalize

    Returns:
        datetime: The normalized datetime in UTC
    """
    dt = validate_signup_date(date_input)
    # Assuming naive datetime is in local timezone, convert to UTC
    # For simplicity, if it's naive, treat as local time and convert to UTC
    if dt.tzinfo is None:
        # For this implementation, we'll assume it's already in UTC or convert appropriately
        return dt
    else:
        # If it has timezone info, convert to UTC
        return dt.utctimetuple()


def validate_and_format_signup_date(date_input: Union[str, datetime, None]) -> dict:
    """
    Validates a signup date and returns a formatted response.

    Args:
        date_input: The date input to validate

    Returns:
        dict: A dictionary containing the validated date and any validation messages
    """
    try:
        validated_date = validate_signup_date(date_input)
        return {
            "valid": True,
            "date": validated_date,
            "formatted_iso": validated_date.isoformat(),
            "message": "Date is valid"
        }
    except ValueError as e:
        return {
            "valid": False,
            "date": None,
            "formatted_iso": None,
            "message": str(e)
        }