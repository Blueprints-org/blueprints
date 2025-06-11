"""Testing formula 5.18 from EN 1993-1-9:2005."""

import pytest

from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_5_structural_analysis.formula_5_18 import Form5Dot18ComparisonGeneralSecondOrderEffects
from blueprints.validations import LessOrEqualToZeroError


class TestForm5Dot18ComparisonGeneralSecondOrderEffects:
    """Testing formula 5.18 from EN 1993-1-9:2005."""

    @pytest.mark.parametrize(
        ("f_ved", "k_1", "n_s", "length", "e_cd", "i_c", "result_manual"),
        [
            (53.3333, 0.8, 2, 5, 30_000, 100_000_000, True),
            (666.6667, 1.2, 4, 3, 35_000, 200_000_000, False),
        ],
    )
    def test_comparison(self, f_ved: float, k_1: float, n_s: float, length: float, e_cd: float, i_c: float, result_manual: bool) -> None:
        """Test the evaluation of the comparison."""
        form_5_18 = bool(Form5Dot18ComparisonGeneralSecondOrderEffects(f_ved=f_ved, k_1=k_1, n_s=n_s, length=length, e_cd=e_cd, i_c=i_c))
        assert form_5_18 == pytest.approx(expected=result_manual)

    @pytest.mark.parametrize(
        ("f_ved", "k_1", "n_s", "length", "e_cd", "i_c"),
        [
            (53.3333, 0.8, 2, 5, 30_000, 100_000_000),
            (666.6667, 1.2, 4, 3, 35_000, 200_000_000),
        ],
    )
    def test_evaluation(self, f_ved: float, k_1: float, n_s: float, length: float, e_cd: float, i_c: float) -> None:
        """Test the right-hand side evaluation of the result."""
        form_5_18 = Form5Dot18ComparisonGeneralSecondOrderEffects(f_ved=f_ved, k_1=k_1, n_s=n_s, length=length, e_cd=e_cd, i_c=i_c)
        assert form_5_18.right_hand_side == pytest.approx(expected=f_ved, abs=1e-3)

    def test_raise_error_if_negative_n_e(self) -> None:
        """Test that a NegativeValueError is raised when a negative value is passed for n_s."""
        n_s = -1.6  # -
        def_test = 10
        with pytest.raises(LessOrEqualToZeroError):
            bool(Form5Dot18ComparisonGeneralSecondOrderEffects(f_ved=def_test, k_1=def_test, n_s=n_s, length=def_test, e_cd=def_test, i_c=def_test))

    @pytest.mark.parametrize(
        ("f_ved", "k_1", "n_s", "length", "e_cd", "i_c", "expected_lhs_rhs"),
        [
            (53.3333, 0.8, 2, 5, 30_000, 100_000_000, 53.3333),
            (666.6667, 1.2, 4, 3, 35_000, 200_000_000, 666.6667),
        ],
    )
    def test_properties(self, f_ved: float, k_1: float, n_s: float, length: float, e_cd: float, i_c: float, expected_lhs_rhs: float) -> None:
        """Test the properties of the comparison."""
        form_5_18 = Form5Dot18ComparisonGeneralSecondOrderEffects(f_ved=f_ved, k_1=k_1, n_s=n_s, length=length, e_cd=e_cd, i_c=i_c)
        assert form_5_18.left_hand_side == pytest.approx(expected_lhs_rhs, abs=1e-3)
        assert form_5_18.right_hand_side == pytest.approx(expected_lhs_rhs, abs=1e-3)
        assert form_5_18.ratio == pytest.approx(1, abs=1e-3)

    def test_str_representation(self) -> None:
        """Test the string representation of the comparison."""
        form_5_18 = Form5Dot18ComparisonGeneralSecondOrderEffects(f_ved=53.3333, k_1=0.8, n_s=2, length=5, e_cd=30_000, i_c=100_000_000)
        expected_str = (
            r"CHECK \rightarrow F_{V,Ed} \leq \frac{n_s}{n_s + 1.6} \cdot \frac{\sum E_{cd} \cdot I_c}{L^2} \rightarrow 53.333\leq \frac{2}{3.6} "
            r"\cdot \frac{\sum 30000 \cdot 100000000}{25} \rightarrow OK"
        )
        assert str(form_5_18) == expected_str

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"CHECK \rightarrow F_{V,Ed} \leq \frac{n_s}{n_s + 1.6} \cdot \frac{\sum E_{cd} \cdot I_c}{L^2} "
                r"\rightarrow 53.333\leq \frac{2}{3.6} \cdot \frac{\sum 30000 \cdot 100000000}{25} \rightarrow OK",
            ),
            ("short", r"CHECK \rightarrow OK"),
        ],
    )
    def test_latex_ok(self, representation: str, expected: str) -> None:
        """Test the latex representation of the comparison."""
        # Example values
        f_ved = 53.3333
        k_1 = 0.8
        n_s = 2
        length = 5
        e_cd = 30_000
        i_c = 100_000_000

        # Object to test
        form_5_18_latex = Form5Dot18ComparisonGeneralSecondOrderEffects(f_ved=f_ved, k_1=k_1, n_s=n_s, length=length, e_cd=e_cd, i_c=i_c).latex()

        actual = {
            "complete": form_5_18_latex.complete,
            "short": form_5_18_latex.short,
        }

        assert actual[representation] == expected, f"{representation} representation failed."

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"CHECK \rightarrow F_{V,Ed} \leq \frac{n_s}{n_s + 1.6} \cdot \frac{\sum E_{cd} \cdot I_c}{L^2} \rightarrow 2000.000\leq \frac{2}{"
                r"3.6} \cdot \frac{\sum 30000 \cdot 100000000}{25} \rightarrow \text{Not OK}",
            ),
            ("short", r"CHECK \rightarrow \text{Not OK}"),
        ],
    )
    def test_latex_not_ok(self, representation: str, expected: str) -> None:
        """Test the latex representation of the comparison."""
        # Example values
        f_ved = 2000
        k_1 = 0.8
        n_s = 2
        length = 5
        e_cd = 30_000
        i_c = 100_000_000

        # Object to test
        form_5_18_latex = Form5Dot18ComparisonGeneralSecondOrderEffects(f_ved=f_ved, k_1=k_1, n_s=n_s, length=length, e_cd=e_cd, i_c=i_c).latex()

        actual = {
            "complete": form_5_18_latex.complete,
            "short": form_5_18_latex.short,
        }

        assert actual[representation] == expected, f"{representation} representation failed."
