"""Tests for Table3StrengthClassesHardwoodBendingTests class."""

import pytest

from blueprints.codes.eurocode.en_338_2016.chapter_5_classification_of_structural_timber.table_3 import (
    HardwoodStrengthClass,
    Table3StrengthClassesHardwoodBendingTests,
)
from blueprints.type_alias import KG_M3, MPA


class TestTable3StrengthClassesHardwoodBendingTests:
    """Tests for the Table3StrengthClassesHardwoodBendingTests class."""

    def test_valid_initialization(self) -> None:
        """Test that valid parameters create the instance successfully."""
        # Test with a common hardwood strength class
        table = Table3StrengthClassesHardwoodBendingTests(HardwoodStrengthClass.D40)
        assert table.timber_class == HardwoodStrengthClass.D40

    def test_invalid_timber_class(self) -> None:
        """Test that an invalid hardwood class raises ValueError."""

        # Creating a mock hardwood class that doesn't exist in the data
        class MockHardwoodClass:
            pass

        with pytest.raises(ValueError) as excinfo:
            Table3StrengthClassesHardwoodBendingTests(MockHardwoodClass())  # type: ignore[arg-type]

        assert "Invalid hardwood class" in str(excinfo.value)

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
            (HardwoodStrengthClass.D18, 18, 11, 0.6, 18, 4.8, 3.5, 9500.0, 8000.0, 630.0, 590.0, 475, 570),
            (HardwoodStrengthClass.D80, 80, 48, 0.6, 38, 13.5, 5.0, 24000.0, 20200.0, 1600.0, 1500.0, 900, 1080),
        ],
    )
    def test_timber_strength_values(  # noqa: PLR0913
        self,
        timber_class: HardwoodStrengthClass,
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
        table = Table3StrengthClassesHardwoodBendingTests(timber_class)
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
        table = Table3StrengthClassesHardwoodBendingTests(HardwoodStrengthClass.D40)
        expected_str = "D40, f_m,k=40 N/mm², E_0,mean=13000.0 N/mm², rho_mean=660 kg/m³"
        assert str(table) == expected_str
