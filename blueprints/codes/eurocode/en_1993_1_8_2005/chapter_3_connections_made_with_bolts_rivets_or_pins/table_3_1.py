"""Table 3.1 from EN 1993-1-8:2005: Chapter 3 - Connections made with bolts, rivets or pins."""

from dataclasses import dataclass, field
from enum import StrEnum
from typing import ClassVar

from blueprints.codes.eurocode.en_1993_1_8_2005 import EN_1993_1_8_2005
from blueprints.type_alias import MPA


class BoltClass(StrEnum):
    """Bolt classes for which the rules of EN 1993-1-8:2005 are valid, art.3.1.1(2).

    Art.3.1.1(3) gives the yield strength and the ultimate tensile strength of each of them in Table
    3.1, to be used as characteristic values. The note under that table says a National Annex may
    exclude certain classes; it does not add any, so this list is closed.
    """

    CLASS_4_6 = "4.6"
    CLASS_4_8 = "4.8"
    CLASS_5_6 = "5.6"
    CLASS_5_8 = "5.8"
    CLASS_6_8 = "6.8"
    CLASS_8_8 = "8.8"
    CLASS_10_9 = "10.9"

    @property
    def can_be_preloaded(self) -> bool:
        """Whether the class may be used as a preloaded bolt.

        Art.3.1.2(1) allows only classes 8.8 and 10.9 to be used as preloaded bolts, and only where
        they conform to the reference standards for high strength structural bolting.

        Returns
        -------
        bool
            True for classes 8.8 and 10.9, False for the remaining classes.
        """
        return self in {BoltClass.CLASS_8_8, BoltClass.CLASS_10_9}


@dataclass(frozen=True)
class Table3Dot1NominalValuesBolts:
    """Implementation of table 3.1 from EN 1993-1-8:2005.

    Nominal values of the yield strength [$f_{yb}$] and the ultimate tensile strength [$f_{ub}$] for
    bolts. Art.3.1.1(3) says these are to be used as characteristic values in design calculations.

    The two values of every class follow the designation, [$f_{ub}$] being the first number times 100
    and [$f_{yb}$] the product of both numbers times 10, but the printed values are held here rather
    than derived from the name, so that the table stays the single source and a mistyped class cannot
    silently produce a strength.

    Parameters
    ----------
    bolt_class : BoltClass
        The bolt class according to art.3.1.1(2).

    Methods
    -------
    f_yb : MPA
        Returns the nominal yield strength in N/mm2.
    f_ub : MPA
        Returns the nominal ultimate tensile strength in N/mm2.

    Examples
    --------
    >>> table = Table3Dot1NominalValuesBolts(BoltClass.CLASS_8_8)
    >>> table.f_yb
    640
    >>> table.f_ub
    800
    """

    bolt_class: BoltClass
    label: str = field(init=False, default="Table 3.1")
    source_document: str = field(init=False, default=EN_1993_1_8_2005)

    # Per bolt class the yield strength first and the ultimate tensile strength second, both in MPa.
    _strength_data: ClassVar[dict[BoltClass, tuple[int, int]]] = {
        BoltClass.CLASS_4_6: (240, 400),
        BoltClass.CLASS_4_8: (320, 400),
        BoltClass.CLASS_5_6: (300, 500),
        BoltClass.CLASS_5_8: (400, 500),
        BoltClass.CLASS_6_8: (480, 600),
        BoltClass.CLASS_8_8: (640, 800),
        BoltClass.CLASS_10_9: (900, 1000),
    }

    @property
    def f_yb(self) -> MPA:
        """[$f_{yb}$] Nominal yield strength of the bolt [$MPa$].

        Returns
        -------
        MPA
            The yield strength printed in Table 3.1 for this class.
        """
        return self._strength_data[self.bolt_class][0]

    @property
    def f_ub(self) -> MPA:
        """[$f_{ub}$] Nominal ultimate tensile strength of the bolt [$MPa$].

        Returns
        -------
        MPA
            The ultimate tensile strength printed in Table 3.1 for this class.
        """
        return self._strength_data[self.bolt_class][1]
