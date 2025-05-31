"""Testing sub-formula 2 of 3.14 of EN 1992-1-1:2004."""

import pytest

from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_3_materials.formula_3_14 import SubForm3Dot14K


class TestSub2Form3Dot14K:
    """Validation for sub-formula 2 of 3.14 from EN 1992-1-1:2004."""

    def test_evaluation(self) -> None:
        """Test the evaluation of the result."""
        # Example values
        e_cm = 3.3  # MPa
        epsilon_c1 = 0.43  # -
        f_cm = 6.7  # MPa

        sub_2_form_3_14 = SubForm3Dot14K(e_cm=e_cm, epsilon_c1=epsilon_c1, f_cm=f_cm)

        # Expected result, manually calculated
        manually_calculated_result = 0.22238

        assert sub_2_form_3_14 == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_raise_error_when_negative_e_cm_is_given(self) -> None:
        """Test formula raising error by a negative value."""
        # Example values
        e_cm = -3.3  # MPa
        epsilon_c1 = 0.43  # -
        f_cm = 6.7  # MPa

        with pytest.raises(ValueError):
            SubForm3Dot14K(e_cm=e_cm, epsilon_c1=epsilon_c1, f_cm=f_cm)

    def test_raise_error_when_negative_or_zero_f_cm_is_given(self) -> None:
        """Test formula raising error by a negative or zero value."""
        # Example values
        e_cm = 3.3  # MPa
        epsilon_c1 = 0.43  # -
        f_cm = 0  # MPa

        with pytest.raises(ValueError):
            SubForm3Dot14K(e_cm=e_cm, epsilon_c1=epsilon_c1, f_cm=f_cm)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"k = 1.05 \cdot E_{cm} \cdot |\epsilon_{c1}| / f_{cm} = 1.05 \cdot 3.300 \cdot |0.430| / 6.700 = 0.222",
            ),
            ("short", r"k = 0.222"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        e_cm = 3.3  # MPa
        epsilon_c1 = 0.43  # -
        f_cm = 6.7  # MPa

        # Object to test
        form_3_14sub2_latex = SubForm3Dot14K(e_cm=e_cm, epsilon_c1=epsilon_c1, f_cm=f_cm).latex()

        actual = {"complete": form_3_14sub2_latex.complete, "short": form_3_14sub2_latex.short}

        assert actual[representation] == expected, f"{representation} representation failed."
