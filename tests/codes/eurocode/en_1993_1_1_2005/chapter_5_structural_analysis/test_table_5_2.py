"""Testing table 5.2 of EN 1993-1-1:2005."""

import re
from typing import ClassVar

import pytest

from blueprints.codes.eurocode.en_1993_1_1_2005.chapter_5_structural_analysis.table_5_2 import (
    CrossSectionClass,
    Table5Dot2CompressionPart,
    Table5Dot2LoadingCondition,
    Table5Dot2MaximumWidthToThicknessRatio,
    _LimitSpecification,
)
from blueprints.codes.formula import ComparisonFormula
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestLimitSpecification:
    """Validation of a single criterion of table 5.2."""

    def test_raise_error_if_a_placeholder_is_not_a_declared_parameter(self) -> None:
        """A placeholder that is not declared would survive into the rendered latex."""
        limit_spec = _LimitSpecification(
            params=("c", "t"),
            lhs_fn=lambda c, t, **_: c / t,
            rhs_fn=lambda **_: 72.0,
            lhs_latex=r"\frac{@c@}{@t@}",
            rhs_latex=r"72 \cdot @epsilon@",
        )

        with pytest.raises(ValueError, match=re.escape("use placeholders ['c', 'epsilon', 't'], but the criterion declares")):
            limit_spec._validate_latex_rendering()  # noqa: SLF001

    def test_raise_error_if_a_declared_parameter_has_no_placeholder(self) -> None:
        """A declared parameter that never appears in the templates is a mistake as well."""
        limit_spec = _LimitSpecification(
            params=("c", "t", "epsilon"),
            lhs_fn=lambda c, t, **_: c / t,
            rhs_fn=lambda **_: 72.0,
            lhs_latex=r"\frac{@c@}{@t@}",
            rhs_latex=r"72",
        )

        with pytest.raises(ValueError, match=re.escape("use placeholders ['c', 't'], but the criterion declares")):
            limit_spec._validate_latex_rendering()  # noqa: SLF001

    def test_raise_error_if_a_parameter_has_no_latex_symbol(self) -> None:
        """Every parameter must have a latex symbol to render the symbolic equation with."""
        limit_spec = _LimitSpecification(
            params=("gamma",),
            lhs_fn=lambda gamma, **_: gamma,
            rhs_fn=lambda **_: 1.0,
            lhs_latex=r"@gamma@",
            rhs_latex=r"1",
        )

        with pytest.raises(ValueError, match=re.escape("No latex symbol is defined for gamma.")):
            limit_spec._validate_latex_rendering()  # noqa: SLF001


