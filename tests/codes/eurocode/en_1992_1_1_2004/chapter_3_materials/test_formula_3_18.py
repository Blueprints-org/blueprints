"""Testing formula 3.18 of EN 1992-1-1:2004."""

import pytest

from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_3_materials.formula_3_18 import Form3Dot18CompressiveStressConcrete


class TestForm3Dot18CompressiveStressConcrete:
    """Validation for formula 3.18 from EN 1992-1-1:2004."""

    def test_evaluation(self) -> None:
        """Test the evaluation of the result."""
        # Example values
        f_cd = 18.50  # MPa

        form_3_18 = Form3Dot18CompressiveStressConcrete(f_cd=f_cd)

        # Expected result, manually calculated
        manually_calculated_result = 18.50

        assert form_3_18 == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_raise_error_when_negative_f_cd_is_given(self) -> None:
        """Test a negative value."""
        # Example values
        f_cd = -18.50  # MPa

        with pytest.raises(ValueError):
            Form3Dot18CompressiveStressConcrete(f_cd=f_cd)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"\sigma_c = f_{cd} = 18.500 = 18.500",
            ),
            ("short", r"\sigma_c = 18.500"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        f_cd = 18.50  # MPa

        # Object to test
        form_3_18_latex = Form3Dot18CompressiveStressConcrete(f_cd=f_cd).latex()

        actual = {"complete": form_3_18_latex.complete, "short": form_3_18_latex.short}

        assert actual[representation] == expected, f"{representation} representation failed."
