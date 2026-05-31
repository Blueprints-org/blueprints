"""Testing Table 6.6 of EN 1993-1-1:2005."""

import numpy as np
import pytest

from blueprints.codes.eurocode.en_1993_1_1_2005.chapter_6_ultimate_limit_state.table_6_6 import (
    MomentDistributionType,
    Table6Dot6CorrectionFactorKc,
)


class TestTable6Dot6CorrectionFactorKc:
    """Validation for Table 6.6 from EN 1993-1-1:2005."""

    def test_constant_moment_distribution(self) -> None:
        """Test correction factor for constant moment distribution (k_c = 1.0)."""
        # Object to test
        k_c = Table6Dot6CorrectionFactorKc(MomentDistributionType.CONSTANT)

        # Expected result from table
        assert k_c == 1.0

    @pytest.mark.parametrize(
        ("psi", "expected_k_c"),
        [
            (-1.0, 1.0 / (1.33 - 0.33 * -1.0)),  # psi = -1 (full reversal)
            (-0.5, 1.0 / (1.33 - 0.33 * -0.5)),  # psi = -0.5
            (0.0, 1.0 / (1.33 - 0.33 * 0.0)),  # psi = 0 (no moment at one end)
            (0.5, 1.0 / (1.33 - 0.33 * 0.5)),  # psi = 0.5
            (1.0, 1.0 / (1.33 - 0.33 * 1.0)),  # psi = 1 (constant moment)
        ],
    )
    def test_linear_moment_distribution(self, psi: float, expected_k_c: float) -> None:
        """Test correction factor for linear moment distribution with various psi values."""
        # Object to test
        k_c = Table6Dot6CorrectionFactorKc(MomentDistributionType.LINEAR, psi=psi)

        # Expected result from formula: k_c = 1 / (1.33 - 0.33 * psi)
        assert k_c == pytest.approx(expected=expected_k_c, rel=0.01)

    def test_linear_without_psi_raises_error(self) -> None:
        """Test that LINEAR distribution without psi parameter raises ValueError."""
        with pytest.raises(ValueError, match="Parameter 'psi' must be provided"):
            Table6Dot6CorrectionFactorKc(MomentDistributionType.LINEAR)

    @pytest.mark.parametrize(
        "psi",
        [
            -1.5,  # Below valid range
            -1.1,  # Just below -1
            1.1,  # Just above 1
            2.0,  # Above valid range
        ],
    )
    def test_linear_with_invalid_psi_raises_error(self, psi: float) -> None:
        """Test that LINEAR distribution with psi outside [-1, 1] raises ValueError."""
        with pytest.raises(ValueError, match="Parameter 'psi' must be between -1 and 1"):
            Table6Dot6CorrectionFactorKc(MomentDistributionType.LINEAR, psi=psi)

    def test_simply_supported_uniform_load(self) -> None:
        """Test correction factor for simply supported beam with uniform load (k_c = 0.94)."""
        # Object to test
        k_c = Table6Dot6CorrectionFactorKc(MomentDistributionType.SIMPLY_SUPPORTED_UNIFORM)

        # Expected result from table
        assert k_c == 0.94

    def test_double_clamped_uniform_load(self) -> None:
        """Test correction factor for double clamped beam with uniform load (k_c = 0.90)."""
        # Object to test
        k_c = Table6Dot6CorrectionFactorKc(MomentDistributionType.DOUBLE_CLAMPED_UNIFORM)

        # Expected result from table
        assert k_c == 0.90

    def test_simple_clamped_uniform_load(self) -> None:
        """Test correction factor for simple and clamped beam with uniform load (k_c = 0.91)."""
        # Object to test
        k_c = Table6Dot6CorrectionFactorKc(MomentDistributionType.SIMPLE_CLAMPED_UNIFORM)

        # Expected result from table
        assert k_c == 0.91

    def test_simply_supported_point_load(self) -> None:
        """Test correction factor for simply supported beam with point load (k_c = 0.86)."""
        # Object to test
        k_c = Table6Dot6CorrectionFactorKc(MomentDistributionType.SIMPLY_SUPPORTED_POINT)

        # Expected result from table
        assert k_c == 0.86

    def test_double_clamped_point_load(self) -> None:
        """Test correction factor for double clamped beam with point load (k_c = 0.77)."""
        # Object to test
        k_c = Table6Dot6CorrectionFactorKc(MomentDistributionType.DOUBLE_CLAMPED_POINT)

        # Expected result from table
        assert k_c == 0.77

    def test_simple_clamped_point_load(self) -> None:
        """Test correction factor for simple and clamped beam with point load (k_c = 0.82)."""
        # Object to test
        k_c = Table6Dot6CorrectionFactorKc(MomentDistributionType.SIMPLE_CLAMPED_POINT)

        # Expected result from table
        assert k_c == 0.82

    @pytest.mark.parametrize(
        ("distribution_type", "expected_latex"),
        [
            (
                (MomentDistributionType.CONSTANT, None),
                r"k_c = \text{constant} = 1.00",
            ),
            (
                (MomentDistributionType.LINEAR, 0.5),
                r"k_c = \frac{1}{1.33 - 0.33 \cdot 0.5} = 0.86",
            ),
            (
                (MomentDistributionType.SIMPLY_SUPPORTED_UNIFORM, None),
                r"k_c = \text{simply_supported_uniform} = 0.94",
            ),
        ],
    )
    def test_latex(self, distribution_type: tuple, expected_latex: str) -> None:
        """Test the latex representation of the table."""
        moment_type, psi = distribution_type
        k_c = Table6Dot6CorrectionFactorKc(moment_type, psi=psi)
        latex = k_c.latex()

        assert expected_latex == latex.complete


