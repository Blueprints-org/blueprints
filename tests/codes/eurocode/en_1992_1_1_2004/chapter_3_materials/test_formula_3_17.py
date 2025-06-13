"""Testing formula 3.17 of EN 1992-1-1:2004."""

import pytest

from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_3_materials.formula_3_17 import Form3Dot17CompressiveStressConcrete


class TestForm3Dot17CompressiveStressConcrete:
    """Validation for formula 3.17 from EN 1992-1-1:2004."""

    def test_evaluation(self) -> None:
        """Test the evaluation of the result."""
        # Example values
        f_cd = 18.50  # MPa
        epsilon_c = 0.64  # -
        epsilon_c2 = 0.81  # -
        n = 2.0  # -

        form_3_17 = Form3Dot17CompressiveStressConcrete(f_cd=f_cd, epsilon_c=epsilon_c, epsilon_c2=epsilon_c2, n=n)

        # Expected result, manually calculated
        manually_calculated_result = 17.68511

        assert form_3_17 == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_raise_error_when_negative_f_cd_is_given(self) -> None:
        """Test a negative value."""
        # Example values
        f_cd = -18.50  # MPa
        epsilon_c = 0.64  # -
        epsilon_c2 = 0.81  # -
        n = 2.0  # -

        with pytest.raises(ValueError):
            Form3Dot17CompressiveStressConcrete(f_cd=f_cd, epsilon_c=epsilon_c, epsilon_c2=epsilon_c2, n=n)

    def test_raise_error_when_negative_epsilon_c_is_given(self) -> None:
        """Test a negative value."""
        # Example values
        f_cd = 18.50  # MPa
        epsilon_c = -0.64  # -
        epsilon_c2 = 0.81  # -
        n = 2.0  # -

        with pytest.raises(ValueError):
            Form3Dot17CompressiveStressConcrete(f_cd=f_cd, epsilon_c=epsilon_c, epsilon_c2=epsilon_c2, n=n)

    def test_raise_error_when_epsilon_c_is_larger_than_epsilon_c2(self) -> None:
        """Test a negative value."""
        # Example values
        f_cd = 18.50  # MPa
        epsilon_c = 1.64  # -
        epsilon_c2 = 0.81  # -
        n = 2.0  # -

        with pytest.raises(ValueError):
            Form3Dot17CompressiveStressConcrete(f_cd=f_cd, epsilon_c=epsilon_c, epsilon_c2=epsilon_c2, n=n)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"\sigma_c = f_{cd} \cdot \left[ 1 - \left( 1 - \frac{\epsilon_c}{\epsilon_{c2}} \right)^n \right] = "
                r"18.500 \cdot \left[ 1 - \left( 1 - \frac{0.640}{0.810} \right)^{2.000} \right] = 17.685",
            ),
            ("short", r"\sigma_c = 17.685"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        f_cd = 18.50  # MPa
        epsilon_c = 0.64  # -
        epsilon_c2 = 0.81  # -
        n = 2.0  # -

        # Object to test
        form_3_17_latex = Form3Dot17CompressiveStressConcrete(f_cd=f_cd, epsilon_c=epsilon_c, epsilon_c2=epsilon_c2, n=n).latex()

        actual = {"complete": form_3_17_latex.complete, "short": form_3_17_latex.short}

        assert actual[representation] == expected, f"{representation} representation failed."
