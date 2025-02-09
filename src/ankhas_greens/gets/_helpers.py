"""Utility functions for Ankha's Gets."""

# Built-ins
from typing import Any, Callable
import unicodedata
import re

# Ankha's Gets
from ._exceptions import NonIntegerError, InvalidAttemptsValueError, AttemptsExceededError


def within_attempts(function: Callable[..., Any], attempts: int, *args, **kwargs) -> Any:
    if attempts <= 0:
        raise InvalidAttemptsValueError(attempts)
    elif attempts == 1:
        return function(*args, **kwargs)
    else:
        for _ in range(attempts):
            try:
                return function(*args, **kwargs)
            except ValueError as error:
                if kwargs.get('verbose'):
                    warn(str(error))
                continue
        else:
            raise AttemptsExceededError(attempts)


def warn(warning: str) -> None:
    """Prints the warning message the stream, if there is one."""
    if warning:
        print(warning)


def float_to_int(float_number: float, warning: str | None = None) -> int:
    """Return a float as an integer if said float can be converted into an integer without loss of data.

    :raise NonIntegerError: If float is not an integer.
    """
    if float_number.is_integer():
        return int(float_number)
    else:
        raise NonIntegerError(warning)


def normalize_to_ascii(non_ascii_string: str) -> str:
    """Convert a Japanese full-width number to half-width."""
    return re.sub('[ー－―—‐]', '-', unicodedata.normalize('NFKC', non_ascii_string))
