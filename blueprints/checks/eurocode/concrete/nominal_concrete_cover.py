r"""Calculation of nominal concrete cover from EN 1992-1-1: Chapter 4 - Durability and cover to reinforcement."""

from dataclasses import dataclass, field
from typing import Literal

from blueprints.checks.check_protocol import CheckProtocol
from blueprints.checks.check_result import CheckResult
from blueprints.codes.eurocode.en_1992_1_1_2004 import EN_1992_1_1_2004
from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_4_durability_and_cover._base_classes.nominal_cover_constants import (
    AbrasionClass,
    CastingSurface,
)
from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_4_durability_and_cover._base_classes.nominal_cover_constants import (
    NominalConcreteCoverConstantsBase as ConstantsBase,
)
from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_4_durability_and_cover._base_classes.structural_class import ConcreteStructuralClassBase
from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_4_durability_and_cover.formula_4_1 import Form4Dot1NominalConcreteCover
from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_4_durability_and_cover.formula_4_2 import Form4Dot2MinimumConcreteCover
from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_4_durability_and_cover.table_4_1 import (
    Carbonation,
    Chemical,
    Chloride,
    ChlorideSeawater,
    FreezeThaw,
    Table4Dot1ExposureClasses,
)
from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_4_durability_and_cover.table_4_2 import Table4Dot2MinimumCoverWithRegardToBond
from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_4_durability_and_cover.table_4_4n import (
    Table4Dot4nMinimumCoverDurabilityReinforcementSteel,
)
from blueprints.codes.latex_formula import latex_max_curly_brackets
from blueprints.type_alias import MM
from blueprints.utils.report import Report


