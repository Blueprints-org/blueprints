"""Testing formula 5.13N of NEN-EN 1992-1-1+C2:2011."""

import pytest

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011.chapter_5_structural_analysis.formula_5_13n import (
    Form5Dot13aCreepFactor,
    Form5Dot13bMechanicalReinforcementFactor,
    Form5Dot13cMomentFactor,
    Form5Dot13nSlendernessCriterionIsolatedMembers,
)
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestForm5Dot13nSlendernessCriterionIsolatedMembers:
    """Validation for formula 5.13N from NEN-EN 1992-1-1+C2:2011."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        a = 0.7
        b = 1.1
        c = 0.7
        n_ed = 1000000.0
        a_c = 500000.0
        f_cd = 20.0

        # Object to test
        formula = Form5Dot13nSlendernessCriterionIsolatedMembers(a=a, b=b, c=c, n_ed=n_ed, a_c=a_c, f_cd=f_cd)

        # Expected result, manually calculated
        manually_calculated_result = 3.409

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("a", "b", "c", "n_ed", "a_c", "f_cd"),
        [
            (-0.7, 1.1, 0.7, 1000000.0, 500000.0, 20.0),  # a is negative
            (0.7, -1.1, 0.7, 1000000.0, 500000.0, 20.0),  # b is negative
            (0.7, 1.1, -0.7, 1000000.0, 500000.0, 20.0),  # c is negative
        ],
    )
    def test_raise_error_when_negative_values_are_given(self, a: float, b: float, c: float, n_ed: float, a_c: float, f_cd: float) -> None:
        """Test negative values for a, b, and c."""
        with pytest.raises(NegativeValueError):
            Form5Dot13nSlendernessCriterionIsolatedMembers(a=a, b=b, c=c, n_ed=n_ed, a_c=a_c, f_cd=f_cd)

    @pytest.mark.parametrize(
        ("a", "b", "c", "n_ed", "a_c", "f_cd"),
        [
            (0.7, 1.1, 0.7, 0.0, 500000.0, 20.0),  # n_ed is zero
            (0.7, 1.1, 0.7, -1000000.0, 500000.0, 20.0),  # n_ed is negative
            (0.7, 1.1, 0.7, 1000000.0, 0.0, 20.0),  # a_c is zero
            (0.7, 1.1, 0.7, 1000000.0, -500000.0, 20.0),  # a_c is negative
            (0.7, 1.1, 0.7, 1000000.0, 500000.0, 0.0),  # f_cd is zero
            (0.7, 1.1, 0.7, 1000000.0, 500000.0, -20.0),  # f_cd is negative
        ],
    )
    def test_raise_error_when_zero_or_negative_values_are_given(self, a: float, b: float, c: float, n_ed: float, a_c: float, f_cd: float) -> None:
        """Test zero and negative values for n_ed, a_c, and f_cd."""
        with pytest.raises(LessOrEqualToZeroError):
            Form5Dot13nSlendernessCriterionIsolatedMembers(a=a, b=b, c=c, n_ed=n_ed, a_c=a_c, f_cd=f_cd)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"\lambda_{lim} = 20 \cdot A \cdot B \cdot C \cdot \sqrt{\frac{N_{Ed}}{A_c \cdot f_{cd}}} = "
                r"20 \cdot 0.700 \cdot 1.100 \cdot 0.700 \cdot \sqrt{\frac{1000000.000}{500000.000 \cdot 20.000}} = 3.409 \ -",
            ),
            (
                "complete_with_units",
                r"\lambda_{lim} = 20 \cdot A \cdot B \cdot C \cdot \sqrt{\frac{N_{Ed}}{A_c \cdot f_{cd}}} = "
                r"20 \cdot 0.700 \cdot 1.100 \cdot 0.700 \cdot \sqrt{\frac{1000000.000 \ N}{500000.000 \ mm^2 \cdot 20.000 \ MPa}} = 3.409 \ -",
            ),
            ("short", r"\lambda_{lim} = 3.409 \ -"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        a = 0.7
        b = 1.1
        c = 0.7
        n_ed = 1000000.0
        a_c = 500000.0
        f_cd = 20.0

        # Object to test
        latex = Form5Dot13nSlendernessCriterionIsolatedMembers(a=a, b=b, c=c, n_ed=n_ed, a_c=a_c, f_cd=f_cd).latex()

        actual = {
            "complete": latex.complete,
            "complete_with_units": latex.complete_with_units,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."


class TestForm5Dot13aCreepFactor:
    """Validation for formula 5.13a from NEN-EN 1992-1-1+C2:2011."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example value
        phi_ef = 2.5

        # Object to test
        formula = Form5Dot13aCreepFactor(phi_ef=phi_ef)

        # Expected result, manually calculated
        manually_calculated_result = 0.6666666667

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_raise_error_when_invalid_values_are_given(self) -> None:
        """Test invalid values."""
        with pytest.raises(NegativeValueError):
            Form5Dot13aCreepFactor(phi_ef=-1.0)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"A = \frac{1}{(1 + 0.2 \cdot \phi_{ef})} = \frac{1}{(1 + 0.2 \cdot 2.500)} = 0.667 \ -",
            ),
            ("short", r"A = 0.667 \ -"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example value
        phi_ef = 2.5

        # Object to test
        latex = Form5Dot13aCreepFactor(phi_ef=phi_ef).latex()

        actual = {
            "complete": latex.complete,
            "complete_with_units": latex.complete_with_units,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."


class TestForm5Dot13bMechanicalReinforcementFactor:
    """Validation for formula 5.13b from NEN-EN 1992-1-1+C2:2011."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        a_s = 1000.0
        f_yd = 500.0
        a_c = 10000.0
        f_cd = 20.0

        # Object to test
        formula = Form5Dot13bMechanicalReinforcementFactor(a_s=a_s, f_yd=f_yd, a_c=a_c, f_cd=f_cd)

        # Expected result, manually calculated
        manually_calculated_result = 2.5  # dimensionless

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("a_s", "f_yd", "a_c", "f_cd"),
        [
            (-1000.0, 500.0, 10000.0, 20.0),  # a_s is negative
            (1000.0, -500.0, 10000.0, 20.0),  # f_yd is negative
        ],
    )
    def test_raise_error_when_negative_values_are_given(self, a_s: float, f_yd: float, a_c: float, f_cd: float) -> None:
        """Test negative values."""
        with pytest.raises(NegativeValueError):
            Form5Dot13bMechanicalReinforcementFactor(a_s=a_s, f_yd=f_yd, a_c=a_c, f_cd=f_cd)

    @pytest.mark.parametrize(
        ("a_s", "f_yd", "a_c", "f_cd"),
        [
            (1000.0, 500.0, 0.0, 20.0),  # a_c is zero
            (1000.0, 500.0, -10000.0, 20.0),  # a_c is negative
            (1000.0, 500.0, 10000.0, 0.0),  # f_cd is zero
            (1000.0, 500.0, 10000.0, -20.0),  # f_cd is negative
        ],
    )
    def test_raise_error_when_less_or_equal_to_zero_values_are_given(self, a_s: float, f_yd: float, a_c: float, f_cd: float) -> None:
        """Test less or equal to zero values."""
        with pytest.raises(LessOrEqualToZeroError):
            Form5Dot13bMechanicalReinforcementFactor(a_s=a_s, f_yd=f_yd, a_c=a_c, f_cd=f_cd)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"B = \frac{A_s \cdot f_{yd}}{A_c \cdot f_{cd}} = "
                r"\frac{1000.000 \cdot 500.000}{10000.000 \cdot 20.000} = 2.500 \ -",
            ),
            (
                "complete_with_units",
                r"B = \frac{A_s \cdot f_{yd}}{A_c \cdot f_{cd}} = "
                r"\frac{1000.000 \ mm^2 \cdot 500.000 \ MPa}{10000.000 \ mm^2 \cdot 20.000 \ MPa} = 2.500 \ -",
            ),
            ("short", r"B = 2.500 \ -"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        a_s = 1000.0
        f_yd = 500.0
        a_c = 10000.0
        f_cd = 20.0

        # Object to test
        latex = Form5Dot13bMechanicalReinforcementFactor(a_s=a_s, f_yd=f_yd, a_c=a_c, f_cd=f_cd).latex()

        actual = {
            "complete": latex.complete,
            "complete_with_units": latex.complete_with_units,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."


class TestForm5Dot13cMomentFactor:
    """Validation for formula 5.13c from NEN-EN 1992-1-1+C2:2011."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        m_01 = 100.0
        m_02 = 150.0

        # Object to test
        formula = Form5Dot13cMomentFactor(m_01=m_01, m_02=m_02)

        # Expected result, manually calculated
        manually_calculated_result = 0.666667  # dimensionless

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_raise_error_when_m_01_is_negative(self) -> None:
        """Test invalid value for m_01."""
        with pytest.raises(NegativeValueError):
            Form5Dot13cMomentFactor(m_01=-100.0, m_02=150.0)

    def test_raise_error_when_m_02_is_zero(self) -> None:
        """Test invalid value for m_02 (zero)."""
        with pytest.raises(LessOrEqualToZeroError):
            Form5Dot13cMomentFactor(m_01=100.0, m_02=0.0)

    def test_raise_error_when_m_02_is_negative(self) -> None:
        """Test invalid value for m_02 (negative)."""
        with pytest.raises(LessOrEqualToZeroError):
            Form5Dot13cMomentFactor(m_01=100.0, m_02=-150.0)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"C = \frac{M_{01}}{M_{02}} = \frac{100.000}{150.000} = 0.667 \ -",
            ),
            (
                "complete_with_units",
                r"C = \frac{M_{01}}{M_{02}} = \frac{100.000 \ kNm}{150.000 \ kNm} = 0.667 \ -",
            ),
            ("short", r"C = 0.667 \ -"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        m_01 = 100.0
        m_02 = 150.0

        # Object to test
        latex = Form5Dot13cMomentFactor(m_01=m_01, m_02=m_02).latex()

        actual = {
            "complete": latex.complete,
            "complete_with_units": latex.complete_with_units,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."
