"""Testing formula 6.70 of EN 1992-1-1:2004."""

import pytest

from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_6_ultimate_limit_state.formula_6_70 import Form6Dot70FatigueDamageFactor
from blueprints.validations import LessOrEqualToZeroError, ListsNotSameLengthError, NegativeValueError


class TestForm6Dot70FatigueDamageFactor:
    """Validation for formula 6.70 from EN 1992-1-1:2004."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        n_delta_sigma_i = [100.0, 200.0, 300.0]
        capital_n_delta_sigma_i = [400.0, 500.0, 600.0]

        # Object to test
        formula = Form6Dot70FatigueDamageFactor(n_delta_sigma_i, capital_n_delta_sigma_i)

        # Expected result, manually calculated
        expected_result = False

        assert formula == expected_result

    @pytest.mark.parametrize(
        ("n_delta_sigma_i", "capital_n_delta_sigma_i"),
        [
            ([-100.0, 200.0, 300.0], [400.0, 500.0, 600.0]),  # n_delta_sigma_i contains negative value
            ([100.0, 200.0, 300.0], [0.0, 500.0, 600.0]),  # capital_n_delta_sigma_i contains zero
            ([100.0, 200.0, 300.0], [-400.0, 500.0, 600.0]),  # capital_n_delta_sigma_i contains negative value
            ([100.0, 200.0, 300.0], [400.0, 500.0]),  # n_delta_sigma_i and capital_n_delta_sigma_i have different lengths
        ],
    )
    def test_raise_error_when_negative_n_delta_sigma_i_is_given(self, n_delta_sigma_i: list, capital_n_delta_sigma_i: list) -> None:
        """Test invalid tests."""
        with pytest.raises((NegativeValueError, LessOrEqualToZeroError, ListsNotSameLengthError)):
            Form6Dot70FatigueDamageFactor(n_delta_sigma_i, capital_n_delta_sigma_i)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"CHECK \to \sum_{i} \frac{n(\Delta \sigma_i)}{N(\Delta \sigma_i)} < 1 \to \frac{100.000}{400.000} + "
                r"\frac{200.000}{500.000} + \frac{300.000}{600.000} < 1 \to \text{Not OK}",
            ),
            ("short", r"CHECK \to \text{Not OK}"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        n_delta_sigma_i = [100.0, 200.0, 300.0]
        capital_n_delta_sigma_i = [400.0, 500.0, 600.0]

        # Object to test
        latex = Form6Dot70FatigueDamageFactor(n_delta_sigma_i, capital_n_delta_sigma_i).latex()

        actual = {
            "complete": latex.complete,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."
