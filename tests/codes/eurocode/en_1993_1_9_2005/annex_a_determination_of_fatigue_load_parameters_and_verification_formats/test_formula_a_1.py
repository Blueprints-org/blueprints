"""Testing formula A.1 from EN 1993-1-9:2005: Annex A - Determination of fatigue load parameters and verification formats."""

import pytest

from blueprints.codes.eurocode.en_1993_1_9_2005.annex_a_determination_of_fatigue_load_parameters_and_verification_formats.formula_a_1 import (
    FormADot1DamageDuringDesignLife,
)
from blueprints.validations import LessOrEqualToZeroError, ListsNotSameLengthError, NegativeValueError


class TestFormADot1DamageDuringDesignLife:
    """Validation for formula A.1 from EN 1993-1-9:2005."""

    def test_evaluation(self) -> None:
        """Test the evaluation of the result."""
        # example values
        n_e = [5.0, 4.0, 3.0]  # [-]
        n_r = [10.0, 20.0, 30.0]  # [-]

        form_a_1 = FormADot1DamageDuringDesignLife(n_e=n_e, n_r=n_r)
        # manually calculated result
        manually_calculated_result = 5 / 10 + 4 / 20 + 3 / 30  # -

        assert form_a_1 == pytest.approx(expected=manually_calculated_result, rel=1e-9)

    def test_raise_error_if_negative_n_e(self) -> None:
        """Test that a NegativeValueError is raised when a negative value is passed for n_e."""
        n_e = [-5.0, 4.0, 3.0]  # [-]
        n_r = [10.0, 20.0, 30.0]  # [-]
        with pytest.raises(NegativeValueError):
            FormADot1DamageDuringDesignLife(n_e=n_e, n_r=n_r)

    @pytest.mark.parametrize(
        ("n_e", "n_r"),
        [
            ([5.0, 4.0, 3.0], [10.0, -20.0, 30.0]),
            ([5.0, 4.0, 3.0], [10.0, 20.0, 0.0]),
        ],
    )
    def test_raise_error_if_negative_n_r(self, n_e: list[float], n_r: list[float]) -> None:
        """Test that a LessOrEqualToZeroError is raised when a negative value is passed for n_r."""
        with pytest.raises(LessOrEqualToZeroError):
            FormADot1DamageDuringDesignLife(n_e=n_e, n_r=n_r)

    def test_raise_error_if_n_e_and_n_r_are_different_length(self) -> None:
        """Test that a ListsNotSameLengthError is raised when n_e and n_r are not the same length."""
        n_e = [5.0, 4.0]  # [-]
        n_r = [10.0, 20.0, 30.0]  # [-]
        with pytest.raises(ListsNotSameLengthError):
            FormADot1DamageDuringDesignLife(n_e=n_e, n_r=n_r)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"D_d = \sum_{i}^{n} \frac{n_{Ei}}{N_Ri} = \frac{5.000}{10.000} + \frac{4.000}{20.000} + \frac{3.000}{30.000} = 0.800",
            ),
            ("short", r"D_d = 0.800"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        n_e = [5.0, 4.0, 3.0]  # [-]
        n_r = [10.0, 20.0, 30.0]  # [-]

        # Object to test
        form_a_1_latex = FormADot1DamageDuringDesignLife(n_e=n_e, n_r=n_r).latex()

        actual = {
            "complete": form_a_1_latex.complete,
            "short": form_a_1_latex.short,
        }

        assert actual[representation] == expected, f"{representation} representation failed."
