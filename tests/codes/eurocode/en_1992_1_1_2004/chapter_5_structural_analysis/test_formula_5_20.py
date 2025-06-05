"""Testing formula 5.20 from EN 1992-1-1:2004."""

import pytest

from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_5_structural_analysis.formula_5_20 import Form5Dot20DesignModulusElasticity
from blueprints.validations import LessOrEqualToZeroError


class TestForm5Dot20DesignModulusElasticity:
    """Validation for formula 5.20 from EN 1992-1-1:2004."""

    @pytest.fixture
    def form_5_20(self) -> Form5Dot20DesignModulusElasticity:
        """Setup and teardown for test."""
        return Form5Dot20DesignModulusElasticity(e_cm=30000, gamma_ce=1.2)

    def test_evaluation(self, form_5_20: Form5Dot20DesignModulusElasticity) -> None:
        """Test the evaluation of the result."""
        # Expected result, manually calculated
        manually_calculated_result = 30000 / 1.2
        assert form_5_20 == pytest.approx(manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("e_cm", "gamma_ce"),
        [
            (30000, 0),
        ],
    )
    def test_raise_error_when_zero_pars_are_given(self, e_cm: float, gamma_ce: float) -> None:
        """Test zero values for e_cm, gamma_ce."""
        with pytest.raises(LessOrEqualToZeroError):
            Form5Dot20DesignModulusElasticity(e_cm=e_cm, gamma_ce=gamma_ce)

    @pytest.mark.parametrize(
        ("e_cm", "gamma_ce", "expected"),
        [
            (30000, 1.2, 25000),
            (35000, 1.2, 29166.67),
        ],
    )
    def test_properties(self, e_cm: float, gamma_ce: float, expected: float) -> None:
        """Test the properties of the formula."""
        form_5_20 = Form5Dot20DesignModulusElasticity(e_cm=e_cm, gamma_ce=gamma_ce)
        assert form_5_20 == pytest.approx(expected, rel=1e-4)

    def test_latex(self, form_5_20: Form5Dot20DesignModulusElasticity) -> None:
        """Test the latex representation of the formula."""
        # Object to test
        form_5_20_latex = form_5_20.latex()
        expected_complete = r"E_{cd} = \frac{E_{cm}}{\gamma_{CE}} = \frac{30000}{1.2} = 25000.000"
        expected_short = r"E_{cd} = 25000.000"

        assert form_5_20_latex.complete == expected_complete, "Complete representation failed."
        assert form_5_20_latex.short == expected_short, "Short representation failed."
