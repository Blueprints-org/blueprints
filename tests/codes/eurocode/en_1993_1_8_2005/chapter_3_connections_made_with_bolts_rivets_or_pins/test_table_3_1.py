"""Testing table 3.1 of EN 1993-1-8:2005."""

import pytest

from blueprints.codes.eurocode.en_1993_1_8_2005.chapter_3_connections_made_with_bolts_rivets_or_pins.table_3_1 import (
    FastenerClass,
    Table3Dot1NominalValuesBolts,
)


class TestFastenerClass:
    """Validation of the bolt classes of EN 1993-1-8:2005."""

    def test_the_seven_classes_of_the_standard_are_present(self) -> None:
        """Art.3.1.1(2) names exactly these seven, and a National Annex can only exclude, never add."""
        assert [bolt_class.value for bolt_class in FastenerClass] == ["4.6", "4.8", "5.6", "5.8", "6.8", "8.8", "10.9"]

    @pytest.mark.parametrize(
        ("bolt_class", "expected"),
        [
            (FastenerClass.CLASS_4_6, False),
            (FastenerClass.CLASS_4_8, False),
            (FastenerClass.CLASS_5_6, False),
            (FastenerClass.CLASS_5_8, False),
            (FastenerClass.CLASS_6_8, False),
            (FastenerClass.CLASS_8_8, True),
            (FastenerClass.CLASS_10_9, True),
        ],
    )
    def test_can_be_preloaded(self, bolt_class: FastenerClass, expected: bool) -> None:
        """Art.3.1.2(1) allows only classes 8.8 and 10.9 to be used as preloaded bolts."""
        assert bolt_class.can_be_preloaded is expected


class TestTable3Dot1NominalValuesBolts:
    """Validation for table 3.1 from EN 1993-1-8:2005."""

    @pytest.mark.parametrize(
        ("bolt_class", "f_yb", "f_ub"),
        [
            (FastenerClass.CLASS_4_6, 240, 400),
            (FastenerClass.CLASS_4_8, 320, 400),
            (FastenerClass.CLASS_5_6, 300, 500),
            (FastenerClass.CLASS_5_8, 400, 500),
            (FastenerClass.CLASS_6_8, 480, 600),
            (FastenerClass.CLASS_8_8, 640, 800),
            (FastenerClass.CLASS_10_9, 900, 1000),
        ],
    )
    def test_the_printed_values(self, bolt_class: FastenerClass, f_yb: int, f_ub: int) -> None:
        """Every pair of the printed table, read from the standard."""
        table = Table3Dot1NominalValuesBolts(bolt_class=bolt_class)

        assert table.f_yb == f_yb
        assert table.f_ub == f_ub

    @pytest.mark.parametrize("bolt_class", list(FastenerClass))
    def test_the_values_follow_the_designation(self, bolt_class: FastenerClass) -> None:
        """The designation encodes both strengths, which is a cross-check on the transcribed table.

        For a class written a.b the ultimate strength is a * 100 and the yield strength a * b * 10.
        The table itself stays the source of the values; this only proves none of them was mistyped.
        """
        first, second = (float(part) for part in bolt_class.value.split("."))
        table = Table3Dot1NominalValuesBolts(bolt_class=bolt_class)

        assert table.f_ub == pytest.approx(expected=first * 100)
        assert table.f_yb == pytest.approx(expected=first * second * 10)

    def test_the_label_and_source_document(self) -> None:
        """The table carries its own identification, like the other table implementations."""
        table = Table3Dot1NominalValuesBolts(bolt_class=FastenerClass.CLASS_8_8)

        assert table.label == "Table 3.1"
        assert table.source_document == "EN 1993-1-8:2005"
