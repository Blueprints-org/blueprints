"""Testing formula 3.29 of NEN-EN 1992-1-1+C2:2011."""
# pylint: disable=arguments-differ
import pytest

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011.chapter_3_materials import Form3Dot29RatioLossOfPreStressClass2


class TestForm3Dot29RatioLossOfPreStressClass2:
    """Validation for formula 3.29 from NEN-EN 1992-1-1+C2:2011."""

    def test_evaluation(self) -> None:
        """Test the evaluation of the result."""
        # Example values
        rho_1000 = 35.2  # %
        mu = 0.28  # -
        t = 7.4  # hours

        form_3_29 = Form3Dot29RatioLossOfPreStressClass2(rho_1000=rho_1000, mu=mu, t=t)

        # Expected result, manually calculated
        manually_calculated_result = 2.099201 * 10**-4

        assert form_3_29 == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_raise_error_when_negative_rho_1000_is_given(self) -> None:
        """Test a negative value."""
        # Example values
        rho_1000 = -35.2  # %
        mu = 0.28  # -
        t = 7.4  # hours

        with pytest.raises(ValueError):
            Form3Dot29RatioLossOfPreStressClass2(rho_1000=rho_1000, mu=mu, t=t)

    def test_raise_error_when_negative_t_is_given(self) -> None:
        """Test a negative value."""
        # Example values
        rho_1000 = 35.2  # %
        mu = 0.28  # -
        t = -7.4  # hours

        with pytest.raises(ValueError):
            Form3Dot29RatioLossOfPreStressClass2(rho_1000=rho_1000, mu=mu, t=t)
