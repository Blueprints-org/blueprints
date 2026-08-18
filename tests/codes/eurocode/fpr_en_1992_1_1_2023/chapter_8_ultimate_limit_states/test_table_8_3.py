"""Testing table 8.3 of FprEN 1992-1-1:2023."""

import pytest

from blueprints.codes.eurocode.fpr_en_1992_1_1_2023.chapter_8_ultimate_limit_states.table_8_3 import (
    PunchingSupportType,
    SubTable8Dot3RefinedCoefficientShearForceConcentration,
    Table8Dot3CoefficientsShearForceConcentration,
)
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestPunchingSupportType:
    """Validation for the types of support of table 8.3 from FprEN 1992-1-1:2023."""

    @pytest.mark.parametrize(
        ("support_type", "expected"),
        [
            (PunchingSupportType.INTERNAL_COLUMN, True),
            (PunchingSupportType.EDGE_COLUMN, True),
            (PunchingSupportType.CORNER_COLUMN, True),
            (PunchingSupportType.END_OF_WALL, False),  # the printed cell spans both columns of the table
            (PunchingSupportType.CORNER_OF_WALL, False),  # the printed cell spans both columns of the table
        ],
    )
    def test_has_refined_value(self, support_type: PunchingSupportType, expected: bool) -> None:
        """Tests which rows of the table offer a refined coefficient."""
        assert support_type.has_refined_value is expected


