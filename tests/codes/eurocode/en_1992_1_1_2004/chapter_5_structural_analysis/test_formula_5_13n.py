"""Testing formula 5.13N of EN 1992-1-1:2004."""

from contextlib import AbstractContextManager
from contextlib import nullcontext as does_not_raise

import pytest

from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_5_structural_analysis.formula_5_13n import (
    Form5Dot13nSlendernessCriterionIsolatedMembers,
    SubForm5Dot13aCreepRatio,
    SubForm5Dot13bMechanicalReinforcementFactor,
    SubForm5Dot13cMomentRatio,
)
from blueprints.validations import EqualToZeroError, LessOrEqualToZeroError, NegativeValueError


class TestForm5Dot13nSlendernessCriterionIsolatedMembers:
    """Validation for formula 5.13N from EN 1992-1-1:2004."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        a = 0.7
        b = 1.1
        c = 0.7
        n_ed = 1_000_000
        a_c = 500_000
        f_cd = 20

        # Object to test
        formula = Form5Dot13nSlendernessCriterionIsolatedMembers(a=a, b=b, c=c, n_ed=n_ed, a_c=a_c, f_cd=f_cd)

        # Expected result, manually calculated
        manually_calculated_result = 34.0893

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
                r"\lambda_{lim} = \frac{20 \cdot A \cdot B \cdot C}{\sqrt{N_{Ed} \cdot A_c \cdot f_{cd}}} = "
                r"\frac{20 \cdot 0.700 \cdot 1.100 \cdot 0.700}{\sqrt{1000000.000 \cdot 500000.000 \cdot 20.000}} "
                r"= 34.089 \ -",
            ),
            (
                "complete_with_units",
                r"\lambda_{lim} = \frac{20 \cdot A \cdot B \cdot C}{\sqrt{N_{Ed} \cdot A_c \cdot f_{cd}}} = "
                r"\frac{20 \cdot 0.700 \cdot 1.100 \cdot 0.700}{\sqrt{1000000.000 \ N \cdot 500000.000 "
                r"\ mm^2 \cdot 20.000 \ MPa}} = 34.089 \ -",
            ),
            ("short", r"\lambda_{lim} = 34.089 \ -"),
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
    """Validation for formula 5.13a from EN 1992-1-1:2004."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example value
        phi_ef = 2.5

        # Object to test
        formula = SubForm5Dot13aCreepRatio(phi_ef=phi_ef)

        # Expected result, manually calculated
        manually_calculated_result = 0.6666666667

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_raise_error_when_invalid_values_are_given(self) -> None:
        """Test invalid values."""
        with pytest.raises(NegativeValueError):
            SubForm5Dot13aCreepRatio(phi_ef=-1.0)

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
        latex = SubForm5Dot13aCreepRatio(phi_ef=phi_ef).latex()

        actual = {
            "complete": latex.complete,
            "complete_with_units": latex.complete_with_units,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."


class TestForm5Dot13bMechanicalReinforcementFactor:
    """Validation for formula 5.13b from EN 1992-1-1:2004."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        a_s = 1000.0
        f_yd = 500.0
        a_c = 10000.0
        f_cd = 20.0

        # Object to test
        formula = SubForm5Dot13bMechanicalReinforcementFactor(a_s=a_s, f_yd=f_yd, a_c=a_c, f_cd=f_cd)

        # Expected result, manually calculated
        manually_calculated_result = 2.4494  # dimensionless

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
            SubForm5Dot13bMechanicalReinforcementFactor(a_s=a_s, f_yd=f_yd, a_c=a_c, f_cd=f_cd)

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
            SubForm5Dot13bMechanicalReinforcementFactor(a_s=a_s, f_yd=f_yd, a_c=a_c, f_cd=f_cd)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"B = \sqrt{1 + 2 \cdot \frac{A_s \cdot f_{yd}}{A_c \cdot f_{cd}}} = \sqrt{1 + 2 \cdot "
                r"\frac{1000.000 \cdot 500.000}{10000.000 \cdot 20.000}} = 2.449 \ -",
            ),
            (
                "complete_with_units",
                r"B = \sqrt{1 + 2 \cdot \frac{A_s \cdot f_{yd}}{A_c \cdot f_{cd}}} = \sqrt{1 + 2 \cdot "
                r"\frac{1000.000 \ mm^2 \cdot 500.000 \ MPa}{10000.000 \ mm^2 \cdot 20.000 \ MPa}} = 2.449 \ -",
            ),
            ("short", r"B = 2.449 \ -"),
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
        latex = SubForm5Dot13bMechanicalReinforcementFactor(a_s=a_s, f_yd=f_yd, a_c=a_c, f_cd=f_cd).latex()

        actual = {
            "complete": latex.complete,
            "complete_with_units": latex.complete_with_units,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."


class TestForm5Dot13cMomentFactor:
    """Validation for formula 5.13c from EN 1992-1-1:2004."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        m_01 = 100.0
        m_02 = 150.0

        # Object to test
        formula = SubForm5Dot13cMomentRatio(m_01=m_01, m_02=m_02)

        # Expected result, manually calculated
        manually_calculated_result = 1.033333  # dimensionless

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("m_01", "m_02", "expectation"),
        [
            (100.0, 150.0, does_not_raise()),
            (70, 70, does_not_raise()),  # m_01 == m_02
            (150, 0, pytest.raises(EqualToZeroError)),  # m_02 is zero
            (100, 50, pytest.raises(ValueError)),  # m_02 > m_01
        ],
        ids=[
            "passes",
            "m_01==m_02",
            "m_02=0",
            "m_02>m_01",
        ],
    )
    def test_raise_error_incorrect_args(self, m_01: float, m_02: float, expectation: AbstractContextManager) -> None:
        """Test if errors are raised."""
        with expectation:
            assert SubForm5Dot13cMomentRatio(m_01=m_01, m_02=m_02) is not None

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"C = 1.7 - \frac{M_{01}}{M_{02}} = 1.7 - \frac{100.000}{150.000} = 1.033 \ -",
            ),
            (
                "complete_with_units",
                r"C = 1.7 - \frac{M_{01}}{M_{02}} = 1.7 - \frac{100.000 \ kNm}{150.000 \ kNm} = 1.033 \ -",
            ),
            ("short", r"C = 1.033 \ -"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        m_01 = 100.0
        m_02 = 150.0

        # Object to test
        latex = SubForm5Dot13cMomentRatio(m_01=m_01, m_02=m_02).latex()

        actual = {
            "complete": latex.complete,
            "complete_with_units": latex.complete_with_units,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."
