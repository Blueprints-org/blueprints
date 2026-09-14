"""Testing formula 8.4 of FprEN 1992-1-1:2023."""

import pytest

from blueprints.codes.eurocode.fpr_en_1992_1_1_2023.chapter_8_ultimate_limit_states.formula_8_4 import (
    Form8Dot4DesignStressCompressionZone,
)
from blueprints.validations import NegativeValueError


class TestForm8Dot4DesignStressCompressionZone:
    """Validation for formula 8.4 from FprEN 1992-1-1:2023."""

    def test_evaluation_parabolic_branch(self) -> None:
        """Tests the evaluation of the result on the parabolic branch."""
        # Example values
        f_cd = 20.0
        epsilon_c = 0.001

        # Object to test
        formula = Form8Dot4DesignStressCompressionZone(f_cd=f_cd, epsilon_c=epsilon_c)

        # Expected result, manually calculated: 20 * (1 - (1 - 0.001 / 0.002)**2) = 20 * 0.75
        manually_calculated_result = 15.0

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_evaluation_plateau_branch(self) -> None:
        """Tests the evaluation of the result on the plateau branch."""
        # Example values
        f_cd = 20.0
        epsilon_c = 0.003

        # Object to test
        formula = Form8Dot4DesignStressCompressionZone(f_cd=f_cd, epsilon_c=epsilon_c)

        # Expected result, as printed in the standard: f_cd on the plateau
        manually_calculated_result = 20.0

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_evaluation_at_epsilon_c2_boundary(self) -> None:
        """Tests the evaluation of the result exactly at the boundary between the two branches."""
        # Example values
        f_cd = 20.0
        epsilon_c = 0.002

        # Object to test
        formula = Form8Dot4DesignStressCompressionZone(f_cd=f_cd, epsilon_c=epsilon_c)

        # Expected result: both branches agree at epsilon_c = epsilon_c2
        manually_calculated_result = 20.0

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("f_cd", "epsilon_c"),
        [
            (-20.0, 0.001),  # f_cd is negative
            (20.0, -0.001),  # epsilon_c is negative
        ],
    )
    def test_raise_error_when_negative_values_are_given(self, f_cd: float, epsilon_c: float) -> None:
        """Test invalid values."""
        with pytest.raises(NegativeValueError):
            Form8Dot4DesignStressCompressionZone(f_cd=f_cd, epsilon_c=epsilon_c)

    def test_raise_error_when_epsilon_c_exceeds_epsilon_cu(self) -> None:
        """Test invalid value beyond the range covered by formula (8.4)."""
        with pytest.raises(ValueError, match="outside the range covered by formula"):
            Form8Dot4DesignStressCompressionZone(f_cd=20.0, epsilon_c=0.004)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                (
                    r"\sigma_{cd} = \begin{cases} f_{cd} \left[1 - \left(1 - \frac{\varepsilon_c}{\varepsilon_{c2}}\right)^2\right] "
                    r"& \text{for } 0 \leq \varepsilon_c \leq \varepsilon_{c2} \\ "
                    r"f_{cd} & \text{for } \varepsilon_{c2} \leq \varepsilon_c \leq \varepsilon_{cu} \end{cases} = "
                    r"\begin{cases} 20.000 \left[1 - \left(1 - \frac{0.001}{0.002}\right)^2\right] "
                    r"& \text{for } 0 \leq 0.001 \leq 0.002 \\ "
                    r"20.000 & \text{for } 0.002 \leq 0.001 \leq 0.0035 \end{cases} = 15.000 \ MPa"
                ),
            ),
            (
                "complete_with_units",
                (
                    r"\sigma_{cd} = \begin{cases} f_{cd} \left[1 - \left(1 - \frac{\varepsilon_c}{\varepsilon_{c2}}\right)^2\right] "
                    r"& \text{for } 0 \leq \varepsilon_c \leq \varepsilon_{c2} \\ "
                    r"f_{cd} & \text{for } \varepsilon_{c2} \leq \varepsilon_c \leq \varepsilon_{cu} \end{cases} = "
                    r"\begin{cases} 20.000 \ MPa \left[1 - \left(1 - \frac{0.001}{0.002}\right)^2\right] "
                    r"& \text{for } 0 \leq 0.001 \leq 0.002 \\ "
                    r"20.000 \ MPa & \text{for } 0.002 \leq 0.001 \leq 0.0035 \end{cases} = 15.000 \ MPa"
                ),
            ),
            ("short", r"\sigma_{cd} = 15.000 \ MPa"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        f_cd = 20.0
        epsilon_c = 0.001

        # Object to test
        latex = Form8Dot4DesignStressCompressionZone(f_cd=f_cd, epsilon_c=epsilon_c).latex()

        actual = {
            "complete": latex.complete,
            "complete_with_units": latex.complete_with_units,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."