class TestTable8Dot3CoefficientsShearForceConcentration:
    """Validation for table 8.3 from FprEN 1992-1-1:2023."""

    @pytest.mark.parametrize(
        ("support_type", "expected"),
        [
            (PunchingSupportType.INTERNAL_COLUMN, 1.15),
            (PunchingSupportType.EDGE_COLUMN, 1.4),
            (PunchingSupportType.CORNER_COLUMN, 1.5),
            (PunchingSupportType.END_OF_WALL, 1.4),
            (PunchingSupportType.CORNER_OF_WALL, 1.2),
        ],
    )
    def test_beta_e_approximated(self, support_type: PunchingSupportType, expected: float) -> None:
        """Tests the approximated coefficient printed per row of the table."""
        assert Table8Dot3CoefficientsShearForceConcentration(support_type=support_type).beta_e_approximated == pytest.approx(expected, rel=1e-4)

    @pytest.mark.parametrize(
        ("support_type", "e_b_x", "e_b_y", "expected"),
        [
            (PunchingSupportType.INTERNAL_COLUMN, 30.0, 40.0, 50.0),  # sqrt(30^2 + 40^2)
            (PunchingSupportType.EDGE_COLUMN, 30.0, 40.0, 55.0),  # 0.5 * 30 + 40
            (PunchingSupportType.CORNER_COLUMN, 30.0, 40.0, 18.9),  # 0.27 * (30 + 40)
            (PunchingSupportType.INTERNAL_COLUMN, -30.0, -40.0, 50.0),  # the sign of the eccentricities does not matter
            (PunchingSupportType.EDGE_COLUMN, -30.0, -40.0, 55.0),  # the sign of the eccentricities does not matter
            (PunchingSupportType.CORNER_COLUMN, -30.0, -40.0, 18.9),  # the sign of the eccentricities does not matter
        ],
    )
    def test_e_b(self, support_type: PunchingSupportType, e_b_x: float, e_b_y: float, expected: float) -> None:
        """Tests the eccentricity combined according to the type of support."""
        table = Table8Dot3CoefficientsShearForceConcentration(support_type=support_type, e_b_x=e_b_x, e_b_y=e_b_y)

        assert table.e_b == pytest.approx(expected, rel=1e-4)

    @pytest.mark.parametrize(
        ("support_type", "swapped_is_equal"),
        [
            (PunchingSupportType.INTERNAL_COLUMN, True),  # a root of squares, so symmetric in the two directions
            (PunchingSupportType.CORNER_COLUMN, True),  # both absolute values carry the same factor
            (PunchingSupportType.EDGE_COLUMN, False),  # only the component perpendicular to the slab edge is halved
        ],
    )
    def test_e_b_orientation(self, support_type: PunchingSupportType, swapped_is_equal: bool) -> None:
        """Tests that x and y are interchangeable except for an edge column, where x is perpendicular to the slab edge."""
        as_printed = Table8Dot3CoefficientsShearForceConcentration(support_type=support_type, e_b_x=30.0, e_b_y=40.0)
        swapped = Table8Dot3CoefficientsShearForceConcentration(support_type=support_type, e_b_x=40.0, e_b_y=30.0)

        assert (as_printed.e_b == pytest.approx(swapped.e_b, rel=1e-4)) is swapped_is_equal

    def test_e_b_of_an_edge_column_halves_the_eccentricity_across_the_slab_edge(self) -> None:
        """Tests that the factor 0,5 sits on the eccentricity perpendicular to the slab edge, per Figure 8.21 a)."""
        table = Table8Dot3CoefficientsShearForceConcentration(
            support_type=PunchingSupportType.EDGE_COLUMN,
            e_b_x=30.0,
            e_b_y=40.0,
        )

        # Expected result, manually calculated: 0.5 * 30 + 40, and not 30 + 0.5 * 40 = 50
        manually_calculated_result = 55.0  # mm

        assert table.e_b == pytest.approx(manually_calculated_result, rel=1e-4)

    def test_b_b(self) -> None:
        """Tests the geometric mean of the two overall widths of the control perimeter."""
        table = Table8Dot3CoefficientsShearForceConcentration(
            support_type=PunchingSupportType.INTERNAL_COLUMN,
            b_b_min=400.0,
            b_b_max=900.0,
        )

        # Expected result, manually calculated
        manually_calculated_result = 600.0  # mm, sqrt(400 * 900)

        assert table.b_b == pytest.approx(manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("support_type", "expected"),
        [
            # e_b = 50.0 mm and b_b = 600.0 mm, so 1 + 1.1 * 50 / 600 = 1.0916667, above the lower bound
            (PunchingSupportType.INTERNAL_COLUMN, 1.0916667),
            # e_b = 55.0 mm and b_b = 600.0 mm, so 1 + 1.1 * 55 / 600 = 1.1008333, above the lower bound
            (PunchingSupportType.EDGE_COLUMN, 1.1008333),
            # e_b = 18.9 mm and b_b = 600.0 mm, so 1 + 1.1 * 18.9 / 600 = 1.034650, below the lower bound of 1.05
            (PunchingSupportType.CORNER_COLUMN, 1.05),
        ],
    )
    def test_beta_e_refined(self, support_type: PunchingSupportType, expected: float) -> None:
        """Tests the refined coefficient, including the lower bound the table prints."""
        table = Table8Dot3CoefficientsShearForceConcentration(
            support_type=support_type,
            e_b_x=30.0,
            e_b_y=40.0,
            b_b_min=400.0,
            b_b_max=900.0,
        )

        assert table.beta_e_refined == pytest.approx(expected, rel=1e-4)

    def test_beta_e_refined_carries_a_latex_representation(self) -> None:
        """Tests that the refined coefficient is a formula and not a bare float."""
        table = Table8Dot3CoefficientsShearForceConcentration(
            support_type=PunchingSupportType.INTERNAL_COLUMN,
            e_b_x=30.0,
            e_b_y=40.0,
            b_b_min=400.0,
            b_b_max=900.0,
        )

        assert table.beta_e_refined.latex().short == r"\beta_e = 1.092 \ -"

    @pytest.mark.parametrize("support_type", [PunchingSupportType.END_OF_WALL, PunchingSupportType.CORNER_OF_WALL])
    def test_raise_error_when_refined_route_is_asked_for_a_wall(self, support_type: PunchingSupportType) -> None:
        """Test that the two rows without a refined cell reject the refined route."""
        table = Table8Dot3CoefficientsShearForceConcentration(
            support_type=support_type,
            e_b_x=30.0,
            e_b_y=40.0,
            b_b_min=400.0,
            b_b_max=900.0,
        )

        with pytest.raises(ValueError, match="no refined coefficient"):
            _ = table.e_b
        with pytest.raises(ValueError, match="no refined coefficient"):
            _ = table.b_b

    @pytest.mark.parametrize(
        ("e_b_x", "e_b_y"),
        [
            (None, 40.0),  # e_b_x is missing
            (30.0, None),  # e_b_y is missing
        ],
    )
    def test_raise_error_when_an_eccentricity_is_missing(self, e_b_x: float | None, e_b_y: float | None) -> None:
        """Test that the refined route rejects an incomplete pair of eccentricities."""
        table = Table8Dot3CoefficientsShearForceConcentration(
            support_type=PunchingSupportType.INTERNAL_COLUMN,
            e_b_x=e_b_x,
            e_b_y=e_b_y,
        )

        with pytest.raises(ValueError, match="e_b_x and e_b_y"):
            _ = table.e_b

    @pytest.mark.parametrize(
        ("b_b_min", "b_b_max"),
        [
            (None, 900.0),  # b_b_min is missing
            (400.0, None),  # b_b_max is missing
        ],
    )
    def test_raise_error_when_a_width_is_missing(self, b_b_min: float | None, b_b_max: float | None) -> None:
        """Test that the refined route rejects an incomplete pair of widths."""
        table = Table8Dot3CoefficientsShearForceConcentration(
            support_type=PunchingSupportType.INTERNAL_COLUMN,
            b_b_min=b_b_min,
            b_b_max=b_b_max,
        )

        with pytest.raises(ValueError, match="b_b_min and b_b_max"):
            _ = table.b_b

    @pytest.mark.parametrize(
        ("b_b_min", "b_b_max"),
        [
            (-400.0, 900.0),  # b_b_min is negative
            (0.0, 900.0),  # b_b_min is zero
            (400.0, -900.0),  # b_b_max is negative
            (400.0, 0.0),  # b_b_max is zero
        ],
    )
    def test_raise_error_when_a_width_is_invalid(self, b_b_min: float, b_b_max: float) -> None:
        """Test invalid widths."""
        table = Table8Dot3CoefficientsShearForceConcentration(
            support_type=PunchingSupportType.INTERNAL_COLUMN,
            b_b_min=b_b_min,
            b_b_max=b_b_max,
        )

        with pytest.raises(LessOrEqualToZeroError):
            _ = table.b_b


