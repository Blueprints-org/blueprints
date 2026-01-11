"""Test suite for corrosion_utils module."""

import pytest

from blueprints.structural_sections.steel.profile_definitions.corrosion_utils import (
    _update_double_corrosion,
    _update_single_corrosion,
    update_name_with_corrosion,
)


class TestUpdateNameWithCorrosion:
    """Test suite for update_name_with_corrosion function."""

    def test_both_single_and_double_parameters_raises_error(self) -> None:
        """Test that providing both single and double corrosion parameters raises ValueError."""
        with pytest.raises(ValueError, match="Cannot use both single corrosion and double"):
            update_name_with_corrosion(
                "IPE200",
                corrosion=1.5,
                corrosion_inside=1.0,
                corrosion_outside=2.0,
            )  # type: ignore[call-overload]

    def test_neither_single_nor_double_parameters_raises_error(self) -> None:
        """Test that providing neither single nor double corrosion parameters raises ValueError."""
        with pytest.raises(ValueError, match="At least one corrosion parameter must be provided"):
            update_name_with_corrosion("IPE200")  # type: ignore[call-overload]

    def test_only_corrosion_provided(self) -> None:
        """Test update when only uniform corrosion is provided."""
        result = update_name_with_corrosion("IPE200", corrosion=1.5)
        expected = "IPE200 (corrosion: 1.5 mm)"
        assert result == expected

    def test_only_outside_corrosion_provided(self) -> None:
        """Test update when only outside corrosion is provided."""
        result = update_name_with_corrosion("RHS200x100x5", corrosion_outside=2.0, corrosion_inside=0)
        expected = "RHS200x100x5 (corrosion inside: 0 mm, outside: 2.0 mm)"
        assert result == expected

    def test_only_inside_corrosion_provided(self) -> None:
        """Test update when only inside corrosion is provided."""
        result = update_name_with_corrosion("RHS200x100x5", corrosion_outside=0, corrosion_inside=1.0)
        expected = "RHS200x100x5 (corrosion inside: 1.0 mm, outside: 0 mm)"
        assert result == expected

    def test_both_outside_and_inside_corrosions_provided(self) -> None:
        """Test update when both outside and inside corrosions are provided."""
        result = update_name_with_corrosion(
            "RHS200x100x5",
            corrosion_inside=1.0,
            corrosion_outside=2.0,
        )
        expected = "RHS200x100x5 (corrosion inside: 1.0 mm, outside: 2.0 mm)"
        assert result == expected

    def test_uniform_corrosion_with_existing_value(self) -> None:
        """Test adding uniform corrosion to a name that already has corrosion."""
        result = update_name_with_corrosion("IPE200 (corrosion: 1.5 mm)", corrosion=0.5)
        expected = "IPE200 (corrosion: 2.0 mm)"
        assert result == expected

    def test_double_corrosion_with_existing_values(self) -> None:
        """Test adding double corrosion to a name that already has corrosion."""
        result = update_name_with_corrosion(
            "RHS200x100x5 (corrosion inside: 1.0 mm, outside: 2.0 mm)",
            corrosion_inside=0.5,
            corrosion_outside=1.0,
        )
        expected = "RHS200x100x5 (corrosion inside: 1.5 mm, outside: 3.0 mm)"
        assert result == expected


class TestUpdateSingleCorrosion:
    """Test suite for _update_single_corrosion function."""

    def test_no_existing_corrosion(self) -> None:
        """Test updating a name with no existing corrosion."""
        result = _update_single_corrosion("IPE200", 1.5)
        expected = "IPE200 (corrosion: 1.5 mm)"
        assert result == expected

    def test_with_existing_corrosion(self) -> None:
        """Test updating a name with existing corrosion."""
        result = _update_single_corrosion("IPE200 (corrosion: 1.5 mm)", 0.5)
        expected = "IPE200 (corrosion: 2.0 mm)"
        assert result == expected

    def test_zero_additional_corrosion_no_existing(self) -> None:
        """Test adding zero corrosion to a name with no existing corrosion."""
        result = _update_single_corrosion("IPE200", 0.0)
        expected = "IPE200 (corrosion: 0.0 mm)"
        assert result == expected

    def test_zero_additional_corrosion_with_existing(self) -> None:
        """Test adding zero corrosion to a name with existing corrosion."""
        result = _update_single_corrosion("IPE200 (corrosion: 2.5 mm)", 0.0)
        expected = "IPE200 (corrosion: 2.5 mm)"
        assert result == expected

    def test_decimal_corrosion_values(self) -> None:
        """Test with decimal corrosion values."""
        result = _update_single_corrosion("IPE200 (corrosion: 1.25 mm)", 0.75)
        expected = "IPE200 (corrosion: 2.0 mm)"
        assert result == expected

    def test_preserves_base_name_with_whitespace(self) -> None:
        """Test that trailing/leading whitespace is handled correctly."""
        result = _update_single_corrosion("IPE200   (corrosion: 1.0 mm)  ", 0.5)
        expected = "IPE200 (corrosion: 1.5 mm)"
        assert result == expected


