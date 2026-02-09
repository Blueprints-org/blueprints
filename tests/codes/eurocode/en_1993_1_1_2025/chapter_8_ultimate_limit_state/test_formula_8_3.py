"""Testing formula 8.3 from EN 1993-1-1:2025, chapter 8, ultimate limit state."""

import pytest

from blueprints.codes.eurocode.en_1993_1_1_2025.chapter_8_ultimate_limit_state.formula_8_3 import Form8Dot3UtilizationRatio
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestForm8Dot3UtilizationRatio:
    """Validation for formula 8.3 from EN 1993-1-1:2025, chapter 8, ultimate limit state."""

    def test_evaluation(self) -> None:
        """Test the evaluation of the result."""
        # example values
        n_ed = 5.0  # [-]
        n_rd = 10.0  # [-]
        m_y_ed = 4.0  # [-]
        m_y_rd = 20.0  # [-]
        m_z_ed = 3.0  # [-]
        m_z_rd = 30.0  # [-]

        form_8_3 = Form8Dot3UtilizationRatio(n_ed=n_ed, n_rd=n_rd, m_y_ed=m_y_ed, m_y_rd=m_y_rd, m_z_ed=m_z_ed, m_z_rd=m_z_rd)
        # manually calculated result
        manually_calculated_result = (5 / 10) + (4 / 20) + (3 / 30)  # -

        assert form_8_3 == pytest.approx(manually_calculated_result, rel=1e-9)

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
            Form8Dot3UtilizationRatio(n_ed=n_ed, n_rd=n_rd, m_y_ed=m_y_ed, m_y_rd=m_y_rd, m_z_ed=m_z_ed, m_z_rd=m_z_rd)

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
            Form8Dot3UtilizationRatio(n_ed=n_ed, n_rd=n_rd, m_y_ed=m_y_ed, m_y_rd=m_y_rd, m_z_ed=m_z_ed, m_z_rd=m_z_rd)

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
        form_8_3_latex = Form8Dot3UtilizationRatio(n_ed=n_ed, n_rd=n_rd, m_y_ed=m_y_ed, m_y_rd=m_y_rd, m_z_ed=m_z_ed, m_z_rd=m_z_rd).latex()

        actual = {
            "complete": form_8_3_latex.complete,
            "short": form_8_3_latex.short,
        }

        assert actual[representation] == expected, f"{representation} representation failed."
