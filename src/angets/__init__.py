"""Angets (Ankha's Gets): Functions for user input."""

# Built-ins
import importlib.metadata

__version__: str = importlib.metadata.version("angets")

__all__: list[str] = [
    "get_non_empty_str",
    "get_constrained_number",
    "get_float",
    "get_constrained_float",
    "get_positive_float",
    "get_non_negative_float",
    "get_int",
    "get_constrained_int",
    "get_positive_int",
    "get_non_negative_int",
    "get_confirmation",
    "get_date",
    "decorators",
    "helpers",
    "exceptions"
]

# Angets
from ._core import (
    get_non_empty_str,
    get_constrained_number,
    get_float,
    get_constrained_float,
    get_positive_float,
    get_non_negative_float,
    get_int,
    get_constrained_int,
    get_positive_int,
    get_non_negative_int,
    get_confirmation,
    get_date,
)
from . import _decorators as decorators
from . import _helpers as helpers
from . import _exceptions as exceptions
