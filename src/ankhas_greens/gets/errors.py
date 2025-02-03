"""Custom exceptions for Ankha's Gets."""


class AttemptsExceededError(Exception):
    """Given attempts exceeded."""

    def __init__(self, attempts: int) -> None:
        """Create and return a new AttemptsExceededError object."""
        super(AttemptsExceededError, self).__init__(f'Attempts exceeded, Total attempts: {attempts}')


class InvalidISOFormatError(ValueError):
    """Invalid ISO format."""

    def __init__(self, warning: str) -> None:
        """Create and return a new InvalidISOFormatError object."""
        warning = warning or 'Invalid ISO format. Example: (1970-01-01)'
        super(InvalidISOFormatError, self).__init__(warning)


class InvalidConfirmationError(ValueError):
    """Invalid confirmation string."""

    def __init__(self, warning: str) -> None:
        """Create and return a new InvalidConfirmationError object."""
        warning = warning or 'Invalid confirmation string. Example: "yes"'
        super(InvalidConfirmationError, self).__init__(warning)


class InvalidIntervalError(Exception):
    """Invalid interval."""

    def __init__(self, valid_intervals: list[str], invalid_interval: str) -> None:
        """Create and return a new InvalidIntervalError object."""
        super(InvalidIntervalError, self).__init__(
            f'Invalid interval: {invalid_interval}\nValid intervals: {" or ".join(valid_intervals)}')


class OutOfBoundsError(ValueError):
    """Value not within bounds."""

    def __init__(self, warning: str) -> None:
        """Create and return a new OutOfBoundsError object."""
        warning = warning or 'Value not within bounds. Please check the bounds.'
        super(OutOfBoundsError, self).__init__(warning)


class EmptyStringError(ValueError):
    """Empty string."""

    def __init__(self, warning: str) -> None:
        """Create and return a new EmptyStringError object."""
        warning = warning or 'Input is empty. Please input a valid string.'
        super(EmptyStringError, self).__init__(warning)


class NonFloatingPointError(ValueError):
    """Non-floating-point number."""

    def __init__(self, warning: str) -> None:
        """Create and return a new NonFloatingPointError object."""
        warning = warning or 'Not a floating-point number. Please input a valid floating-point number.'
        super(NonFloatingPointError, self).__init__(warning)


class NonIntegerError(ValueError):
    """Non-integer number."""

    def __init__(self, warning: str) -> None:
        """Create and return a new NonIntegerError object."""
        warning = warning or 'Not an integer. Please input a valid integer number.'
        super(NonIntegerError, self).__init__(warning)
