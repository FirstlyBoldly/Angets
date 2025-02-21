"""Unit tests for Angets."""
# Angets
import angets

# Third-party
import pytest


class TestGetNonEmptyStr:
    def test_attempts_exceeded(self, monkeypatch):
        inputs = iter(['', '', ''])
        monkeypatch.setattr('builtins.input', lambda _: next(inputs))
        with pytest.raises(angets.exceptions.AttemptsExceededError):
            angets.get_non_empty_str(attempts=3)

    def test_returned_value(self, monkeypatch):
        monkeypatch.setattr('builtins.input', lambda _: 'Bob')
        result = angets.get_non_empty_str()
        assert result == 'Bob'
