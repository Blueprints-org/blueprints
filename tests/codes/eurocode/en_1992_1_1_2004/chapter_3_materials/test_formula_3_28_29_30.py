"""Testing test formula for 3.28, 3.29 and 3.30 of EN 1992-1-1:2004."""

import pytest

from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_3_materials.sub_formula_3_28_29_30 import SubForm3Dot28And29And30Mu


class TestSubForm3Dot28And29And30Mu:
    """Validation for formula for 3.28, 3.29 and 3.30 from EN 1992-1-1:2004."""

    def test_evaluation(self) -> None:
        """Test the evaluation of the result."""
        # Example values
        sigma_pi = 2.4  # MPa
        f_pk = 8.5  # MPa

        sub_form_3_28_29_30 = SubForm3Dot28And29And30Mu(sigma_pi=sigma_pi, f_pk=f_pk)

        # Expected result, manually calculated
        manually_calculated_result = 0.282353

        assert sub_form_3_28_29_30 == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_raise_error_when_negative_f_pk_is_given(self) -> None:
        """Test a negative value."""
        # Example values
        sigma_pi = 2.4  # MPa
        f_pk = -8.5  # MPa

        with pytest.raises(ValueError):
            SubForm3Dot28And29And30Mu(sigma_pi=sigma_pi, f_pk=f_pk)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"\mu = \sigma_{pi} / f_{pk} = 2.400 / 8.500 = 0.282",
            ),
            ("short", r"\mu = 0.282"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        sigma_pi = 2.4  # MPa
        f_pk = 8.5  # MPa

        # Object to test
        sub_form_3_28_29_30_latex = SubForm3Dot28And29And30Mu(sigma_pi=sigma_pi, f_pk=f_pk).latex()

        actual = {"complete": sub_form_3_28_29_30_latex.complete, "short": sub_form_3_28_29_30_latex.short}

        assert actual[representation] == expected, f"{representation} representation failed."
