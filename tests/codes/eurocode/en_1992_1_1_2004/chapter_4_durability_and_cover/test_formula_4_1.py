"""Testing formula 4.1 of EN 1992-1-1:2004."""

import pytest

from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_4_durability_and_cover.formula_4_1 import Form4Dot1NominalConcreteCover
from blueprints.validations import NegativeValueError


class TestForm4Dot1NominalConcreteCover:
    """Validation for formula 4.1 from EN 1992-1-1:2004."""

    def test_evaluation(self) -> None:
        """Test the evaluation of the result."""
        # Example values
        c_min = 60  # mm
        delta_c_dev = 5  # mm
        form_4_1 = Form4Dot1NominalConcreteCover(c_min=c_min, delta_c_dev=delta_c_dev)

        # Expected result, manually calculated
        manually_calculated_result = 65

        assert form_4_1 == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_raise_error_when_negative_c_min_is_given(self) -> None:
        """Test the evaluation of the result."""
        # Example values
        c_min = -60  # mm
        delta_c_dev = 5  # mm

        with pytest.raises(NegativeValueError):
            Form4Dot1NominalConcreteCover(c_min=c_min, delta_c_dev=delta_c_dev)

    def test_raise_error_when_negative_delta_c_dev_is_given(self) -> None:
        """Test the evaluation of the result."""
        # Example values
        c_min = 60  # mm
        delta_c_dev = -5  # mm

        with pytest.raises(NegativeValueError):
            Form4Dot1NominalConcreteCover(c_min=c_min, delta_c_dev=delta_c_dev)

    @pytest.mark.parametrize(
        ("representation", "expected_result"),
        [
            ("complete", r"c_{nom} = c_{min}+\Delta c_{dev} = 60+5 = 65.0"),
            ("short", "c_{nom} = 65.0"),
            ("string", r"c_{nom} = c_{min}+\Delta c_{dev} = 60+5 = 65.0"),
        ],
    )
    def test_latex(self, representation: str, expected_result: str) -> None:
        """Test the latex implementation."""
        c_min = 60  # mm
        delta_c_dev = 5  # mm
        form = Form4Dot1NominalConcreteCover(c_min=c_min, delta_c_dev=delta_c_dev).latex()

        actual = {
            "complete": form.complete,
            "short": form.short,
            "string": str(form),
        }

        assert actual[representation] == expected_result, f"{representation} representation failed."
