"""Core - Implementation details."""

# Built-ins
from typing import Callable, Any
from datetime import date
from math import inf

# Ankha's Gets
from ._decorators import loop
from ._helpers import float_to_int, normalize_to_ascii
from ._exceptions import (EmptyStringError, InvalidConfirmationError, InvalidISOFormatError, InvalidIntervalError,
                          OutOfBoundsError, NonFloatingPointError, NonIntegerError)


@loop
def get_non_empty_str(prompt: str = '', **kwargs: dict[str, Any]) -> str:
    """Prompts for a non-empty string."""
    user_input: str = input(prompt)
    if not user_input.isspace() and len(user_input) != 0:
        return user_input
    else:
        raise EmptyStringError(kwargs.get('warning'))


@loop
def get_constrained_number(get_number: Callable[[str, Any], float | int], prompt: str = '',
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


@loop
def get_float(prompt: str = '', warning: str = '') -> float:
    """Prompts for a floating-point number."""
    try:
        return float(normalize_to_ascii(get_non_empty_str(prompt)))
    except ValueError:
        raise NonFloatingPointError(warning)


@loop
def get_constrained_float(_get_float: Callable[..., float], **kwargs) -> float:
    """Prompts for a float within the constraints."""
    return get_constrained_number(_get_float, **kwargs)


@loop
def get_positive_float(prompt: str = '', warning: str = '') -> float:
    """Prompts for a positive integer."""
    return get_constrained_float(get_float, prompt=prompt, within=(0, inf), warning=warning)


@loop
def get_non_negative_float(prompt: str = '', warning: str = '') -> float:
    """Prompts for a non-negative integer."""
    return get_constrained_float(get_float, prompt=prompt, within=(-1, inf), warning=warning)


@loop
def get_int(prompt: str = '', warning: str = '') -> int:
    """Prompts for an integer."""
    try:
        return int(normalize_to_ascii(get_non_empty_str(prompt)))
    except ValueError:
        raise NonIntegerError(warning)


@loop
def get_constrained_int(_get_int: Callable[..., int], **kwargs) -> int:
    """Prompts for an integer within the constraints."""
    return get_constrained_int(_get_int, **kwargs)


@loop
def get_positive_int(prompt: str = '', warning: str = '') -> int:
    """Prompts for a positive integer."""
    return float_to_int(get_constrained_int(get_int, prompt=prompt, within=(0, inf), warning=warning))


@loop
def get_non_negative_int(prompt: str = '', warning: str = '') -> int:
    """Prompts for a non-negative integer."""
    return float_to_int(get_constrained_int(get_int, prompt=prompt, within=(-1, inf), warning=warning))


@loop
def get_date(prompt: str = '', warning: str = '') -> date:
    """Prompts for a string with valid ISO 8601 formatting.

    :return: A date object.
    """
    try:
        user_input: str = normalize_to_ascii(get_non_empty_str(prompt))
        return date.fromisoformat(user_input)
    except ValueError:
        raise InvalidISOFormatError(warning)


@loop
def get_confirmation(prompt: str = '(Y/n)', warning: str = '') -> bool:
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
        return valid_confirmations[get_non_empty_str(prompt).strip().lower()]
    except KeyError:
        raise InvalidConfirmationError(warning)
