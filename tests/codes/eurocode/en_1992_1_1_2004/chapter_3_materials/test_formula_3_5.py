"""Testing formula 3.5 of EN 1992-1-1:2004."""

import pytest

from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_3_materials.formula_3_5 import Form3Dot5ApproximationVarianceElasticModulusOverTime


class TestForm3Dot5ApproximationVarianceElasticModulusOverTime:
    """Validation for formula 3.5 from EN 1992-1-1:2004."""

    def test_evaluation(self) -> None:
        """Test the evaluation of the result."""
        # Example values
        f_cm_t = 2.34  # MPa
        f_cm = 3.4  # MPa
        e_cm = 2.9  # MPa
        form_3_5 = Form3Dot5ApproximationVarianceElasticModulusOverTime(f_cm_t=f_cm_t, f_cm=f_cm, e_cm=e_cm)

        # Expected result, manually calculated
        manually_calculated_result = 2.592502

        assert form_3_5 == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_raise_error_when_negative_f_cm_t_is_given(self) -> None:
        """Test a negative value."""
        # Example values
        f_cm_t = -2.34  # MPa
        f_cm = 3.4  # MPa
        e_cm = 2.9  # MPa

        with pytest.raises(ValueError):
            Form3Dot5ApproximationVarianceElasticModulusOverTime(f_cm_t=f_cm_t, f_cm=f_cm, e_cm=e_cm)

    def test_raise_error_when_negative_f_cm_is_given(self) -> None:
        """Test a negative value."""
        # Example values
        f_cm_t = 2.34  # MPa
        f_cm = -3.4  # MPa
        e_cm = 2.9  # MPa

        with pytest.raises(ValueError):
            Form3Dot5ApproximationVarianceElasticModulusOverTime(f_cm_t=f_cm_t, f_cm=f_cm, e_cm=e_cm)

    def test_raise_error_when_negative_e_cm_is_given(self) -> None:
        """Test a negative value."""
        # Example values
        f_cm_t = 2.34  # MPa
        f_cm = 3.4  # MPa
        e_cm = -2.9  # MPa

        with pytest.raises(ValueError):
            Form3Dot5ApproximationVarianceElasticModulusOverTime(f_cm_t=f_cm_t, f_cm=f_cm, e_cm=e_cm)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"E_{cm}(t) = ( f_{cm}(t) / f_{cm} )^{0.3} \cdot E_{cm} = ( 2.340 / 3.400 )^{0.3} \cdot 2.900 = 2.593",
            ),
            ("short", r"E_{cm}(t) = 2.593"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        f_cm_t = 2.34  # MPa
        f_cm = 3.4  # MPa
        e_cm = 2.9  # MPa

        # Object to test
        form_3_5_latex = Form3Dot5ApproximationVarianceElasticModulusOverTime(f_cm_t=f_cm_t, f_cm=f_cm, e_cm=e_cm).latex()

        actual = {"complete": form_3_5_latex.complete, "short": form_3_5_latex.short}

        assert actual[representation] == expected, f"{representation} representation failed."