@dataclass(frozen=True)
class NominalConcreteCover(CheckProtocol):
    r"""Class responsible for the calculation of the nominal concrete cover [$c_{nom}$] [$mm$].
    It takes considerations of art.4.4.1.2 and 4.4.1.3 into account.

    Parameters
    ----------
    reinforcement_diameter: MM
        The diameter of the reinforcement [$mm$].
    nominal_max_aggregate_size: MM
        The nominal maximum aggregate size [$mm$].
    constants: ConstantsBase
        The constants for the calculation of the nominal concrete cover.
    structural_class: ConcreteStructuralClassBase | int
        The structural class of the concrete. Either an instance of the ConcreteStructuralClassBase class or an integer.
        Tip: Use the :class:`Table4Dot3ConcreteStructuralClass` class to calculate the structural class.
    carbonation: Carbonation | Literal["XC1", "XC2", "XC3", "XC4", "NA"]
        The classification of corrosion induced by carbonation. Default is "Not applicable".
    chloride: Chloride | Literal["XD1", "XD2", "XD3", "NA"]
        The classification of corrosion induced by chlorides other than by sea water. Default is "Not applicable".
    chloride_seawater: ChlorideSeawater | Literal["XS1", "XS2", "XS3", "NA"]
        The classification of corrosion induced by chlorides from sea water. Default is "Not applicable".
    delta_c_dur_gamma: MM
        [$\Delta c_{dur,\gamma}$] An additional safety requirement based on art. 4.4.1.2 (6) [$mm$].
        The value of [$\Delta c_{dur,\gamma}$] for use in a Country may be found in its National Annex.
        The recommended value is 0 mm. 0 mm is the default value in the formula if not specified otherwise.
    delta_c_dur_st: MM
        [$\Delta c_{dur,st}$] A reduction of minimum concrete cover when using stainless steel based on art. 4.4.1.2 (7) [$mm$].
        The value of [$\Delta c_{dur,st}$] for use in a Country may be found in its National Annex.
        The recommended value, without further specification, is 0 mm. 0 mm is the default value in the formula if not specified otherwise.
    delta_c_dur_add: MM
        [$\Delta c_{dur,add}$] A reduction of minimum concrete cover when using additional protection based on art. 4.4.1.2 (8) [$mm$].
        The value of [$\Delta c_{dur,add}$] for use in a Country may be found in its National Annex.
        The recommended value, without further specification, is 0 mm. 0 mm is the default value in the formula if not specified otherwise.
    casting_surface: CastingSurface
        The casting surface of the concrete according to art. 4.4.1.3 (4).
        The default value is "Permanently exposed".
    uneven_surface: bool
        Is the surface uneven according to art. 4.4.1.2 (11)?
        The default value is False.
    abrasion_class: AbrasionClass
        The abrasion class of the concrete surface according to art. 4.4.1.2 (13).
        The default value is "Not applicable".
    """

    name = "Nominal concrete cover according to art. 4.4.1"

    reinforcement_diameter: MM
    nominal_max_aggregate_size: MM
    constants: ConstantsBase
    structural_class: ConcreteStructuralClassBase | int
    carbonation: Carbonation | Literal["XC1", "XC2", "XC3", "XC4", "NA"] = field(default_factory=lambda: Carbonation.NA)
    chloride: Chloride | Literal["XD1", "XD2", "XD3", "NA"] = field(default_factory=lambda: Chloride.NA)
    chloride_seawater: ChlorideSeawater | Literal["XS1", "XS2", "XS3", "NA"] = field(default_factory=lambda: ChlorideSeawater.NA)
    delta_c_dur_gamma: MM = field(default=0)
    delta_c_dur_st: MM = field(default=0)
    delta_c_dur_add: MM = field(default=0)
    casting_surface: CastingSurface = field(default=CastingSurface.PERMANENTLY_EXPOSED)
    uneven_surface: bool = field(default=False)
    abrasion_class: AbrasionClass = field(default=AbrasionClass.NA)

    def __post_init__(self) -> None:
        """Check the input parameters for validity."""
        if not isinstance(self.uneven_surface, bool):
            raise TypeError(f"Invalid type for uneven_surface: {type(self.uneven_surface)}. Expected type is bool.")

        if not isinstance(self.abrasion_class, AbrasionClass):
            raise TypeError(f"Invalid type for abrasion_class: {type(self.abrasion_class)}. Expected type is AbrasionClass.")

        if not isinstance(self.casting_surface, CastingSurface):
            raise TypeError(f"Invalid type for casting_surface: {type(self.casting_surface)}. Expected type is CastingSurface.")

        if isinstance(self.carbonation, str):
            object.__setattr__(self, "carbonation", Carbonation[self.carbonation.upper()])
        if isinstance(self.chloride, str):
            object.__setattr__(self, "chloride", Chloride[self.chloride.upper()])
        if isinstance(self.chloride_seawater, str):
            object.__setattr__(self, "chloride_seawater", ChlorideSeawater[self.chloride_seawater.upper()])

    def exposure_classes(self) -> Table4Dot1ExposureClasses:
        """Exposure classes according to table 4.1 from EN 1992-1-1."""
        return Table4Dot1ExposureClasses(self.carbonation, self.chloride, self.chloride_seawater, FreezeThaw.NA, Chemical.NA)  # type: ignore[arg-type]

    def c_min_b(self) -> Table4Dot2MinimumCoverWithRegardToBond:
        """Minimum concrete cover with regard to bond according to table 4.2 from EN 1992-1-1."""
        return Table4Dot2MinimumCoverWithRegardToBond(self.reinforcement_diameter, self.nominal_max_aggregate_size > 32)

    def c_min_dur(self) -> Table4Dot4nMinimumCoverDurabilityReinforcementSteel:
        """Minimum concrete cover with regard to durability according to table 4.4N from EN 1992-1-1."""
        return Table4Dot4nMinimumCoverDurabilityReinforcementSteel(self.exposure_classes(), self.structural_class)  # type: ignore[arg-type]

    def c_min(self) -> Form4Dot2MinimumConcreteCover:
        """Minimum concrete cover according to formula 4.2 from EN 1992-1-1."""
        return Form4Dot2MinimumConcreteCover(
            c_min_b=self.c_min_b(),
            c_min_dur=self.c_min_dur(),
            delta_c_dur_gamma=self.delta_c_dur_gamma,
            delta_c_dur_st=self.delta_c_dur_st,
            delta_c_dur_add=self.delta_c_dur_add,
        )

    def cover_increase_for_uneven_surface(self) -> MM:
        """Calculate the increase of the concrete cover for uneven surface according to art. 4.4.1.2 (11)."""
        return self.constants.COVER_INCREASE_FOR_UNEVEN_SURFACE * self.uneven_surface

    def cover_increase_for_abrasion_class(self) -> MM:
        """Calculate the increase of the concrete cover for abrasion class according to art. 4.4.1.2 (13)."""
        return self.constants.COVER_INCREASE_FOR_ABRASION_CLASS[self.abrasion_class]

    def c_min_total(self) -> MM:
        """Total minimum concrete cover according to art. 4.4.1.2 (11) and (13) from EN 1992-1-1."""
        c_min = self.c_min()
        # According to art. 4.4.1.2 (11) from EN 1992-1-1
        c_min += self.cover_increase_for_uneven_surface()  # type: ignore[assignment]
        # According to art. 4.4.1.2 (13) from EN 1992-1-1
        c_min += self.cover_increase_for_abrasion_class()  # type: ignore[assignment]
        return c_min

    def c_nom(self) -> Form4Dot1NominalConcreteCover:
        """Nominal concrete cover according to art. 4.4.1 from EN 1992-1-1."""
        return Form4Dot1NominalConcreteCover(c_min=self.c_min_total(), delta_c_dev=self.constants.DEFAULT_DELTA_C_DEV)

    def minimum_cover_with_regard_to_casting_surface(self) -> MM:
        """Calculate the minimum cover with regard to casting surface according to art. 4.4.1.3 (4) from EN 1992-1-1."""
        return self.constants.minimum_cover_with_regard_to_casting_surface(self.c_min_dur(), self.casting_surface)

    def value(self) -> MM:
        """Get the value of the nominal concrete cover."""
        return max(
            self.c_nom(),
            self.minimum_cover_with_regard_to_casting_surface(),
        )

    def latex(self, n: int = 1) -> str:
        """Returns the lateX string representation for Nominal concrete cover check."""
        return str(self.report(n=n).to_latex())

    def __str__(self) -> str:
        """Return the string representation of the nominal concrete cover."""
        return rf"{self.name} = {self.value()} \ mm"

    @staticmethod
    def source_docs() -> list[str]:
        """The source documents for this check.

        Returns
        -------
        list[str]
            List of source document identifiers
        """
        return [EN_1992_1_1_2004]

    def subchecks(self) -> dict[str, CheckProtocol]:
        """There are no sub-checks for the NominalConcreteCover check as it is intended to be used as a
        sub-check in a larger durability check according to art. 4.4.1 from EN 1992-1-1.

        Returns
        -------
        dict[str, CheckProtocol]
            Empty dictionary as there are no sub-checks for this check.
        """
        return {}

    def result(self) -> CheckResult:
        """Execute check and return standardized result.

        This is the primary public API method. Call this to execute your
        structural check and get a pass/fail result in a standardized format.

        Returns
        -------
        CheckResult
            Standardized Blueprints result object.
        """
        raise NotImplementedError(
            "The result method is not implemented for the NominalConcreteCover check. "
            "This check is intended to be used as a sub-check in a larger durability check according to art. 4.4.1 from EN 1992-1-1."
        )

    def report(self, n: int = 2) -> Report:
        """Generate formatted report of check results.

        Produces human-readable reports in various formats for documentation.

        Parameters
        ----------
        n : int, optional
            Number of decimal places for numerical values in the report (default is 2).

        Returns
        -------
        Report
            Formatted report on the nominal concrete cover calculation, including
            minimum cover requirements, durability considerations, and the governing value.
        """
        report = Report(f"Nominal concrete cover according to art. 4.4.1 from {self.constants.CODE_PREFIX}EN 1992-1-1{self.constants.CODE_SUFFIX}")

        # Minimum cover with regard to bond
        report.add_paragraph("Minimum concrete cover with regard to bond according to table 4.2:")
        report.add_formula(self.c_min_b(), n=n)
        report.add_newline(n=2)

        # Minimum cover with regard to durability
        report.add_paragraph("Minimum concrete cover with regard to durability according to table 4.4N:")
        report.add_formula(self.c_min_dur(), n=n)
        report.add_newline(n=2)

        # Minimum concrete cover
        report.add_paragraph("Minimum concrete cover according to formula 4.2:")
        report.add_formula(self.c_min(), n=n)
        report.add_newline(n=2)

        # Total minimum concrete cover with additional requirements
        report.add_paragraph("Total minimum concrete cover including adjustments for uneven surface and abrasion class (art. 4.4.1.2 (11) and (13)):")
        report.add_equation(
            r"c_{min,total} = c_{min} + \Delta c_{uneven\ surface} + \Delta c_{abrasion\ class} = "
            rf"{self.c_min():.{n}f} + {self.cover_increase_for_uneven_surface():.{n}f} + "
            rf"{self.cover_increase_for_abrasion_class():.{n}f} = {self.c_min_total():.{n}f} \ mm"
        )
        report.add_newline(n=2)

        # Nominal concrete cover
        report.add_paragraph("Nominal concrete cover according to formula 4.1:")
        report.add_formula(self.c_nom(), n=n)
        report.add_newline(n=2)

        # Minimum cover with regard to casting surface
        report.add_paragraph(
            text=f"Minimum cover with regard to casting surface according to art. 4.4.1.3 (4): "
            f"{self.minimum_cover_with_regard_to_casting_surface():.{n}f} mm"
        )
        report.add_newline(n=2)

        # Governing value
        report.add_paragraph(text="Governing nominal concrete cover:", bold=True)
        report.add_equation(
            rf"c_{{nom}} = {latex_max_curly_brackets(f'{float(self.c_nom()):.{n}f}', f'{self.minimum_cover_with_regard_to_casting_surface():.{n}f}')}"
            rf" = {self.value():.{n}f} \ mm"
        )

        return report
