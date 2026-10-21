"""Testing table 8.2 of FprEN 1992-1-1:2023."""

import pytest

from blueprints.codes.eurocode.fpr_en_1992_1_1_2023.chapter_8_ultimate_limit_states.table_8_2 import (
    SurfaceRoughness,
    Table8Dot2CoefficientsSurfaceRoughness,
)


class TestSurfaceRoughness:
    """Validation for the roughness classes of art. 8.2.6(6)."""

    def test_all_five_classes_of_the_table_are_present(self) -> None:
        """The table prints exactly five rows, so the enumeration is closed."""
        assert [roughness.value for roughness in SurfaceRoughness] == ["very smooth", "smooth", "rough", "very rough", "keyed"]

    @pytest.mark.parametrize(
        ("surface_roughness", "expected_start"),
        [
            (SurfaceRoughness.VERY_SMOOTH, "a surface cast against steel"),
            (SurfaceRoughness.SMOOTH, "a surface with less than 3 mm roughness"),
            (SurfaceRoughness.ROUGH, "a surface with at least 3 mm roughness"),
            (SurfaceRoughness.VERY_ROUGH, "a surface with at least 6 mm roughness"),
            (SurfaceRoughness.KEYED, "a surface with shear keys"),
        ],
    )
    def test_description(self, surface_roughness: SurfaceRoughness, expected_start: str) -> None:
        """Tests the classification printed in art. 8.2.6(6)."""
        assert surface_roughness.description.startswith(expected_start)


class TestTable8Dot2CoefficientsSurfaceRoughness:
    """Validation for table 8.2 from FprEN 1992-1-1:2023."""

    @pytest.mark.parametrize(
        ("surface_roughness", "c_v1", "mu_v", "c_v2", "k_v", "k_dowel"),
        [
            (SurfaceRoughness.VERY_SMOOTH, 0.01, 0.5, 0.0, 0.0, 1.5),
            (SurfaceRoughness.SMOOTH, 0.08, 0.6, 0.0, 0.5, 1.1),
            (SurfaceRoughness.ROUGH, 0.15, 0.7, 0.08, 0.5, 0.9),
            (SurfaceRoughness.VERY_ROUGH, 0.19, 0.9, 0.15, 0.5, 0.9),
            (SurfaceRoughness.KEYED, 0.37, 0.9, None, None, None),
        ],
    )
    def test_printed_coefficients(
        self,
        surface_roughness: SurfaceRoughness,
        c_v1: float,
        mu_v: float,
        c_v2: float | None,
        k_v: float | None,
        k_dowel: float | None,
    ) -> None:
        """Tests every cell of the table as printed."""
        table = Table8Dot2CoefficientsSurfaceRoughness(surface_roughness=surface_roughness)

        assert table.c_v1 == pytest.approx(expected=c_v1)
        assert table.mu_v == pytest.approx(expected=mu_v)
        assert table.c_v2 == (c_v2 if c_v2 is None else pytest.approx(expected=c_v2))
        assert table.k_v == (k_v if k_v is None else pytest.approx(expected=k_v))
        assert table.k_dowel == (k_dowel if k_dowel is None else pytest.approx(expected=k_dowel))

    @pytest.mark.parametrize(
        ("surface_roughness", "c_v1", "c_v2"),
        [
            (SurfaceRoughness.VERY_SMOOTH, 0.0, 0.0),
            (SurfaceRoughness.SMOOTH, 0.0, 0.0),
            (SurfaceRoughness.ROUGH, 0.0, 0.0),
            (SurfaceRoughness.VERY_ROUGH, 0.0, 0.0),
            (SurfaceRoughness.KEYED, 0.37, None),  # the keyed row prints no footnote marker
        ],
    )
    def test_footnote_a_under_perpendicular_tension(self, surface_roughness: SurfaceRoughness, c_v1: float, c_v2: float | None) -> None:
        """Tests footnote a, which zeroes the marked cells when the interface carries perpendicular tension."""
        table = Table8Dot2CoefficientsSurfaceRoughness(surface_roughness=surface_roughness, tension_perpendicular_to_interface=True)

        assert table.c_v1 == pytest.approx(expected=c_v1)
        assert table.c_v2 == (c_v2 if c_v2 is None else pytest.approx(expected=c_v2))

    def test_footnote_a_leaves_the_other_coefficients_alone(self) -> None:
        """Footnote a names only the two cohesion factors, so the remaining coefficients are unaffected."""
        table = Table8Dot2CoefficientsSurfaceRoughness(surface_roughness=SurfaceRoughness.ROUGH, tension_perpendicular_to_interface=True)

        assert table.mu_v == pytest.approx(expected=0.7)
        assert table.k_v == pytest.approx(expected=0.5)
        assert table.k_dowel == pytest.approx(expected=0.9)

    def test_label_and_source_document(self) -> None:
        """Tests the identification of the table."""
        table = Table8Dot2CoefficientsSurfaceRoughness(surface_roughness=SurfaceRoughness.ROUGH)

        assert table.label == "Table 8.2"
        assert table.source_document == "FprEN 1992-1-1:2023"
