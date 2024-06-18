"""Testing formula 6.71 of NEN-EN 1992-1-1+C2:2011."""

import pytest

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011.chapter_6_ultimate_limit_state.formula_6_71 import (
    Form6Dot71CriteriaBasedOnStressRange,
    Form6Dot71CriteriaBasedOnStressRangeLHS,
    Form6Dot71CriteriaBasedOnStressRangeRHS,
)
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestForm6Dot71CriteriaBasedOnStressRangeLHS:
    """Validation for LHS formula 6.71 from NEN-EN 1992-1-1+C2:2011."""

    def test_evaluation(self) -> None:
        """Test the evaluation of the result."""
        # Example values
        gamma_f_fat = 1.5  # -
        delta_sigma_s_equ_n_star = 10.0  # MPa
        form = Form6Dot71CriteriaBasedOnStressRangeLHS(gamma_f_fat=gamma_f_fat, delta_sigma_s_equ_n_star=delta_sigma_s_equ_n_star)

        # Expected result, manually calculated
        expected = 15.0

        assert form == expected

    @pytest.mark.parametrize(
        ("gamma_f_fat", "delta_sigma_s_equ_n_star"),
        [
            (-1, 10),
            (10, -1),
        ],
    )
    def test_raise_error_when_negative_is_given(self, gamma_f_fat: float, delta_sigma_s_equ_n_star: float) -> None:
        """Test a negative value for v_rd_s."""
        with pytest.raises(NegativeValueError):
            Form6Dot71CriteriaBasedOnStressRangeLHS(gamma_f_fat=gamma_f_fat, delta_sigma_s_equ_n_star=delta_sigma_s_equ_n_star)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"\Delta \sigma_{Ed} = \gamma_{F,fat} \cdot \Delta \sigma_{s,equ} (N^*) = 1.500 \cdot 10.000 = 15.000",
            ),
            ("short", r"\Delta \sigma_{Ed} = 15.000"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        gamma_f_fat = 1.5  # -
        delta_sigma_s_equ_n_star = 10.0  # MPa

        # Object to test
        form_latex = Form6Dot71CriteriaBasedOnStressRangeLHS(gamma_f_fat=gamma_f_fat, delta_sigma_s_equ_n_star=delta_sigma_s_equ_n_star).latex()

        actual = {
            "complete": form_latex.complete,
            "short": form_latex.short,
        }

        assert actual[representation] == expected, f"{representation} representation failed."


class TestForm6Dot71CriteriaBasedOnStressRangeRHS:
    """Validation for RHS formula 6.71 from NEN-EN 1992-1-1+C2:2011."""

    def test_evaluation(self) -> None:
        """Test the evaluation of the result."""
        # Example values
        gamma_s_fat = 2.0  # -
        delta_sigma_rsk_n_star = 10.0  # MPa
        form = Form6Dot71CriteriaBasedOnStressRangeRHS(gamma_s_fat=gamma_s_fat, delta_sigma_rsk_n_star=delta_sigma_rsk_n_star)

        # Expected result, manually calculated
        expected = 5.0

        assert form == expected

    @pytest.mark.parametrize(
        ("gamma_s_fat", "delta_sigma_rsk_n_star"),
        [
            (-1, 10),
            (0, 10),
        ],
    )
    def test_raise_error_when_gamma_is_not_positive(self, gamma_s_fat: float, delta_sigma_rsk_n_star: float) -> None:
        """Test a non postive values for gamma_s_fat."""
        with pytest.raises(LessOrEqualToZeroError):
            Form6Dot71CriteriaBasedOnStressRangeRHS(gamma_s_fat=gamma_s_fat, delta_sigma_rsk_n_star=delta_sigma_rsk_n_star)

    def test_raise_error_when_delta_sigma_is_negative(self) -> None:
        """Test a negative value for delta_sigma_rsk_n_star."""
        # Example values
        gamma_s_fat = 1.0  # -
        delta_sigma_rsk_n_star = -3  # MPa

        with pytest.raises(NegativeValueError):
            Form6Dot71CriteriaBasedOnStressRangeRHS(gamma_s_fat=gamma_s_fat, delta_sigma_rsk_n_star=delta_sigma_rsk_n_star)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"\Delta \sigma_{Rd} = \frac{\Delta \sigma_{Rsk} (N^*)}{\gamma_{s,fat}} = \frac{10.000}{2.000} = 5.000",
            ),
            ("short", r"\Delta \sigma_{Rd} = 5.000"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        gamma_s_fat = 2.0  # -
        delta_sigma_rsk_n_star = 10.0  # MPa

        # Object to test
        form_latex = Form6Dot71CriteriaBasedOnStressRangeRHS(gamma_s_fat=gamma_s_fat, delta_sigma_rsk_n_star=delta_sigma_rsk_n_star).latex()

        actual = {
            "complete": form_latex.complete,
            "short": form_latex.short,
        }

        assert actual[representation] == expected, f"{representation} representation failed."


class TestForm6Dot71CriteriaBasedOnStressRange:
    """Validation for formula 6.71 from NEN-EN 1992-1-1+C2:2011."""

    @pytest.mark.parametrize(
        ("gamma_f_fat", "delta_sigma_s_equ_n_star", "gamma_s_fat", "delta_sigma_rsk_n_star", "result_manual"),
        [
            (1.5, 10.0, 2.0, 40.0, True),
            (1.5, 10.0, 2.0, 30.0, True),
            (1.5, 10.0, 2.0, 20.0, False),
        ],
    )
    def test_evaluation(
        self, gamma_f_fat: float, delta_sigma_s_equ_n_star: float, gamma_s_fat: float, delta_sigma_rsk_n_star: float, result_manual: bool
    ) -> None:
        """Test the evaluation of the result."""
        form = Form6Dot71CriteriaBasedOnStressRange(
            gamma_f_fat=gamma_f_fat,
            delta_sigma_s_equ_n_star=delta_sigma_s_equ_n_star,
            gamma_s_fat=gamma_s_fat,
            delta_sigma_rsk_n_star=delta_sigma_rsk_n_star,
        )

        # Expected result, manually calculated
        expected = result_manual

        assert form == expected

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                (
                    r"CHECK \rightarrow \gamma_{F,fat} \cdot \Delta \sigma_{s,equ} (N^*) "
                    r"\leq \frac{\Delta \sigma_{Rsk} (N^*)}{\gamma_{s,fat}} \rightarrow "
                    r"1.500 \cdot 10.000 \leq \frac{10.000}{2.000} \rightarrow NOT\;OK"
                ),
            ),
            ("short", r"CHECK \rightarrow NOT\;OK"),
        ],
    )
    def test_latex_not_ok(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        gamma_f_fat = 1.5  # -
        delta_sigma_s_equ_n_star = 10.0  # MPa
        gamma_s_fat = 2.0  # -
        delta_sigma_rsk_n_star = 10.0  # MPa

        # Object to test
        form_latex = Form6Dot71CriteriaBasedOnStressRange(
            gamma_f_fat=gamma_f_fat,
            delta_sigma_s_equ_n_star=delta_sigma_s_equ_n_star,
            gamma_s_fat=gamma_s_fat,
            delta_sigma_rsk_n_star=delta_sigma_rsk_n_star,
        ).latex()

        actual = {
            "complete": form_latex.complete,
            "short": form_latex.short,
        }

        assert actual[representation] == expected, f"{representation} representation failed."

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                (
                    r"CHECK \rightarrow \gamma_{F,fat} \cdot \Delta \sigma_{s,equ} (N^*) "
                    r"\leq \frac{\Delta \sigma_{Rsk} (N^*)}{\gamma_{s,fat}} \rightarrow "
                    r"1.500 \cdot 10.000 \leq \frac{40.000}{2.000} \rightarrow OK"
                ),
            ),
            ("short", r"CHECK \rightarrow OK"),
        ],
    )
    def test_latex_ok(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        gamma_f_fat = 1.5  # -
        delta_sigma_s_equ_n_star = 10.0  # MPa
        gamma_s_fat = 2.0  # -
        delta_sigma_rsk_n_star = 40.0  # MPa

        # Object to test
        form_latex = Form6Dot71CriteriaBasedOnStressRange(
            gamma_f_fat=gamma_f_fat,
            delta_sigma_s_equ_n_star=delta_sigma_s_equ_n_star,
            gamma_s_fat=gamma_s_fat,
            delta_sigma_rsk_n_star=delta_sigma_rsk_n_star,
        ).latex()

        actual = {
            "complete": form_latex.complete,
            "short": form_latex.short,
        }

        assert actual[representation] == expected, f"{representation} representation failed."

    def test_property_lhs(self) -> None:
        """Test the latex representation of the formula."""
        # Example values
        gamma_f_fat = 1.5  # -
        delta_sigma_s_equ_n_star = 10.0  # MPa
        gamma_s_fat = 2.0  # -
        delta_sigma_rsk_n_star = 40.0  # MPa

        # Object to test
        form = Form6Dot71CriteriaBasedOnStressRange(
            gamma_f_fat=gamma_f_fat,
            delta_sigma_s_equ_n_star=delta_sigma_s_equ_n_star,
            gamma_s_fat=gamma_s_fat,
            delta_sigma_rsk_n_star=delta_sigma_rsk_n_star,
        ).left_hand_side

        # Expected result, manually calculated
        expected = 15.0

        assert form == expected

    def test_property_rhs(self) -> None:
        """Test the latex representation of the formula."""
        # Example values
        gamma_f_fat = 1.5  # -
        delta_sigma_s_equ_n_star = 10.0  # MPa
        gamma_s_fat = 2.0  # -
        delta_sigma_rsk_n_star = 40.0  # MPa

        # Object to test
        form = Form6Dot71CriteriaBasedOnStressRange(
            gamma_f_fat=gamma_f_fat,
            delta_sigma_s_equ_n_star=delta_sigma_s_equ_n_star,
            gamma_s_fat=gamma_s_fat,
            delta_sigma_rsk_n_star=delta_sigma_rsk_n_star,
        ).right_hand_side

        # Expected result, manually calculated
        expected = 20.0

        assert form == expected

    def test_property_ratio(self) -> None:
        """Test the latex representation of the formula."""
        # Example values
        gamma_f_fat = 1.5  # -
        delta_sigma_s_equ_n_star = 10.0  # MPa
        gamma_s_fat = 2.0  # -
        delta_sigma_rsk_n_star = 40.0  # MPa

        # Object to test
        form = Form6Dot71CriteriaBasedOnStressRange(
            gamma_f_fat=gamma_f_fat,
            delta_sigma_s_equ_n_star=delta_sigma_s_equ_n_star,
            gamma_s_fat=gamma_s_fat,
            delta_sigma_rsk_n_star=delta_sigma_rsk_n_star,
        ).ratio

        # Expected result, manually calculated
        expected = 0.75

        assert form == expected
