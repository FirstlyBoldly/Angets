"""Core - Implementation details."""
# Built-ins
from typing import Callable, Any
from datetime import date
from math import inf

# Ankha's Gets
from .settings import ATTEMPTS
from ._helpers import within_attempts, float_to_int, normalize_to_ascii
from ._exceptions import (
    EmptyStringError,
    InvalidConfirmationError,
    InvalidISOFormatError,
    InvalidIntervalError,
    OutOfBoundsError,
    NonFloatingPointError,
    NonIntegerError
)


def _get_non_empty_str(prompt: str = '', **kwargs: Any) -> str:
    """Prompts for a non-empty string."""
    user_input: str = input(prompt)
    if not user_input.isspace() and len(user_input) != 0:
        return user_input
    else:
        raise EmptyStringError(kwargs.get('warning'))


def _get_constrained_number(get_number: Callable[[str, Any], float | int], prompt: str = '',
                            within: tuple[float, float] = (-inf, inf),
                            interval: str = '()', warning: str = '') -> float | int:
    """Prompts for a number within the constraints.

    :param Callable get_number: Function to get the user inputted number (float | int).
    :param str prompt: Prompt for the integer input.
    :param tuple within: A tuple representing (lower, upper) in which the input integer must lie within.
    :param str interval: '(' or ')' for non-inclusive, '[' or ']' for inclusive.
    :param str warning: The warning message if the input floating-point number is out of bounds.

    :return: A number within bounds.

    :raise InvalidIntervalError: if the interval value is invalid.
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


def _get_float(prompt: str = '', warning: str = '') -> float:
    """Prompts for a floating-point number."""
    try:
        return float(normalize_to_ascii(_get_non_empty_str(prompt)))
    except ValueError:
        raise NonFloatingPointError(warning)


def _get_constrained_float(_get_float: Callable[..., float], **kwargs) -> float:
    """Prompts for a float within the constraints."""
    return _get_constrained_number(_get_float, **kwargs)


def _get_positive_float(prompt: str = '', warning: str = '') -> float:
    """Prompts for a positive integer."""
    return _get_constrained_float(_get_float, prompt=prompt, within=(0, inf), warning=warning)


def _get_non_negative_float(prompt: str = '', warning: str = '') -> float:
    """Prompts for a non-negative integer."""
    return _get_constrained_float(_get_float, prompt=prompt, within=(-1, inf), warning=warning)


def _get_int(prompt: str = '', warning: str = '') -> int:
    """Prompts for an integer."""
    try:
        return int(normalize_to_ascii(_get_non_empty_str(prompt)))
    except ValueError:
        raise NonIntegerError(warning)


def _get_constrained_int(_get_int: Callable[..., int], **kwargs) -> int:
    """Prompts for an integer within the constraints."""
    return _get_constrained_int(_get_int, **kwargs)


def _get_positive_int(prompt: str = '', warning: str = '') -> int:
    """Prompts for a positive integer."""
    return float_to_int(_get_constrained_int(_get_int, prompt=prompt, within=(0, inf), warning=warning))


def _get_non_negative_int(prompt: str = '', warning: str = '') -> int:
    """Prompts for a non-negative integer."""
    return float_to_int(_get_constrained_int(_get_int, prompt=prompt, within=(-1, inf), warning=warning))


def _get_date(prompt: str, warning: str = '') -> date:
    """Prompts for a string with valid ISO 8601 formatting.

    :return: A date object.
    """
    user_input: str = normalize_to_ascii(_get_non_empty_str(prompt))
    try:
        return date.fromisoformat(user_input)
    except ValueError:
        raise InvalidISOFormatError(warning)


def _get_confirmation(prompt: str = '(Y/n)', warning: str = '') -> bool:
    """Prompts for a valid confirmation has been read.

    :return: True if 'yes' or 'y', otherwise False.
    """
    valid_confirmations: dict[str, bool] = {
        'yes': True,
        'y': True,
        'no': False,
        'n': False
    }
    try:
        return valid_confirmations[_get_non_empty_str(prompt).strip().lower()]
    except KeyError:
        raise InvalidConfirmationError(warning)


def get_non_empty_str(attempts: int = ATTEMPTS, *args, **kwargs) -> str:
    """Prompts until a non-empty string has been read."""
    return within_attempts(attempts, _get_non_empty_str, *args, **kwargs)


def get_constrained_number(attempts: int = ATTEMPTS, *args, **kwargs) -> float | int:
    """Prompts until a number within the constraints has been read."""
    return within_attempts(attempts, _get_constrained_number, *args, **kwargs)


def get_float(attempts: int = ATTEMPTS, *args, **kwargs) -> float:
    """Prompts until a float has been read."""
    return within_attempts(attempts, _get_float, *args, **kwargs)


def get_constrained_float(attempts: int = ATTEMPTS, *args, **kwargs) -> float:
    """Prompts until a float within the constraints has been read."""
    return within_attempts(attempts, _get_constrained_float, *args, **kwargs)


def get_positive_float(attempts: int = ATTEMPTS, *args, **kwargs) -> float:
    """Prompts until a positive float has been read."""
    return within_attempts(attempts, _get_positive_float, *args, **kwargs)


def get_non_negative_float(attempts: int = ATTEMPTS, *args, **kwargs) -> float:
    """Prompts until a non-negative float has been read."""
    return within_attempts(attempts, _get_non_negative_float, *args, **kwargs)


def get_int(attempts: int = ATTEMPTS, *args, **kwargs) -> int:
    """Prompts until an integer has been read."""
    return within_attempts(attempts, _get_int, *args, **kwargs)


def get_constrained_int(attempts: int = ATTEMPTS, *args, **kwargs) -> int:
    """Prompts until an integer within the constraints has been read."""
    return within_attempts(attempts, _get_constrained_int, *args, **kwargs)


def get_positive_int(attempts: int = ATTEMPTS, *args, **kwargs) -> int:
    """Prompts until a positive integer has been read."""
    return within_attempts(attempts, _get_positive_int, *args, **kwargs)


def get_non_negative_int(attempts: int = ATTEMPTS, *args, **kwargs) -> int:
    """Prompts until a non-negative integer has been read."""
    return within_attempts(attempts, _get_non_negative_int, *args, **kwargs)


def get_confirmation(attempts: int = ATTEMPTS, *args, **kwargs) -> bool:
    """Prompts until a valid confirmation has been read.

    :returns: True if 'yes' or 'y', otherwise False.
    """
    return within_attempts(attempts, _get_confirmation, *args, **kwargs)


def get_date(attempts: int = ATTEMPTS, *args, **kwargs) -> date:
    """Prompts until a string with valid ISO 8601 formatting has been read.

    :returns: A date object.
    """
    return within_attempts(attempts, _get_date, *args, **kwargs)
