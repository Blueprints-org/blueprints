"""Module for timber material properties."""

from dataclasses import dataclass, field
from enum import Enum

from blueprints.codes.eurocode.en_338_2016.chapter_5_classification_of_structural_timber.table_1 import (
    SoftwoodStrengthClassBending,
    Table1StrengthClassesSoftwoodBendingTests,
)
from blueprints.codes.eurocode.en_338_2016.chapter_5_classification_of_structural_timber.table_2 import (
    SoftwoodStrengthClassTension,
    Table2StrengthClassesSoftwoodTensionTests,
)
from blueprints.codes.eurocode.en_338_2016.chapter_5_classification_of_structural_timber.table_3 import (
    HardwoodStrengthClass,
    Table3StrengthClassesHardwoodBendingTests,
)
from blueprints.type_alias import KG_M3, MPA

# Type alias for any timber strength class supported by EN 338:2016 tables 1-3.
type TimberStrengthClass = SoftwoodStrengthClassBending | SoftwoodStrengthClassTension | HardwoodStrengthClass

# Mapping from strength-class enum to the corresponding EN 338:2016 table class.
_TIMBER_TABLE_BY_CLASS_TYPE: dict[
    type,
    type[Table1StrengthClassesSoftwoodBendingTests]
    | type[Table2StrengthClassesSoftwoodTensionTests]
    | type[Table3StrengthClassesHardwoodBendingTests],
] = {
    SoftwoodStrengthClassBending: Table1StrengthClassesSoftwoodBendingTests,
    SoftwoodStrengthClassTension: Table2StrengthClassesSoftwoodTensionTests,
    HardwoodStrengthClass: Table3StrengthClassesHardwoodBendingTests,
}


class DiagramType(Enum):
    """Enumeration of diagram types of stress-strain relations."""

    BI_LINEAR = "Bi-Linear"
    PARABOLIC = "Parabolic"


@dataclass(frozen=True)
class TimberMaterial:
    r"""Representation of the strength and deformation characteristics for timber material.

    Material properties are taken from EN 338:2016 tables 1 (softwood, bending),
    2 (softwood, tension) and 3 (hardwood, bending), depending on the type of
    ``timber_class`` provided.

    Parameters
    ----------
    timber_class: TimberStrengthClass
        Enumeration of timber strength classes (default: C24)
    diagram_type: DiagramType
        Type of stress-strain diagram (default= Bi-Linear)
    quality_class: str
        Quality class of the timber material (default= None)
    custom_name: str
        Use a custom name for the timber material (default= timber class name)
    """

    timber_class: TimberStrengthClass = field(default=SoftwoodStrengthClassBending.C24)
    diagram_type: DiagramType = field(default=DiagramType.BI_LINEAR)
    quality_class: str | None = field(default=None)
    custom_name: str | None = field(default=None, compare=False)

    def __post_init__(self) -> None:
        """Validate that the timber class is a supported EN 338:2016 strength class."""
        if type(self.timber_class) not in _TIMBER_TABLE_BY_CLASS_TYPE:
            raise ValueError(
                f"Invalid timber class: {self.timber_class!r}. Must be one of "
                f"SoftwoodStrengthClassBending, SoftwoodStrengthClassTension or HardwoodStrengthClass."
            )

    @property
    def _table(
        self,
    ) -> Table1StrengthClassesSoftwoodBendingTests | Table2StrengthClassesSoftwoodTensionTests | Table3StrengthClassesHardwoodBendingTests:
        """Return the EN 338:2016 table instance matching the timber class."""
        if isinstance(self.timber_class, SoftwoodStrengthClassBending):
            return Table1StrengthClassesSoftwoodBendingTests(self.timber_class)
        if isinstance(self.timber_class, SoftwoodStrengthClassTension):
            return Table2StrengthClassesSoftwoodTensionTests(self.timber_class)
        # HardwoodStrengthClass
        return Table3StrengthClassesHardwoodBendingTests(self.timber_class)

    @property
    def name(self) -> str:
        """Name of the timber material.

        Returns
        -------
        str
            Example: "C24"
        """
        if self.custom_name:
            return self.custom_name
        return self.timber_class.value

    @property
    def f_m_k(self) -> MPA:
        """Characteristic bending strength [$f_{m,k}$] in $N/mm^2$."""
        return self._table.f_m_k

    @property
    def f_t_0_k(self) -> MPA:
        """Characteristic tension strength parallel to grain [$f_{t,0,k}$] in $N/mm^2$."""
        return self._table.f_t_0_k

    @property
    def f_t_90_k(self) -> MPA:
        """Characteristic tension strength perpendicular to grain [$f_{t,90,k}$] in $N/mm^2$."""
        return self._table.f_t_90_k

    @property
    def f_c_0_k(self) -> MPA:
        """Characteristic compression strength parallel to grain [$f_{c,0,k}$] in $N/mm^2$."""
        return self._table.f_c_0_k

    @property
    def f_c_90_k(self) -> MPA:
        """Characteristic compression strength perpendicular to grain [$f_{c,90,k}$] in $N/mm^2$."""
        return self._table.f_c_90_k

    @property
    def f_v_k(self) -> MPA:
        """Characteristic shear strength [$f_{v,k}$] in $N/mm^2$."""
        return self._table.f_v_k

    @property
    def e_m_0_mean(self) -> MPA:
        """Mean modulus of elasticity parallel to grain [$E_{0,mean}$] in $N/mm^2$."""
        return self._table.e_m_0_mean

    @property
    def e_m_0_k(self) -> MPA:
        """5-percentile modulus of elasticity parallel to grain [$E_{0,05}$] in $N/mm^2$."""
        return self._table.e_m_0_k

    @property
    def e_m_90_mean(self) -> MPA:
        """Mean modulus of elasticity perpendicular to grain [$E_{90,mean}$] in $N/mm^2$."""
        return self._table.e_m_90_mean

    @property
    def g_mean(self) -> MPA:
        """Mean shear modulus [$G_{mean}$] in $N/mm^2$."""
        return self._table.g_mean

    @property
    def rho_k(self) -> KG_M3:
        r"""5-percentile density [$\rho_k$] in $kg/m^3$."""
        return self._table.rho_k

    @property
    def rho_mean(self) -> KG_M3:
        r"""Mean density [$\rho_{mean}$] in $kg/m^3$."""
        return self._table.rho_mean
