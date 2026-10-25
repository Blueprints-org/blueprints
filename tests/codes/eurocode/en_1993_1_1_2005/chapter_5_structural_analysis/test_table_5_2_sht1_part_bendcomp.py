"""Testing Table 5.2 sheet 1 of 3 Part subject to bending and compression of EN 1993-1-1:2005."""

from math import isclose

import pytest

from blueprints.codes.eurocode.en_1993_1_1_2005.chapter_5_structural_analysis.table_5_2_sht1_part_bendcomp import (
    Table5Dot2PartSubjecttoBendingandCompression,
)


class TestTable5Dot2PartSubjecttoBendingandCompression:
    """Testing for Table 5.2 sheet 1 of 3 Part subject to bending and compression of EN 1993-1-1:2005."""

    def test_evaluation(self) -> None:
        """Test evaluation of Table 5.2 sheet 1 of 3 Part subject to bending and compression of EN 1993-1-1:2005."""
        epsilon = 0.8375
        c = 799.9
        t_w = 25.9
        n_ed = 0.0
        a = 62200
        f_y = 335

        # Expected intermediate values
        expected_alpha = 0.5
        expected_psi = -1.0
        expected_beta_1w = 60.3
        expected_beta_2w = 69.5
        expected_beta_3w = 103.9
        expected_c_t_w = 30.9

        form = Table5Dot2PartSubjecttoBendingandCompression(
            epsilon=epsilon,
            c=c,
            t_w=t_w,
            n_ed=n_ed,
            a=a,
            f_y=f_y,
        )

        result = form.evaluate()
        assert result == 1, "Expected Class 1 (Plastic) for the given parameters."

        # Manual calculation checks
        alpha = min(0.5 * (1 + n_ed / (c * t_w * f_y)), 1.0)
        psi = 2 * n_ed / (a * f_y) - 1
        c_t_w = c / t_w

        if alpha > 0.5:
            beta_1w = 396 * epsilon / (13 * alpha - 1)
            beta_2w = 456 * epsilon / (13 * alpha - 1)
        else:
            beta_1w = 36 * epsilon / alpha
            beta_2w = 41.5 * epsilon / alpha

        beta_3w = 62 * epsilon * (1 - psi) * abs(psi) ** 0.5 if psi <= -1 else 42 * epsilon / (0.67 + 0.33 * psi)

        # Tolerance-based checks
        assert isclose(alpha, expected_alpha, rel_tol=1e-3)
        assert isclose(psi, expected_psi, rel_tol=1e-3)
        assert isclose(beta_1w, expected_beta_1w, rel_tol=1e-2)
        assert isclose(beta_2w, expected_beta_2w, rel_tol=1e-2)
        assert isclose(beta_3w, expected_beta_3w, rel_tol=1e-2)
        assert isclose(c_t_w, expected_c_t_w, rel_tol=1e-2)

    @pytest.mark.parametrize(
        ("representation", "expected_fragment"),
        [
            ("result", "Class 1: Plastic"),
            ("symbolic_eq", r"\alpha = 0.500"),
            ("numeric_eq", r"\beta_{1w} = 60.300"),
        ],
    )
    def test_latex(self, representation: str, expected_fragment: str) -> None:
        """Test LaTeX representation of the section classification."""
        form = Table5Dot2PartSubjecttoBendingandCompression(
            epsilon=0.8375,
            c=799.9,
            t_w=25.9,
            n_ed=0.0,
            a=62200,
            f_y=335,
        ).latex()

        # Build actual representation dictionary
        actual = {
            "result": form.result,
            "symbolic_eq": form.equation,
            "numeric_eq": form.numeric_equation,
        }

        assert expected_fragment in actual[representation], f"{representation} representation did not contain expected fragment."
