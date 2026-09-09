"""Testing formula 8.66 of FprEN 1992-1-1:2023."""

import pytest

from blueprints.codes.eurocode.fpr_en_1992_1_1_2023.chapter_8_ultimate_limit_states.formula_8_66 import (
    Form8Dot66CheckOmissionOfShearVerification,
)
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestForm8Dot66CheckOmissionOfShearVerification:
    """Validation for formula 8.66 from FprEN 1992-1-1:2023."""

    @pytest.mark.parametrize(
        ("tau_ed", "expected", "expected_unity_check"),
        [
            # the minimum transverse reinforcement carries 400 / (200 * 200) * 435 = 4.35 MPa
            (0.5, True, 0.11494252873563217),
            (5.0, False, 1.1494252873563218),
        ],
    )
    def test_evaluation(self, tau_ed: float, expected: bool, expected_unity_check: float) -> None:
        """Tests the verdict and the unity check that it is based on."""
        # Create object to test
        formula = Form8Dot66CheckOmissionOfShearVerification(tau_ed=tau_ed, a_st_min=400.0, s_f=200.0, h_f=200.0, f_yd=435.0)

        # Perform test by assert
        assert bool(formula) is expected
        assert formula.unity_check == pytest.approx(expected=expected_unity_check, rel=1e-4)

    @pytest.mark.parametrize(
        ("tau_ed", "expected"),
        [
            (4.0, True),  # exactly on the limit, which is inclusive as printed
            (4.000001, False),  # just above it
        ],
    )
    def test_bound_is_inclusive(self, tau_ed: float, expected: bool) -> None:
        """The bound is printed with a less than or equal sign, so a shear stress exactly on it passes.

        The values are chosen so that 400 / (200 * 200) * 400 is exactly 4.0 in floating point. With the 435
        of the other tests the limit comes out as 4.3500000000000005, and a case sitting on it would pass by
        rounding rather than by the printed inequality, which would prove nothing about inclusivity.
        """
        # Create object to test
        formula = Form8Dot66CheckOmissionOfShearVerification(tau_ed=tau_ed, a_st_min=400.0, s_f=200.0, h_f=200.0, f_yd=400.0)

        # Perform test by assert
        assert formula.rhs == 4.0
        assert bool(formula) is expected

    def test_both_sides_are_exposed(self) -> None:
        """The shear stress and the stress the minimum reinforcement carries are both available."""
        # Example values
        formula = Form8Dot66CheckOmissionOfShearVerification(tau_ed=0.5, a_st_min=400.0, s_f=200.0, h_f=200.0, f_yd=435.0)

        # Perform test by assert
        assert formula.lhs == pytest.approx(expected=0.5, rel=1e-4)
        assert formula.rhs == pytest.approx(expected=4.35, rel=1e-4)

    @pytest.mark.parametrize(
        ("tau_ed", "a_st_min", "f_yd"),
        [
            (-0.5, 400.0, 435.0),  # tau_ed is negative
            (0.5, -400.0, 435.0),  # a_st_min is negative
            (0.5, 400.0, -435.0),  # f_yd is negative
        ],
    )
    def test_raise_error_when_negative_values_are_given(self, tau_ed: float, a_st_min: float, f_yd: float) -> None:
        """Test if error is raised for parameters that are not allowed to be negative."""
        with pytest.raises(NegativeValueError):
            Form8Dot66CheckOmissionOfShearVerification(tau_ed=tau_ed, a_st_min=a_st_min, s_f=200.0, h_f=200.0, f_yd=f_yd)

    @pytest.mark.parametrize(
        ("s_f", "h_f"),
        [
            (-200.0, 200.0),  # s_f is negative
            (0.0, 200.0),  # s_f is zero
            (200.0, -200.0),  # h_f is negative
            (200.0, 0.0),  # h_f is zero
        ],
    )
    def test_raise_error_when_less_or_equal_to_zero(self, s_f: float, h_f: float) -> None:
        """Test if error is raised for parameters that are not allowed to be zero or less."""
        with pytest.raises(LessOrEqualToZeroError):
            Form8Dot66CheckOmissionOfShearVerification(tau_ed=0.5, a_st_min=400.0, s_f=s_f, h_f=h_f, f_yd=435.0)

    @pytest.mark.parametrize(
        ("tau_ed", "representation", "expected"),
        [
            (
                0.5,
                "complete",
                r"CHECK \to \tau_{Ed} \leq \frac{A_{st,min}}{s_f \cdot h_f} \cdot f_{yd} \to "
                r"0.500 \leq \frac{400.000}{200.000 \cdot 200.000} \cdot 435.000 \to OK",
            ),
            (
                0.5,
                "complete_with_units",
                r"CHECK \to \tau_{Ed} \leq \frac{A_{st,min}}{s_f \cdot h_f} \cdot f_{yd} \to "
                r"0.500 \ MPa \leq \frac{400.000 \ mm^2}{200.000 \ mm \cdot 200.000 \ mm} \cdot 435.000 \ MPa \to OK",
            ),
            (0.5, "short", r"CHECK \to OK"),
            (5.0, "short", r"CHECK \to \text{Not OK}"),
        ],
    )
    def test_latex(self, tau_ed: float, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Object to test
        test_latex = Form8Dot66CheckOmissionOfShearVerification(tau_ed=tau_ed, a_st_min=400.0, s_f=200.0, h_f=200.0, f_yd=435.0).latex()

        actual = {
            "complete": test_latex.complete,
            "complete_with_units": test_latex.complete_with_units,
            "short": test_latex.short,
        }

        assert expected == actual[representation]
