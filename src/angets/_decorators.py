"""Decorators for Angets."""

# Built-ins
from typing import Callable
from functools import wraps

# Angets
from ._defaults import ATTEMPTS
from ._helpers import warn
from ._exceptions import AttemptsExceededError, InvalidAttemptsValueError


def loop(function: Callable):
    """Returns a looped function.

    | The decorator itself will not take in the number of attempts.
    | One must include **kwargs as a function argument in the function to wrap and define it like the following:
    | >>> function(..., attempts=${YOUR_ATTEMPTS})
    |
    | If there are no attempts defined, the default number of attempts will be used.
    |
    | Possible key word arguments for the functions to be wrapped:
    | attempts - Number of attempts to be made before an exception is raised.
    | verbose - Whether to print the warning message to the console or not.

    :param function: The function to wrap.
    :return: The wrapped function.
    :raise InvalidAttemptsValueError: If the given number of attempts is invalid.
    :raise AttemptsExceededError: If the given number of attempts is exceeded.
    """
    @wraps(function)
    def wrapper(*args, **kwargs):
        attempts: int = kwargs.get("attempts", ATTEMPTS)
        if attempts <= 0:
            raise InvalidAttemptsValueError(attempts)
        elif attempts == 1:
            return function(*args, **kwargs)
        else:
            for _ in range(attempts):
                try:
                    return function(*args, **kwargs)
                except ValueError as error:
                    if kwargs.get("verbose"):
                        warn(str(error))
                    continue
            else:
                raise AttemptsExceededError(attempts)

    return wrapper
