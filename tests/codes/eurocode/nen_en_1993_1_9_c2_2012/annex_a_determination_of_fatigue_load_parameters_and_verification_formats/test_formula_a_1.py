"""Testing formula A.1 from NEN-EN 1993-1-9+C2:2012: Annex A - Determination of fatigue load parameters and verification formats."""

import pytest

from blueprints.codes.eurocode.nen_en_1993_1_9_c2_2012.annex_a_determination_of_fatigue_load_parameters_and_verification_formats.formula_a_1 import FormADot1DamageDuringDesignLife
from blueprints.validations import NegativeValueError, LessOrEqualToZeroError, ListsNotSameLengthError, EmptyListError


class TestFormADot1DamageDuringDesignLife:
    """Validation for formula A.1 from NEN-EN 1993-1-9+C2:2012."""

    def test_evaluation(self) -> None:
        """Test the evaluation of the result."""
        # example values
        n_E = [5, 4, 3]
        N_R = [10, 20, 30]

        form_a_1 = FormADot1DamageDuringDesignLife(n_E=n_E, N_R=N_R)
        # manually calculated result
        manually_calculated_result = 5 / 10 + 4 / 20 + 3 / 30

        assert form_a_1 == pytest.approx(expected=manually_calculated_result, rel=1e-9)

    def test_raise_error_if_negative_n_E(self) -> None:
        """Test that a NegativeValueError is raised when a negative value is passed for n_E."""
        n_E = [-5, 4, 3]
        N_R = [10, 20, 30]
        with pytest.raises(NegativeValueError):
            FormADot1DamageDuringDesignLife(n_E=n_E, N_R=N_R)

    def test_raise_error_if_negative_N_R(self) -> None:
        """Test that a LessOrEqualToZeroError is raised when a negative value is passed for N_R."""
        n_E = [5, 4, 3]
        N_R = [10, -20, 30]
        with pytest.raises(LessOrEqualToZeroError):
            FormADot1DamageDuringDesignLife(n_E=n_E, N_R=N_R)

    def test_raise_error_if_zero_N_R(self) -> None:
        """Test that a LessOrEqualToZeroError is raised when a zero value is passed for N_R."""
        n_E = [5, 4, 3]
        N_R = [10, 20, 0]
        with pytest.raises(LessOrEqualToZeroError):
            FormADot1DamageDuringDesignLife(n_E=n_E, N_R=N_R)

    def test_raise_error_if_n_E_is_empty(self) -> None:
        """Test that a EmptyListError is raised when an empty list is passed for n_E."""
        n_E = []
        N_R = [10, 20, 30]
        with pytest.raises(EmptyListError):
            FormADot1DamageDuringDesignLife(n_E=n_E, N_R=N_R)

    def test_raise_error_if_N_R_is_empty(self) -> None:
        """Test that a EmptyListError is raised when an empty list is passed for N_R."""
        n_E = [5, 4, 3]
        N_R = []
        with pytest.raises(EmptyListError):
            FormADot1DamageDuringDesignLife(n_E=n_E, N_R=N_R)

    def test_raise_error_if_n_E_and_N_R_are_different_length(self) -> None:
        """Test that a ListsNotSameLengthError is raised when n_E and N_R are not the same length."""
        n_E = [5, 4]
        N_R = [10, 20, 30]
        with pytest.raises(ListsNotSameLengthError):
            FormADot1DamageDuringDesignLife(n_E=n_E, N_R=N_R)
