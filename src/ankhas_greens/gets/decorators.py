"""Decorators for Ankha's Gets."""
# Built-ins
from collections.abc import Callable
from typing import Any

# Ankha's Gets
from errors import AttemptsExceededError
from settings import ATTEMPTS
from helpers import warn


def within_attempts(attempts: int = ATTEMPTS):
    def decorator(function: Callable):
        def wrapper(*args: Any, **kwargs: Any):
            for _ in range(attempts):
                try:
                    return function(*args, **kwargs)
                except ValueError as error:
                    warn(str(error))
            else:
                raise AttemptsExceededError(attempts)

        return wrapper

    return decorator
