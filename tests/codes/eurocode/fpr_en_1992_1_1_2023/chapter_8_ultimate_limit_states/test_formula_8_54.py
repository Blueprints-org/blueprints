"""Testing formula 8.54 of FprEN 1992-1-1:2023."""

import pytest

from blueprints.codes.eurocode.fpr_en_1992_1_1_2023.chapter_8_ultimate_limit_states.formula_8_54 import Form8Dot54NominalWebWidth
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestForm8Dot54NominalWebWidth:
    """Validation for formula 8.54 from FprEN 1992-1-1:2023."""

    @pytest.mark.parametrize(
        ("b_w", "k_duct", "sum_phi_duct", "expected"),
        [
            (400.0, 0.8, 100.0, 320.0),  # grouted plastic ducts with a thin wall
            (400.0, 0.5, 100.0, 350.0),  # grouted steel ducts
            (400.0, 1.2, 100.0, 280.0),  # non-grouted ducts
        ],
    )
    def test_evaluation(self, b_w: float, k_duct: float, sum_phi_duct: float, expected: float) -> None:
        """Tests the evaluation of the result for the three values of k_duct that the standard gives."""
        # Create object to test
        formula = Form8Dot54NominalWebWidth(b_w=b_w, k_duct=k_duct, sum_phi_duct=sum_phi_duct)

        # Perform test by assert
        assert formula == pytest.approx(expected=expected, rel=1e-4)

    def test_result_is_not_clamped_at_zero(self) -> None:
        """The standard prints no lower bound on the nominal web width. Ducts that take up more than the web
        leave a result that is zero or negative, and that result is returned unchanged rather than clamped,
        since a clamp would be an addition beyond the printed text.
        """
        # Example values, with the ducts wider than the web itself
        formula = Form8Dot54NominalWebWidth(b_w=400.0, k_duct=1.2, sum_phi_duct=400.0)

        # 400 - 1.2 * 400 = -80
        assert formula == pytest.approx(expected=-80.0, rel=1e-4)

    @pytest.mark.parametrize(
        ("b_w", "k_duct", "sum_phi_duct"),
        [
            (400.0, -0.8, 100.0),  # k_duct is negative
            (400.0, 0.8, -100.0),  # sum_phi_duct is negative
        ],
    )
    def test_raise_error_when_negative_values_are_given(self, b_w: float, k_duct: float, sum_phi_duct: float) -> None:
        """Test if error is raised for parameters that are not allowed to be negative."""
        with pytest.raises(NegativeValueError):
            Form8Dot54NominalWebWidth(b_w=b_w, k_duct=k_duct, sum_phi_duct=sum_phi_duct)

    @pytest.mark.parametrize(
        ("b_w", "k_duct", "sum_phi_duct"),
        [
            (-400.0, 0.8, 100.0),  # b_w is negative
            (0.0, 0.8, 100.0),  # b_w is zero
        ],
    )
    def test_raise_error_when_less_or_equal_to_zero(self, b_w: float, k_duct: float, sum_phi_duct: float) -> None:
        """Test if error is raised for parameters that are not allowed to be zero or less."""
        with pytest.raises(LessOrEqualToZeroError):
            Form8Dot54NominalWebWidth(b_w=b_w, k_duct=k_duct, sum_phi_duct=sum_phi_duct)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            ("complete", r"b_{w,nom} = b_w - k_{duct} \cdot \Sigma\phi_{duct} = 400.000 - 0.800 \cdot 100.000 = 320.000 \ mm"),
            (
                "complete_with_units",
                r"b_{w,nom} = b_w - k_{duct} \cdot \Sigma\phi_{duct} = 400.000 \ mm - 0.800 \cdot 100.000 \ mm = 320.000 \ mm",
            ),
            ("short", r"b_{w,nom} = 320.000 \ mm"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        b_w = 400.0
        k_duct = 0.8
        sum_phi_duct = 100.0

        # Object to test
        test_latex = Form8Dot54NominalWebWidth(b_w=b_w, k_duct=k_duct, sum_phi_duct=sum_phi_duct).latex()

        actual = {
            "complete": test_latex.complete,
            "complete_with_units": test_latex.complete_with_units,
            "short": test_latex.short,
        }

        assert expected == actual[representation]
