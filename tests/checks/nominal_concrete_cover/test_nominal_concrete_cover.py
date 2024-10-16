"""Testing nominal concrete cover check of NEN-EN 1992-1-1."""

import pytest

from blueprints.checks.nominal_concrete_cover.constants.base import NominalConcreteCoverConstantsBase
from blueprints.checks.nominal_concrete_cover.constants.constants_nen_en_1992_1_1_c2_2011 import NominalConcreteCoverConstants2011C2
from blueprints.checks.nominal_concrete_cover.definitions import AbrasionClass, CastingSurface
from blueprints.checks.nominal_concrete_cover.nominal_concrete_cover import NominalConcreteCover
from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011.chapter_4_durability_and_cover.table_4_1 import (
    Carbonation,
    Chemical,
    Chloride,
    ChlorideSeawater,
    FreezeThaw,
    Table4Dot1ExposureClasses,
)
from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011.chapter_4_durability_and_cover.table_4_3 import Table4Dot3ConcreteStructuralClass
from blueprints.codes.eurocode.structural_class import ConcreteStructuralClassBase
from blueprints.materials.concrete import ConcreteMaterial
from blueprints.type_alias import MM

exposure_classes = Table4Dot1ExposureClasses(Carbonation.XC1, Chloride.XD1, ChlorideSeawater.XS1, FreezeThaw.NA, Chemical.NA)
structural_class = Table4Dot3ConcreteStructuralClass(exposure_classes, 50, ConcreteMaterial(), False, False)


