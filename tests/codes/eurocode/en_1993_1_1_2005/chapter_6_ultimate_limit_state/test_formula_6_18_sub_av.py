"""Testing subformulas a to g from 6.18 of EN 1993-1-1:2005."""

import pytest

from blueprints.codes.eurocode.en_1993_1_1_2005.chapter_6_ultimate_limit_state.formula_6_18_sub_av import (
    Form6Dot18SubARolledIandHSection,
    Form6Dot18SubBRolledChannelSection,
    Form6Dot18SubCTSectionRolled,
    Form6Dot18SubCTSectionWelded,
    Form6Dot18SubDWeldedIHandBoxSection,
    Form6Dot18SubEWeldedIHandBoxSection,
    Form6Dot18SubF1RolledRectangularHollowSectionDepth,
    Form6Dot18SubF2RolledRectangularHollowSectionWidth,
    Form6Dot18SubGCircularHollowSection,
)
from blueprints.validations import ListsNotSameLengthError, NegativeValueError


class TestForm6Dot18SubARolledIandHSection:
    """Validation for formula 6.18suba from EN 1993-1-1:2005."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        a = 10000.0
        b1 = 200.0
        b2 = 200.0
        hw = 250.0
        r1 = 10.0
        r2 = 10.0
        tf1 = 15.0
        tf2 = 15.0
        tw = 8.0
        eta = 1.0

        formula = Form6Dot18SubARolledIandHSection(a=a, b1=b1, b2=b2, hw=hw, r1=r1, r2=r2, tf1=tf1, tf2=tf2, tw=tw, eta=eta)
        manually_calculated_result = 4420.0  # mm^2

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_evaluation_non_symmetric(self) -> None:
        """Tests the evaluation of the result for a non-symmetric profile."""
        a = 10000.0
        b1 = 180.0
        b2 = 200.0
        hw = 250.0
        r1 = 10.0
        r2 = 10.0
        tf1 = 15.0
        tf2 = 15.0
        tw = 8.0
        eta = 1.0

        formula = Form6Dot18SubARolledIandHSection(a=a, b1=b1, b2=b2, hw=hw, r1=r1, r2=r2, tf1=tf1, tf2=tf2, tw=tw, eta=eta)
        manually_calculated_result = 4720.0  # mm^2

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("a", "b1", "b2", "hw", "r1", "r2", "tf1", "tf2", "tw", "eta"),
        [
            (-10000.0, 200.0, 200.0, 250.0, 10.0, 10.0, 15.0, 15.0, 8.0, 1.0),  # a is negative
            (10000.0, -200.0, 200.0, 250.0, 10.0, 10.0, 15.0, 15.0, 8.0, 1.0),  # b1 is negative
            (10000.0, 200.0, -200.0, 250.0, 10.0, 10.0, 15.0, 15.0, 8.0, 1.0),  # b2 is negative
            (10000.0, 200.0, 200.0, -250.0, 10.0, 10.0, 15.0, 15.0, 8.0, 1.0),  # hw is negative
            (10000.0, 200.0, 200.0, 250.0, -10.0, 10.0, 15.0, 15.0, 8.0, 1.0),  # r1 is negative
            (10000.0, 200.0, 200.0, 250.0, 10.0, -10.0, 15.0, 15.0, 8.0, 1.0),  # r2 is negative
            (10000.0, 200.0, 200.0, 250.0, 10.0, 10.0, -15.0, 15.0, 8.0, 1.0),  # tf1 is negative
            (10000.0, 200.0, 200.0, 250.0, 10.0, 10.0, 15.0, -15.0, 8.0, 1.0),  # tf2 is negative
            (10000.0, 200.0, 200.0, 250.0, 10.0, 10.0, 15.0, 15.0, -8.0, 1.0),  # tw is negative
            (10000.0, 200.0, 200.0, 250.0, 10.0, 10.0, 15.0, 15.0, 8.0, -1.0),  # eta is negative
        ],
    )
    def test_raise_error_when_invalid_values_are_given(
        self, a: float, b1: float, b2: float, hw: float, r1: float, r2: float, tf1: float, tf2: float, tw: float, eta: float
    ) -> None:
        """Test invalid values."""
        with pytest.raises(NegativeValueError):
            Form6Dot18SubARolledIandHSection(a=a, b1=b1, b2=b2, hw=hw, r1=r1, r2=r2, tf1=tf1, tf2=tf2, tw=tw, eta=eta)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"A_v = \max(A - b_1 \cdot t_{f1} - b_2 \cdot t_{f2} + (t_w + 2 \cdot r_1) \cdot \frac{t_{f1}}{2} + "
                r"(t_w + 2 \cdot r_2) \cdot \frac{t_{f2}}{2}; \eta \cdot h_w \cdot t_w) = "
                r"\max(10000.000 - 200.000 \cdot 15.000 - 200.000 \cdot 15.000 + (8.000 + 2 \cdot 10.000) "
                r"\cdot \frac{15.000}{2} + (8.000 + 2 \cdot 10.000) \cdot \frac{15.000}{2}; 1.000 \cdot 250.000 \cdot 8.000) = 4420.000 \ mm^2",
            ),
            ("short", r"A_v = 4420.000 \ mm^2"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        a = 10000.0
        b1 = 200.0
        b2 = 200.0
        hw = 250.0
        r1 = 10.0
        r2 = 10.0
        tf1 = 15.0
        tf2 = 15.0
        tw = 8.0
        eta = 1.0

        latex = Form6Dot18SubARolledIandHSection(a=a, b1=b1, b2=b2, hw=hw, r1=r1, r2=r2, tf1=tf1, tf2=tf2, tw=tw, eta=eta).latex()

        actual = {
            "complete": latex.complete,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."


class TestForm6Dot18SubBRolledChannelSection:
    """Validation for formula 6.18subb from EN 1993-1-1:2005."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        a = 8000.0
        b = 150.0
        tf = 12.0
        tw = 6.0
        r = 8.0

        formula = Form6Dot18SubBRolledChannelSection(a=a, b=b, tf=tf, tw=tw, r=r)
        manually_calculated_result = 4568.0  # mm^2

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("a", "b", "tf", "tw", "r"),
        [
            (-8000.0, 150.0, 12.0, 6.0, 8.0),  # a is negative
            (8000.0, -150.0, 12.0, 6.0, 8.0),  # b is negative
            (8000.0, 150.0, -12.0, 6.0, 8.0),  # tf is negative
            (8000.0, 150.0, 12.0, -6.0, 8.0),  # tw is negative
            (8000.0, 150.0, 12.0, 6.0, -8.0),  # r is negative
        ],
    )
    def test_raise_error_when_invalid_values_are_given(self, a: float, b: float, tf: float, tw: float, r: float) -> None:
        """Test invalid values."""
        with pytest.raises(NegativeValueError):
            Form6Dot18SubBRolledChannelSection(a=a, b=b, tf=tf, tw=tw, r=r)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"A_v = A - 2 \cdot b \cdot t_f + (t_w + r) \cdot t_f = "
                r"8000.000 - 2 \cdot 150.000 \cdot 12.000 + (6.000 + 8.000) \cdot 12.000 = 4568.000 \ mm^2",
            ),
            ("short", r"A_v = 4568.000 \ mm^2"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        a = 8000.0
        b = 150.0
        tf = 12.0
        tw = 6.0
        r = 8.0

        latex = Form6Dot18SubBRolledChannelSection(a=a, b=b, tf=tf, tw=tw, r=r).latex()

        actual = {
            "complete": latex.complete,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."


class TestForm6Dot18SubCRolledTSectionRolled:
    """Validation for formula 6.18subc from EN 1993-1-1:2005."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        a = 6000.0
        b = 100.0
        tf = 10.0
        tw = 8.0
        r = 5.0

        formula = Form6Dot18SubCTSectionRolled(a=a, b=b, tf=tf, tw=tw, r=r)
        manually_calculated_result = 5090.0  # mm^2

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("a", "b", "tf", "tw", "r"),
        [
            (-6000.0, 100.0, 10.0, 8.0, 5.0),  # a is negative
            (6000.0, -100.0, 10.0, 8.0, 5.0),  # b is negative
            (6000.0, 100.0, -10.0, 8.0, 5.0),  # tf is negative
            (6000.0, 100.0, 10.0, -8.0, 5.0),  # tw is negative
            (6000.0, 100.0, 10.0, 8.0, -5.0),  # r is negative
        ],
    )
    def test_raise_error_when_invalid_values_are_given(self, a: float, b: float, tf: float, tw: float, r: float) -> None:
        """Test invalid values."""
        with pytest.raises(NegativeValueError):
            Form6Dot18SubCTSectionRolled(a=a, b=b, tf=tf, tw=tw, r=r)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"A_v = A - b \cdot t_f + (t_w + 2 \cdot r) \cdot \frac{t_f}{2} = "
                r"6000.000 - 100.000 \cdot 10.000 + (8.000 + 2 \cdot 5.000) \cdot \frac{10.000}{2} = 5090.000 \ mm^2",
            ),
            ("short", r"A_v = 5090.000 \ mm^2"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        a = 6000.0
        b = 100.0
        tf = 10.0
        tw = 8.0
        r = 5.0

        latex = Form6Dot18SubCTSectionRolled(a=a, b=b, tf=tf, tw=tw, r=r).latex()

        actual = {
            "complete": latex.complete,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."


class TestForm6Dot18SubCRolledTSectionWelded:
    """Validation for formula 6.18subc from EN 1993-1-1:2005."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        tf = 10.0
        tw = 8.0
        h = 200.0

        formula = Form6Dot18SubCTSectionWelded(tf=tf, tw=tw, h=h)
        manually_calculated_result = 8000.0  # mm^2

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("tf", "tw", "h"),
        [
            (-10.0, 8.0, 200.0),  # tf is negative
            (10.0, -8.0, 200.0),  # tw is negative
            (10.0, 8.0, -200.0),  # h is negative
        ],
    )
    def test_raise_error_when_invalid_values_are_given(self, tf: float, tw: float, h: float) -> None:
        """Test invalid values."""
        with pytest.raises(NegativeValueError):
            Form6Dot18SubCTSectionWelded(tf=tf, tw=tw, h=h)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"A_v = t_w \cdot (h \cdot t_f / 2) = "
                r"8.000 \cdot (200.000 \cdot 10.000 / 2) = 8000.000 \ mm^2",
            ),
            ("short", r"A_v = 8000.000 \ mm^2"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        tf = 10.0
        tw = 8.0
        h = 200.0

        latex = Form6Dot18SubCTSectionWelded(tf=tf, tw=tw, h=h).latex()

        actual = {
            "complete": latex.complete,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."


class TestForm6Dot18SubDWeldedIHandBoxSection:
    """Validation for formula 6.18subd from EN 1993-1-1:2005."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        hw_list = [250.0, 300.0]
        tw_list = [8.0, 10.0]
        eta = 1.0

        formula = Form6Dot18SubDWeldedIHandBoxSection(hw_list=hw_list, tw_list=tw_list, eta=eta)
        manually_calculated_result = 5000.0  # mm^2

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("hw_list", "tw_list", "eta"),
        [
            ([250.0, -300.0], [8.0, 10.0], 1.0),  # hw_list contains negative value
            ([250.0, 300.0], [8.0, -10.0], 1.0),  # tw_list contains negative value
            ([250.0, 300.0], [8.0, 10.0], -1.0),  # eta is negative
            ([250.0], [8.0, 10.0], 1.0),  # hw_list and tw_list are not the same length
        ],
    )
    def test_raise_error_when_invalid_values_are_given(self, hw_list: list[float], tw_list: list[float], eta: float) -> None:
        """Test invalid values."""
        with pytest.raises((NegativeValueError, ListsNotSameLengthError)):
            Form6Dot18SubDWeldedIHandBoxSection(hw_list=hw_list, tw_list=tw_list, eta=eta)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"A_v = \eta \cdot \sum (h_{w} \cdot t_{w}) = "
                r"1.000 \cdot (250.000 \cdot 8.000 + 300.000 \cdot 10.000) = 5000.000 \ mm^2",
            ),
            ("short", r"A_v = 5000.000 \ mm^2"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        hw_list = [250.0, 300.0]
        tw_list = [8.0, 10.0]
        eta = 1.0

        latex = Form6Dot18SubDWeldedIHandBoxSection(hw_list=hw_list, tw_list=tw_list, eta=eta).latex()

        actual = {
            "complete": latex.complete,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."


class TestForm6Dot18SubEWeldedIHandBoxSection:
    """Validation for formula 6.18sube from EN 1993-1-1:2005."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        a = 12000.0
        hw_list = [250.0, 300.0]
        tw_list = [8.0, 10.0]

        formula = Form6Dot18SubEWeldedIHandBoxSection(a=a, hw_list=hw_list, tw_list=tw_list)
        manually_calculated_result = 7000.0  # mm^2

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("a", "hw_list", "tw_list"),
        [
            (-12000.0, [250.0, 300.0], [8.0, 10.0]),  # a is negative
            (12000.0, [250.0, -300.0], [8.0, 10.0]),  # hw_list contains negative value
            (12000.0, [250.0, 300.0], [8.0, -10.0]),  # tw_list contains negative value
            (12000.0, [250.0, 300.0], [8.0, 10.0, 12.0]),  # hw_list and tw_list are not the same length
        ],
    )
    def test_raise_error_when_invalid_values_are_given(self, a: float, hw_list: list[float], tw_list: list[float]) -> None:
        """Test invalid values."""
        with pytest.raises((NegativeValueError, ListsNotSameLengthError)):
            Form6Dot18SubEWeldedIHandBoxSection(a=a, hw_list=hw_list, tw_list=tw_list)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"A_v = A - \sum (h_{w} \cdot t_{w}) = "
                r"12000.000 - (250.000 \cdot 8.000 + 300.000 \cdot 10.000) = 7000.000 \ mm^2",
            ),
            ("short", r"A_v = 7000.000 \ mm^2"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        a = 12000.0
        hw_list = [250.0, 300.0]
        tw_list = [8.0, 10.0]

        latex = Form6Dot18SubEWeldedIHandBoxSection(a=a, hw_list=hw_list, tw_list=tw_list).latex()

        actual = {
            "complete": latex.complete,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."


class TestForm6Dot18SubF1RolledRectangularHollowSectionDepth:
    """Validation for formula 6.18subf1 from EN 1993-1-1:2005."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        a = 5000.0
        b = 100.0
        h = 200.0

        formula = Form6Dot18SubF1RolledRectangularHollowSectionDepth(a=a, b=b, h=h)
        manually_calculated_result = 3333.333  # mm^2

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("a", "b", "h"),
        [
            (-5000.0, 100.0, 200.0),  # a is negative
            (5000.0, -100.0, 200.0),  # b is negative
            (5000.0, 100.0, -200.0),  # h is negative
        ],
    )
    def test_raise_error_when_invalid_values_are_given(self, a: float, b: float, h: float) -> None:
        """Test invalid values."""
        with pytest.raises(NegativeValueError):
            Form6Dot18SubF1RolledRectangularHollowSectionDepth(a=a, b=b, h=h)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"A_v = \frac{A \cdot h}{b + h} = "
                r"\frac{5000.000 \cdot 200.000}{100.000 + 200.000} = 3333.333 \ mm^2",
            ),
            ("short", r"A_v = 3333.333 \ mm^2"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        a = 5000.0
        b = 100.0
        h = 200.0

        latex = Form6Dot18SubF1RolledRectangularHollowSectionDepth(a=a, b=b, h=h).latex()

        actual = {
            "complete": latex.complete,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."


class TestForm6Dot18SubF2RolledRectangularHollowSectionWidth:
    """Validation for formula 6.18subf2 from EN 1993-1-1:2005."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        a = 5000.0
        b = 100.0
        h = 200.0

        formula = Form6Dot18SubF2RolledRectangularHollowSectionWidth(a=a, b=b, h=h)
        manually_calculated_result = 1666.667  # mm^2

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("a", "b", "h"),
        [
            (-5000.0, 100.0, 200.0),  # a is negative
            (5000.0, -100.0, 200.0),  # b is negative
            (5000.0, 100.0, -200.0),  # h is negative
        ],
    )
    def test_raise_error_when_invalid_values_are_given(self, a: float, b: float, h: float) -> None:
        """Test invalid values."""
        with pytest.raises(NegativeValueError):
            Form6Dot18SubF2RolledRectangularHollowSectionWidth(a=a, b=b, h=h)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"A_v = \frac{A \cdot b}{b + h} = "
                r"\frac{5000.000 \cdot 100.000}{100.000 + 200.000} = 1666.667 \ mm^2",
            ),
            ("short", r"A_v = 1666.667 \ mm^2"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        a = 5000.0
        b = 100.0
        h = 200.0

        latex = Form6Dot18SubF2RolledRectangularHollowSectionWidth(a=a, b=b, h=h).latex()

        actual = {
            "complete": latex.complete,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."


class TestForm6Dot18SubGCircularHollowSection:
    """Validation for formula 6.18subg from EN 1993-1-1:2005."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        a = 4000.0

        formula = Form6Dot18SubGCircularHollowSection(a=a)
        manually_calculated_result = 2546.4790899483937  # mm^2

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        "a",
        [
            -4000.0,  # a is negative
        ],
    )
    def test_raise_error_when_invalid_values_are_given(self, a: float) -> None:
        """Test invalid values."""
        with pytest.raises(NegativeValueError):
            Form6Dot18SubGCircularHollowSection(a=a)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"A_v = \frac{2 \cdot A}{\pi} = "
                r"\frac{2 \cdot 4000.000}{\pi} = 2546.479 \ mm^2",
            ),
            ("short", r"A_v = 2546.479 \ mm^2"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        a = 4000.0

        latex = Form6Dot18SubGCircularHollowSection(a=a).latex()

        actual = {
            "complete": latex.complete,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."
