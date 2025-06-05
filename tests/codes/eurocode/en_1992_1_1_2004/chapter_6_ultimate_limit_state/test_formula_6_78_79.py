"""Testing formula 6.78/6.79 of EN 1992-1-1:2004."""

import pytest

from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_6_ultimate_limit_state.formula_6_78_79 import Form6Dot78And79FatigueResistance
from blueprints.validations import NegativeValueError


class TestForm6Dot78And79FatigueResistance:
    """Validation for formula 6.78/6.79 from EN 1992-1-1:2004."""

    def test_evaluation_78(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        v_ed_max = 100.0
        v_ed_min = 50.0
        v_rd_c = 200.0
        f_ck = 30.0

        # Object to test
        formula = Form6Dot78And79FatigueResistance(v_ed_max=v_ed_max, v_ed_min=v_ed_min, v_rd_c=v_rd_c, f_ck=f_ck)

        # Expected result, manually calculated
        expected_result = True

        assert formula == expected_result

    def test_evaluation_79(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        v_ed_max = 100.0
        v_ed_min = -50.0
        v_rd_c = 200.0
        f_ck = 30.0

        # Object to test
        formula = Form6Dot78And79FatigueResistance(v_ed_max=v_ed_max, v_ed_min=v_ed_min, v_rd_c=v_rd_c, f_ck=f_ck)

        # Expected result, manually calculated
        expected_result = False

        assert formula == expected_result

    @pytest.mark.parametrize(
        ("v_ed_max", "v_ed_min", "v_rd_c", "f_ck"),
        [
            (100.0, 50.0, -200.0, 30.0),  # v_rd_c is negative
            (100.0, 50.0, 200.0, -30.0),  # f_ck is negative
        ],
    )
    def test_raise_error_when_invalid_values_are_given(self, v_ed_max: float, v_ed_min: float, v_rd_c: float, f_ck: float) -> None:
        """Test invalid values."""
        with pytest.raises(NegativeValueError):
            Form6Dot78And79FatigueResistance(v_ed_max=v_ed_max, v_ed_min=v_ed_min, v_rd_c=v_rd_c, f_ck=f_ck)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"CHECK \to \begin{cases} \frac{\left|V_{Ed,max}\right|}{\left|V_{Rd,c}\right|} \leq "
                r"\min\left(0.5 + 0.45 \cdot \frac{\left|V_{Ed,min}\right|}{\left|V_{Rd,c}\right|}, "
                r"\begin{cases} 0.9 & \text{if } f_{ck} \le 50 \\ 0.8 & \text{if } f_{ck} > 50 \end{cases} \right) "
                r"& \text{if } \frac{V_{Ed,min}}{V_{Ed,max}} \geq 0 \\ \frac{\left|V_{Ed,max}\right|}"
                r"{\left|V_{Rd,c}\right|} \leq 0.5 - \frac{\left|V_{Ed,min}\right|}{\left|V_{Rd,c}\right|} & \text{if } "
                r"\frac{V_{Ed,min}}{V_{Ed,max}} < 0 \end{cases} \to "
                r"\begin{cases} \frac{\left|100.000\right|}{\left|200.000\right|} \leq \min\left(0.5 + "
                r"0.45 \cdot \frac{\left|50.000\right|}{\left|200.000\right|}, \begin{cases} 0.9 & \text{if } 30.000 "
                r"\le 50 \\ 0.8 & \text{if } 30.000 > 50 \end{cases} \right) & \text{if } \frac{50.000}{100.000} \geq 0 "
                r"\\ \frac{\left|100.000\right|}{\left|200.000\right|} \leq 0.5 - \frac{\left|50.000\right|}{\left|200.000\right|} "
                r"& \text{if } \frac{50.000}{100.000} < 0 \end{cases} \to OK",
            ),
            ("short", r"CHECK \to OK"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        v_ed_max = 100.0
        v_ed_min = 50.0
        v_rd_c = 200.0
        f_ck = 30.0

        # Object to test
        latex = Form6Dot78And79FatigueResistance(v_ed_max=v_ed_max, v_ed_min=v_ed_min, v_rd_c=v_rd_c, f_ck=f_ck).latex()

        actual = {
            "complete": latex.complete,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."
