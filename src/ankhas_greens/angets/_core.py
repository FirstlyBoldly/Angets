"""Core - Implementation details."""

# Built-ins
from typing import Callable
from datetime import date
from math import inf

# Angets
from ._decorators import loop
from ._helpers import convert_float_to_int, normalize_to_ascii
from ._exceptions import (EmptyStringError, InvalidConfirmationError, InvalidISOFormatError, InvalidIntervalError,
                          OutOfBoundsError, NonFloatingPointError, NonIntegerError)


@loop
def get_non_empty_str(prompt: str = '', warning: str = '', **kwargs) -> str:
    """Prompts for a non-empty string.

    :param str prompt: Prompt for the integer input.
    :param str warning: The warning message if the input floating-point number is out of bounds.

    :return: A non-empty string.

    :raise EmptyStringError: If the input string is empty.
    """
    user_input: str = input(prompt)
    if not user_input.isspace() and len(user_input) != 0:
        return user_input
    else:
        raise EmptyStringError(warning)


@loop
def get_constrained_number(get_number: Callable, within: tuple[float, float], interval: str, prompt: str = '',
                           warning: str = '', **kwargs) -> float | int:
    """Prompts for a number within the constraints.

    :param Callable get_number: Function to get the user inputted number (float | int).
    :param tuple within: A tuple representing (lower, upper) in which the input integer must lie within.
    :param str interval: '(' or ')' for non-inclusive, '[' or ']' for inclusive.
    :param str prompt: Prompt for the integer input.
    :param str warning: The warning message if the input floating-point number is out of bounds.

    :return: A number within bounds.

    :raise InvalidIntervalError: If the interval value is invalid.
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
def get_float(prompt: str = '', warning: str = '', **kwargs) -> float:
    """Prompts for a floating-point number."""
    try:
        return float(normalize_to_ascii(get_non_empty_str(prompt)))
    except ValueError:
        raise NonFloatingPointError(warning)


@loop
def get_constrained_float(within: tuple[float, float], interval: str, prompt: str = '', warning: str = '',
                          **kwargs) -> float:
    """Prompts for a float within the constraints."""
    return get_constrained_number(get_float, within, interval, prompt, warning, **kwargs)


@loop
def get_positive_float(prompt: str = '', warning: str = '', **kwargs) -> float:
    """Prompts for a positive integer."""
    return get_constrained_float((0, inf), '()', prompt, warning, **kwargs)


@loop
def get_non_negative_float(prompt: str = '', warning: str = '', **kwargs) -> float:
    """Prompts for a non-negative integer."""
    return get_constrained_float((0, inf), '[)', prompt, warning, **kwargs)


@loop
def get_int(prompt: str = '', warning: str = '', **kwargs) -> int:
    """Prompts for an integer."""
    try:
        return int(normalize_to_ascii(get_non_empty_str(prompt)))
    except ValueError:
        raise NonIntegerError(warning)


@loop
def get_constrained_int(within: tuple[float, float], interval: str, prompt: str = '', warning: str = '',
                        **kwargs) -> int:
    """Prompts for an integer within the constraints."""
    return convert_float_to_int(get_constrained_number(get_int, within, interval, prompt, warning, **kwargs))


@loop
def get_positive_int(prompt: str = '', warning: str = '', **kwargs) -> int:
    """Prompts for a positive integer."""
    return get_constrained_int((0, inf), '()', prompt, warning, **kwargs)


@loop
def get_non_negative_int(prompt: str = '', warning: str = '', **kwargs) -> int:
    """Prompts for a non-negative integer."""
    return get_constrained_int((0, inf), '[)', prompt, warning, **kwargs)


@loop
def get_date(prompt: str = '', warning: str = '', **kwargs) -> date:
    """Prompts for a string with valid ISO 8601 formatting.

    :return: A date object.
    """
    try:
        user_input: str = normalize_to_ascii(get_non_empty_str(prompt))
        return date.fromisoformat(user_input)
    except ValueError:
        raise InvalidISOFormatError(warning)


@loop
def get_confirmation(prompt: str = '(Y/n)', warning: str = '', selection: dict[str, bool] | None = None,
                     **kwargs) -> bool:
    """Prompts for a valid confirmation has been read.

    :return: True if 'yes' or 'y', otherwise False.
    """
    selection = selection or {'yes': True, 'y': True, 'no': False, 'n': False}
    # Make the selection keys case-insensitive.
    selection = {key.lower(): value for key, value in selection}
    try:
        return selection[get_non_empty_str(prompt).strip().lower()]
    except KeyError:
        raise InvalidConfirmationError(warning)
