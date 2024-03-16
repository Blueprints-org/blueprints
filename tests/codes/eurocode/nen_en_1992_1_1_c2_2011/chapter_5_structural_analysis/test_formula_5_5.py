"""Testing formula 5.5 of NEN-EN 1992-1-1+C2:2011."""

import pytest

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011.chapter_5_structural_analysis.formula_5_5 import Form5Dot5TransverseForceEffectFloorDiaphragm
from blueprints.validations import NegativeValueError


class TestForm5Dot5TransverseForceEffectFloorDiaphragm:
    """Validation for formula 5.5 from NEN-EN 1992-1-1+C2:2011."""

    def test_evaluation(self) -> None:
        """Test the evaluation of the result."""
        # Example values
        theta_i = 0.003  # -
        n_a = 5  # kN
        n_b = 10  # kN

        # Object to test
        form_5_4 = Form5Dot5TransverseForceEffectFloorDiaphragm(theta_i=theta_i, n_a=n_a, n_b=n_b)

        # Expected result, manually calculated
        manually_calculated_result = 0.0225  # kN

        assert form_5_4 == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_raise_error_when_negative_theta_i_is_given(self) -> None:
        """Test a negative value for theta_i."""
        # Example values
        theta_i = -0.003
        n_a = 5
        n_b = 10

        with pytest.raises(NegativeValueError):
            Form5Dot5TransverseForceEffectFloorDiaphragm(theta_i=theta_i, n_a=n_a, n_b=n_b)

    def test_raise_error_when_negative_n_a_is_given(self) -> None:
        """Test a negative value for n_a."""
        # Example values
        theta_i = 0.003
        n_a = -5
        n_b = 10

        with pytest.raises(NegativeValueError):
            Form5Dot5TransverseForceEffectFloorDiaphragm(theta_i=theta_i, n_a=n_a, n_b=n_b)

    def test_raise_error_when_negative_n_b_is_given(self) -> None:
        """Test a negative value for n_b."""
        # Example values
        theta_i = 0.003
        n_a = 5
        n_b = -10

        with pytest.raises(NegativeValueError):
            Form5Dot5TransverseForceEffectFloorDiaphragm(theta_i=theta_i, n_a=n_a, n_b=n_b)

    def test_latex(self) -> None:
        """Test the latex representation of the formula."""
        # Example values
        theta_i = 0.003  # -
        n_a = 5  # kN
        n_b = 10  # kN

        # Object to test
        form_5_5_latex = Form5Dot5TransverseForceEffectFloorDiaphragm(
            theta_i=theta_i,
            n_a=n_a,
            n_b=n_b,
        ).latex()

        # Expected result
        latex_complete = r"H_{i} = Θ_{i} \cdot (N_{b} + N_{a}) / 2 = 0.003 \cdot (10.000 + 5.000) / 2 = 0.022"
        latex_short = r"H_{i} = 0.022"

        latex_test_sample = {
            "complete": {
                "expected": latex_complete,
                "actual": form_5_5_latex.complete,
            },
            "short": {"expected": latex_short, "actual": form_5_5_latex.short},
            "string": {"expected": latex_complete, "actual": str(form_5_5_latex)},
        }

        assertion_errors = []

        # A try-except block inside a loop is considered bad practice by Ruff
        # However, the documentation states that ignoring this will only have a negligible impact on performance
        # https://docs.astral.sh/ruff/rules/try-except-in-loop/
        # In this case, the desired behavior is to collect all the errors and raise them at once
        for representation, values in latex_test_sample.items():
            try:
                assert values["expected"] == values["actual"]
            except AssertionError as error_message:  # noqa: PERF203
                assertion_errors.append(rf"Error in {representation} representation. {error_message}")

        if assertion_errors:
            raise AssertionError("{} errors occurred:\n{}".format(len(assertion_errors), "\n".join(assertion_errors)))
