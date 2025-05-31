"""Testing formula 4.2 of EN 1992-1-1:2004."""

import pytest

from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_4_durability_and_cover.formula_4_2 import Form4Dot2MinimumConcreteCover
from blueprints.validations import NegativeValueError


class TestForm4Dot1NominalConcreteCover:
    """Validation for formula 4.2 from EN 1992-1-1:2004."""

    def test_evaluation(self) -> None:
        """Test the evaluation of the result."""
        # Example values
        c_min_b = 15  # mm
        c_min_dur = 10  # mm
        delta_c_dur_gamma = 5  # mm
        delta_c_dur_st = 5  # mm
        delta_c_dur_add = 0  # mm
        form_4_2 = Form4Dot2MinimumConcreteCover(
            c_min_b=c_min_b,
            c_min_dur=c_min_dur,
            delta_c_dur_gamma=delta_c_dur_gamma,
            delta_c_dur_st=delta_c_dur_st,
            delta_c_dur_add=delta_c_dur_add,
        )

        # Expected result, manually calculated
        manually_calculated_result = 15

        assert form_4_2 == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_evaluation_default_values(self) -> None:
        """Test the evaluation of the result using the default values for delta parameters."""
        # Example values
        c_min_b = 15  # mm
        c_min_dur = 20  # mm
        form_4_2 = Form4Dot2MinimumConcreteCover(
            c_min_b=c_min_b,
            c_min_dur=c_min_dur,
        )

        # Expected result, manually calculated
        manually_calculated_result = 20

        assert form_4_2 == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_raise_error_when_negative_c_min_b_is_given(self) -> None:
        """Test the evaluation of the result."""
        # Example values
        c_min_b = -15  # mm
        c_min_dur = 10  # mm
        delta_c_dur_gamma = 5  # mm
        delta_c_dur_st = 5  # mm
        delta_c_dur_add = 0  # mm

        with pytest.raises(NegativeValueError):
            Form4Dot2MinimumConcreteCover(
                c_min_b=c_min_b,
                c_min_dur=c_min_dur,
                delta_c_dur_gamma=delta_c_dur_gamma,
                delta_c_dur_st=delta_c_dur_st,
                delta_c_dur_add=delta_c_dur_add,
            )

    def test_raise_error_when_negative_c_min_dur_is_given(self) -> None:
        """Test the evaluation of the result."""
        # Example values
        c_min_b = 15  # mm
        c_min_dur = -10  # mm
        delta_c_dur_gamma = 5  # mm
        delta_c_dur_st = 5  # mm
        delta_c_dur_add = 0  # mm

        with pytest.raises(NegativeValueError):
            Form4Dot2MinimumConcreteCover(
                c_min_b=c_min_b,
                c_min_dur=c_min_dur,
                delta_c_dur_gamma=delta_c_dur_gamma,
                delta_c_dur_st=delta_c_dur_st,
                delta_c_dur_add=delta_c_dur_add,
            )

    def test_raise_error_when_negative_delta_c_dur_gamma_is_given(self) -> None:
        """Test the evaluation of the result."""
        # Example values
        c_min_b = 15  # mm
        c_min_dur = 10  # mm
        delta_c_dur_gamma = -5  # mm
        delta_c_dur_st = 5  # mm
        delta_c_dur_add = 0  # mm

        with pytest.raises(NegativeValueError):
            Form4Dot2MinimumConcreteCover(
                c_min_b=c_min_b,
                c_min_dur=c_min_dur,
                delta_c_dur_gamma=delta_c_dur_gamma,
                delta_c_dur_st=delta_c_dur_st,
                delta_c_dur_add=delta_c_dur_add,
            )

    def test_raise_error_when_negative_delta_c_dur_st_is_given(self) -> None:
        """Test the evaluation of the result."""
        # Example values
        c_min_b = 15  # mm
        c_min_dur = 10  # mm
        delta_c_dur_gamma = 5  # mm
        delta_c_dur_st = -5  # mm
        delta_c_dur_add = 0  # mm

        with pytest.raises(NegativeValueError):
            Form4Dot2MinimumConcreteCover(
                c_min_b=c_min_b,
                c_min_dur=c_min_dur,
                delta_c_dur_gamma=delta_c_dur_gamma,
                delta_c_dur_st=delta_c_dur_st,
                delta_c_dur_add=delta_c_dur_add,
            )

    def test_raise_error_when_negative_delta_c_dur_add_is_given(self) -> None:
        """Test the evaluation of the result."""
        # Example values
        c_min_b = 15  # mm
        c_min_dur = 10  # mm
        delta_c_dur_gamma = 5  # mm
        delta_c_dur_st = 5  # mm
        delta_c_dur_add = -5  # mm

        with pytest.raises(NegativeValueError):
            Form4Dot2MinimumConcreteCover(
                c_min_b=c_min_b,
                c_min_dur=c_min_dur,
                delta_c_dur_gamma=delta_c_dur_gamma,
                delta_c_dur_st=delta_c_dur_st,
                delta_c_dur_add=delta_c_dur_add,
            )

    @pytest.mark.parametrize(
        ("representation", "expected_result"),
        [
            (
                "complete",
                r"c_{min} = \max \left\{c_{min,b}; c_{min,dur}+\Delta c_{dur,\gamma}-\Delta c_{dur,st}-\Delta c_{dur,add}; 10 "
                r"\text{mm}\right\} = \max \left\{15; 10+5-5-0; 10\right\} = 15.0",
            ),
            ("short", "c_{min} = 15.0"),
            (
                "string",
                r"c_{min} = \max \left\{c_{min,b}; c_{min,dur}+\Delta c_{dur,\gamma}-\Delta c_{dur,st}-\Delta c_{dur,add}; 10 "
                r"\text{mm}\right\} = \max \left\{15; 10+5-5-0; 10\right\} = 15.0",
            ),
        ],
    )
    def test_latex(self, representation: str, expected_result: str) -> None:
        """Test the latex implementation."""
        c_min_b = 15  # mm
        c_min_dur = 10  # mm
        delta_c_dur_gamma = 5  # mm
        delta_c_dur_st = 5  # mm
        delta_c_dur_add = 0  # mm

        form = Form4Dot2MinimumConcreteCover(
            c_min_b=c_min_b,
            c_min_dur=c_min_dur,
            delta_c_dur_gamma=delta_c_dur_gamma,
            delta_c_dur_st=delta_c_dur_st,
            delta_c_dur_add=delta_c_dur_add,
        ).latex()

        actual = {
            "complete": form.complete,
            "short": form.short,
            "string": str(form),
        }

        assert actual[representation] == expected_result, f"{representation} representation failed."
