"""Unit tests for Angets."""
# Angets
import angets

# Third-party
import pytest

err = angets.exceptions


class TestGetNonEmptyStr:
    def test_exception0(self, monkeypatch):
        monkeypatch.setattr('builtins.input', lambda _: '')
        with pytest.raises(err.EmptyStringError):
            angets.get_non_empty_str()

    def test_exception1(self, monkeypatch):
        monkeypatch.setattr('builtins.input', lambda _: ' ')
        with pytest.raises(err.EmptyStringError):
            angets.get_non_empty_str()

    def test_attempts_exception(self, monkeypatch):
        inputs = iter(['', '', ''])
        monkeypatch.setattr('builtins.input', lambda _: next(inputs))
        with pytest.raises(err.AttemptsExceededError):
            angets.get_non_empty_str(attempts=3)

    def test_returned_value(self, monkeypatch):
        monkeypatch.setattr('builtins.input', lambda _: 'Bob')
        result = angets.get_non_empty_str()
        assert result == 'Bob'


class TestFloat:
    def test_exception0(self, monkeypatch):
        monkeypatch.setattr('builtins.input', lambda _: '')
        with pytest.raises(err.NonFloatingPointError):
            angets.get_float()

    def test_exception1(self, monkeypatch):
        monkeypatch.setattr('builtins.input', lambda _: 'テスト用')
        with pytest.raises(err.AttemptsExceededError):
            angets.get_float(attempts=100)

    def test_returned_value0(self, monkeypatch):
        monkeypatch.setattr('builtins.input', lambda _: '10')
        result = angets.get_float()
        assert result == 10.0

    def test_returned_value1(self, monkeypatch):
        monkeypatch.setattr('builtins.input', lambda _: ' 1991.12 ')
        result = angets.get_float()
        assert result == 1991.12

    def test_normalization0(self, monkeypatch):
        monkeypatch.setattr('builtins.input', lambda _: '４２０．０２４')
        result = angets.get_float()
        assert result == 420.024

    def test_normalization1(self, monkeypatch):
        monkeypatch.setattr('builtins.input', lambda _: 'ー3．1４')
        result = angets.get_float()
        assert result == -3.14
