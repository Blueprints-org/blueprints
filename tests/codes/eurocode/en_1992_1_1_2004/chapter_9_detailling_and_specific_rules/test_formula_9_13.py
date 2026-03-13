"""Testing formula 9.13 of EN 1992-1-1:2004."""

import pytest

from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_9_detailling_and_specific_rules.formula_9_13 import Form9Dot13TensileForceToBeAnchored
from blueprints.validations import NegativeValueError


class TestForm9Dot13TensileForceToBeAnchored:
    """Validation for formula 9.13 from EN 1992-1-1:2004."""

    def test_evaluation(self) -> None:
        """Test the evaluation of the result."""
        # Example values
        r = 100  # mm
        z_e = 50  # mm
        z_i = 20  # mm
        form_9_13 = Form9Dot13TensileForceToBeAnchored(r=r, z_e=z_e, z_i=z_i)

        # Expected result, manually calculated
        manually_calculated_result = 250

        assert form_9_13 == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_raise_error_when_negative_r_is_given(self) -> None:
        """Test whether negative value error is raised if r is negative."""
        r = -100  # mm
        z_e = 50  # mm
        z_i = 20  # mm

        with pytest.raises(NegativeValueError):
            Form9Dot13TensileForceToBeAnchored(r=r, z_e=z_e, z_i=z_i)

    def test_raise_error_when_negative_z_e_is_given(self) -> None:
        """Test whether negative value error is raised if z_e is negative."""
        r = 100  # mm
        z_e = -50  # mm
        z_i = 20  # mm

        with pytest.raises(NegativeValueError):
            Form9Dot13TensileForceToBeAnchored(r=r, z_e=z_e, z_i=z_i)

    def test_raise_error_when_negative_z_i_is_given(self) -> None:
        """Test whether negative value error is raised if z_i is negative."""
        r = 100  # mm
        z_e = 50  # mm
        z_i = -20  # mm

        with pytest.raises(NegativeValueError):
            Form9Dot13TensileForceToBeAnchored(r=r, z_e=z_e, z_i=z_i)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"F_s = R \cdot z_e / z_i = 100.00 \cdot 50.00 / 20.00 = 250.00",
            ),
            ("short", r"F_s = 250.00"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        r = 100  # mm
        z_e = 50  # mm
        z_i = 20  # mm

        # Object to test
        form_9_13_latex = Form9Dot13TensileForceToBeAnchored(r=r, z_e=z_e, z_i=z_i).latex()

        actual = {"complete": form_9_13_latex.complete, "short": form_9_13_latex.short}

        assert actual[representation] == expected, f"{representation} representation failed."
