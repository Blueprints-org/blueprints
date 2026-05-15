"""Table 6.6 from EN 1993-1-1:2005: Chapter 6 - Ultimate limit state, to calculate the correction factor [$k_c$].

Two main functionalities are provided:
1. Direct calculation of $k_c$ based on a specified moment distribution type.
2. Interpretation of moment distribution data to determine the best-fit $k_c$ value based on standard patterns.
"""

from collections.abc import Callable
from enum import Enum

import numpy as np
from numpy.typing import NDArray
from scipy.optimize import curve_fit

from blueprints.codes.eurocode.en_1993_1_1_2005 import EN_1993_1_1_2005
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula
from blueprints.type_alias import DIMENSIONLESS


class MomentDistributionType(Enum):
    """Enumeration for moment distribution types according to Table 6.6."""

    CONSTANT = ("constant", 1.0)
    LINEAR = ("linear", None)  # k_c depends on psi parameter
    SIMPLY_SUPPORTED_UNIFORM = ("simply_supported_uniform", 0.94)
    DOUBLE_CLAMPED_UNIFORM = ("double_clamped_uniform", 0.90)
    SIMPLE_CLAMPED_UNIFORM = ("simple_clamped_uniform", 0.91)
    SIMPLY_SUPPORTED_POINT = ("simply_supported_point", 0.86)
    DOUBLE_CLAMPED_POINT = ("double_clamped_point", 0.77)
    SIMPLE_CLAMPED_POINT = ("simple_clamped_point", 0.82)

    def __init__(self, description: str, k_c_value: float | None) -> None:
        self.description = description
        self.k_c_value = k_c_value