class TestNominalConcreteCover:
    """Validation for nominal concrete cover check from NEN-EN 1992-1-1."""

    @pytest.mark.parametrize(
        (
            "reinforcement_diameter",
            "nominal_max_aggregate_size",
            "constants",
            "structural_class",
            "carbonation",
            "chloride",
            "chloride_seawater",
            "delta_c_dur_gamma",
            "delta_c_dur_st",
            "delta_c_dur_add",
            "casting_surface",
            "uneven_surface",
            "abrasion_class",
            "expected",
        ),
        [
            (
                25,
                False,
                NominalConcreteCoverConstants2011C2(),
                structural_class,
                Carbonation.XC1,
                Chloride.XD1,
                ChlorideSeawater.XS1,
                0,
                0,
                0,
                CastingSurface.PERMANENTLY_EXPOSED,
                False,
                AbrasionClass.XM1,
                50,
            ),
            (
                32,
                True,
                NominalConcreteCoverConstants2011C2(),
                6,
                Carbonation.XC3,
                Chloride.XD2,
                ChlorideSeawater.XS2,
                0,
                0,
                0,
                CastingSurface.PREPARED_GROUND,
                False,
                AbrasionClass.XM2,
                70,
            ),
            (
                20,
                False,
                NominalConcreteCoverConstants2011C2(),
                2,
                Carbonation.XC1,
                Chloride.XD3,
                ChlorideSeawater.XS3,
                0,
                0,
                0,
                CastingSurface.DIRECTLY_AGAINST_SOIL,
                False,
                AbrasionClass.XM2,
                80,
            ),
        ],
    )
    def test_evaluation(  # noqa: PLR0913
        self,
        reinforcement_diameter: MM,
        nominal_max_aggregate_size: bool,
        constants: NominalConcreteCoverConstantsBase,
        structural_class: ConcreteStructuralClassBase,
        carbonation: Carbonation,
        chloride: Chloride,
        chloride_seawater: ChlorideSeawater,
        delta_c_dur_gamma: MM,
        delta_c_dur_st: MM,
        delta_c_dur_add: MM,
        casting_surface: CastingSurface,
        uneven_surface: bool,
        abrasion_class: AbrasionClass,
        expected: MM,
    ) -> None:
        """Test the evaluation of the result."""
        nominal_concrete_cover = NominalConcreteCover(
            reinforcement_diameter=reinforcement_diameter,
            nominal_max_aggregate_size=nominal_max_aggregate_size,
            constants=constants,
            structural_class=structural_class,
            carbonation=carbonation,
            chloride=chloride,
            chloride_seawater=chloride_seawater,
            delta_c_dur_gamma=delta_c_dur_gamma,
            delta_c_dur_st=delta_c_dur_st,
            delta_c_dur_add=delta_c_dur_add,
            casting_surface=casting_surface,
            uneven_surface=uneven_surface,
            abrasion_class=abrasion_class,
        ).value()

        assert nominal_concrete_cover == pytest.approx(expected=expected, rel=1e-4)

    @pytest.mark.parametrize(
        "uneven_surface",
        [1, "False", None, 0.5],
    )
    def test_uneven_surface_type_error(
        self,
        uneven_surface: bool,
    ) -> None:
        """Test type error for uneven_surface parameter."""
        with pytest.raises(TypeError, match="Invalid type for uneven_surface: .* Expected type is bool."):
            NominalConcreteCover(
                reinforcement_diameter=25,
                nominal_max_aggregate_size=32,
                constants=NominalConcreteCoverConstants2011C2(),
                structural_class=structural_class,
                carbonation=Carbonation.XC1,
                chloride=Chloride.XD1,
                chloride_seawater=ChlorideSeawater.XS1,
                delta_c_dur_gamma=0,
                delta_c_dur_st=0,
                delta_c_dur_add=0,
                casting_surface=CastingSurface.PERMANENTLY_EXPOSED,
                uneven_surface=uneven_surface,
                abrasion_class=AbrasionClass.XM1,
            )

    @pytest.mark.parametrize(
        "abrasion_class",
        [1, "XM1", None, 0.5],
    )
    def test_abrasion_class_type_error(
        self,
        abrasion_class: AbrasionClass,
    ) -> None:
        """Test type error for abrasion_class parameter."""
        with pytest.raises(TypeError, match="Invalid type for abrasion_class: .* Expected type is AbrasionClass."):
            NominalConcreteCover(
                reinforcement_diameter=25,
                nominal_max_aggregate_size=32,
                constants=NominalConcreteCoverConstants2011C2(),
                structural_class=structural_class,
                carbonation=Carbonation.XC1,
                chloride=Chloride.XD1,
                chloride_seawater=ChlorideSeawater.XS1,
                delta_c_dur_gamma=0,
                delta_c_dur_st=0,
                delta_c_dur_add=0,
                casting_surface=CastingSurface.PERMANENTLY_EXPOSED,
                uneven_surface=False,
                abrasion_class=abrasion_class,
            )

    @pytest.mark.parametrize(
        "casting_surface",
        [1, "PERMANENTLY_EXPOSED", None, 0.5],
    )
    def test_casting_surface_type_error(
        self,
        casting_surface: CastingSurface,
    ) -> None:
        """Test type error for casting_surface parameter."""
        with pytest.raises(TypeError, match="Invalid type for casting_surface: .* Expected type is CastingSurface."):
            NominalConcreteCover(
                reinforcement_diameter=25,
                nominal_max_aggregate_size=32,
                constants=NominalConcreteCoverConstants2011C2(),
                structural_class=structural_class,
                carbonation=Carbonation.XC1,
                chloride=Chloride.XD1,
                chloride_seawater=ChlorideSeawater.XS1,
                delta_c_dur_gamma=0,
                delta_c_dur_st=0,
                delta_c_dur_add=0,
                casting_surface=casting_surface,
                uneven_surface=False,
                abrasion_class=AbrasionClass.XM1,
            )

    def test_latex(self) -> None:
        """Test the latex representation of the formula."""
        nominal_concrete_cover = NominalConcreteCover(
            reinforcement_diameter=25,
            nominal_max_aggregate_size=32,
            constants=NominalConcreteCoverConstants2011C2(),
            structural_class=structural_class,
            carbonation=Carbonation.XC1,
            chloride=Chloride.XD1,
            chloride_seawater=ChlorideSeawater.XS1,
            delta_c_dur_gamma=0,
            delta_c_dur_st=0,
            delta_c_dur_add=0,
            casting_surface=CastingSurface.PERMANENTLY_EXPOSED,
            uneven_surface=False,
            abrasion_class=AbrasionClass.XM1,
        )

        assert nominal_concrete_cover.latex() == r"\(45\, \text{mm}\)"
