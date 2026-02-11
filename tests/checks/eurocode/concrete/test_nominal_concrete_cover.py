"""Testing nominal concrete cover check of EN 1992-1-1."""

import pytest

from blueprints.checks.eurocode.concrete.nominal_concrete_cover import NominalConcreteCover
from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_4_durability_and_cover._base_classes.nominal_cover_constants import (
    AbrasionClass,
    CastingSurface,
    NominalConcreteCoverConstantsBase,
)
from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_4_durability_and_cover._base_classes.structural_class import ConcreteStructuralClassBase
from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_4_durability_and_cover.constants import NominalConcreteCoverConstants
from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_4_durability_and_cover.table_4_1 import (
    Carbonation,
    Chemical,
    Chloride,
    ChlorideSeawater,
    FreezeThaw,
    Table4Dot1ExposureClasses,
)
from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_4_durability_and_cover.table_4_3 import Table4Dot3ConcreteStructuralClass
from blueprints.materials.concrete import ConcreteMaterial
from blueprints.type_alias import MM

exposure_classes = Table4Dot1ExposureClasses(Carbonation.XC1, Chloride.XD1, ChlorideSeawater.XS1, FreezeThaw.NA, Chemical.NA)
structural_class = Table4Dot3ConcreteStructuralClass(exposure_classes, 50, ConcreteMaterial(), False, False)


class TestNominalConcreteCover:
    """Validation for nominal concrete cover check from EN 1992-1-1."""

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
                NominalConcreteCoverConstants(),
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
                25,
                False,
                NominalConcreteCoverConstants(),
                structural_class,
                "XC1",
                "XD1",
                "XS1",
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
                NominalConcreteCoverConstants(),
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
                90,
            ),
            (
                20,
                False,
                NominalConcreteCoverConstants(),
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
                105,
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
        with pytest.raises(TypeError, match=r"Invalid type for uneven_surface: .* Expected type is bool."):
            NominalConcreteCover(
                reinforcement_diameter=25,
                nominal_max_aggregate_size=32,
                constants=NominalConcreteCoverConstants(),
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
        with pytest.raises(TypeError, match=r"Invalid type for abrasion_class: .* Expected type is AbrasionClass."):
            NominalConcreteCover(
                reinforcement_diameter=25,
                nominal_max_aggregate_size=32,
                constants=NominalConcreteCoverConstants(),
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
        with pytest.raises(TypeError, match=r"Invalid type for casting_surface: .* Expected type is CastingSurface."):
            NominalConcreteCover(
                reinforcement_diameter=25,
                nominal_max_aggregate_size=32,
                constants=NominalConcreteCoverConstants(),
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

    def test_latex_representation(self) -> None:
        """Test the latex representation of the formula."""
        nominal_concrete_cover = NominalConcreteCover(
            reinforcement_diameter=25,
            nominal_max_aggregate_size=40,
            constants=NominalConcreteCoverConstants(),
            structural_class=structural_class,
            carbonation=Carbonation.XC1,
            chloride=Chloride.XD1,
            chloride_seawater=ChlorideSeawater.XS1,
            delta_c_dur_gamma=0,
            delta_c_dur_st=0,
            delta_c_dur_add=0,
            casting_surface=CastingSurface.DIRECTLY_AGAINST_SOIL,
            uneven_surface=True,
            abrasion_class=AbrasionClass.XM1,
        )

        assert (
            nominal_concrete_cover.latex() == r"\text{Nominal concrete cover according to art. 4.4.1 from EN 1992-1-1:2004:}\newline "
            r"\text{max(Nominal concrete cover according to art. 4.4.1 } (c_{nom}) "
            r"\text{, Minimum cover with regard to casting surface according to art. 4.4.1.3 (4) ) } \newline"
            r"= \max \left\{55.0; 110.0\right\} = 110.0 mm\newline \newline "
            r"\text{Where:}\newline "
            r"c_{nom} = c_{min,total}+\Delta c_{dev} = 45.0+10 = 55.0 mm\newline "
            r"\Delta c_{dev} \text{ is determined according to art. 4.4.1.3 (1)}\newline "
            r"c_{min,total} = c_{min} + \Delta c_{uneven surface}  + \Delta c_{abrasion class} = 35.0 + 5 + 5 = 45.0 mm\newline "
            r"\Delta c_{uneven surface} \text{ and } \Delta c_{abrasion class} "
            r"\text{ are determined according to art. 4.4.1.2 (11) and (13)}\newline "
            r"c_{min} = \max \left\{c_{min,b}; c_{min,dur}+\Delta c_{dur,\gamma}-\Delta c_{dur,st}-\Delta c_{dur,add}; 10 \ mm\right\} \newline "
            r"= \max \left\{30.0; 35.0+0-0-0; 10\right\} = 35.0 mm\newline "
            r"\Delta c_{dur,\gamma} , \Delta c_{dur,st} \text{ and } \Delta c_{dur,add} "
            r"\text{ are determined according to art. 4.4.1.2 (6), (7) and (8)}\newline "
            r"c_{min,b} \text{ is determined according to table 4.2 based on (equivalent) rebar diameter + 5} = 25 + 5 = 30 mm\newline "
            r"c_{min,dur} \text{ is determined according to table 4.4 based on structural class S4 & "
            r"exposure classes (XC1, XD1, XS1)} = 35 mm\newline "
            r"\text{Minimum cover with regard to casting surface according to art. 4.4.1.3 (4) = }k2 \ge c_{min,dur} "
            r"+ 75 mm for Directly against soil\newline "
        )

        assert str(nominal_concrete_cover) == r"Nominal concrete cover according to art. 4.4.1 = 110.0 \ mm"

    def test_source_docs(self) -> None:
        """Test the source_docs method returns the expected list."""
        nominal_concrete_cover = NominalConcreteCover(
            reinforcement_diameter=25,
            nominal_max_aggregate_size=32,
            constants=NominalConcreteCoverConstants(),
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

        assert nominal_concrete_cover.source_docs() == ["EN 1992-1-1"]

    def test_result_not_implemented(self) -> None:
        """Test the result method raises NotImplementedError."""
        nominal_concrete_cover = NominalConcreteCover(
            reinforcement_diameter=25,
            nominal_max_aggregate_size=32,
            constants=NominalConcreteCoverConstants(),
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

        with pytest.raises(
            NotImplementedError,
            match=r"The result method is not implemented for the NominalConcreteCover check\. "
            r"This check is intended to be used as a sub-check in a larger durability check according to art\. 4\.4\.1 from EN 1992-1-1\.",
        ):
            nominal_concrete_cover.result()

    def test_report_not_implemented(self) -> None:
        """Test the report method raises NotImplementedError."""
        nominal_concrete_cover = NominalConcreteCover(
            reinforcement_diameter=25,
            nominal_max_aggregate_size=32,
            constants=NominalConcreteCoverConstants(),
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

        with pytest.raises(
            NotImplementedError,
            match=r"The report method is not implemented for the NominalConcreteCover check\. "
            r"This check is intended to be used as a sub-check in a larger durability check according to art\. 4\.4\.1 from EN 1992-1-1\.",
        ):
            nominal_concrete_cover.report(n=2)
