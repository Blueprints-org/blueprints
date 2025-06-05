"""Testing formula 8.15 from EN 1992-1-1:2004."""

import pytest

from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_8_detailing_of_reinforcement_and_prestressing_tendons.formula_8_2 import (
    SubForm8Dot2CoefficientQualityOfBond,
)
from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_8_detailing_of_reinforcement_and_prestressing_tendons.formula_8_15 import (
    Form8Dot15PrestressTransferStress,
    SubForm8Dot15EtaP1,
    SubForm8Dot15TensileStrengthAtRelease,
)
from blueprints.validations import NegativeValueError


class TestForm8Dot15Form8Dot15PrestressTransferStress:
    """Validation for formula 8.15 from EN 1992-1-1:2004."""

    def test_evaluation(self) -> None:
        """Test the evaluation of the result."""
        # example values
        eta_p1 = 2.7  # [-]
        eta_1 = 1  # [-]
        f_ctd_t = 2.5  # MPa
        form_8_15 = Form8Dot15PrestressTransferStress(
            eta_p1=eta_p1,
            eta_1=eta_1,
            f_ctd_t=f_ctd_t,
        )

        # manually calculated result
        manually_calculated_result = 6.75  # MPa

        assert form_8_15 == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_negative_eta_p1(self) -> None:
        """Test the evaluation of the result."""
        # example values
        eta_p1 = -2.7  # [-]
        eta_1 = 1  # [-]
        f_ctd_t = 2.5  # MPa
        with pytest.raises(NegativeValueError):
            Form8Dot15PrestressTransferStress(
                eta_p1=eta_p1,
                eta_1=eta_1,
                f_ctd_t=f_ctd_t,
            )

    def test_negative_eta_1(self) -> None:
        """Test the evaluation of the result."""
        # example values
        eta_p1 = 2.7  # [-]
        eta_1 = -1  # [-]
        f_ctd_t = 2.5  # MPa
        with pytest.raises(NegativeValueError):
            Form8Dot15PrestressTransferStress(
                eta_p1=eta_p1,
                eta_1=eta_1,
                f_ctd_t=f_ctd_t,
            )

    def test_negative_f_ctd_t(self) -> None:
        """Test the evaluation of the result."""
        # example values
        eta_p1 = 2.7  # [-]
        eta_1 = 1  # [-]
        f_ctd_t = -2.5  # MPa
        with pytest.raises(NegativeValueError):
            Form8Dot15PrestressTransferStress(
                eta_p1=eta_p1,
                eta_1=eta_1,
                f_ctd_t=f_ctd_t,
            )

    def test_integration_with_sub_form_8_15_1(self) -> None:
        """Test the integration with sub-formula 8.15."""
        # example values
        eta_1 = 1  # [-]
        f_ctd_t = 2.5  # MPa
        type_of_wire = "indented"
        eta_p1 = SubForm8Dot15EtaP1(type_of_wire=type_of_wire)  # [-]
        form_8_15 = Form8Dot15PrestressTransferStress(eta_p1=eta_p1, eta_1=eta_1, f_ctd_t=f_ctd_t)

        manually_calculated_result = 6.75  # MPa

        assert form_8_15 == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_integration_with_sub_form_8_15_2(self) -> None:
        """Test the integration with sub-formula 8.15."""
        # example values
        eta_p1 = 1  # [-]
        eta_1 = 1  # [-]
        alpha_ct = 1  # [-]
        f_ctm_t = 2.5  # MPa
        gamma_c = 1.5  # [-]
        f_ctd_t = SubForm8Dot15TensileStrengthAtRelease(
            alpha_ct=alpha_ct,
            f_ctm_t=f_ctm_t,
            gamma_c=gamma_c,
        )

        form_8_15 = Form8Dot15PrestressTransferStress(eta_p1=eta_p1, eta_1=eta_1, f_ctd_t=f_ctd_t)

        manually_calculated_result = 1.16666666666666666666  # MPa

        assert form_8_15 == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_integration_with_sub_form_8_2_coefficient_of_bond(self) -> None:
        """Test the integration with sub-formula 8.2."""
        # example values
        eta_p1 = 1
        eta_1 = SubForm8Dot2CoefficientQualityOfBond(bond_quality="good")
        f_ctd_t = 2.5  # MPa

        form_8_15 = Form8Dot15PrestressTransferStress(eta_p1=eta_p1, eta_1=eta_1, f_ctd_t=f_ctd_t)

        manually_calculated_result = 2.5  # MPa

        assert form_8_15 == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                (r"f_{bpt} = \eta_{p1} \cdot \eta_1 \cdot f_{ctd}(t) = 2.70 \cdot 1.00 \cdot 2.50 = 6.75"),
            ),
            ("short", r"f_{bpt} = 6.75"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # example values
        eta_1 = 1  # [-]
        f_ctd_t = 2.5  # MPa
        type_of_wire = "indented"
        eta_p1 = SubForm8Dot15EtaP1(type_of_wire=type_of_wire)  # [-]

        # Object to test
        form_8_15_latex = Form8Dot15PrestressTransferStress(eta_p1=eta_p1, eta_1=eta_1, f_ctd_t=f_ctd_t).latex()

        actual = {"complete": form_8_15_latex.complete, "short": form_8_15_latex.short}

        assert actual[representation] == expected, f"{representation} representation failed."