class TestTable5Dot2MaximumWidthToThicknessRatio:
    """Validation for table 5.2 from EN 1993-1-1:2005."""

    @pytest.mark.parametrize(
        ("cell", "limit_specs"),
        Table5Dot2MaximumWidthToThicknessRatio._ratio_factor_mapping.items(),  # noqa: SLF001
        ids=str,
    )
    def test_every_criterion_of_the_table_is_valid(self, cell: object, limit_specs: tuple[_LimitSpecification, ...]) -> None:
        """Validation is not done on import, so check every cell of the table here instead."""
        assert limit_specs, f"Cell {cell} has no criteria."
        for limit_spec in limit_specs:
            limit_spec._validate_latex_rendering()  # noqa: SLF001

    # (part, cross-section class, loading condition, parameters, expected bool, expected unity check)
    testdata: ClassVar[list[tuple]] = [
        # Internal compression parts
        (
            Table5Dot2CompressionPart.INTERNAL_COMPRESSION_PART,
            CrossSectionClass.CLASS_1,
            Table5Dot2LoadingCondition.SUBJECT_TO_BENDING,
            {"c": 500, "t": 10, "epsilon": 0.81},
            True,
            50 / (72 * 0.81),
        ),
        (
            Table5Dot2CompressionPart.INTERNAL_COMPRESSION_PART,
            CrossSectionClass.CLASS_1,
            Table5Dot2LoadingCondition.SUBJECT_TO_BENDING,
            {"c": 800, "t": 10, "epsilon": 0.81},
            False,
            80 / (72 * 0.81),
        ),
        (
            Table5Dot2CompressionPart.INTERNAL_COMPRESSION_PART,
            CrossSectionClass.CLASS_2,
            Table5Dot2LoadingCondition.SUBJECT_TO_COMPRESSION,
            {"c": 300, "t": 10, "epsilon": 1.0},
            True,
            30 / 38,
        ),
        # alpha > 0.5 branch of the piecewise limit
        (
            Table5Dot2CompressionPart.INTERNAL_COMPRESSION_PART,
            CrossSectionClass.CLASS_1,
            Table5Dot2LoadingCondition.SUBJECT_TO_BENDING_AND_COMPRESSION,
            {"c": 500, "t": 10, "alpha": 0.7, "epsilon": 1.0},
            False,
            50 / (396 / (13 * 0.7 - 1)),
        ),
        # alpha <= 0.5 branch of the piecewise limit
        (
            Table5Dot2CompressionPart.INTERNAL_COMPRESSION_PART,
            CrossSectionClass.CLASS_1,
            Table5Dot2LoadingCondition.SUBJECT_TO_BENDING_AND_COMPRESSION,
            {"c": 500, "t": 10, "alpha": 0.4, "epsilon": 1.0},
            True,
            50 / (36 / 0.4),
        ),
        (
            Table5Dot2CompressionPart.INTERNAL_COMPRESSION_PART,
            CrossSectionClass.CLASS_2,
            Table5Dot2LoadingCondition.SUBJECT_TO_BENDING_AND_COMPRESSION,
            {"c": 500, "t": 10, "alpha": 0.4, "epsilon": 1.0},
            True,
            50 / (41.5 / 0.4),
        ),
        # psi > -1 branch of the piecewise limit
        (
            Table5Dot2CompressionPart.INTERNAL_COMPRESSION_PART,
            CrossSectionClass.CLASS_3,
            Table5Dot2LoadingCondition.SUBJECT_TO_BENDING_AND_COMPRESSION,
            {"c": 500, "t": 10, "psi": -0.5, "epsilon": 1.0},
            True,
            50 / (42 / (0.67 + 0.33 * -0.5)),
        ),
        # psi <= -1 branch of the piecewise limit
        (
            Table5Dot2CompressionPart.INTERNAL_COMPRESSION_PART,
            CrossSectionClass.CLASS_3,
            Table5Dot2LoadingCondition.SUBJECT_TO_BENDING_AND_COMPRESSION,
            {"c": 500, "t": 10, "psi": -2.0, "epsilon": 1.0},
            True,
            50 / (62 * 3 * 2**0.5),
        ),
        # Outstand flanges
        (
            Table5Dot2CompressionPart.OUTSTAND_FLANGE,
            CrossSectionClass.CLASS_1,
            Table5Dot2LoadingCondition.SUBJECT_TO_COMPRESSION,
            {"c": 100, "t": 10, "epsilon": 1.0},
            False,
            10 / 9,
        ),
        (
            Table5Dot2CompressionPart.OUTSTAND_FLANGE,
            CrossSectionClass.CLASS_1,
            Table5Dot2LoadingCondition.SUBJECT_TO_BENDING_AND_COMPRESSION_TIP_IN_TENSION,
            {"c": 500, "t": 10, "alpha": 0.25, "epsilon": 1.0},
            True,
            50 / (9 / (0.25 * 0.25**0.5)),
        ),
        (
            Table5Dot2CompressionPart.OUTSTAND_FLANGE,
            CrossSectionClass.CLASS_2,
            Table5Dot2LoadingCondition.SUBJECT_TO_BENDING_AND_COMPRESSION_TIP_IN_TENSION,
            {"c": 500, "t": 10, "alpha": 0.25, "epsilon": 1.0},
            True,
            50 / (10 / (0.25 * 0.25**0.5)),
        ),
        (
            Table5Dot2CompressionPart.OUTSTAND_FLANGE,
            CrossSectionClass.CLASS_3,
            Table5Dot2LoadingCondition.SUBJECT_TO_BENDING_AND_COMPRESSION_TIP_IN_COMPRESSION,
            {"c": 200, "t": 10, "k_sigma": 4.0, "epsilon": 1.0},
            True,
            20 / 42,
        ),
        # Angles: both criteria satisfied
        (
            Table5Dot2CompressionPart.ANGLE,
            CrossSectionClass.CLASS_3,
            Table5Dot2LoadingCondition.SUBJECT_TO_COMPRESSION,
            {"h": 100, "b": 100, "t": 10, "epsilon": 1.0},
            True,
            10 / 11.5,
        ),
        # Angles: h/t satisfied but (h + b) / 2t not, so the aggregation fails on the maximum
        (
            Table5Dot2CompressionPart.ANGLE,
            CrossSectionClass.CLASS_3,
            Table5Dot2LoadingCondition.SUBJECT_TO_COMPRESSION,
            {"h": 100, "b": 200, "t": 10, "epsilon": 1.0},
            False,
            15 / 11.5,
        ),
        # Tubular sections
        (
            Table5Dot2CompressionPart.TUBULAR_SECTION,
            CrossSectionClass.CLASS_1,
            Table5Dot2LoadingCondition.SUBJECT_TO_COMPRESSION,
            {"d": 400, "t": 10, "epsilon": 1.0},
            True,
            40 / 50,
        ),
        (
            Table5Dot2CompressionPart.TUBULAR_SECTION,
            CrossSectionClass.CLASS_3,
            Table5Dot2LoadingCondition.SUBJECT_TO_COMPRESSION,
            {"d": 1000, "t": 10, "epsilon": 1.0},
            False,
            100 / 90,
        ),
        (
            Table5Dot2CompressionPart.TUBULAR_SECTION,
            CrossSectionClass.CLASS_2,
            Table5Dot2LoadingCondition.SUBJECT_TO_BENDING,
            {"d": 600, "t": 10, "epsilon": 1.0},
            True,
            60 / 70,
        ),
        (
            Table5Dot2CompressionPart.TUBULAR_SECTION,
            CrossSectionClass.CLASS_3,
            Table5Dot2LoadingCondition.SUBJECT_TO_BENDING_AND_COMPRESSION,
            {"d": 1000, "t": 10, "epsilon": 1.0},
            False,
            100 / 90,
        ),
    ]

    @pytest.mark.parametrize(("part", "cross_section_class", "loading_condition", "params", "expected", "unity_check"), testdata)
    def test_evaluation(
        self,
        part: Table5Dot2CompressionPart,
        cross_section_class: CrossSectionClass,
        loading_condition: Table5Dot2LoadingCondition,
        params: dict[str, float],
        expected: bool,
        unity_check: float,
    ) -> None:
        """Test the evaluation of the check and its unity check."""
        form = Table5Dot2MaximumWidthToThicknessRatio(cross_section_class, part, loading_condition, **params)

        assert bool(form) is expected
        assert form.unity_check == pytest.approx(expected=unity_check, rel=1e-4)

    def test_maximum_width_to_thickness_ratio_of_a_single_criterion(self) -> None:
        """A cell holding one criterion returns its limit as a float."""
        form = Table5Dot2MaximumWidthToThicknessRatio(
            CrossSectionClass.CLASS_1,
            Table5Dot2CompressionPart.INTERNAL_COMPRESSION_PART,
            Table5Dot2LoadingCondition.SUBJECT_TO_BENDING,
            c=500,
            t=10,
            epsilon=0.81,
        )

        assert form.maximum_width_to_thickness_ratio == pytest.approx(expected=72 * 0.81, rel=1e-4)

    def test_maximum_width_to_thickness_ratio_of_several_criteria(self) -> None:
        """A cell holding several criteria returns a limit per criterion."""
        form = Table5Dot2MaximumWidthToThicknessRatio(
            CrossSectionClass.CLASS_3,
            Table5Dot2CompressionPart.ANGLE,
            Table5Dot2LoadingCondition.SUBJECT_TO_COMPRESSION,
            h=100,
            b=200,
            t=10,
            epsilon=1.0,
        )

        assert form.maximum_width_to_thickness_ratio == pytest.approx(expected=(15.0, 11.5), rel=1e-4)

    def test_is_a_comparison_formula(self) -> None:
        """An instance of the table is a ComparisonFormula, and so are the checks it aggregates."""
        form = Table5Dot2MaximumWidthToThicknessRatio(
            CrossSectionClass.CLASS_1,
            Table5Dot2CompressionPart.INTERNAL_COMPRESSION_PART,
            Table5Dot2LoadingCondition.SUBJECT_TO_BENDING,
            c=500,
            t=10,
            epsilon=0.81,
        )

        assert isinstance(form, ComparisonFormula)
        assert all(isinstance(check, ComparisonFormula) for check in form.comparison_formulas)

    def test_cross_section_class_accepts_an_int(self) -> None:
        """The cross-section class may be given as a plain integer."""
        params = {"c": 500, "t": 10, "epsilon": 0.81}
        form = Table5Dot2MaximumWidthToThicknessRatio(
            1, Table5Dot2CompressionPart.INTERNAL_COMPRESSION_PART, Table5Dot2LoadingCondition.SUBJECT_TO_BENDING, **params
        )

        assert form.cell.cross_section_class == CrossSectionClass.CLASS_1
        assert bool(form) is True

    def test_name_identifies_the_cell_and_the_criterion(self) -> None:
        """Each check reports which cell of the table it comes from, and which criterion it is."""
        form = Table5Dot2MaximumWidthToThicknessRatio(
            CrossSectionClass.CLASS_3,
            Table5Dot2CompressionPart.ANGLE,
            Table5Dot2LoadingCondition.SUBJECT_TO_COMPRESSION,
            h=100,
            b=200,
            t=10,
            epsilon=1.0,
        )

        assert [check.name for check in form.comparison_formulas] == [
            r"Table 5.2 - Angle, class 3, compression - \frac{h}{t} \le 15 \cdot \epsilon",
            r"Table 5.2 - Angle, class 3, compression - \frac{h + b}{2 \cdot t} \le 11.5 \cdot \epsilon",
        ]

    def test_latex(self) -> None:
        """Test the latex representation of a single check."""
        form = Table5Dot2MaximumWidthToThicknessRatio(
            CrossSectionClass.CLASS_1,
            Table5Dot2CompressionPart.INTERNAL_COMPRESSION_PART,
            Table5Dot2LoadingCondition.SUBJECT_TO_BENDING,
            c=500,
            t=10,
            epsilon=0.81,
        )
        latex = form.latex()

        assert latex.equation == r"\frac{c}{t} \le 72 \cdot \epsilon"
        assert latex.numeric_equation == r"\frac{500.000}{10.000} \le 72 \cdot 0.810"
        assert latex.complete == (r"CHECK \to \frac{c}{t} \le 72 \cdot \epsilon \to \frac{500.000}{10.000} \le 72 \cdot 0.810 \to OK")

    def test_latex_of_the_aggregated_check(self) -> None:
        """The two criteria of an angle are joined into a single latex representation."""
        form = Table5Dot2MaximumWidthToThicknessRatio(
            CrossSectionClass.CLASS_3,
            Table5Dot2CompressionPart.ANGLE,
            Table5Dot2LoadingCondition.SUBJECT_TO_COMPRESSION,
            h=100,
            b=200,
            t=10,
            epsilon=1.0,
        )
        latex = form.latex()

        assert latex.equation == (r"\frac{h}{t} \le 15 \cdot \epsilon\ \&\ \frac{h + b}{2 \cdot t} \le 11.5 \cdot \epsilon")
        assert latex.numeric_equation == (
            r"\frac{100.000}{10.000} \le 15 \cdot 1.000\ \&\ \frac{100.000 + 200.000}{2 \cdot 10.000} \le 11.5 \cdot 1.000"
        )

    def test_latex_parenthesises_negative_values(self) -> None:
        """A negative psi is parenthesised so that it composes with the surrounding latex."""
        form = Table5Dot2MaximumWidthToThicknessRatio(
            CrossSectionClass.CLASS_3,
            Table5Dot2CompressionPart.INTERNAL_COMPRESSION_PART,
            Table5Dot2LoadingCondition.SUBJECT_TO_BENDING_AND_COMPRESSION,
            c=500,
            t=10,
            psi=-0.5,
            epsilon=1.0,
        )
        numeric_equation = form.latex().numeric_equation

        assert r"0.67 + 0.33 \cdot \left(-0.500\right)" in numeric_equation
        assert "--0.500" not in numeric_equation

    def test_raise_error_if_the_combination_is_not_in_the_table(self) -> None:
        """Table 5.2 does not define a limit for every combination."""
        with pytest.raises(ValueError, match=re.escape("Table 5.2 does not define a limit for Angle, class 1, compression.")):
            Table5Dot2MaximumWidthToThicknessRatio(
                CrossSectionClass.CLASS_1,
                Table5Dot2CompressionPart.ANGLE,
                Table5Dot2LoadingCondition.SUBJECT_TO_COMPRESSION,
                h=100,
                b=100,
                t=10,
                epsilon=1.0,
            )

    def test_raise_error_if_a_required_parameter_is_missing(self) -> None:
        """A parameter needed by the selected cell must be provided."""
        with pytest.raises(ValueError, match=re.escape("requires c, t, epsilon; missing: c, t.")):
            Table5Dot2MaximumWidthToThicknessRatio(
                CrossSectionClass.CLASS_1,
                Table5Dot2CompressionPart.INTERNAL_COMPRESSION_PART,
                Table5Dot2LoadingCondition.SUBJECT_TO_BENDING,
                epsilon=1.0,
            )

    @pytest.mark.parametrize("t", [0.0, -1.0])
    def test_raise_error_if_required_thickness_is_not_positive(self, t: float) -> None:
        """Thickness must be positive when the selected criterion uses it."""
        with pytest.raises(LessOrEqualToZeroError):
            Table5Dot2MaximumWidthToThicknessRatio(
                CrossSectionClass.CLASS_1,
                Table5Dot2CompressionPart.INTERNAL_COMPRESSION_PART,
                Table5Dot2LoadingCondition.SUBJECT_TO_BENDING,
                c=500,
                t=t,
                epsilon=1.0,
            )

    @pytest.mark.parametrize("alpha", [0.0, -1.0])
    def test_raise_error_if_required_alpha_is_not_positive(self, alpha: float) -> None:
        """Alpha must be positive when the selected criterion uses it."""
        with pytest.raises(LessOrEqualToZeroError):
            Table5Dot2MaximumWidthToThicknessRatio(
                CrossSectionClass.CLASS_1,
                Table5Dot2CompressionPart.INTERNAL_COMPRESSION_PART,
                Table5Dot2LoadingCondition.SUBJECT_TO_BENDING_AND_COMPRESSION,
                c=500,
                t=10,
                alpha=alpha,
                epsilon=1.0,
            )

    def test_raise_error_if_required_k_sigma_is_negative(self) -> None:
        """The buckling factor must be non-negative when the selected criterion uses it."""
        with pytest.raises(NegativeValueError):
            Table5Dot2MaximumWidthToThicknessRatio(
                CrossSectionClass.CLASS_3,
                Table5Dot2CompressionPart.OUTSTAND_FLANGE,
                Table5Dot2LoadingCondition.SUBJECT_TO_BENDING_AND_COMPRESSION_TIP_IN_COMPRESSION,
                c=200,
                t=10,
                k_sigma=-1.0,
                epsilon=1.0,
            )

    def test_negative_psi_is_valid(self) -> None:
        """Negative psi remains valid, including the sqrt(-psi) branch at psi <= -1."""
        form = Table5Dot2MaximumWidthToThicknessRatio(
            CrossSectionClass.CLASS_3,
            Table5Dot2CompressionPart.INTERNAL_COMPRESSION_PART,
            Table5Dot2LoadingCondition.SUBJECT_TO_BENDING_AND_COMPRESSION,
            c=500,
            t=10,
            psi=-2.0,
            epsilon=1.0,
        )

        assert form.maximum_width_to_thickness_ratio == pytest.approx(62 * 3 * 2**0.5)

    def test_unused_optional_parameters_are_not_validated(self) -> None:
        """Invalid-looking optional inputs are ignored when the selected criterion does not use them."""
        form = Table5Dot2MaximumWidthToThicknessRatio(
            CrossSectionClass.CLASS_1,
            Table5Dot2CompressionPart.INTERNAL_COMPRESSION_PART,
            Table5Dot2LoadingCondition.SUBJECT_TO_BENDING,
            c=500,
            t=10,
            alpha=-1.0,
            k_sigma=-1.0,
            epsilon=1.0,
        )

        assert bool(form) is True
