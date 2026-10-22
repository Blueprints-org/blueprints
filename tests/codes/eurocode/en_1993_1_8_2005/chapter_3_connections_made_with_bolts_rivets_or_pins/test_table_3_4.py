"""Testing table 3.4 of EN 1993-1-8:2005."""

import pytest

from blueprints.codes.eurocode.en_1993_1_8_2005.chapter_3_connections_made_with_bolts_rivets_or_pins.table_3_1 import BoltClass
from blueprints.codes.eurocode.en_1993_1_8_2005.chapter_3_connections_made_with_bolts_rivets_or_pins.table_3_4 import (
    ALPHA_V_THREADED,
    BoltHead,
    BoltPositionParallel,
    BoltPositionPerpendicular,
    HoleType,
    ShearPlane,
    Table3Dot4AlphaB,
    Table3Dot4AlphaD,
    Table3Dot4BearingResistance,
    Table3Dot4CombinedShearAndTension,
    Table3Dot4K1,
    Table3Dot4PunchingShearResistance,
    Table3Dot4ShearResistanceBolt,
    Table3Dot4ShearResistanceRivet,
    Table3Dot4TensionResistanceBolt,
    Table3Dot4TensionResistanceRivet,
)
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestAlphaVThreaded:
    """Validation of the shear factor that Table 3.4 attaches to each bolt class."""

    @pytest.mark.parametrize(
        ("bolt_class", "expected"),
        [
            (BoltClass.CLASS_4_6, 0.6),
            (BoltClass.CLASS_5_6, 0.6),
            (BoltClass.CLASS_8_8, 0.6),
            (BoltClass.CLASS_4_8, 0.5),
            (BoltClass.CLASS_5_8, 0.5),
            (BoltClass.CLASS_6_8, 0.5),
            (BoltClass.CLASS_10_9, 0.5),
        ],
    )
    def test_alpha_v_threaded(self, bolt_class: BoltClass, expected: float) -> None:
        """The table gives 0.6 for classes 4.6, 5.6 and 8.8, and 0.5 for 4.8, 5.8, 6.8 and 10.9."""
        assert ALPHA_V_THREADED[bolt_class] == pytest.approx(expected=expected)

    def test_every_bolt_class_of_table_3_1_is_mapped(self) -> None:
        """A class without a factor would raise a KeyError, so the mapping has to be complete."""
        assert set(ALPHA_V_THREADED) == set(BoltClass)


class TestBoltHead:
    """Validation of the tension factor that Table 3.4 attaches to each head shape."""

    @pytest.mark.parametrize(("bolt_head", "expected"), [(BoltHead.NORMAL, 0.9), (BoltHead.COUNTERSUNK, 0.63)])
    def test_k_2(self, bolt_head: BoltHead, expected: float) -> None:
        """The table gives 0,63 for a countersunk bolt and 0,9 otherwise."""
        assert bolt_head.k_2 == pytest.approx(expected=expected)


class TestHoleType:
    """Validation of the bearing reduction of note 1 of Table 3.4."""

    @pytest.mark.parametrize(
        ("hole_type", "expected"),
        [(HoleType.NORMAL, 1.0), (HoleType.OVERSIZED, 0.8), (HoleType.SLOTTED_PERPENDICULAR, 0.6)],
    )
    def test_reduction(self, hole_type: HoleType, expected: float) -> None:
        """Note 1 reduces the bearing resistance to 0,8 in an oversized hole and to 0,6 in a slotted hole."""
        assert hole_type.reduction == pytest.approx(expected=expected)


