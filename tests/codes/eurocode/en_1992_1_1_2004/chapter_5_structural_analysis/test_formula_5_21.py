"""Testing formula 5.21 of EN 1992-1-1:2004."""

import pytest

from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_5_structural_analysis.formula_5_21 import Form5Dot21NominalStiffness
from blueprints.validations import NegativeValueError


class TestForm5Dot21NominalStiffness:
    """Validation for formula 5.21 from EN 1992-1-1:2004."""

    def test_evaluation(self) -> None:
        """Test the evaluation of the result."""
        # Example values
        k_c = 0.8  # -
        e_cd = 30000  # MPa
        i_c = 5000  # mm^4
        k_s = 0.2  # -
        e_s = 200000  # MPa
        i_s = 1000  # mm^4

        # Object to test
        form_5_21 = Form5Dot21NominalStiffness(k_c=k_c, e_cd=e_cd, i_c=i_c, k_s=k_s, e_s=e_s, i_s=i_s)

        # Expected result, manually calculated
        manually_calculated_result = 160000000  # Nmm^2

        assert form_5_21 == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_raise_error_when_k_c_is_negative(self) -> None:
        """Test negative value for k_c."""
        k_c = -0.8
        e_cd = 30000
        i_c = 5000
        k_s = 0.2
        e_s = 200000
        i_s = 1000

        with pytest.raises(NegativeValueError):
            Form5Dot21NominalStiffness(k_c=k_c, e_cd=e_cd, i_c=i_c, k_s=k_s, e_s=e_s, i_s=i_s)

    def test_raise_error_when_e_cd_is_negative(self) -> None:
        """Test negative value for e_cd."""
        k_c = 0.8
        e_cd = -30000
        i_c = 5000
        k_s = 0.2
        e_s = 200000
        i_s = 1000

        with pytest.raises(NegativeValueError):
            Form5Dot21NominalStiffness(k_c=k_c, e_cd=e_cd, i_c=i_c, k_s=k_s, e_s=e_s, i_s=i_s)

    def test_raise_error_when_i_c_is_negative(self) -> None:
        """Test negative value for i_c."""
        k_c = 0.8
        e_cd = 30000
        i_c = -5000
        k_s = 0.2
        e_s = 200000
        i_s = 1000

        with pytest.raises(NegativeValueError):
            Form5Dot21NominalStiffness(k_c=k_c, e_cd=e_cd, i_c=i_c, k_s=k_s, e_s=e_s, i_s=i_s)

    def test_raise_error_when_k_s_is_negative(self) -> None:
        """Test negative value for k_s."""
        k_c = 0.8
        e_cd = 30000
        i_c = 5000
        k_s = -0.2
        e_s = 200000
        i_s = 1000

        with pytest.raises(NegativeValueError):
            Form5Dot21NominalStiffness(k_c=k_c, e_cd=e_cd, i_c=i_c, k_s=k_s, e_s=e_s, i_s=i_s)

    def test_raise_error_when_e_s_is_negative(self) -> None:
        """Test negative value for e_s."""
        k_c = 0.8
        e_cd = 30000
        i_c = 5000
        k_s = 0.2
        e_s = -200000
        i_s = 1000

        with pytest.raises(NegativeValueError):
            Form5Dot21NominalStiffness(k_c=k_c, e_cd=e_cd, i_c=i_c, k_s=k_s, e_s=e_s, i_s=i_s)

    def test_raise_error_when_i_s_is_negative(self) -> None:
        """Test negative value for i_s."""
        k_c = 0.8
        e_cd = 30000
        i_c = 5000
        k_s = 0.2
        e_s = 200000
        i_s = -1000

        with pytest.raises(NegativeValueError):
            Form5Dot21NominalStiffness(k_c=k_c, e_cd=e_cd, i_c=i_c, k_s=k_s, e_s=e_s, i_s=i_s)

    @pytest.mark.parametrize(
        ("representation", "expected_result"),
        [
            (
                "complete",
                r"EI = K_{c} \cdot E_{cd} \cdot I_{c} + K_{s} \cdot E_{s} \cdot I_{s} = 0.800 \cdot 30000.000 \cdot 5000.000 + "
                r"0.200 \cdot 200000.000 \cdot 1000.000 = 160000000.000",
            ),
            ("short", r"EI = 160000000.000"),
        ],
    )
    def test_latex(self, representation: str, expected_result: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        k_c = 0.8  # -
        e_cd = 30000  # MPa
        i_c = 5000  # mm^4
        k_s = 0.2  # -
        e_s = 200000  # MPa
        i_s = 1000  # mm^4

        # Object to test
        form_5_21_latex = Form5Dot21NominalStiffness(
            k_c=k_c,
            e_cd=e_cd,
            i_c=i_c,
            k_s=k_s,
            e_s=e_s,
            i_s=i_s,
        ).latex()

        actual = {
            "complete": form_5_21_latex.complete,
            "short": form_5_21_latex.short,
        }

        assert actual[representation] == expected_result, f"{representation} representation failed."