class TestInterpretMomentDistributionForKcNormalize:
    """Tests for the _normalize method of Table6Dot6CorrectionFactorKc."""

    def test_normalizing_data_mid_positive_right_negative(self) -> None:
        """Test that mirroring of data works correctly."""
        y_data = [0, 100, -100]
        x_data = [0, 1, 2]

        rescaled_x, rescaled_y = Table6Dot6CorrectionFactorKc._normalize(  # noqa: SLF001
            x_data=x_data, y_data=y_data
        )

        assert all(rescaled_x == [0.0, 0.5, 1.0])
        assert all(rescaled_y == [0.0, 1.0, -1.0])

    def test_normalizing_data_mid_negative_left_positive(self) -> None:
        """Test that mirroring of data works correctly."""
        # Original data (linearly decreasing)
        y_data = [100, -100, 0]
        x_data = [0, 1, 4]

        rescaled_x, rescaled_y = Table6Dot6CorrectionFactorKc._normalize(  # noqa: SLF001
            x_data=x_data, y_data=y_data
        )

        assert all(rescaled_x == [0.0, 0.25, 1.0])
        assert all(rescaled_y == [1.0, -1.0, 0.0])

    def test_normalizing_data_mid_negative_left_negative(self) -> None:
        """Test that mirroring of data works correctly."""
        # Original data (linearly decreasing)
        y_data = [-100, 100, 0]
        x_data = [-1, 0, 1]

        rescaled_x, rescaled_y = Table6Dot6CorrectionFactorKc._normalize(  # noqa: SLF001
            x_data=x_data, y_data=y_data
        )

        assert all(rescaled_x == [0.0, 0.5, 1.0])
        assert all(rescaled_y == [-1.0, 1.0, 0.0])

    def test_normalizing_data_mid_negative_right_postive(self) -> None:
        """Test that mirroring of data works correctly."""
        y_data = [0, -100, 100]
        x_data = [1, 3, 5]

        rescaled_x, rescaled_y = Table6Dot6CorrectionFactorKc._normalize(  # noqa: SLF001
            x_data=x_data, y_data=y_data
        )

        assert all(rescaled_x == [0.0, 0.5, 1.0])
        assert all(rescaled_y == [0.0, -1.0, 1.0])


