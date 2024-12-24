"""Testing formula 5.13N of NEN-EN 1992-1-1+C2:2011."""

import pytest

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011.chapter_5_structural_analysis.formula_5_13n import (
    Form5Dot13NLimitSlenderness,
    Form5Dot13NSub1FactorForEffectiveCreepRatio,
    Form5Dot13NSub2FactorForMechanicalReinforcementRatio,
    Form5Dot13NSub3FactorForMomentRatio,
)
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestForm5Dot13NLimitSlenderness:
    """Validation for formula 5.13N from NEN-EN 1992-1-1+C2:2011."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        a = 1.0
        b = 2.0
        c = 3.0
        n = 4.0

        # Object to test
        formula = Form5Dot13NLimitSlenderness(a=a, b=b, c=c, n=n)

        # Expected result, manually calculated
        manually_calculated_result = 60.0

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("a", "b", "c", "n"),
        [
            (-1.0, 2.0, 3.0, 4.0),  # a is negative
            (1.0, -2.0, 3.0, 4.0),  # b is negative
            (1.0, 2.0, -3.0, 4.0),  # c is negative
            (1.0, 2.0, 3.0, -4.0),  # n is negative
            (1.0, 2.0, 3.0, 0.0),  # n is zero
        ],
    )
    def test_raise_error_when_invalid_values_are_given(self, a: float, b: float, c: float, n: float) -> None:
        """Test invalid values."""
        with pytest.raises((NegativeValueError, LessOrEqualToZeroError)):
            Form5Dot13NLimitSlenderness(a=a, b=b, c=c, n=n)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"\lambda_{lim} = 20 \cdot A \cdot B \cdot C / \sqrt{n} = 20 \cdot 1.000 " r"\cdot 2.000 \cdot 3.000 / \sqrt{4.000} = 60.000 -",
            ),
            ("short", r"\lambda_{lim} = 60.000 -"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        a = 1.0
        b = 2.0
        c = 3.0
        n = 4.0

        # Object to test
        latex = Form5Dot13NLimitSlenderness(a=a, b=b, c=c, n=n).latex()

        actual = {
            "complete": latex.complete,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."


class TestForm5Dot13NSub1FactorForEffectiveCreepRatio:
    """Validation for formula 5.13Nsub1 from NEN-EN 1992-1-1+C2:2011."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example value
        phi_ef = 2.0

        # Object to test
        formula = Form5Dot13NSub1FactorForEffectiveCreepRatio(phi_ef=phi_ef)

        # Expected result, manually calculated
        manually_calculated_result = 1 / 1.4

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        "phi_ef",
        [
            -1.0,  # phi_ef is negative
        ],
    )
    def test_raise_error_when_invalid_values_are_given(self, phi_ef: float) -> None:
        """Test invalid values."""
        with pytest.raises((NegativeValueError, LessOrEqualToZeroError)):
            Form5Dot13NSub1FactorForEffectiveCreepRatio(phi_ef=phi_ef)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"A = 1 / (1 + 0.2 \cdot \phi_{ef}) = 1 / (1 + 0.2 \cdot 2.000) = 0.714 -",
            ),
            ("short", r"A = 0.714 -"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example value
        phi_ef = 2.0

        # Object to test
        latex = Form5Dot13NSub1FactorForEffectiveCreepRatio(phi_ef=phi_ef).latex()

        actual = {
            "complete": latex.complete,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."


class TestForm5Dot13NSub2FactorForMechanicalReinforcementRatio:
    """Validation for formula 5.13Nsub2 from NEN-EN 1992-1-1+C2:2011."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        a_s = 1000.0
        f_yd = 500.0
        a_c = 2000.0
        f_cd = 30.0

        # Object to test
        formula = Form5Dot13NSub2FactorForMechanicalReinforcementRatio(a_s=a_s, f_yd=f_yd, a_c=a_c, f_cd=f_cd)

        # Expected result, manually calculated
        manually_calculated_result = 4.203

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("a_s", "f_yd", "a_c", "f_cd"),
        [
            (-1000.0, 500.0, 2000.0, 30.0),  # a_s is negative
            (1000.0, -500.0, 2000.0, 30.0),  # f_yd is negative
            (1000.0, 500.0, -2000.0, 30.0),  # a_c is negative
            (1000.0, 500.0, 2000.0, -30.0),  # f_cd is negative
            (1000.0, 500.0, 0.0, 30.0),  # a_c is zero
            (1000.0, 500.0, 2000.0, 0.0),  # f_cd is zero
        ],
    )
    def test_raise_error_when_invalid_values_are_given(self, a_s: float, f_yd: float, a_c: float, f_cd: float) -> None:
        """Test invalid values."""
        with pytest.raises((NegativeValueError, LessOrEqualToZeroError)):
            Form5Dot13NSub2FactorForMechanicalReinforcementRatio(a_s=a_s, f_yd=f_yd, a_c=a_c, f_cd=f_cd)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"B = \sqrt{1 + 2 \cdot \frac{A_s \cdot f_{yd}}{A_c \cdot f_{cd}}} = \sqrt{1 + 2 \cdot "
                r"\frac{1000.000 \cdot 500.000}{2000.000 \cdot 30.000}} = 4.203 -",
            ),
            ("short", r"B = 4.203 -"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        a_s = 1000.0
        f_yd = 500.0
        a_c = 2000.0
        f_cd = 30.0

        # Object to test
        latex = Form5Dot13NSub2FactorForMechanicalReinforcementRatio(a_s=a_s, f_yd=f_yd, a_c=a_c, f_cd=f_cd).latex()

        actual = {
            "complete": latex.complete,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."


class TestForm5Dot13NSub3FactorForMomentRatio:
    """Validation for formula 5.13Nsub3 from NEN-EN 1992-1-1+C2:2011."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        m_01 = 10.0
        m_02 = 20.0

        # Object to test
        formula = Form5Dot13NSub3FactorForMomentRatio(m_01=m_01, m_02=m_02)

        # Expected result, manually calculated
        manually_calculated_result = 1.2

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("m_01", "m_02"),
        [
            (-10.0, 20.0),  # m_01 is negative
            (10.0, -20.0),  # m_02 is negative
            (10.0, 0.0),  # m_02 is zero
            (30.0, 20.0),  # m_01 is greater than m_02
        ],
    )
    def test_raise_error_when_invalid_values_are_given(self, m_01: float, m_02: float) -> None:
        """Test invalid values."""
        with pytest.raises((NegativeValueError, ValueError)):
            Form5Dot13NSub3FactorForMomentRatio(m_01=m_01, m_02=m_02)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"C = 1.7 - \frac{M_{01}}{M_{02}} = 1.7 - \frac{10.000}{20.000} = 1.200 -",
            ),
            ("short", r"C = 1.200 -"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        m_01 = 10.0
        m_02 = 20.0

        # Object to test
        latex = Form5Dot13NSub3FactorForMomentRatio(m_01=m_01, m_02=m_02).latex()

        actual = {
            "complete": latex.complete,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."