class TestUpdateDoubleCorrosion:
    """Test suite for _update_double_corrosion function."""

    def test_no_existing_corrosion(self) -> None:
        """Test updating a name with no existing corrosion."""
        result = _update_double_corrosion("RHS200x100x5", 1.0, 2.0)
        expected = "RHS200x100x5 (corrosion inside: 1.0 mm, outside: 2.0 mm)"
        assert result == expected

    def test_with_existing_corrosion(self) -> None:
        """Test updating a name with existing corrosion."""
        result = _update_double_corrosion(
            "RHS200x100x5 (corrosion inside: 1.0 mm, outside: 2.0 mm)",
            0.5,
            1.0,
        )
        expected = "RHS200x100x5 (corrosion inside: 1.5 mm, outside: 3.0 mm)"
        assert result == expected

    def test_inside_zero_outside_nonzero_no_existing(self) -> None:
        """Test with inside corrosion zero and outside corrosion non-zero, no existing corrosion."""
        result = _update_double_corrosion("RHS200x100x5", 0.0, 2.5)
        expected = "RHS200x100x5 (corrosion inside: 0.0 mm, outside: 2.5 mm)"
        assert result == expected

    def test_inside_nonzero_outside_zero_no_existing(self) -> None:
        """Test with inside corrosion non-zero and outside corrosion zero, no existing corrosion."""
        result = _update_double_corrosion("RHS200x100x5", 1.5, 0.0)
        expected = "RHS200x100x5 (corrosion inside: 1.5 mm, outside: 0.0 mm)"
        assert result == expected

    def test_inside_zero_outside_nonzero_with_existing(self) -> None:
        """Test with inside corrosion zero and outside corrosion non-zero, with existing corrosion."""
        result = _update_double_corrosion(
            "RHS200x100x5 (corrosion inside: 1.0 mm, outside: 2.0 mm)",
            0.0,
            1.5,
        )
        expected = "RHS200x100x5 (corrosion inside: 1.0 mm, outside: 3.5 mm)"
        assert result == expected

    def test_inside_nonzero_outside_zero_with_existing(self) -> None:
        """Test with inside corrosion non-zero and outside corrosion zero, with existing corrosion."""
        result = _update_double_corrosion(
            "RHS200x100x5 (corrosion inside: 1.0 mm, outside: 2.0 mm)",
            0.5,
            0.0,
        )
        expected = "RHS200x100x5 (corrosion inside: 1.5 mm, outside: 2.0 mm)"
        assert result == expected

    def test_both_zero_no_existing(self) -> None:
        """Test with both corrosion values zero and no existing corrosion."""
        result = _update_double_corrosion("RHS200x100x5", 0.0, 0.0)
        expected = "RHS200x100x5 (corrosion inside: 0.0 mm, outside: 0.0 mm)"
        assert result == expected

    def test_both_zero_with_existing(self) -> None:
        """Test with both corrosion values zero and existing corrosion."""
        result = _update_double_corrosion(
            "RHS200x100x5 (corrosion inside: 1.0 mm, outside: 2.0 mm)",
            0.0,
            0.0,
        )
        expected = "RHS200x100x5 (corrosion inside: 1.0 mm, outside: 2.0 mm)"
        assert result == expected

    def test_decimal_corrosion_values(self) -> None:
        """Test with decimal corrosion values."""
        result = _update_double_corrosion(
            "RHS200x100x5 (corrosion inside: 1.25 mm, outside: 2.75 mm)",
            0.25,
            0.25,
        )
        expected = "RHS200x100x5 (corrosion inside: 1.5 mm, outside: 3.0 mm)"
        assert result == expected

    def test_preserves_base_name_with_whitespace(self) -> None:
        """Test that trailing/leading whitespace is handled correctly."""
        result = _update_double_corrosion(
            "RHS200x100x5   (corrosion inside: 1.0 mm, outside: 2.0 mm)  ",
            0.5,
            1.0,
        )
        expected = "RHS200x100x5 (corrosion inside: 1.5 mm, outside: 3.0 mm)"
        assert result == expected
