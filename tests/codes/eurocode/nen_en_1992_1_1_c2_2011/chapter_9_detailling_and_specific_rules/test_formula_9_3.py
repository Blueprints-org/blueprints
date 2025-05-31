"""Testing formula 9.3 of EN 1992-1-1:2004."""

import pytest

from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_9_detailling_and_specific_rules.formula_9_3 import Form9Dot3ShiftInMomentDiagram
from blueprints.validations import NegativeValueError


class TestForm9Dot3ShiftInMomentDiagram:
    """Validation for formula 9.3 from EN 1992-1-1:2004."""

    def test_evaluation(self) -> None:
        """Test the evaluation of the result."""
        # Example values
        v_ed = -200  # kN
        a_l = 200  # mm
        z = 250  # mm
        n_ed = 500  # kN
        form_9_3 = Form9Dot3ShiftInMomentDiagram(
            v_ed=v_ed,
            a_l=a_l,
            z=z,
            n_ed=n_ed,
        )

        # Expected result, manually calculated
        manually_calculated_result = 660

        assert form_9_3 == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_raise_error_when_negative_z_is_given(self) -> None:
        """Test if error is raised when z is negative."""
        # Example values
        v_ed = -200  # kN
        a_l = 200  # mm
        z = -250  # mm
        n_ed = 500  # kN

        with pytest.raises(NegativeValueError):
            Form9Dot3ShiftInMomentDiagram(
                v_ed=v_ed,
                a_l=a_l,
                z=z,
                n_ed=n_ed,
            )

    def test_raise_error_when_negative_a_l_is_given(self) -> None:
        """Test if error is raised when a_l is negative."""
        # Example values
        v_ed = -200  # kN
        a_l = -200  # mm
        z = 250  # mm
        n_ed = 500  # kN

        with pytest.raises(NegativeValueError):
            Form9Dot3ShiftInMomentDiagram(
                v_ed=v_ed,
                a_l=a_l,
                z=z,
                n_ed=n_ed,
            )

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"F_E = |V_{Ed}| \cdot a_l / z + N_{Ed} = |-200.00| \cdot 200.00 / 250.00 + 500.00 = 660.00",
            ),
            ("short", r"F_E = 660.00"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        v_ed = -200  # kN
        a_l = 200  # mm
        z = 250  # mm
        n_ed = 500  # kN

        # Object to test
        form_9_3_latex = Form9Dot3ShiftInMomentDiagram(
            v_ed=v_ed,
            a_l=a_l,
            z=z,
            n_ed=n_ed,
        ).latex()

        actual = {"complete": form_9_3_latex.complete, "short": form_9_3_latex.short}

        assert actual[representation] == expected, f"{representation} representation failed."
