"""Tests for Table1StrengthClassesSoftwoodBendingTests class."""

import pytest

from blueprints.codes.eurocode.en_338_2016.chapter_5_classification_of_structural_timber.table_1 import (
    SoftwoodStrengthClassBending,
    Table1StrengthClassesSoftwoodBendingTests,
)
from blueprints.type_alias import KG_M3, MPA


class TestTable1StrengthClassesSoftwoodBendingTests:
    """Tests for the Table1StrengthClassesSoftwoodBendingTests class."""

    def test_valid_initialization(self) -> None:
        """Test that valid parameters create the instance successfully."""
        # Test with a common softwood bending strength class
        table = Table1StrengthClassesSoftwoodBendingTests(SoftwoodStrengthClassBending.C24)
        assert table.timber_class == SoftwoodStrengthClassBending.C24

    def test_invalid_timber_class(self) -> None:
        """Test that an invalid timber class raises ValueError."""

        # Creating a mock timber class that doesn't exist in the data
        class MockTimberClass:
            pass

        with pytest.raises(ValueError) as excinfo:
            Table1StrengthClassesSoftwoodBendingTests(MockTimberClass())  # type: ignore[arg-type]

        assert "Invalid timber class" in str(excinfo.value)

    @pytest.mark.parametrize(
        (
            "timber_class",
            "expected_f_m_k",
            "expected_f_t_0_k",
            "expected_f_t_90_k",
            "expected_f_c_0_k",
            "expected_f_c_90_k",
            "expected_f_v_k",
            "expected_e_m_0_mean",
            "expected_e_m_0_k",
            "expected_e_m_90_mean",
            "expected_g_mean",
            "expected_rho_k",
            "expected_rho_mean",
        ),
        [
            (SoftwoodStrengthClassBending.C14, 14, 7.2, 0.4, 16, 2.0, 3.0, 7000.0, 4700.0, 230.0, 440.0, 290, 350),
            (SoftwoodStrengthClassBending.C50, 50, 33.5, 0.4, 30, 3.0, 4.0, 16000.0, 10700.0, 530.0, 1000.0, 430, 520),
        ],
    )
    def test_timber_strength_values(  # noqa: PLR0913
        self,
        timber_class: SoftwoodStrengthClassBending,
        expected_f_m_k: MPA,
        expected_f_t_0_k: MPA,
        expected_f_t_90_k: MPA,
        expected_f_c_0_k: MPA,
        expected_f_c_90_k: MPA,
        expected_f_v_k: MPA,
        expected_e_m_0_mean: MPA,
        expected_e_m_0_k: MPA,
        expected_e_m_90_mean: MPA,
        expected_g_mean: MPA,
        expected_rho_k: KG_M3,
        expected_rho_mean: KG_M3,
    ) -> None:
        """Test that timber strength values match expected values for various classes."""
        table = Table1StrengthClassesSoftwoodBendingTests(timber_class)
        assert table.f_m_k == expected_f_m_k
        assert table.f_t_0_k == expected_f_t_0_k
        assert table.f_t_90_k == expected_f_t_90_k
        assert table.f_c_0_k == expected_f_c_0_k
        assert table.f_c_90_k == expected_f_c_90_k
        assert table.f_v_k == expected_f_v_k
        assert table.e_m_0_mean == expected_e_m_0_mean
        assert table.e_m_0_k == expected_e_m_0_k
        assert table.e_m_90_mean == expected_e_m_90_mean
        assert table.g_mean == expected_g_mean
        assert table.rho_k == expected_rho_k
        assert table.rho_mean == expected_rho_mean

    def test_string_representation(self) -> None:
        """Test that __str__ returns the expected string format."""
        table = Table1StrengthClassesSoftwoodBendingTests(SoftwoodStrengthClassBending.C24)
        expected_str = "C24, f_m,k=24 N/mm², E_0,mean=11000.0 N/mm², rho_mean=420 kg/m³"
        assert str(table) == expected_str
