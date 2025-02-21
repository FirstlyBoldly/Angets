"""Unit tests for Angets."""
# Built-ins
from unittest import mock
import unittest

# Angets
import angets


class TestAngets(unittest.TestCase):
    @mock.patch('angets._core.input', create=True)
    def test_get_non_empty_str(self, mocked_input):
        # Raise exception when all 3 inputs are empty.
        with self.assertRaises(angets.exceptions.AttemptsExceededError):
            mocked_input.side_effect = ['', '', '']
            angets.get_non_empty_str(attempts=3)


if __name__ == '__main__':
    unittest.main()
