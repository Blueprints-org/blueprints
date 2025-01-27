"""Testing formula 5.13 of NEN-EN 1993-5:2008."""

import pytest

from blueprints.codes.eurocode.nen_en_1993_5_2008.chapter_5_ultimate_limit_states.formula_5_13 import Form5Dot13SimplifiedBucklingCheck
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestForm5Dot13SimplifiedBucklingCheck:
    """Validation for formula 5.13 from NEN-EN 1993-5:2008."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        n_ed = 100.0  # kN
        m_ed = 50.0  # kNm
        a = 2000.0  # mm^2
        f_y = 355.0  # MPa
        gamma_m0 = 1.0  # dimensionless
        gamma_m1 = 1.0  # dimensionless
        chi = 0.9  # dimensionless
        m_c_rd = 110.0  # kNm

        # Object to test
        formula = Form5Dot13SimplifiedBucklingCheck(n_ed=n_ed, m_ed=m_ed, a=a, f_y=f_y, gamma_m0=gamma_m0, gamma_m1=gamma_m1, chi=chi, m_c_rd=m_c_rd)

        # Expected result, manually calculated
        expected_result = True

        assert formula == expected_result

    @pytest.mark.parametrize(
        ("n_ed", "m_ed", "a", "f_y", "gamma_m0", "gamma_m1", "chi", "m_c_rd"),
        [
            (-100.0, 50.0, 2000.0, 355.0, 1.0, 1.0, 0.9, 100.0),  # n_ed is negative
            (100.0, -50.0, 2000.0, 355.0, 1.0, 1.0, 0.9, 100.0),  # m_ed is negative
            (100.0, 50.0, -2000.0, 355.0, 1.0, 1.0, 0.9, 100.0),  # a is negative
            (100.0, 50.0, 0, 355.0, 1.0, 1.0, 0.9, 100.0),  # a is zero
            (100.0, 50.0, 2000.0, -355.0, 1.0, 1.0, 0.9, 100.0),  # f_y is negative
            (100.0, 50.0, 2000.0, 0, 1.0, 1.0, 0.9, 100.0),  # f_y is zero
            (100.0, 50.0, 2000.0, 355.0, -1.0, 1.0, 0.9, 100.0),  # gamma_m0 is negative
            (100.0, 50.0, 2000.0, 355.0, 0.0, 1.0, 0.9, 100.0),  # gamma_m0 is zero
            (100.0, 50.0, 2000.0, 355.0, 1.0, -1.0, 0.9, 100.0),  # gamma_m1 is negative
            (100.0, 50.0, 2000.0, 355.0, 1.0, 0.0, 0.9, 100.0),  # gamma_m1 is zero
            (100.0, 50.0, 2000.0, 355.0, 1.0, 1.0, -0.9, 100.0),  # chi is negative
            (100.0, 50.0, 2000.0, 355.0, 1.0, 1.0, 0, 100.0),  # chi is zero
            (100.0, 50.0, 2000.0, 355.0, 1.0, 1.0, 0.9, -100.0),  # m_c_rd is negative
            (100.0, 50.0, 2000.0, 355.0, 1.0, 1.0, 0.9, 0),  # m_c_rd is zero
        ],
    )
    def test_raise_error_when_invalid_values_are_given(
        self, n_ed: float, m_ed: float, a: float, f_y: float, gamma_m0: float, gamma_m1: float, chi: float, m_c_rd: float
    ) -> None:
        """Test invalid values."""
        with pytest.raises((NegativeValueError, LessOrEqualToZeroError)):
            Form5Dot13SimplifiedBucklingCheck(n_ed=n_ed, m_ed=m_ed, a=a, f_y=f_y, gamma_m0=gamma_m0, gamma_m1=gamma_m1, chi=chi, m_c_rd=m_c_rd)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"CHECK \to \frac{N_{Ed}}{\chi \cdot (A \cdot f_{y} / \gamma_{M0}) \cdot \left( \frac{\gamma_{M0}}{\gamma_{M1}} \right)} + "
                r"1.15 \cdot \frac{M_{Ed}}{M_{c,Rd} \cdot \left( \frac{\gamma_{M0}}{\gamma_{M1}} \right)} \leq 1.0"
                r" \to \frac{100.000}{0.900 \cdot (2000.00 \cdot 355.0 / 1.0) \cdot \left( \frac{1.0}{1.0} \right)} + "
                r"1.15 \cdot \frac{50.000}{100.000 \cdot \left( \frac{1.0}{1.0} \right)} \leq 1.0 \to OK",
            ),
            ("short", r"CHECK \to OK"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        n_ed = 100.0  # kN
        m_ed = 50.0  # kNm
        a = 2000.0  # mm^2
        f_y = 355.0  # MPa
        gamma_m0 = 1.0  # dimensionless
        gamma_m1 = 1.0  # dimensionless
        chi = 0.9  # dimensionless
        m_c_rd = 100.0  # kNm

        # Object to test
        latex = Form5Dot13SimplifiedBucklingCheck(
            n_ed=n_ed, m_ed=m_ed, a=a, f_y=f_y, gamma_m0=gamma_m0, gamma_m1=gamma_m1, chi=chi, m_c_rd=m_c_rd
        ).latex()

        actual = {
            "complete": latex.complete,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"CHECK \to \frac{N_{Ed}}{\chi \cdot (A \cdot f_{y} / \gamma_{M0}) \cdot \left( \frac{\gamma_{M0}}{\gamma_{M1}} \right)} + "
                r"1.15 \cdot \frac{M_{Ed}}{M_{c,Rd} \cdot \left( \frac{\gamma_{M0}}{\gamma_{M1}} \right)} \leq 1.0"
                r" \to \frac{10000.000}{0.900 \cdot (2000.00 \cdot 355.0 / 1.0) \cdot \left( \frac{1.0}{1.0} \right)} + "
                r"1.15 \cdot \frac{50.000}{100.000 \cdot \left( \frac{1.0}{1.0} \right)} \leq 1.0 \to \text{Not OK}",
            ),
            ("short", r"CHECK \to \text{Not OK}"),
        ],
    )
    def test_latex_not_ok(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula "Not OK" case."""
        # Example values
        n_ed = 10000.0  # kN
        m_ed = 50.0  # kNm
        a = 2000.0  # mm^2
        f_y = 355.0  # MPa
        gamma_m0 = 1.0  # dimensionless
        gamma_m1 = 1.0  # dimensionless
        chi = 0.9  # dimensionless
        m_c_rd = 100.0  # kNm

        # Object to test
        latex = Form5Dot13SimplifiedBucklingCheck(
            n_ed=n_ed, m_ed=m_ed, a=a, f_y=f_y, gamma_m0=gamma_m0, gamma_m1=gamma_m1, chi=chi, m_c_rd=m_c_rd
        ).latex()

        actual = {
            "complete": latex.complete,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."
