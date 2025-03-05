"""Test for formula 2.21 from CUR 228."""

import pytest

from blueprints.codes.cur.cur_228.formula_2_21 import Form2Dot21ModulusHorizontalSubgrade
from blueprints.validations import LessOrEqualToZeroError


class TestForm2Dot21ModulusHorizontalSubgrade:
    """Validation for formula 2.21 from CUR 228."""

    def test_evaluation(self) -> None:
        """Test the evaluation of the result."""
        # Example values
        r = 0.5  # m
        e_p = 2.47  # kN/m²
        alpha = 1 / 3  # -
        form_2_21 = Form2Dot21ModulusHorizontalSubgrade(r=r, e_p=e_p, alpha=alpha)

        # Expected result, manually calculated
        manually_calculated_result = 9.187357198

        assert form_2_21 == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("e_p", "r", "alpha"),
        [
            (-500.0, -0.6, -0.33),
            (0.0, 0.0, 0.0),
        ],
    )
    def test_raise_error_when_invalid_values_are_given(self, e_p: float, r: float, alpha: float) -> None:
        """Test invalid values."""
        with pytest.raises(LessOrEqualToZeroError):
            Form2Dot21ModulusHorizontalSubgrade(r=r, e_p=e_p, alpha=alpha)

    @pytest.mark.parametrize(
        ("r"),
        [
            (0.2),
            (0.29),
        ],
    )
    def test_raise_error_when_invalid_diameter_values_are_given(self, r: float) -> None:
        """Test invalid values."""
        with pytest.raises(ValueError):
            Form2Dot21ModulusHorizontalSubgrade(r=r, e_p=500, alpha=0.33)

    def test_latex_method(self) -> None:
        """Test the latex method."""
        r = 0.5  # m
        e_p = 2.47  # kN/m²
        alpha = 1 / 3  # -
        form_2_21 = Form2Dot21ModulusHorizontalSubgrade(r=r, e_p=e_p, alpha=alpha)

        # Test the full LaTeX representation
        assert isinstance(form_2_21.latex().complete, str)
