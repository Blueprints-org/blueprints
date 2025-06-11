"""Testing formula 6.41 of EN 1993-1-1:2005."""

import pytest

from blueprints.codes.eurocode.en_1993_1_1_2005.chapter_6_ultimate_limit_state.formula_6_41 import Form6Dot41BiaxialBendingCheck
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestForm6Dot41BiaxialBendingCheck:
    """Validation for formula 6.41 from EN 1993-1-1:2005."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        my_ed = 100.0
        m_n_y_rd = 200.0
        mz_ed = 50.0
        m_n_z_rd = 150.0
        alpha = 1.0
        beta = 1.0

        # Object to test
        formula = Form6Dot41BiaxialBendingCheck(
            my_ed=my_ed,
            m_n_y_rd=m_n_y_rd,
            mz_ed=mz_ed,
            m_n_z_rd=m_n_z_rd,
            alpha=alpha,
            beta=beta,
        )

        # Expected result, manually calculated
        expected_result = True

        assert formula == expected_result

    def test_evaluation_not_ok(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        my_ed = 100.0
        m_n_y_rd = 200.0
        mz_ed = 50.0
        m_n_z_rd = 150.0
        alpha = 1.0
        beta = 0.63

        # Object to test
        formula = Form6Dot41BiaxialBendingCheck(
            my_ed=my_ed,
            m_n_y_rd=m_n_y_rd,
            mz_ed=mz_ed,
            m_n_z_rd=m_n_z_rd,
            alpha=alpha,
            beta=beta,
        )

        # Expected result, manually calculated
        expected_result = False

        assert formula == expected_result

    @pytest.mark.parametrize(
        ("my_ed", "m_n_y_rd", "mz_ed", "m_n_z_rd", "alpha", "beta"),
        [
            (-100.0, 200.0, 50.0, 150.0, 1.0, 1.0),  # my_ed is negative
            (100.0, 200.0, -50.0, 150.0, 1.0, 1.0),  # mz_ed is negative
            (100.0, 200.0, 50.0, 150.0, -1.0, 1.0),  # alpha is negative
            (100.0, 200.0, 50.0, 150.0, 1.0, -1.0),  # beta is negative
        ],
    )
    def test_raise_error_when_negative_values_are_given(
        self, my_ed: float, m_n_y_rd: float, mz_ed: float, m_n_z_rd: float, alpha: float, beta: float
    ) -> None:
        """Test invalid negative values."""
        with pytest.raises(NegativeValueError):
            Form6Dot41BiaxialBendingCheck(
                my_ed=my_ed,
                m_n_y_rd=m_n_y_rd,
                mz_ed=mz_ed,
                m_n_z_rd=m_n_z_rd,
                alpha=alpha,
                beta=beta,
            )

    @pytest.mark.parametrize(
        ("my_ed", "m_n_y_rd", "mz_ed", "m_n_z_rd", "alpha", "beta"),
        [
            (100.0, 0.0, 50.0, 150.0, 1.0, 1.0),  # m_n_y_rd is zero
            (100.0, -200.0, 50.0, 150.0, 1.0, 1.0),  # m_n_y_rd is negative
            (100.0, 200.0, 50.0, 0.0, 1.0, 1.0),  # m_n_z_rd is zero
            (100.0, 200.0, 50.0, -150.0, 1.0, 1.0),  # m_n_z_rd is negative
        ],
    )
    def test_raise_error_when_invalid_denominator_values_are_given(
        self, my_ed: float, m_n_y_rd: float, mz_ed: float, m_n_z_rd: float, alpha: float, beta: float
    ) -> None:
        """Test invalid denominator values."""
        with pytest.raises(LessOrEqualToZeroError):
            Form6Dot41BiaxialBendingCheck(
                my_ed=my_ed,
                m_n_y_rd=m_n_y_rd,
                mz_ed=mz_ed,
                m_n_z_rd=m_n_z_rd,
                alpha=alpha,
                beta=beta,
            )

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"CHECK \to \left[ \frac{M_{y,Ed}}{M_{N,y,Rd}} \right]^{\alpha} + "
                r"\left[ \frac{M_{z,Ed}}{M_{N,z,Rd}} \right]^{\beta} \leq 1 \to "
                r"\left[ \frac{100.000}{200.000} \right]^{1.000} + "
                r"\left[ \frac{50.000}{150.000} \right]^{1.000} \leq 1 \to OK",
            ),
            (
                "complete_with_units",
                r"CHECK \to \left[ \frac{M_{y,Ed}}{M_{N,y,Rd}} \right]^{\alpha} + "
                r"\left[ \frac{M_{z,Ed}}{M_{N,z,Rd}} \right]^{\beta} \leq 1 \to "
                r"\left[ \frac{100.000 \ Nmm}{200.000 \ Nmm} \right]^{1.000} + "
                r"\left[ \frac{50.000 \ Nmm}{150.000 \ Nmm} \right]^{1.000} \leq 1 \to OK",
            ),
            ("short", r"CHECK \to OK"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        my_ed = 100.0
        m_n_y_rd = 200.0
        mz_ed = 50.0
        m_n_z_rd = 150.0
        alpha = 1.0
        beta = 1.0

        # Object to test
        latex = Form6Dot41BiaxialBendingCheck(
            my_ed=my_ed,
            m_n_y_rd=m_n_y_rd,
            mz_ed=mz_ed,
            m_n_z_rd=m_n_z_rd,
            alpha=alpha,
            beta=beta,
        ).latex()

        actual = {
            "complete": latex.complete,
            "complete_with_units": latex.complete_with_units,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."
