"""Module contains tests for formula 2.1a from NEN 9997-1+C2:2017: Chapter 2: Basis of geotechnical design."""

import pytest

from blueprints.codes.eurocode.nen_9997_1_c2_2017.chapter_2_basic_of_geotechnical_design.formula_2_1_a import Form2Dot1aDesignValueLoad
from blueprints.codes.eurocode.nen_9997_1_c2_2017.chapter_2_basic_of_geotechnical_design.formula_2_1_b import Form2Dot1bRepresentativeValue
from blueprints.type_alias import DIMENSIONLESS
from blueprints.validations import NegativeValueError


class TestForm2Dot1aDesignValueLoad:
    """Class containing tests for formula 2.1a from NEN 9997-1+C2:2017: Chapter 2: Basis of geotechnical design."""

    @pytest.mark.parametrize(
        ("gamma_f", "f_rep", "expected_result"),
        [
            (1.35, 100, 135),
            (1.35, 0.0, 0.0),
            (1.35, -100, -135),
        ],
    )
    def test_formula_2_1_a(
        self,
        gamma_f: DIMENSIONLESS,
        f_rep: float,
        expected_result: float,
    ) -> None:
        """Method to test formula 2.1a from NEN 9997-1+C2:2017: Chapter 2: Basis of geotechnical design."""
        assert Form2Dot1aDesignValueLoad(gamma_f=gamma_f, f_rep=f_rep) == pytest.approx(expected_result, rel=1e-9)

    def test_raise_error_if_gamma_f_is_negative(self) -> None:
        """Test if an error is raised when gamma_f is negative."""
        with pytest.raises(NegativeValueError):
            Form2Dot1aDesignValueLoad(gamma_f=-1.35, f_rep=100)

    def test_integration_with_2_1_b(self) -> None:
        """Test the integration of formula 2.1a with 2.1b."""
        f_rep = Form2Dot1bRepresentativeValue(psi=2, f_k=50)
        gamma_f = 1.35
        result = Form2Dot1aDesignValueLoad(gamma_f=gamma_f, f_rep=f_rep)

        assert result == pytest.approx(expected=135, rel=1e-9)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"F_d = \gamma_F \cdot F_{rep} = 1.20 \cdot 100.00 = 120.00",
            ),
            ("short", r"F_d = 120.00"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        gamma_f = 1.2  # [-]
        f_rep = 100  # kN

        # Object to test
        form_2_1_a_latex = Form2Dot1aDesignValueLoad(gamma_f=gamma_f, f_rep=f_rep).latex()

        actual = {"complete": form_2_1_a_latex.complete, "short": form_2_1_a_latex.short}

        assert actual[representation] == expected, f"{representation} representation failed."
