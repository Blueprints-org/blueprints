"""Tests for CoversRectangular class."""

from blueprints.structural_sections.concrete.reinforced_concrete_sections.covers import CoversRectangular


class TestCoversRectangular:
    """Tests for the CoversRectangular class."""

    def test_get_covers_info_with_all_equal_covers(self) -> None:
        """Test if the method `get_covers_info` returns the correct string when all covers are equal."""
        covers = CoversRectangular(upper=50.0, right=50.0, lower=50.0, left=50.0)
        assert covers.get_covers_info() == "Cover: 50 mm"

    def test_get_covers_info_with_different_covers(self) -> None:
        """Test if the method `get_covers_info` returns the correct string when all covers are different."""
        covers = CoversRectangular(upper=40.0, right=50.0, lower=60.0, left=70.0)
        expected_output = "Cover:\n  upper: 40 mm\n  right: 50 mm\n  lower: 60 mm\n  left: 70 mm"
        assert covers.get_covers_info() == expected_output

    def test_get_covers_info_with_two_equal_covers(self) -> None:
        """Test if the method `get_covers_info` returns the correct string when two covers are equal."""
        # Upper and left covers are equal
        covers = CoversRectangular(upper=50.0, right=60.0, lower=50.0, left=70.0)
        expected_output = "Cover:\n  upper|lower: 50 mm\n  right: 60 mm\n  left: 70 mm"
        assert covers.get_covers_info == expected_output

        # Upper and right covers are equal adnd lower and left covers are equal
        covers = CoversRectangular(upper=50.0, right=50.0, lower=60.0, left=60.0)
        expected_output = "Cover:\n  upper|right: 50 mm\n  lower|left: 60 mm"
        assert covers.get_covers_info == expected_output

    def test_get_covers_info_with_three_equal_covers(self) -> None:
        """Test if the method `get_covers_info` returns the correct string when three covers are equal."""
        covers = CoversRectangular(upper=50.0, right=50.0, lower=50.0, left=60.0)
        expected_output = "Cover:\n  upper|lower|right: 50 mm\n  left: 60 mm"
        assert covers.get_covers_info == expected_output
