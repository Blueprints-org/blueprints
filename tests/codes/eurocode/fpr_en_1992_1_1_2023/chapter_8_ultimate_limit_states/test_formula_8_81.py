"""Testing formula 8.81 of FprEN 1992-1-1:2023."""

import pytest

from blueprints.codes.eurocode.fpr_en_1992_1_1_2023.chapter_8_ultimate_limit_states.formula_8_81 import (
    Form8Dot81DesignTorsionalCapacity,
)
from blueprints.validations import NegativeValueError


class TestForm8Dot81DesignTorsionalCapacity:
    """Validation for formula 8.81 from FprEN 1992-1-1:2023."""

    @pytest.mark.parametrize(
        ("tau_t_rd_sw", "tau_t_rd_sl", "tau_t_rd_max", "expected"),
        [
            # The three values of the worked examples of Formulas (8.82), (8.83) and (8.84)
            (3.625, 2.9, 4.0, 2.9),  # the longitudinal reinforcement governs
            (2.5, 2.9, 4.0, 2.5),  # the shear reinforcement governs
            (3.625, 2.9, 1.5, 1.5),  # crushing of the compression field governs
            (2.9, 2.9, 2.9, 2.9),  # all three coincide
        ],
    )
    def test_evaluation(self, tau_t_rd_sw: float, tau_t_rd_sl: float, tau_t_rd_max: float, expected: float) -> None:
        """Tests that each of the three candidates governs when it is the smallest."""
        # Object to test
        formula = Form8Dot81DesignTorsionalCapacity(tau_t_rd_sw=tau_t_rd_sw, tau_t_rd_sl=tau_t_rd_sl, tau_t_rd_max=tau_t_rd_max)

        assert formula == pytest.approx(expected=expected, rel=1e-4)

    @pytest.mark.parametrize(
        ("tau_t_rd_sw", "tau_t_rd_sl", "tau_t_rd_max"),
        [
            (-3.625, 2.9, 4.0),  # tau_t_rd_sw is negative
            (3.625, -2.9, 4.0),  # tau_t_rd_sl is negative
            (3.625, 2.9, -4.0),  # tau_t_rd_max is negative
        ],
    )
    def test_raise_error_when_invalid_values_are_given(self, tau_t_rd_sw: float, tau_t_rd_sl: float, tau_t_rd_max: float) -> None:
        """Test invalid values."""
        with pytest.raises(NegativeValueError):
            Form8Dot81DesignTorsionalCapacity(tau_t_rd_sw=tau_t_rd_sw, tau_t_rd_sl=tau_t_rd_sl, tau_t_rd_max=tau_t_rd_max)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                (
                    r"\tau_{t,Rd} = \min\left\{\tau_{t,Rd,sw}; \tau_{t,Rd,sl}; \tau_{t,Rd,max}\right\} = "
                    r"\min\left\{3.625; 2.900; 4.000\right\} = 2.900 \ MPa"
                ),
            ),
            (
                "complete_with_units",
                (
                    r"\tau_{t,Rd} = \min\left\{\tau_{t,Rd,sw}; \tau_{t,Rd,sl}; \tau_{t,Rd,max}\right\} = "
                    r"\min\left\{3.625 \ MPa; 2.900 \ MPa; 4.000 \ MPa\right\} = 2.900 \ MPa"
                ),
            ),
            ("short", r"\tau_{t,Rd} = 2.900 \ MPa"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Object to test
        latex = Form8Dot81DesignTorsionalCapacity(tau_t_rd_sw=3.625, tau_t_rd_sl=2.9, tau_t_rd_max=4.0).latex()

        actual = {
            "complete": latex.complete,
            "complete_with_units": latex.complete_with_units,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."
