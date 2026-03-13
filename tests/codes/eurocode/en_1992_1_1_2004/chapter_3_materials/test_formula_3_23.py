"""Testing formula 3.23 of EN 1992-1-1:2004."""

import pytest

from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_3_materials.formula_3_23 import Form3Dot23FlexuralTensileStrength


class TestForm3Dot23FlexuralTensileStrength:
    """Validation for formula 3.23 from EN 1992-1-1:2004."""

    def test_evaluation_1(self) -> None:
        """Test the evaluation of the result."""
        # Example values
        h = 305.3  # mm
        f_ctm = 23.8  # MPa

        form_3_23 = Form3Dot23FlexuralTensileStrength(h=h, f_ctm=f_ctm)

        # Expected result, manually calculated
        manually_calculated_result = 30.81386

        assert form_3_23 == pytest.approx(expected=manually_calculated_result, rel=1e-5)

    def test_evaluation_2(self) -> None:
        """Test the evaluation of the result."""
        # Example values
        h = 1000  # mm
        f_ctm = 23.8  # MPa

        form_3_23 = Form3Dot23FlexuralTensileStrength(h=h, f_ctm=f_ctm)

        # Expected result, manually calculated
        manually_calculated_result = 23.8

        assert form_3_23 == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_raise_error_when_negative_h_is_given(self) -> None:
        """Test a negative value for h."""
        # Example values
        h = -1000  # mm
        f_ctm = 23.8  # MPa

        with pytest.raises(ValueError):
            Form3Dot23FlexuralTensileStrength(h=h, f_ctm=f_ctm)

    def test_raise_error_when_negative_f_ctm_is_given(self) -> None:
        """Test a negative value for f_ctm."""
        # Example values
        h = 1000  # mm
        f_ctm = -23.8  # MPa

        with pytest.raises(ValueError):
            Form3Dot23FlexuralTensileStrength(h=h, f_ctm=f_ctm)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"f_{ctm,fl} = \max \left[ (1.6 - h/1000) \cdot f_{ctm} ; f_{ctm} \right] = "
                r"\max \left[ (1.6 - 305.300/1000) \cdot 23.800 ; 23.800 \right] = 30.814",
            ),
            ("short", r"f_{ctm,fl} = 30.814"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        h = 305.3  # mm
        f_ctm = 23.8  # MPa

        # Object to test
        form_3_23_latex = Form3Dot23FlexuralTensileStrength(h=h, f_ctm=f_ctm).latex()

        actual = {"complete": form_3_23_latex.complete, "short": form_3_23_latex.short}

        assert actual[representation] == expected, f"{representation} representation failed."
