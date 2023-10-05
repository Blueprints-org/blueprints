import pytest


def dummy_function():
    """A function that returns True."""
    return True


def test_dummy_function():
    """
    Test if dummy_function returns True.

    This is a dummy test intended to always pass to check if the testing environment is correctly set up.

    Raises
    ------
    AssertionError
        If the function does not return True.
    """
    # Calling dummy_function and checking its return value
    result = dummy_function()
    assert result == True, "Should return True"
