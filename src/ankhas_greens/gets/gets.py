"""Ankha's Gets - Custom functions for user input."""
# Built-ins
from typing import Callable
from datetime import date
from math import inf

# Ankha's Gets
from helpers import float_to_int, normalize_to_ascii
from errors import (
    EmptyStringError,
    InvalidConfirmationError,
    InvalidISOFormatError,
    InvalidIntervalError,
    OutOfBoundsError,
    NonFloatingPointError,
    NonIntegerError
)


def get_non_empty_string(prompt: str = '', warning: str = '') -> str:
    """Prompts until a non-empty string has been read."""
    user_input: str = input(prompt)
    if not user_input.isspace() and len(user_input) != 0:
        return user_input
    else:
        raise EmptyStringError(warning)


def get_constrained_number(get_number: Callable[[str, str], float | int], prompt: str = '',
                           within: tuple[float, float] = (-inf, inf),
                           interval: str = '()', warning: str = '') -> float:
    """Prompts until a number within the range has been read.

    Parameters:
        get_number (Callable): Function to get the user inputted number (float | int).
        prompt (str): Prompt for the integer input.
        within (tuple): A tuple representing (lower, upper) in which the input integer must lie within.
        interval (str): '(' or ')' for non-inclusive, '[' or ']' for inclusive.
        warning (str): The warning message if the input floating-point number is out of bounds.

    Returns:
        float | int: A number within bounds.

    Raises:
        InvalidIntervalError if the interval value is invalid.
    """
    intervals: list[str] = ['()', '[]', '(]', '[)']
    if interval not in intervals:
        raise InvalidIntervalError(intervals, interval)

    user_input: float | int = get_number(prompt, warning)
    is_within_lower_bound: bool = within[0] < user_input if interval[0] == '(' else within[0] <= user_input
    is_within_upper_bound: bool = within[1] > user_input if interval[1] == ')' else within[1] >= user_input
    if is_within_lower_bound and is_within_upper_bound:
        return user_input
    else:
        raise OutOfBoundsError(warning)


def get_float(prompt: str = '', warning: str = '') -> float:
    """Prompts until a floating-point number has been read."""
    try:
        return float(normalize_to_ascii(get_non_empty_string(prompt)))
    except ValueError:
        raise NonFloatingPointError(warning)


def get_positive_float(prompt: str = '', warning: str = '') -> float:
    """Prompts until a positive integer has been read."""
    return get_constrained_number(get_float, prompt, (0, inf), '()', warning)


def get_non_negative_float(prompt: str = '', warning: str = '') -> float:
    """Prompts until a non-negative integer has been read."""
    return get_constrained_number(get_float, prompt, (-1, inf), '()', warning)


def get_int(prompt: str = '', warning: str = '') -> int:
    """Prompts until an integer has been read."""
    try:
        return int(normalize_to_ascii(get_non_empty_string(prompt)))
    except ValueError:
        raise NonIntegerError(warning)


def get_positive_int(prompt: str = '', warning: str = '') -> int:
    """Prompts until a positive integer has been read."""
    return float_to_int(get_constrained_number(get_int, prompt, (0, inf), '()', warning))


def get_non_negative_int(prompt: str = '', warning: str = '') -> int:
    """Prompts until a non-negative integer has been read."""
    return float_to_int(get_constrained_number(get_int, prompt, (-1, inf), '()', warning))


def get_date(prompt: str, warning: str = '') -> date:
    """Prompts until a string with valid ISO formatting has been read. Returns a date object."""
    user_input: str = normalize_to_ascii(get_non_empty_string(prompt))
    try:
        return date.fromisoformat(user_input)
    except ValueError:
        raise InvalidISOFormatError(warning)


def get_confirmation(prompt: str = '(Y/n)', warning: str = '') -> bool:
    """Prompts until a valid confirmation has been read. Returns True if 'yes' or 'y', otherwise False."""
    valid_confirmations: dict[str, bool] = {
        'yes': True,
        'y': True,
        'no': False,
        'n': False
    }
    try:
        return valid_confirmations[get_non_empty_string(prompt).strip().lower()]
    except KeyError:
        raise InvalidConfirmationError(warning)
