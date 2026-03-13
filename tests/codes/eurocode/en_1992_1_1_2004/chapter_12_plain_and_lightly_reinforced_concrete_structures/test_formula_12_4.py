"""Testing formula 12.4 of EN 1992-1-1:2004."""

import pytest

from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_12_plain_and_lightly_reinforced_concrete_structures.formula_12_4 import (
    Form12Dot4PlainConcreteShearStress,
    Form12Dot4PlainConcreteShearStressComparison,
)
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestForm12Dot4PlainConcreteShearStress:
    """Validation for formula 12.4 from EN 1992-1-1:2004."""

    def test_evaluation(self) -> None:
        """Test the evaluation of the result."""
        # Example values
        k = 1.5  # Nationally determined parameter
        v_ed = 100000.0  # N
        a_cc = 50000.0  # mm^2

        # Object to test
        form_12_4 = Form12Dot4PlainConcreteShearStress(k=k, v_ed=v_ed, a_cc=a_cc)

        # Expected result, manually calculated
        manually_calculated_result = 3.0  # MPa

        assert round(form_12_4, 3) == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("k", "v_ed", "a_cc"),
        [
            (1.5, 100000.0, 0.0),
        ],
    )
    def test_raise_error_when_values_are_less_or_equal_to_zero(
        self,
        k: float,
        v_ed: float,
        a_cc: float,
    ) -> None:
        """Test values less or equal to zero for v_ed and a_cc."""
        with pytest.raises(LessOrEqualToZeroError):
            Form12Dot4PlainConcreteShearStress(k=k, v_ed=v_ed, a_cc=a_cc)

    @pytest.mark.parametrize(
        ("k", "v_ed", "a_cc"),
        [
            (1.5, -100000.0, 50000.0),
        ],
    )
    def test_raise_error_when_negative_values_are_given(
        self,
        k: float,
        v_ed: float,
        a_cc: float,
    ) -> None:
        """Test negative values for v_ed and a_cc."""
        with pytest.raises(NegativeValueError):
            Form12Dot4PlainConcreteShearStress(k=k, v_ed=v_ed, a_cc=a_cc)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"\tau_{cp} = k \cdot \frac{V_{Ed}}{A_{cc}} = 1.500 \cdot \frac{100000.000}{50000.000} = 3.000",
            ),
            ("short", r"\tau_{cp} = 3.000"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        k = 1.5  # Nationally determined parameter
        v_ed = 100000.0  # N
        a_cc = 50000.0  # mm^2

        # Object to test
        form_12_4_latex = Form12Dot4PlainConcreteShearStress(
            k=k,
            v_ed=v_ed,
            a_cc=a_cc,
        ).latex()

        actual = {
            "complete": form_12_4_latex.complete,
            "short": form_12_4_latex.short,
            "string": str(form_12_4_latex),
        }

        assert actual[representation] == expected, f"{representation} representation failed."


class TestForm12Dot4PlainConcreteShearStressComparison:
    """Validation for Form12Dot4PlainConcreteShearStressComparison."""

    def test_comparison_true(self) -> None:
        """Test the comparison when sigma_cp is less than or equal to sigma_c_lim."""
        comparison = Form12Dot4PlainConcreteShearStressComparison(sigma_cp=1.0, sigma_c_lim=1.5)
        assert comparison.comparison is True

    def test_comparison_false(self) -> None:
        """Test the comparison when sigma_cp is greater than sigma_c_lim."""
        comparison = Form12Dot4PlainConcreteShearStressComparison(sigma_cp=2.0, sigma_c_lim=1.5)
        assert comparison.comparison is False

    @pytest.mark.parametrize(
        ("sigma_cp", "sigma_c_lim"),
        [
            (-1.0, 1.5),
            (1.0, -1.5),
        ],
    )
    def test_raise_error_when_negative_values_are_given(
        self,
        sigma_cp: float,
        sigma_c_lim: float,
    ) -> None:
        """Test negative values for sigma_cp and sigma_c_lim."""
        with pytest.raises(NegativeValueError):
            Form12Dot4PlainConcreteShearStressComparison(sigma_cp=sigma_cp, sigma_c_lim=sigma_c_lim)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"CHECK \rightarrow \sigma_{cp} ≤ \sigma_{c,lim} \rightarrow 1.000 ≤ 1.500 \rightarrow OK",
            ),
            (
                "complete_not_ok",
                r"CHECK \rightarrow \sigma_{cp} ≤ \sigma_{c,lim} \rightarrow 2.000 ≤ 1.500 \rightarrow \text{Not OK}",
            ),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the comparison."""
        if representation == "complete":
            comparison = Form12Dot4PlainConcreteShearStressComparison(sigma_cp=1.0, sigma_c_lim=1.5)
        else:
            comparison = Form12Dot4PlainConcreteShearStressComparison(sigma_cp=2.0, sigma_c_lim=1.5)

        actual = {
            "complete": comparison.latex().complete,
            "complete_not_ok": comparison.latex().complete,
        }

        assert actual[representation] == expected, f"{representation} representation failed."

    def test_str(self) -> None:
        """Test the string representation of the comparison."""
        comparison = Form12Dot4PlainConcreteShearStressComparison(sigma_cp=1.0, sigma_c_lim=1.5)
        expected_str = r"CHECK \rightarrow \sigma_{cp} ≤ \sigma_{c,lim} \rightarrow 1.000 ≤ 1.500 \rightarrow OK"
        assert str(comparison) == expected_str

        comparison_not_ok = Form12Dot4PlainConcreteShearStressComparison(sigma_cp=2.0, sigma_c_lim=1.5)
        expected_str_not_ok = r"CHECK \rightarrow \sigma_{cp} ≤ \sigma_{c,lim} \rightarrow 2.000 ≤ 1.500 \rightarrow " r"\text{Not OK}"
        assert str(comparison_not_ok) == expected_str_not_ok