class TestInterpretMomentDistributionForKc:
    """Tests for the interpretation_of_moment_distribution_for_kc method."""

    def test_interpret_constant_moment(self) -> None:
        """Test interpretation of constant moment distribution."""
        # Constant moment data
        y_data = [100, 100, 100, 100, 100, 100]

        # Interpret the distribution
        k_c = Table6Dot6CorrectionFactorKc.interpretation_of_moment_distribution_for_kc(y_data)

        # Should identify as linear with slope ~0 (constant)
        assert k_c == 1.0

    def test_interpret_constant_negative_moment(self) -> None:
        """Test interpretation of constant negative moment distribution."""
        # Constant negative moment data
        y_data = [-100, -100, -100, -100, -100, -100]

        # Interpret the distribution
        k_c = Table6Dot6CorrectionFactorKc.interpretation_of_moment_distribution_for_kc(y_data)

        # Should identify as linear with slope ~0 (constant)
        assert k_c == 1.0

    def test_interpret_constant_all_zeros(self) -> None:
        """Test interpretation of constant zero moment distribution."""
        # Constant zero moment data
        y_data = [0, 0, 0, 0, 0, 0]

        # Interpret the distribution
        k_c = Table6Dot6CorrectionFactorKc.interpretation_of_moment_distribution_for_kc(y_data)

        # Should identify as linear with slope ~0 (constant)
        assert k_c == 1.0

    def test_interpret_linear_decreasing_moment(self) -> None:
        """Test interpretation of linearly decreasing moment distribution."""
        # Linear decreasing moment (from high to low)
        y_data = [100, 80, 60, 40, 20, 0]

        # Interpret the distribution
        k_c = Table6Dot6CorrectionFactorKc.interpretation_of_moment_distribution_for_kc(y_data)

        # Should identify as linear distribution
        # k_c should be between the bounds for linear distribution
        assert k_c == pytest.approx(expected=1.0 / 1.33, abs=0.01)

    def test_interpret_linear_increasing_moment(self) -> None:
        """Test interpretation of linearly increasing moment distribution."""
        # Linear increasing moment (from low to high)
        y_data = [0, 20, 40, 60, 80, 100]

        # Interpret the distribution
        k_c = Table6Dot6CorrectionFactorKc.interpretation_of_moment_distribution_for_kc(y_data)

        # Should identify as linear distribution
        assert k_c == pytest.approx(expected=1.0 / 1.33, abs=0.01)

    def test_interpret_linear_negative_decreasing_moment(self) -> None:
        """Test interpretation of linearly decreasing negative moment distribution."""
        # Linear decreasing negative moment (from zero to far negative)
        y_data = [0, -20, -40, -60, -80, -100]

        # Interpret the distribution
        k_c = Table6Dot6CorrectionFactorKc.interpretation_of_moment_distribution_for_kc(y_data)

        # Should identify as linear distribution
        assert k_c == pytest.approx(expected=1.0 / 1.33, abs=0.01)

    def test_interpret_linear_negative_increasing_moment(self) -> None:
        """Test interpretation of linearly increasing negative moment distribution."""
        # Linear increasing negative moment (from far negative to zero)
        y_data = [-100, -80, -60, -40, -20, 0]

        # Interpret the distribution
        k_c = Table6Dot6CorrectionFactorKc.interpretation_of_moment_distribution_for_kc(y_data)

        # Should identify as linear distribution
        assert k_c == pytest.approx(expected=1.0 / 1.33, abs=0.01)

    def test_interpret_simply_supported_uniform_load(self) -> None:
        """Test interpretation of simply supported beam with uniform load."""
        # Generate data that matches simply supported beam with uniform load
        x_data = np.linspace(0, 1, 11)
        y_data = 4 * x_data - 4 * x_data**2

        # Interpret the distribution
        k_c = Table6Dot6CorrectionFactorKc.interpretation_of_moment_distribution_for_kc(y_data, x_data)

        # Expected k_c = 0.94 for simply supported with uniform load
        assert k_c == 0.94

    def test_interpret_simply_supported_point_load(self) -> None:
        """Test interpretation of simply supported beam with point load."""
        # Generate data that matches simply supported beam with point load
        x_data = np.linspace(0, 1, 21)
        y_data = np.where(x_data < 0.5, 2 * x_data, 2 - 2 * x_data)

        # Interpret the distribution
        k_c = Table6Dot6CorrectionFactorKc.interpretation_of_moment_distribution_for_kc(y_data, x_data)

        # Expected k_c = 0.86 for simply supported with point load
        assert k_c == 0.86

    def test_interpret_with_custom_x_data(self) -> None:
        """Test interpretation with custom position data."""
        # Example from kc_calculator.py
        y_data = [20, 20, 20, 20, 15]
        x_data = [0, 1, 2, 3, 6]

        # Interpret the distribution
        k_c = Table6Dot6CorrectionFactorKc.interpretation_of_moment_distribution_for_kc(y_data, x_data)

        # Should return a valid k_c value of 0.94..
        assert 0.94 <= k_c <= 0.95

    def test_interpret_example_from_calculator_1(self) -> None:
        """Test interpretation with example data from kc_calculator.py."""
        # Example data with varying moment distribution
        y_data = [-60.22, -48.78, -38.54, -29.51, -21.68, -15.06, -9.64, 5.42, -2.41, -0.6, 0]

        # Interpret the distribution
        k_c = Table6Dot6CorrectionFactorKc.interpretation_of_moment_distribution_for_kc(y_data)

        # Closest resembles line 8 (simple and clamped with uniform load) with k_c = 0.82
        assert k_c == 0.82

    def test_interpret_example_from_calculator_2(self) -> None:
        """Test interpretation with second example from kc_calculator.py."""
        # Example data: symmetric parabolic distribution
        y_data = [-10.04, -4.62, -0.4, 2.61, 4.42, 5.02, 4.42, 2.61, -0.4, -4.62, -10.04]

        # Interpret the distribution
        k_c = Table6Dot6CorrectionFactorKc.interpretation_of_moment_distribution_for_kc(y_data)

        assert k_c == 0.90

    def test_interpret_without_x_data(self) -> None:
        """Test interpretation without providing x_data (assumes equally spaced)."""
        # Moment data without position data
        y_data = [0, 25, 50, 75, 100]

        # Should work without x_data (assumes equally spaced points)
        k_c = Table6Dot6CorrectionFactorKc.interpretation_of_moment_distribution_for_kc(y_data)

        # Should return a valid k_c value
        assert k_c == pytest.approx(expected=1.0 / (1.33), abs=0.01)

    def test_interpret_double_clamped_distribution(self) -> None:
        """Test interpretation of double clamped beam distribution."""
        # Generate data for double clamped beam with uniform load (a=0 for symmetry)
        x_data = np.linspace(0, 1, 11)
        # For a=0: y = 4x² - 4x + 1 (which has negative moments at supports and positive in middle)
        y_data = 4 * x_data**2 - 4 * x_data + 1

        # Interpret the distribution
        k_c = Table6Dot6CorrectionFactorKc.interpretation_of_moment_distribution_for_kc(y_data, x_data)

        # Expected k_c = 0.90 for double clamped with uniform load
        assert k_c == 0.9

    def test_interpret_returns_float(self) -> None:
        """Test that interpret method returns a float value."""
        y_data = [100, 90, 80, 70, 60]

        k_c = Table6Dot6CorrectionFactorKc.interpretation_of_moment_distribution_for_kc(y_data)

        assert isinstance(k_c, float)

    def test_single_datapoint(self) -> None:
        """Test interpretation with minimal number of data points."""
        # Just 1 point (minimum for any fit)
        y_data = [100]

        # Should still work with minimal data
        k_c = Table6Dot6CorrectionFactorKc.interpretation_of_moment_distribution_for_kc(y_data)

        # Should return k_c = 1.0 for single data point (default to constant)
        assert k_c == 1.0

    def test_no_datapoint(self) -> None:
        """Test interpretation with minimal number of data points."""
        # No data points
        y_data = []

        # Should still work with minimal data
        k_c = Table6Dot6CorrectionFactorKc.interpretation_of_moment_distribution_for_kc(y_data)

        # Should return k_c = 1.0 for empty data (default to constant)
        assert k_c == 1.0

    def test_data_in_wrong_order(self) -> None:
        """Test interpretation with data in non-monotonic order."""
        # Data that is not in monotonic order (should still be interpreted correctly)
        y_data = [0, 100, 50]
        x_data = [0, 4, 2]

        k_c = Table6Dot6CorrectionFactorKc.interpretation_of_moment_distribution_for_kc(y_data, x_data)

        # Should identify as linear distribution
        assert k_c == pytest.approx(expected=1.0 / (1.33), abs=0.01)
