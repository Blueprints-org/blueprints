"""Test Timber material from EN 338:2016."""

import pytest

from blueprints.codes.eurocode.en_338_2016.chapter_5_classification_of_structural_timber.table_1 import SoftwoodStrengthClassBending
from blueprints.codes.eurocode.en_338_2016.chapter_5_classification_of_structural_timber.table_2 import SoftwoodStrengthClassTension
from blueprints.codes.eurocode.en_338_2016.chapter_5_classification_of_structural_timber.table_3 import HardwoodStrengthClass
from blueprints.materials.timber import DiagramType, TimberMaterial


class TestTimberMaterial:
    """Test class for the timber material object."""

    def test_default_name(self) -> None:
        """Tests the default name."""
        timber = TimberMaterial()
        assert timber.name == "C24"

    def test_custom_name(self) -> None:
        """Tests the custom name."""
        timber = TimberMaterial(custom_name="Custom Timber")
        assert timber.name == "Custom Timber"

    def test_softwood_bending_class_c24_properties(self) -> None:
        """Tests properties for softwood bending class C24."""
        timber = TimberMaterial(timber_class=SoftwoodStrengthClassBending.C24)
        assert timber.name == "C24"
        assert timber.f_m_k == 24
        assert timber.f_t_0_k == 14.5
        assert timber.f_t_90_k == 0.4
        assert timber.f_c_0_k == 21
        assert timber.f_c_90_k == 2.5
        assert timber.f_v_k == 4.0
        assert timber.e_m_0_mean == 11000.0
        assert timber.e_m_0_k == 7400.0
        assert timber.e_m_90_mean == 370.0
        assert timber.g_mean == 690.0
        assert timber.rho_k == 350
        assert timber.rho_mean == 420

    def test_hardwood_class_d40_properties(self) -> None:
        """Tests properties for hardwood class D40."""
        timber = TimberMaterial(timber_class=HardwoodStrengthClass.D40)
        assert timber.name == "D40"
        assert timber.f_m_k == 40
        assert timber.f_t_0_k == 24
        assert timber.f_t_90_k == 0.6
        assert timber.f_c_0_k == 30
        assert timber.f_c_90_k == 4.8
        assert timber.f_v_k == 5.0
        assert timber.e_m_0_mean == 16000.0
        assert timber.e_m_0_k == 12000.0
        assert timber.e_m_90_mean == 630.0
        assert timber.g_mean == 590.0
        assert timber.rho_k == 475
        assert timber.rho_mean == 570

    def test_softwood_tension_class_t14_properties(self) -> None:
        """Tests properties for softwood tension class T14."""
        timber = TimberMaterial(timber_class=SoftwoodStrengthClassTension.T14)
        assert timber.name == "T14"
        assert timber.f_m_k == 20.5
        assert timber.f_t_0_k == 14
        assert timber.f_t_90_k == 0.4
        assert timber.f_c_0_k == 16
        assert timber.f_c_90_k == 2.0
        assert timber.f_v_k == 2.8
        assert timber.e_m_0_mean == 11000.0
        assert timber.e_m_0_k == 7400.0
        assert timber.e_m_90_mean == 370.0
        assert timber.g_mean == 690.0
        assert timber.rho_k == 350
        assert timber.rho_mean == 420

    def test_diagram_type_default(self) -> None:
        """Tests the default diagram type."""
        timber = TimberMaterial()
        assert timber.diagram_type == DiagramType.BI_LINEAR

    def test_diagram_type_custom(self) -> None:
        """Tests the custom diagram type."""
        timber = TimberMaterial(diagram_type=DiagramType.PARABOLIC)
        assert timber.diagram_type == DiagramType.PARABOLIC

    def test_eq_with_different_name(self) -> None:
        """Test equality with different name."""
        timber1 = TimberMaterial(timber_class=SoftwoodStrengthClassBending.C24)
        timber2 = TimberMaterial(timber_class=SoftwoodStrengthClassBending.C24, custom_name="Custom Name")
        assert timber1 == timber2

    def test_inequality_with_different_timber_class(self) -> None:
        """Test inequality with different timber class."""
        timber1 = TimberMaterial(timber_class=SoftwoodStrengthClassBending.C24)
        timber2 = TimberMaterial(timber_class=SoftwoodStrengthClassBending.C30)
        assert timber1 != timber2

    def test_invalid_timber_class(self) -> None:
        """Test invalid timber class raises ValueError."""
        with pytest.raises(ValueError) as excinfo:
            TimberMaterial(timber_class="INVALID_CLASS")  # type: ignore[arg-type]
        assert "Invalid timber class" in str(excinfo.value)

    def test_quality_class(self) -> None:
        """Test quality class parameter."""
        timber = TimberMaterial(quality_class="GL24h")
        assert timber.quality_class == "GL24h"

    def test_different_softwood_classes(self) -> None:
        """Test different softwood bending classes."""
        c14 = TimberMaterial(timber_class=SoftwoodStrengthClassBending.C14)
        c50 = TimberMaterial(timber_class=SoftwoodStrengthClassBending.C50)
        assert c14.f_m_k == 14
        assert c50.f_m_k == 50
        assert c14.rho_mean == 350
        assert c50.rho_mean == 520