class TestSubTable8Dot3RefinedCoefficientShearForceConcentration:
    """Validation for the refined coefficient of table 8.3 from FprEN 1992-1-1:2023."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        e_b = 50.0
        b_b = 600.0

        # Object to test
        formula = SubTable8Dot3RefinedCoefficientShearForceConcentration(e_b=e_b, b_b=b_b)

        # Expected result, manually calculated
        manually_calculated_result = 1.0916667  # -

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_evaluation_on_the_lower_bound(self) -> None:
        """Tests that the lower bound the table prints governs a small eccentricity."""
        # Object to test
        formula = SubTable8Dot3RefinedCoefficientShearForceConcentration(e_b=10.0, b_b=600.0)

        # Expected result, manually calculated: 1 + 1.1 * 10 / 600 = 1.0183333, below the lower bound of 1.05
        manually_calculated_result = 1.05  # -

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("e_b", "b_b"),
        [
            (-50.0, 600.0),  # e_b is negative
            (50.0, -600.0),  # b_b is negative
            (50.0, 0.0),  # b_b is zero
        ],
    )
    def test_raise_error_when_invalid_values_are_given(self, e_b: float, b_b: float) -> None:
        """Test invalid values."""
        with pytest.raises((NegativeValueError, LessOrEqualToZeroError)):
            SubTable8Dot3RefinedCoefficientShearForceConcentration(e_b=e_b, b_b=b_b)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                (
                    r"\beta_e = \max\left(1 + 1.1 \cdot \frac{e_b}{b_b}, 1.05\right) = "
                    r"\max\left(1 + 1.1 \cdot \frac{50.000}{600.000}, 1.05\right) = 1.092 \ -"
                ),
            ),
            (
                "complete_with_units",
                (
                    r"\beta_e = \max\left(1 + 1.1 \cdot \frac{e_b}{b_b}, 1.05\right) = "
                    r"\max\left(1 + 1.1 \cdot \frac{50.000 \ mm}{600.000 \ mm}, 1.05\right) = 1.092 \ -"
                ),
            ),
            ("short", r"\beta_e = 1.092 \ -"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Object to test
        latex = SubTable8Dot3RefinedCoefficientShearForceConcentration(e_b=50.0, b_b=600.0).latex()

        actual = {
            "complete": latex.complete,
            "complete_with_units": latex.complete_with_units,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."
