"""Testing formula 6.2 of EN 1993-1-1:2005."""

import pytest

from blueprints.codes.eurocode.en_1993_1_1_2005.chapter_6_ultimate_limit_state.formula_6_2 import Form6Dot2UtilizationRatio
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestForm6Dot2UtilizationRatio:
    """Validation for form 6.2 from EN 1993-1-1:2005."""

    def test_evaluation(self) -> None:
        """Test the evaluation of the result."""
        # example values
        n_ed = 5.0  # [-]
        n_rd = 10.0  # [-]
        m_y_ed = 4.0  # [-]
        m_y_rd = 20.0  # [-]
        m_z_ed = 3.0  # [-]
        m_z_rd = 30.0  # [-]

        form_6_2 = Form6Dot2UtilizationRatio(n_ed=n_ed, n_rd=n_rd, m_y_ed=m_y_ed, m_y_rd=m_y_rd, m_z_ed=m_z_ed, m_z_rd=m_z_rd)
        # manually calculated result
        manually_calculated_result = (5 / 10) + (4 / 20) + (3 / 30)  # -

        assert form_6_2 == pytest.approx(manually_calculated_result, rel=1e-9)

    @pytest.mark.parametrize(
        ("n_ed", "n_rd", "m_y_ed", "m_y_rd", "m_z_ed", "m_z_rd"),
        [
            (-5.0, 10.0, 4.0, 20.0, 3.0, 30.0),
            (5.0, 10.0, -4.0, 20.0, 3.0, 30.0),
            (5.0, 10.0, 4.0, 20.0, -3.0, 30.0),
        ],
    )
    def test_raise_error_if_negative(self, n_ed: float, n_rd: float, m_y_ed: float, m_y_rd: float, m_z_ed: float, m_z_rd: float) -> None:
        """Test that a NegativeValueError is raised when a negative value is passed for n_ed."""
        with pytest.raises(NegativeValueError):
            Form6Dot2UtilizationRatio(n_ed=n_ed, n_rd=n_rd, m_y_ed=m_y_ed, m_y_rd=m_y_rd, m_z_ed=m_z_ed, m_z_rd=m_z_rd)

    @pytest.mark.parametrize(
        ("n_ed", "n_rd", "m_y_ed", "m_y_rd", "m_z_ed", "m_z_rd"),
        [
            (5.0, 0.0, 4.0, 20.0, 3.0, 30.0),
            (5.0, -10.0, 4.0, 20.0, 3.0, 30.0),
            (5.0, 10.0, 4.0, 0.0, 3.0, 30.0),
            (5.0, 10.0, 4.0, -20.0, 3.0, 30.0),
            (5.0, 10.0, 4.0, 20.0, 3.0, 0.0),
            (5.0, 10.0, 4.0, 20.0, 3.0, -30.0),
        ],
    )
    def test_raise_error_if_negative_or_zero(self, n_ed: float, n_rd: float, m_y_ed: float, m_y_rd: float, m_z_ed: float, m_z_rd: float) -> None:
        """Test that a LessOrEqualToZeroError is raised when a zero or negative value is passed for n_rd, m_y_rd, or m_z_rd."""
        with pytest.raises(LessOrEqualToZeroError):
            Form6Dot2UtilizationRatio(n_ed=n_ed, n_rd=n_rd, m_y_ed=m_y_ed, m_y_rd=m_y_rd, m_z_ed=m_z_ed, m_z_rd=m_z_rd)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                (
                    r"UC = \frac{N_{Ed}}{N_{Rd}} + \frac{M_{y,Ed}}{M_{y,Rd}} + \frac{M_{z,Ed}}{M_{z,Rd}} ="
                    r" \frac{5.000}{10.000} + \frac{4.000}{20.000} + \frac{3.000}{30.000} = 0.800"
                ),
            ),
            ("short", r"UC = 0.800"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the form."""
        # Example values
        n_ed = 5.0  # [-]
        n_rd = 10.0  # [-]
        m_y_ed = 4.0  # [-]
        m_y_rd = 20.0  # [-]
        m_z_ed = 3.0  # [-]
        m_z_rd = 30.0  # [-]

        # Object to test
        form_6_2_latex = Form6Dot2UtilizationRatio(n_ed=n_ed, n_rd=n_rd, m_y_ed=m_y_ed, m_y_rd=m_y_rd, m_z_ed=m_z_ed, m_z_rd=m_z_rd).latex()

        actual = {
            "complete": form_6_2_latex.complete,
            "short": form_6_2_latex.short,
        }

        assert actual[representation] == expected, f"{representation} representation failed."
