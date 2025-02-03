"""Decorators for Ankha's Gets."""
# Built-ins
from typing import Any, Callable

# Ankha's Gets
from .exceptions import AttemptsExceededError
from .settings import ATTEMPTS
from .helpers import warn


def within(attempts: int = ATTEMPTS):
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