class Table6Dot6CorrectionFactorKc(Formula):
    r"""Class representing Table 6.6 for the calculation of correction factor [$k_c$] [$-$].

    This table provides correction factors for different moment distributions used in lateral-torsional buckling
    verification according to EN 1993-1-1:2005.

    Use the `interpretation_of_moment_distribution_for_kc` method to analyze moment distribution data and determine
    the appropriate correction factor based on the best fit to standard patterns.
    """

    label = "6.6"
    source_document = EN_1993_1_1_2005

    def __init__(
        self,
        moment_distribution_type: MomentDistributionType,
        psi: DIMENSIONLESS | None = None,
    ) -> None:
        r"""[$k_c$] Calculates the correction factor [$-$] for moment distribution.

        EN 1993-1-1:2005 art.6.3.2.2 - Table 6.6

        Parameters
        ----------
        moment_distribution_type : MomentDistributionType
            The type of moment distribution. Use the [$MomentDistributionType$] enum. [$-$]
        psi : DIMENSIONLESS | None, optional
            The ratio of end moments for linear distribution. Must be between -1 and 1.
            Required only when moment_distribution_type is LINEAR. [$-$]
        """
        super().__init__()
        self.moment_distribution_type = moment_distribution_type
        self.psi = psi

    @staticmethod
    def _evaluate(
        moment_distribution_type: MomentDistributionType,
        psi: DIMENSIONLESS | None = None,
    ) -> DIMENSIONLESS:
        """For more detailed documentation see the class docstring."""
        if moment_distribution_type == MomentDistributionType.LINEAR:
            if psi is None:
                raise ValueError("Parameter 'psi' must be provided for LINEAR moment distribution type.")
            if not -1 <= psi <= 1:
                raise ValueError(f"Parameter 'psi' must be between -1 and 1, got {psi}.")
            return 1 / (1.33 - 0.33 * psi)

        if moment_distribution_type.k_c_value is None:
            raise ValueError(f"No k_c value defined for {moment_distribution_type}.")  # pragma: no cover
        return moment_distribution_type.k_c_value

    def latex(self, n: int = 2) -> LatexFormula:
        """Returns LatexFormula object for table 6.6.

        Parameters
        ----------
        n : int, optional
            Number of decimal places for the result. Default is 2.
        """
        if self.moment_distribution_type == MomentDistributionType.LINEAR:
            equation = rf"\frac{{1}}{{1.33 - 0.33 \cdot {self.psi}}}"
        else:
            equation = r"\text{" + f"{self.moment_distribution_type.description}" + "}"

        return LatexFormula(
            return_symbol=r"k_c",
            result=f"{self:.{n}f}",
            equation=equation,
            comparison_operator_label="=",
        )

    @staticmethod
    def _calculate_r2(y_true: NDArray[np.float64], y_pred: NDArray[np.float64]) -> float:
        """Calculate R² score using numpy.

        Parameters
        ----------
        y_true : NDArray[np.float64]
            True values
        y_pred : NDArray[np.float64]
            Predicted values

        Returns
        -------
        float
            R² score
        """
        ss_res = np.sum((y_true - y_pred) ** 2)
        ss_tot = np.sum((y_true - np.mean(y_true)) ** 2)
        if ss_tot == 0:
            return 1.0 if ss_res == 0 else 0.0
        return 1 - (ss_res / ss_tot)

    @staticmethod
    def _line_1_constant(x: NDArray[np.float64]) -> NDArray[np.float64]:
        """Line 1: Constant moment distribution.

        Parameters
        ----------
        x : NDArray[np.float64]
            Position along beam (0 to 1)

        Returns
        -------
        NDArray[np.float64]
            Moment values (constant)
        """
        return np.ones_like(x)

    @staticmethod
    def _line_2_linear(x: NDArray[np.float64], a: float) -> NDArray[np.float64]:
        """Line 2: Linear distribution with slope parameter a (between 0 and 1).

        Parameters
        ----------
        x : NDArray[np.float64]
            Position along beam (0 to 1)
        a : float
            Slope parameter (0 to 1)

        Returns
        -------
        NDArray[np.float64]
            Moment values
        """
        return 2 * a * x - 2 * a + 1

    @staticmethod
    def _line_3_simply_supported_q(x: NDArray[np.float64]) -> NDArray[np.float64]:
        """Line 3: Simply supported beam with uniform load.

        Parameters
        ----------
        x : NDArray[np.float64]
            Position along beam (0 to 1)

        Returns
        -------
        NDArray[np.float64]
            Moment values
        """
        return 4 * x - 4 * x**2

    @staticmethod
    def _line_4_double_clamped_q(x: NDArray[np.float64], a: float) -> NDArray[np.float64]:
        """Line 4: Double clamped beam with uniform load and deflection parameter a (between 0 and 1).

        Parameters
        ----------
        x : NDArray[np.float64]
            Position along beam (0 to 1)
        a : float
            Maximum deflection parameter (0 to 1)

        Returns
        -------
        NDArray[np.float64]
            Moment values
        """
        return (1 + a) * (4 * x**2 - 4 * x) + 1

    @staticmethod
    def _line_5_simple_and_clamped_q(x: NDArray[np.float64], a: float) -> NDArray[np.float64]:
        """Line 5: Simple and clamped beam with uniform load and deflection parameter a (between 0 and 1).

        Parameters
        ----------
        x : NDArray[np.float64]
            Position along beam (0 to 1)
        a : float
            Deflection halfway span parameter (0 to 1)

        Returns
        -------
        NDArray[np.float64]
            Moment values
        """
        return (2 * x**2 - 1 * x) + (4 * x**2 - 4 * x) * a

    @staticmethod
    def _line_6_simply_supported_f(x: NDArray[np.float64]) -> NDArray[np.float64]:
        """Line 6: Simply supported beam with point load at midspan.

        Parameters
        ----------
        x : NDArray[np.float64]
            Position along beam (0 to 1)

        Returns
        -------
        NDArray[np.float64]
            Moment values
        """
        return np.where(x < 0.5, 2 * x, 2 - 2 * x)

    @staticmethod
    def _line_7_double_clamped_f(x: NDArray[np.float64], a: float) -> NDArray[np.float64]:
        """Line 7: Double clamped beam with point load and deflection parameter a (between 0 and 1).

        Parameters
        ----------
        x : NDArray[np.float64]
            Position along beam (0 to 1)
        a : float
            Deflection at x=0.5 parameter (0 to 1)

        Returns
        -------
        NDArray[np.float64]
            Moment values
        """
        return np.where(x < 0.5, 1 - 2 * x * (1 + a), -1 - 2 * a + 2 * x * (1 + a))

    @staticmethod
    def _line_8_simple_and_clamped_f(x: NDArray[np.float64], a: float) -> NDArray[np.float64]:
        """Line 8: Simple and clamped beam with point load and deflection parameter a (between 0 and 1).

        Parameters
        ----------
        x : NDArray[np.float64]
            Position along beam (0 to 1)
        a : float
            Deflection at x=0.5 parameter (0 to 1)

        Returns
        -------
        NDArray[np.float64]
            Moment values
        """
        return np.where(x < 0.5, -2 * x * a, -1 - 2 * a + 2 * x * (1 + a))

    @staticmethod
    def _normalize(x_data: NDArray[np.float64], y_data: NDArray[np.float64]) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Rescale data to standard range for curve fitting, with x_data in [0, 1] and y_data in [-1, 1].

        Parameters
        ----------
        x_data : NDArray[np.float64]
            Position data
        y_data : NDArray[np.float64]
            Moment data

        Returns
        -------
        tuple[NDArray[np.float64], NDArray[np.float64]]
            Rescaled x_data (range [0, 1]) and y_data (range [-1, 1])
        """
        # Rescale x_data to range [0, 1]
        x_min = np.min(x_data)
        x_max = np.max(x_data)
        x_data = (x_data - x_min) / (x_max - x_min)

        # Rescale y_data to range [-1, 1]
        y_abs_max = np.max(np.abs(y_data))
        y_data = y_data / y_abs_max if y_abs_max != 0 else y_data

        return x_data, y_data

    @staticmethod
    def _curve_fit_and_evaluate(
        num_params: int,
        func: Callable,
        x_data: NDArray[np.float64],
        y_data: NDArray[np.float64],
        name: str,
        results: dict,
    ) -> None:
        """Perform curve fitting and evaluate R² score.

        Parameters
        ----------
        num_params : int
            Number of parameters to fit
        func : callable
            Function to fit
        x_data : NDArray[np.float64]
            Position data
        y_data : NDArray[np.float64]
            Moment data
        name : str
            Name of the line/distribution
        results : dict
            Dictionary to store results
        """
        # Set bounds for parameters to be between 0 and 1
        if num_params > 0:
            bounds = ([0] * num_params, [1] * num_params)
            popt, _ = curve_fit(func, x_data, y_data, bounds=bounds, maxfev=10000)
            y_pred = func(x_data, *popt)
        else:
            # No parameters to fit
            popt = np.array([])
            y_pred = func(x_data)

        # Calculate R² value
        r2 = Table6Dot6CorrectionFactorKc._calculate_r2(y_data, y_pred)

        # Store results
        results[name] = {"parameters": popt, "r2_score": r2, "predictions": y_pred}

    @classmethod
    def interpretation_of_moment_distribution_for_kc(
        cls,
        y_data: NDArray[np.float64] | list[float],
        x_data: NDArray[np.float64] | list[float] | None = None,
    ) -> float:
        """Interpret moment distribution data and determine the best-fit correction factor k_c.

        This method analyzes moment distribution data by fitting it to the 7 standard patterns
        from Table 6.6 (excluding constant which is covered by linear with slope 0) and returns
        the k_c value for the best-matching pattern.

        Parameters
        ----------
        y_data : NDArray[np.float64] | list[float]
            Moment values along the beam
        x_data : NDArray[np.float64] | list[float] | None, optional
            Position values along the beam. If None, assumes equally spaced points.

        Returns
        -------
        float
            The correction factor k_c corresponding to the best-fit moment distribution pattern.
            Returns 1.0 if no valid fit is found.

        Examples
        --------
        >>> y_data = [-60.22, -48.78, -38.54, -29.51, -21.68, -15.06, -9.64, 5.42, -2.41, -0.6, 0]
        >>> k_c = Table6Dot6CorrectionFactorKc.interpret_moment_distribution_for_kc(y_data)
        >>> print(f"Calculated k_c: {k_c:.3f}")
        """
        x_data = np.array(x_data, dtype=np.float64) if x_data is not None else np.arange(len(y_data), dtype=np.float64)
        y_data = np.array(y_data, dtype=np.float64)

        if len(y_data) <= 1:
            return 1.0  # Single data point corresponds to k_c = 1.0

        # Rescale data
        x_data, y_data = cls._normalize(x_data, y_data)

        # List of functions, their names, and parameter counts
        lines = [
            (cls._line_1_constant, "Line 1 (Constant)", 0),
            (cls._line_2_linear, "Line 2 (Linear)", 1),
            (cls._line_3_simply_supported_q, "Line 3 (Simply Supported, q-load)", 0),
            (cls._line_4_double_clamped_q, "Line 4 (Double Clamped, q-load)", 1),
            (cls._line_5_simple_and_clamped_q, "Line 5 (Simple and Clamped, q-load)", 1),
            (cls._line_6_simply_supported_f, "Line 6 (Simply Supported, F-load)", 0),
            (cls._line_7_double_clamped_f, "Line 7 (Double Clamped, F-load)", 1),
            (cls._line_8_simple_and_clamped_f, "Line 8 (Simple and Clamped, F-load)", 1),
        ]

        all_results = {}

        # Try curve fitting for each function with both y_data and -y_data,
        # and also with reversed data to account for different orientations
        for variant in [[x_data, y_data], [x_data, -y_data], [1 - x_data, y_data], [1 - x_data, -y_data]]:
            x_variant, y_variant = variant
            for func, name, num_params in lines:
                results = {}
                cls._curve_fit_and_evaluate(num_params, func, x_variant, y_variant, name, results)
                if name in all_results:
                    # Keep the better fit
                    if results[name]["r2_score"] > all_results[name]["r2_score"]:
                        all_results[name] = results[name]
                else:
                    all_results[name] = results[name]

        # Find best fit from all results
        best_fit = max(
            [(name, data) for name, data in all_results.items() if "r2_score" in data],
            key=lambda x: x[1]["r2_score"],
            default=(None, None),
        )

        # Map line names to MomentDistributionType
        line_to_distribution_type = {
            "Line 1 (Constant)": MomentDistributionType.CONSTANT,
            "Line 2 (Linear)": MomentDistributionType.LINEAR,
            "Line 3 (Simply Supported, q-load)": MomentDistributionType.SIMPLY_SUPPORTED_UNIFORM,
            "Line 4 (Double Clamped, q-load)": MomentDistributionType.DOUBLE_CLAMPED_UNIFORM,
            "Line 5 (Simple and Clamped, q-load)": MomentDistributionType.SIMPLE_CLAMPED_UNIFORM,
            "Line 6 (Simply Supported, F-load)": MomentDistributionType.SIMPLY_SUPPORTED_POINT,
            "Line 7 (Double Clamped, F-load)": MomentDistributionType.DOUBLE_CLAMPED_POINT,
            "Line 8 (Simple and Clamped, F-load)": MomentDistributionType.SIMPLE_CLAMPED_POINT,
        }

        # Get the distribution type for the best fit
        if not best_fit[0]:
            return 0.0  # pragma: no cover - no valid fit found, return 0.0 as a fallback

        distribution_type = line_to_distribution_type.get(best_fit[0])

        # Calculate k_c based on the distribution type
        if distribution_type == MomentDistributionType.LINEAR:
            line_2_slope = all_results.get("Line 2 (Linear)", {}).get("parameters", [None])[0]
            line_2_psi = 1 - 2 * line_2_slope if line_2_slope is not None else None
            k_c = 1 / (1.33 - 0.33 * line_2_psi) if line_2_psi is not None else 1.0
        else:
            k_c = distribution_type.k_c_value if distribution_type and distribution_type.k_c_value is not None else 1.0

        return round(float(k_c), 3)