class TestTable3Dot4ShearResistanceBolt:
    """Validation for the shear resistance of a bolt from table 3.4 of EN 1993-1-8:2005."""

    @pytest.mark.parametrize(
        ("f_ub", "a", "bolt_class", "shear_plane", "expected"),
        [
            # M20 class 8.8, shear plane through the threads: 0.6 * 800 * 245 / 1.25
            (800.0, 245.0, BoltClass.CLASS_8_8, ShearPlane.THREADED, 94080.0),
            # M20 class 10.9, shear plane through the threads: 0.5 * 1000 * 245 / 1.25
            (1000.0, 245.0, BoltClass.CLASS_10_9, ShearPlane.THREADED, 98000.0),
            # M20 class 10.9, shear plane through the shank, so 0.6 despite the class: 0.6 * 1000 * 314.159265 / 1.25
            (1000.0, 314.159265, BoltClass.CLASS_10_9, ShearPlane.SHANK, 150796.4472),
        ],
    )
    def test_evaluation(self, f_ub: float, a: float, bolt_class: BoltClass, shear_plane: ShearPlane, expected: float) -> None:
        """Tests the evaluation of the result."""
        formula = Table3Dot4ShearResistanceBolt(f_ub=f_ub, a=a, bolt_class=bolt_class, shear_plane=shear_plane, gamma_m2=1.25)

        assert formula == pytest.approx(expected=expected, rel=1e-6)

    def test_alpha_v_is_exposed(self) -> None:
        """The factor the table selected is readable, since it is not an argument the caller passed."""
        threaded = Table3Dot4ShearResistanceBolt(
            f_ub=1000.0, a=245.0, bolt_class=BoltClass.CLASS_10_9, shear_plane=ShearPlane.THREADED, gamma_m2=1.25
        )
        shank = Table3Dot4ShearResistanceBolt(f_ub=1000.0, a=245.0, bolt_class=BoltClass.CLASS_10_9, shear_plane=ShearPlane.SHANK, gamma_m2=1.25)

        assert threaded.alpha_v == pytest.approx(expected=0.5)
        assert shank.alpha_v == pytest.approx(expected=0.6)

    @pytest.mark.parametrize(("f_ub", "a"), [(-800.0, 245.0), (800.0, -245.0)])
    def test_raise_error_when_negative_values_are_given(self, f_ub: float, a: float) -> None:
        """Test if error is raised for parameters that are not allowed to be negative."""
        with pytest.raises(NegativeValueError):
            Table3Dot4ShearResistanceBolt(f_ub=f_ub, a=a, bolt_class=BoltClass.CLASS_8_8, shear_plane=ShearPlane.THREADED, gamma_m2=1.25)

    @pytest.mark.parametrize("gamma_m2", [0.0, -1.25])
    def test_raise_error_when_gamma_m2_is_less_or_equal_to_zero(self, gamma_m2: float) -> None:
        """The partial factor divides the result, so it cannot be zero or negative."""
        with pytest.raises(LessOrEqualToZeroError):
            Table3Dot4ShearResistanceBolt(f_ub=800.0, a=245.0, bolt_class=BoltClass.CLASS_8_8, shear_plane=ShearPlane.THREADED, gamma_m2=gamma_m2)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"F_{v,Rd} = \frac{\alpha_v \cdot f_{ub} \cdot A}{\gamma_{M2}} = "
                r"\frac{0.600 \cdot 800.000 \cdot 245.000}{1.250} = 94080.000 \ N",
            ),
            (
                "complete_with_units",
                r"F_{v,Rd} = \frac{\alpha_v \cdot f_{ub} \cdot A}{\gamma_{M2}} = "
                r"\frac{0.600 \cdot 800.000 \ MPa \cdot 245.000 \ mm^2}{1.250} = 94080.000 \ N",
            ),
            ("short", r"F_{v,Rd} = 94080.000 \ N"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        test_latex = Table3Dot4ShearResistanceBolt(
            f_ub=800.0, a=245.0, bolt_class=BoltClass.CLASS_8_8, shear_plane=ShearPlane.THREADED, gamma_m2=1.25
        ).latex()

        actual = {
            "complete": test_latex.complete,
            "complete_with_units": test_latex.complete_with_units,
            "short": test_latex.short,
        }

        assert expected == actual[representation]


class TestTable3Dot4ShearResistanceRivet:
    """Validation for the shear resistance of a rivet from table 3.4 of EN 1993-1-8:2005."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result: 0.6 * 400 * 314.159265 / 1.25."""
        formula = Table3Dot4ShearResistanceRivet(f_ur=400.0, a_0=314.159265, gamma_m2=1.25)

        assert formula == pytest.approx(expected=60318.57888, rel=1e-6)

    @pytest.mark.parametrize(("f_ur", "a_0"), [(-400.0, 314.159265), (400.0, -314.159265)])
    def test_raise_error_when_negative_values_are_given(self, f_ur: float, a_0: float) -> None:
        """Test if error is raised for parameters that are not allowed to be negative."""
        with pytest.raises(NegativeValueError):
            Table3Dot4ShearResistanceRivet(f_ur=f_ur, a_0=a_0, gamma_m2=1.25)

    def test_raise_error_when_gamma_m2_is_zero(self) -> None:
        """The partial factor divides the result, so it cannot be zero."""
        with pytest.raises(LessOrEqualToZeroError):
            Table3Dot4ShearResistanceRivet(f_ur=400.0, a_0=314.159265, gamma_m2=0.0)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"F_{v,Rd} = \frac{0.6 \cdot f_{ur} \cdot A_0}{\gamma_{M2}} = \frac{0.6 \cdot 400.000 \cdot 314.159}{1.250} = 60318.579 \ N",
            ),
            (
                "complete_with_units",
                r"F_{v,Rd} = \frac{0.6 \cdot f_{ur} \cdot A_0}{\gamma_{M2}} = "
                r"\frac{0.6 \cdot 400.000 \ MPa \cdot 314.159 \ mm^2}{1.250} = 60318.579 \ N",
            ),
            ("short", r"F_{v,Rd} = 60318.579 \ N"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        test_latex = Table3Dot4ShearResistanceRivet(f_ur=400.0, a_0=314.159265, gamma_m2=1.25).latex()

        actual = {
            "complete": test_latex.complete,
            "complete_with_units": test_latex.complete_with_units,
            "short": test_latex.short,
        }

        assert expected == actual[representation]


class TestTable3Dot4AlphaD:
    """Validation for the factor alpha_d from table 3.4 of EN 1993-1-8:2005."""

    @pytest.mark.parametrize(
        ("position", "spacing", "expected"),
        [
            # End bolt: e_1 / (3 * d_0) = 40 / 66
            (BoltPositionParallel.END, 40.0, 0.60606060606),
            # Inner bolt: p_1 / (3 * d_0) - 1/4 = 60 / 66 - 0.25
            (BoltPositionParallel.INNER, 60.0, 0.65909090909),
        ],
    )
    def test_evaluation(self, position: BoltPositionParallel, spacing: float, expected: float) -> None:
        """Tests the evaluation of the result for both positions."""
        formula = Table3Dot4AlphaD(position=position, spacing=spacing, d_0=22.0)

        assert formula == pytest.approx(expected=expected, rel=1e-6)

    def test_result_is_not_clamped_at_zero(self) -> None:
        """The expression for an inner bolt turns negative below p_1 = 0,75 * d_0.

        The table prints no lower bound on alpha_d, so that result is returned unchanged. Clamping it
        would be an addition beyond the printed text.
        """
        # p_1 of 15 mm against a hole of 22 mm: 15 / 66 - 0.25
        formula = Table3Dot4AlphaD(position=BoltPositionParallel.INNER, spacing=15.0, d_0=22.0)

        assert formula == pytest.approx(expected=-0.022727272, rel=1e-6)

    def test_raise_error_when_the_spacing_is_negative(self) -> None:
        """Test if error is raised for parameters that are not allowed to be negative."""
        with pytest.raises(NegativeValueError):
            Table3Dot4AlphaD(position=BoltPositionParallel.END, spacing=-40.0, d_0=22.0)

    def test_raise_error_when_the_hole_diameter_is_zero(self) -> None:
        """The hole diameter divides the result, so it cannot be zero."""
        with pytest.raises(LessOrEqualToZeroError):
            Table3Dot4AlphaD(position=BoltPositionParallel.END, spacing=40.0, d_0=0.0)

    @pytest.mark.parametrize(
        ("position", "representation", "expected"),
        [
            (BoltPositionParallel.END, "complete", r"\alpha_d = \frac{e_1}{3 \cdot d_0} = \frac{40.000}{3 \cdot 22.000} = 0.606 \ -"),
            (
                BoltPositionParallel.END,
                "complete_with_units",
                r"\alpha_d = \frac{e_1}{3 \cdot d_0} = \frac{40.000 \ mm}{3 \cdot 22.000 \ mm} = 0.606 \ -",
            ),
            (BoltPositionParallel.END, "short", r"\alpha_d = 0.606 \ -"),
            (
                BoltPositionParallel.INNER,
                "complete",
                r"\alpha_d = \frac{p_1}{3 \cdot d_0} - \frac{1}{4} = \frac{40.000}{3 \cdot 22.000} - \frac{1}{4} = 0.356 \ -",
            ),
            (
                BoltPositionParallel.INNER,
                "complete_with_units",
                r"\alpha_d = \frac{p_1}{3 \cdot d_0} - \frac{1}{4} = \frac{40.000 \ mm}{3 \cdot 22.000 \ mm} - \frac{1}{4} = 0.356 \ -",
            ),
            (BoltPositionParallel.INNER, "short", r"\alpha_d = 0.356 \ -"),
        ],
    )
    def test_latex(self, position: BoltPositionParallel, representation: str, expected: str) -> None:
        """Test the latex representation, which prints the symbol belonging to the position."""
        test_latex = Table3Dot4AlphaD(position=position, spacing=40.0, d_0=22.0).latex()

        actual = {
            "complete": test_latex.complete,
            "complete_with_units": test_latex.complete_with_units,
            "short": test_latex.short,
        }

        assert expected == actual[representation]


class TestTable3Dot4AlphaB:
    """Validation for the factor alpha_b from table 3.4 of EN 1993-1-8:2005."""

    @pytest.mark.parametrize(
        ("alpha_d", "f_ub", "f_u", "expected"),
        [
            # alpha_d governs
            (0.606061, 800.0, 360.0, 0.606061),
            # the strength ratio governs: 400 / 800
            (0.9, 400.0, 800.0, 0.5),
            # 1.0 governs
            (1.5, 800.0, 360.0, 1.0),
        ],
    )
    def test_evaluation(self, alpha_d: float, f_ub: float, f_u: float, expected: float) -> None:
        """Tests that each of the three candidates can govern."""
        formula = Table3Dot4AlphaB(alpha_d=alpha_d, f_ub=f_ub, f_u=f_u)

        assert formula == pytest.approx(expected=expected, rel=1e-6)

    def test_a_negative_alpha_d_is_accepted_and_governs(self) -> None:
        """Table3Dot4AlphaD returns the printed expression unclamped, so it can hand over a negative.

        Rejecting it here would break the chain the two classes are meant to form, and would be an
        addition beyond the printed text just as clamping would be.
        """
        alpha_d = Table3Dot4AlphaD(position=BoltPositionParallel.INNER, spacing=15.0, d_0=22.0)
        formula = Table3Dot4AlphaB(alpha_d=float(alpha_d), f_ub=800.0, f_u=360.0)

        assert formula == pytest.approx(expected=-0.022727272, rel=1e-6)

    def test_raise_error_when_negative_values_are_given(self) -> None:
        """Test if error is raised for parameters that are not allowed to be negative."""
        with pytest.raises(NegativeValueError):
            Table3Dot4AlphaB(alpha_d=0.6, f_ub=-800.0, f_u=360.0)

    def test_raise_error_when_the_plate_strength_is_zero(self) -> None:
        """The plate strength divides the strength ratio, so it cannot be zero."""
        with pytest.raises(LessOrEqualToZeroError):
            Table3Dot4AlphaB(alpha_d=0.6, f_ub=800.0, f_u=0.0)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"\alpha_b = \min\left(\alpha_d, \frac{f_{ub}}{f_u}, 1.0\right) = "
                r"\min\left(0.606, \frac{800.000}{360.000}, 1.0\right) = 0.606 \ -",
            ),
            (
                "complete_with_units",
                r"\alpha_b = \min\left(\alpha_d, \frac{f_{ub}}{f_u}, 1.0\right) = "
                r"\min\left(0.606, \frac{800.000 \ MPa}{360.000 \ MPa}, 1.0\right) = 0.606 \ -",
            ),
            ("short", r"\alpha_b = 0.606 \ -"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        test_latex = Table3Dot4AlphaB(alpha_d=0.606061, f_ub=800.0, f_u=360.0).latex()

        actual = {
            "complete": test_latex.complete,
            "complete_with_units": test_latex.complete_with_units,
            "short": test_latex.short,
        }

        assert expected == actual[representation]


class TestTable3Dot4K1:
    """Validation for the factor k_1 from table 3.4 of EN 1993-1-8:2005."""

    @pytest.mark.parametrize(
        ("position", "e_2", "p_2", "expected"),
        [
            # Edge bolt, the term in e_2 governs: 2.8 * 30 / 22 - 1.7
            (BoltPositionPerpendicular.EDGE, 30.0, 70.0, 2.118181818),
            # Edge bolt, the term in p_2 governs: 1.4 * 55 / 22 - 1.7
            (BoltPositionPerpendicular.EDGE, 40.0, 55.0, 1.8),
            # Edge bolt, the cap of 2.5 governs
            (BoltPositionPerpendicular.EDGE, 40.0, 70.0, 2.5),
            # Inner bolt, the term in p_2 governs
            (BoltPositionPerpendicular.INNER, None, 55.0, 1.8),
            # Inner bolt, the cap of 2.5 governs
            (BoltPositionPerpendicular.INNER, None, 70.0, 2.5),
        ],
    )
    def test_evaluation(self, position: BoltPositionPerpendicular, e_2: float | None, p_2: float, expected: float) -> None:
        """Tests that each candidate of the printed minimum can govern."""
        formula = Table3Dot4K1(position=position, d_0=22.0, e_2=e_2, p_2=p_2)

        assert formula == pytest.approx(expected=expected, rel=1e-6)

    def test_a_single_line_of_fasteners_drops_the_term_in_p_2(self) -> None:
        """With one line of fasteners there is no p_2, so only the remaining terms decide.

        The table prints no rule for a missing p_2, so leaving the term out is an addition made here.
        """
        formula = Table3Dot4K1(position=BoltPositionPerpendicular.EDGE, d_0=22.0, e_2=30.0)

        assert formula == pytest.approx(expected=2.118181818, rel=1e-6)

    def test_result_is_not_clamped_at_zero(self) -> None:
        """The term in e_2 turns negative below e_2 = 0,607 * d_0, and the minimum then returns that.

        The table prints no lower bound on k_1, so the result is returned unchanged. Clamping it would
        be an addition beyond the printed text.
        """
        # e_2 of 10 mm against a hole of 22 mm: 2.8 * 10 / 22 - 1.7
        formula = Table3Dot4K1(position=BoltPositionPerpendicular.EDGE, d_0=22.0, e_2=10.0, p_2=70.0)

        assert formula == pytest.approx(expected=-0.427272727, rel=1e-6)

    def test_raise_error_when_an_edge_bolt_has_no_edge_distance(self) -> None:
        """The table takes the term in e_2 into account for an edge bolt, so it cannot be left out."""
        with pytest.raises(ValueError, match="e_2 must be given"):
            Table3Dot4K1(position=BoltPositionPerpendicular.EDGE, d_0=22.0, p_2=70.0)

    def test_raise_error_when_an_inner_bolt_has_no_spacing(self) -> None:
        """For an inner bolt the table offers only the term in p_2 next to the cap, so it cannot be left out."""
        with pytest.raises(ValueError, match="p_2 must be given"):
            Table3Dot4K1(position=BoltPositionPerpendicular.INNER, d_0=22.0)

    @pytest.mark.parametrize(("e_2", "p_2"), [(-30.0, 70.0), (30.0, -70.0)])
    def test_raise_error_when_negative_values_are_given(self, e_2: float, p_2: float) -> None:
        """Test if error is raised for parameters that are not allowed to be negative."""
        with pytest.raises(NegativeValueError):
            Table3Dot4K1(position=BoltPositionPerpendicular.EDGE, d_0=22.0, e_2=e_2, p_2=p_2)

    def test_raise_error_when_the_hole_diameter_is_zero(self) -> None:
        """The hole diameter divides both terms, so it cannot be zero."""
        with pytest.raises(LessOrEqualToZeroError):
            Table3Dot4K1(position=BoltPositionPerpendicular.EDGE, d_0=0.0, e_2=30.0, p_2=70.0)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"k_1 = \min\left(2.8 \cdot \frac{e_2}{d_0} - 1.7, 1.4 \cdot \frac{p_2}{d_0} - 1.7, 2.5\right) = "
                r"\min\left(2.8 \cdot \frac{30.000}{22.000} - 1.7, 1.4 \cdot \frac{70.000}{22.000} - 1.7, 2.5\right) = 2.118 \ -",
            ),
            (
                "complete_with_units",
                r"k_1 = \min\left(2.8 \cdot \frac{e_2}{d_0} - 1.7, 1.4 \cdot \frac{p_2}{d_0} - 1.7, 2.5\right) = "
                r"\min\left(2.8 \cdot \frac{30.000 \ mm}{22.000 \ mm} - 1.7, "
                r"1.4 \cdot \frac{70.000 \ mm}{22.000 \ mm} - 1.7, 2.5\right) = 2.118 \ -",
            ),
            ("short", r"k_1 = 2.118 \ -"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        test_latex = Table3Dot4K1(position=BoltPositionPerpendicular.EDGE, d_0=22.0, e_2=30.0, p_2=70.0).latex()

        actual = {
            "complete": test_latex.complete,
            "complete_with_units": test_latex.complete_with_units,
            "short": test_latex.short,
        }

        assert expected == actual[representation]

    def test_latex_of_an_inner_bolt_leaves_out_the_term_in_e_2(self) -> None:
        """The printed minimum of an inner bolt has two candidates, not three."""
        test_latex = Table3Dot4K1(position=BoltPositionPerpendicular.INNER, d_0=22.0, p_2=55.0).latex()

        assert test_latex.equation == r"\min\left(1.4 \cdot \frac{p_2}{d_0} - 1.7, 2.5\right)"


class TestTable3Dot4BearingResistance:
    """Validation for the bearing resistance from table 3.4 of EN 1993-1-8:2005."""

    @pytest.mark.parametrize(
        ("hole_type", "expected"),
        [
            # 2.5 * 0.606061 * 360 * 20 * 10 / 1.25
            (HoleType.NORMAL, 87272.784),
            # note 1 reduces the same value to 0.8 times
            (HoleType.OVERSIZED, 69818.2272),
            # note 1 reduces the same value to 0.6 times
            (HoleType.SLOTTED_PERPENDICULAR, 52363.6704),
        ],
    )
    def test_evaluation(self, hole_type: HoleType, expected: float) -> None:
        """Tests the evaluation of the result for each hole shape of note 1."""
        formula = Table3Dot4BearingResistance(k_1=2.5, alpha_b=0.606061, f_u=360.0, d=20.0, t=10.0, gamma_m2=1.25, hole_type=hole_type)

        assert formula == pytest.approx(expected=expected, rel=1e-6)

    def test_a_normal_hole_is_the_default(self) -> None:
        """Leaving the hole shape out gives the unreduced resistance."""
        default = Table3Dot4BearingResistance(k_1=2.5, alpha_b=0.606061, f_u=360.0, d=20.0, t=10.0, gamma_m2=1.25)
        explicit = Table3Dot4BearingResistance(k_1=2.5, alpha_b=0.606061, f_u=360.0, d=20.0, t=10.0, gamma_m2=1.25, hole_type=HoleType.NORMAL)

        assert default == pytest.approx(expected=float(explicit), rel=1e-12)

    def test_a_negative_k_1_is_accepted_and_carries_through(self) -> None:
        """Table3Dot4K1 returns the printed minimum unclamped, so it can hand over a negative.

        Rejecting it here would break the chain the two classes are meant to form. A negative bearing
        resistance signals a detailing violation rather than a real resistance, which is the caller's
        to judge, not this class's to hide.
        """
        k_1 = Table3Dot4K1(position=BoltPositionPerpendicular.EDGE, d_0=22.0, e_2=10.0, p_2=70.0)
        formula = Table3Dot4BearingResistance(k_1=float(k_1), alpha_b=0.606061, f_u=360.0, d=20.0, t=10.0, gamma_m2=1.25)

        # -0.427272727 * 0.606061 * 360 * 20 * 10 / 1.25
        assert formula == pytest.approx(expected=-14915.712, rel=1e-6)

    @pytest.mark.parametrize(
        ("f_u", "d", "t"),
        [(-360.0, 20.0, 10.0), (360.0, -20.0, 10.0), (360.0, 20.0, -10.0)],
    )
    def test_raise_error_when_negative_values_are_given(self, f_u: float, d: float, t: float) -> None:
        """Test if error is raised for parameters that are not allowed to be negative."""
        with pytest.raises(NegativeValueError):
            Table3Dot4BearingResistance(k_1=2.5, alpha_b=0.606061, f_u=f_u, d=d, t=t, gamma_m2=1.25)

    def test_raise_error_when_gamma_m2_is_zero(self) -> None:
        """The partial factor divides the result, so it cannot be zero."""
        with pytest.raises(LessOrEqualToZeroError):
            Table3Dot4BearingResistance(k_1=2.5, alpha_b=0.606061, f_u=360.0, d=20.0, t=10.0, gamma_m2=0.0)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"F_{b,Rd} = \frac{k_1 \cdot \alpha_b \cdot f_u \cdot d \cdot t}{\gamma_{M2}} = "
                r"\frac{2.500 \cdot 0.606 \cdot 360.000 \cdot 20.000 \cdot 10.000}{1.250} = 87272.784 \ N",
            ),
            (
                "complete_with_units",
                r"F_{b,Rd} = \frac{k_1 \cdot \alpha_b \cdot f_u \cdot d \cdot t}{\gamma_{M2}} = "
                r"\frac{2.500 \cdot 0.606 \cdot 360.000 \ MPa \cdot 20.000 \ mm \cdot 10.000 \ mm}{1.250} = 87272.784 \ N",
            ),
            ("short", r"F_{b,Rd} = 87272.784 \ N"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        test_latex = Table3Dot4BearingResistance(k_1=2.5, alpha_b=0.606061, f_u=360.0, d=20.0, t=10.0, gamma_m2=1.25).latex()

        actual = {
            "complete": test_latex.complete,
            "complete_with_units": test_latex.complete_with_units,
            "short": test_latex.short,
        }

        assert expected == actual[representation]

    def test_latex_shows_the_reduction_of_note_1(self) -> None:
        """A reduced hole shape prints its factor, so the reduction is visible in the report."""
        test_latex = Table3Dot4BearingResistance(
            k_1=2.5, alpha_b=0.606061, f_u=360.0, d=20.0, t=10.0, gamma_m2=1.25, hole_type=HoleType.OVERSIZED
        ).latex()

        assert test_latex.equation == r"0.8 \cdot \frac{k_1 \cdot \alpha_b \cdot f_u \cdot d \cdot t}{\gamma_{M2}}"


class TestTable3Dot4TensionResistanceBolt:
    """Validation for the tension resistance of a bolt from table 3.4 of EN 1993-1-8:2005."""

    @pytest.mark.parametrize(
        ("bolt_head", "expected"),
        [
            # 0.9 * 800 * 245 / 1.25
            (BoltHead.NORMAL, 141120.0),
            # 0.63 * 800 * 245 / 1.25
            (BoltHead.COUNTERSUNK, 98784.0),
        ],
    )
    def test_evaluation(self, bolt_head: BoltHead, expected: float) -> None:
        """Tests the evaluation of the result for both head shapes."""
        formula = Table3Dot4TensionResistanceBolt(f_ub=800.0, a_s=245.0, gamma_m2=1.25, bolt_head=bolt_head)

        assert formula == pytest.approx(expected=expected, rel=1e-6)

    def test_k_2_is_exposed(self) -> None:
        """The factor the table selected is readable, since it is not an argument the caller passed."""
        formula = Table3Dot4TensionResistanceBolt(f_ub=800.0, a_s=245.0, gamma_m2=1.25, bolt_head=BoltHead.COUNTERSUNK)

        assert formula.k_2 == pytest.approx(expected=0.63)

    @pytest.mark.parametrize(("f_ub", "a_s"), [(-800.0, 245.0), (800.0, -245.0)])
    def test_raise_error_when_negative_values_are_given(self, f_ub: float, a_s: float) -> None:
        """Test if error is raised for parameters that are not allowed to be negative."""
        with pytest.raises(NegativeValueError):
            Table3Dot4TensionResistanceBolt(f_ub=f_ub, a_s=a_s, gamma_m2=1.25)

    def test_raise_error_when_gamma_m2_is_zero(self) -> None:
        """The partial factor divides the result, so it cannot be zero."""
        with pytest.raises(LessOrEqualToZeroError):
            Table3Dot4TensionResistanceBolt(f_ub=800.0, a_s=245.0, gamma_m2=0.0)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"F_{t,Rd} = \frac{k_2 \cdot f_{ub} \cdot A_s}{\gamma_{M2}} = "
                r"\frac{0.900 \cdot 800.000 \cdot 245.000}{1.250} = 141120.000 \ N",
            ),
            (
                "complete_with_units",
                r"F_{t,Rd} = \frac{k_2 \cdot f_{ub} \cdot A_s}{\gamma_{M2}} = "
                r"\frac{0.900 \cdot 800.000 \ MPa \cdot 245.000 \ mm^2}{1.250} = 141120.000 \ N",
            ),
            ("short", r"F_{t,Rd} = 141120.000 \ N"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        test_latex = Table3Dot4TensionResistanceBolt(f_ub=800.0, a_s=245.0, gamma_m2=1.25).latex()

        actual = {
            "complete": test_latex.complete,
            "complete_with_units": test_latex.complete_with_units,
            "short": test_latex.short,
        }

        assert expected == actual[representation]


class TestTable3Dot4TensionResistanceRivet:
    """Validation for the tension resistance of a rivet from table 3.4 of EN 1993-1-8:2005."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result: 0.6 * 400 * 314.159265 / 1.25."""
        formula = Table3Dot4TensionResistanceRivet(f_ur=400.0, a_0=314.159265, gamma_m2=1.25)

        assert formula == pytest.approx(expected=60318.57888, rel=1e-6)

    @pytest.mark.parametrize(("f_ur", "a_0"), [(-400.0, 314.159265), (400.0, -314.159265)])
    def test_raise_error_when_negative_values_are_given(self, f_ur: float, a_0: float) -> None:
        """Test if error is raised for parameters that are not allowed to be negative."""
        with pytest.raises(NegativeValueError):
            Table3Dot4TensionResistanceRivet(f_ur=f_ur, a_0=a_0, gamma_m2=1.25)

    def test_raise_error_when_gamma_m2_is_zero(self) -> None:
        """The partial factor divides the result, so it cannot be zero."""
        with pytest.raises(LessOrEqualToZeroError):
            Table3Dot4TensionResistanceRivet(f_ur=400.0, a_0=314.159265, gamma_m2=0.0)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"F_{t,Rd} = \frac{0.6 \cdot f_{ur} \cdot A_0}{\gamma_{M2}} = \frac{0.6 \cdot 400.000 \cdot 314.159}{1.250} = 60318.579 \ N",
            ),
            (
                "complete_with_units",
                r"F_{t,Rd} = \frac{0.6 \cdot f_{ur} \cdot A_0}{\gamma_{M2}} = "
                r"\frac{0.6 \cdot 400.000 \ MPa \cdot 314.159 \ mm^2}{1.250} = 60318.579 \ N",
            ),
            ("short", r"F_{t,Rd} = 60318.579 \ N"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        test_latex = Table3Dot4TensionResistanceRivet(f_ur=400.0, a_0=314.159265, gamma_m2=1.25).latex()

        actual = {
            "complete": test_latex.complete,
            "complete_with_units": test_latex.complete_with_units,
            "short": test_latex.short,
        }

        assert expected == actual[representation]


class TestTable3Dot4PunchingShearResistance:
    """Validation for the punching shear resistance from table 3.4 of EN 1993-1-8:2005."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result: 0.6 * pi * 32.4 * 10 * 360 / 1.25."""
        formula = Table3Dot4PunchingShearResistance(d_m=32.4, t_p=10.0, f_u=360.0, gamma_m2=1.25)

        assert formula == pytest.approx(expected=175888.97621506246, rel=1e-9)

    @pytest.mark.parametrize(
        ("d_m", "t_p", "f_u"),
        [(-32.4, 10.0, 360.0), (32.4, -10.0, 360.0), (32.4, 10.0, -360.0)],
    )
    def test_raise_error_when_negative_values_are_given(self, d_m: float, t_p: float, f_u: float) -> None:
        """Test if error is raised for parameters that are not allowed to be negative."""
        with pytest.raises(NegativeValueError):
            Table3Dot4PunchingShearResistance(d_m=d_m, t_p=t_p, f_u=f_u, gamma_m2=1.25)

    def test_raise_error_when_gamma_m2_is_zero(self) -> None:
        """The partial factor divides the result, so it cannot be zero."""
        with pytest.raises(LessOrEqualToZeroError):
            Table3Dot4PunchingShearResistance(d_m=32.4, t_p=10.0, f_u=360.0, gamma_m2=0.0)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"B_{p,Rd} = \frac{0.6 \cdot \pi \cdot d_m \cdot t_p \cdot f_u}{\gamma_{M2}} = "
                r"\frac{0.6 \cdot \pi \cdot 32.400 \cdot 10.000 \cdot 360.000}{1.250} = 175888.976 \ N",
            ),
            (
                "complete_with_units",
                r"B_{p,Rd} = \frac{0.6 \cdot \pi \cdot d_m \cdot t_p \cdot f_u}{\gamma_{M2}} = "
                r"\frac{0.6 \cdot \pi \cdot 32.400 \ mm \cdot 10.000 \ mm \cdot 360.000 \ MPa}{1.250} = 175888.976 \ N",
            ),
            ("short", r"B_{p,Rd} = 175888.976 \ N"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        test_latex = Table3Dot4PunchingShearResistance(d_m=32.4, t_p=10.0, f_u=360.0, gamma_m2=1.25).latex()

        actual = {
            "complete": test_latex.complete,
            "complete_with_units": test_latex.complete_with_units,
            "short": test_latex.short,
        }

        assert expected == actual[representation]


class TestTable3Dot4CombinedShearAndTension:
    """Validation for the combined shear and tension check from table 3.4 of EN 1993-1-8:2005."""

    @pytest.mark.parametrize(
        ("f_v_ed", "f_t_ed", "expected"),
        [
            # 50000 / 94080 + 30000 / (1.4 * 141120) = 0.531 + 0.152
            (50000.0, 30000.0, True),
            # 90000 / 94080 + 100000 / (1.4 * 141120) = 0.957 + 0.506
            (90000.0, 100000.0, False),
        ],
    )
    def test_evaluation(self, f_v_ed: float, f_t_ed: float, expected: bool) -> None:
        """Tests both sides of the printed limit of 1,0."""
        formula = Table3Dot4CombinedShearAndTension(f_v_ed=f_v_ed, f_v_rd=94080.0, f_t_ed=f_t_ed, f_t_rd=141120.0)

        assert bool(formula) is expected

    def test_the_limit_is_inclusive(self) -> None:
        """The table prints the interaction with a less than or equal sign, so exactly 1,0 passes."""
        # A pure tension case, scaled so that the second ratio is exactly 1.0
        formula = Table3Dot4CombinedShearAndTension(f_v_ed=0.0, f_v_rd=94080.0, f_t_ed=1.4 * 141120.0, f_t_rd=141120.0)

        assert formula.lhs == pytest.approx(expected=1.0, rel=1e-12)
        assert bool(formula) is True

    def test_unity_check(self) -> None:
        """The sum of the two ratios is the unity check, since the right-hand side is 1,0."""
        formula = Table3Dot4CombinedShearAndTension(f_v_ed=50000.0, f_v_rd=94080.0, f_t_ed=30000.0, f_t_rd=141120.0)

        assert formula.unity_check == pytest.approx(expected=0.6833090379, rel=1e-6)
        assert formula.rhs == pytest.approx(expected=1.0)

    @pytest.mark.parametrize(("f_v_ed", "f_t_ed"), [(-50000.0, 30000.0), (50000.0, -30000.0)])
    def test_raise_error_when_negative_values_are_given(self, f_v_ed: float, f_t_ed: float) -> None:
        """Test if error is raised for parameters that are not allowed to be negative."""
        with pytest.raises(NegativeValueError):
            Table3Dot4CombinedShearAndTension(f_v_ed=f_v_ed, f_v_rd=94080.0, f_t_ed=f_t_ed, f_t_rd=141120.0)

    @pytest.mark.parametrize(("f_v_rd", "f_t_rd"), [(0.0, 141120.0), (94080.0, 0.0)])
    def test_raise_error_when_a_resistance_is_zero(self, f_v_rd: float, f_t_rd: float) -> None:
        """Both resistances divide a ratio, so neither can be zero."""
        with pytest.raises(LessOrEqualToZeroError):
            Table3Dot4CombinedShearAndTension(f_v_ed=50000.0, f_v_rd=f_v_rd, f_t_ed=30000.0, f_t_rd=f_t_rd)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"CHECK \to \frac{F_{v,Ed}}{F_{v,Rd}} + \frac{F_{t,Ed}}{1.4 \cdot F_{t,Rd}} \leq 1.0 \to "
                r"\frac{50000.000}{94080.000} + \frac{30000.000}{1.4 \cdot 141120.000} \leq 1.0 \to OK",
            ),
            (
                "complete_with_units",
                r"CHECK \to \frac{F_{v,Ed}}{F_{v,Rd}} + \frac{F_{t,Ed}}{1.4 \cdot F_{t,Rd}} \leq 1.0 \to "
                r"\frac{50000.000 \ N}{94080.000 \ N} + \frac{30000.000 \ N}{1.4 \cdot 141120.000 \ N} \leq 1.0 \to OK",
            ),
            ("short", r"CHECK \to OK"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        test_latex = Table3Dot4CombinedShearAndTension(f_v_ed=50000.0, f_v_rd=94080.0, f_t_ed=30000.0, f_t_rd=141120.0).latex()

        actual = {
            "complete": test_latex.complete,
            "complete_with_units": test_latex.complete_with_units,
            "short": test_latex.short,
        }

        assert expected == actual[representation]

    def test_latex_reports_a_failing_check(self) -> None:
        """A check that is not satisfied has to say so in its own representation."""
        test_latex = Table3Dot4CombinedShearAndTension(f_v_ed=90000.0, f_v_rd=94080.0, f_t_ed=100000.0, f_t_rd=141120.0).latex()

        assert test_latex.short == r"CHECK \to \text{Not OK}"
