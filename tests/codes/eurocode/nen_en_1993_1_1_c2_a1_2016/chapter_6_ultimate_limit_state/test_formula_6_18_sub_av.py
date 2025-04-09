"""Testing subformulas a to g from 6.18 of NEN-EN 1993-1-1+C2+A1:2016."""

import pytest

from blueprints.codes.eurocode.nen_en_1993_1_1_c2_a1_2016.chapter_6_ultimate_limit_state.formula_6_18_sub_av import (
    Form6Dot18SubARolledIandHSection,
    Form6Dot18SubBRolledChannelSection,
    Form6Dot18SubCTSection,
    Form6Dot18SubDWeldedIHandBoxSection,
    Form6Dot18SubEWeldedIHandBoxSection,
    Form6Dot18SubF1RolledRectangularHollowSectionDepth,
    Form6Dot18SubF2RolledRectangularHollowSectionWidth,
    Form6Dot18SubGCircularHollowSection,
)
from blueprints.validations import ListsNotSameLengthError, NegativeValueError


class TestForm6Dot18SubARolledIandHSection:
    """Validation for formula 6.18suba from NEN-EN 1993-1-1+C2+A1:2016."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        a = 10000.0
        b = 200.0
        hw = 250.0
        r = 10.0
        tf = 15.0
        tw = 8.0
        eta = 1.0

        formula = Form6Dot18SubARolledIandHSection(a=a, b=b, hw=hw, r=r, tf=tf, tw=tw, eta=eta)
        manually_calculated_result = 4420.0  # mm^2

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("a", "b", "hw", "r", "tf", "tw", "eta"),
        [
            (-10000.0, 200.0, 250.0, 10.0, 15.0, 8.0, 1.0),  # a is negative
            (10000.0, -200.0, 250.0, 10.0, 15.0, 8.0, 1.0),  # b is negative
            (10000.0, 200.0, -250.0, 10.0, 15.0, 8.0, 1.0),  # hw is negative
            (10000.0, 200.0, 250.0, -10.0, 15.0, 8.0, 1.0),  # r is negative
            (10000.0, 200.0, 250.0, 10.0, -15.0, 8.0, 1.0),  # tf is negative
            (10000.0, 200.0, 250.0, 10.0, 15.0, -8.0, 1.0),  # tw is negative
            (10000.0, 200.0, 250.0, 10.0, 15.0, 8.0, -1.0),  # eta is negative
        ],
    )
    def test_raise_error_when_invalid_values_are_given(self, a: float, b: float, hw: float, r: float, tf: float, tw: float, eta: float) -> None:
        """Test invalid values."""
        with pytest.raises(NegativeValueError):
            Form6Dot18SubARolledIandHSection(a=a, b=b, hw=hw, r=r, tf=tf, tw=tw, eta=eta)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"A_v = max(A - 2 \cdot b \cdot t_f + (t_w + 2 \cdot r) \cdot t_f; \eta \cdot h_w \cdot t_w) = "
                r"max(10000.000 - 2 \cdot 200.000 \cdot 15.000 + (8.000 + 2 \cdot 10.000) \cdot 15.000; 1.000 \cdot 250.000 \cdot 8.000) = "
                r"4420.000 \ mm^2",
            ),
            ("short", r"A_v = 4420.000 \ mm^2"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        a = 10000.0
        b = 200.0
        hw = 250.0
        r = 10.0
        tf = 15.0
        tw = 8.0
        eta = 1.0

        latex = Form6Dot18SubARolledIandHSection(a=a, b=b, hw=hw, r=r, tf=tf, tw=tw, eta=eta).latex()

        actual = {
            "complete": latex.complete,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."


class TestForm6Dot18SubBRolledChannelSection:
    """Validation for formula 6.18subb from NEN-EN 1993-1-1+C2+A1:2016."""

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


class TestForm6Dot18SubCTSection:
    """Validation for formula 6.18subc from NEN-EN 1993-1-1+C2+A1:2016."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        a = 6000.0
        b = 100.0
        tf = 10.0

        formula = Form6Dot18SubCTSection(a=a, b=b, tf=tf)
        manually_calculated_result = 4500.0  # mm^2

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("a", "b", "tf"),
        [
            (-6000.0, 100.0, 10.0),  # a is negative
            (6000.0, -100.0, 10.0),  # b is negative
            (6000.0, 100.0, -10.0),  # tf is negative
        ],
    )
    def test_raise_error_when_invalid_values_are_given(self, a: float, b: float, tf: float) -> None:
        """Test invalid values."""
        with pytest.raises(NegativeValueError):
            Form6Dot18SubCTSection(a=a, b=b, tf=tf)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"A_v = 0.9 \cdot (A - b \cdot t_f) = "
                r"0.9 \cdot (6000.000 - 100.000 \cdot 10.000) = 4500.000 \ mm^2",
            ),
            ("short", r"A_v = 4500.000 \ mm^2"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        a = 6000.0
        b = 100.0
        tf = 10.0

        latex = Form6Dot18SubCTSection(a=a, b=b, tf=tf).latex()

        actual = {
            "complete": latex.complete,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."


class TestForm6Dot18SubDWeldedIHandBoxSection:
    """Validation for formula 6.18subd from NEN-EN 1993-1-1+C2+A1:2016."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        hw = [250.0, 300.0]
        tw = [8.0, 10.0]
        eta = 1.0

        formula = Form6Dot18SubDWeldedIHandBoxSection(hw=hw, tw=tw, eta=eta)
        manually_calculated_result = 5000.0  # mm^2

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("hw", "tw", "eta"),
        [
            ([250.0, -300.0], [8.0, 10.0], 1.0),  # hw contains negative value
            ([250.0, 300.0], [8.0, -10.0], 1.0),  # tw contains negative value
            ([250.0, 300.0], [8.0, 10.0], -1.0),  # eta is negative
            ([250.0], [8.0, 10.0], 1.0),  # hw and tw are not the same length
        ],
    )
    def test_raise_error_when_invalid_values_are_given(self, hw: list[float], tw: list[float], eta: float) -> None:
        """Test invalid values."""
        with pytest.raises((NegativeValueError, ListsNotSameLengthError)):
            Form6Dot18SubDWeldedIHandBoxSection(hw=hw, tw=tw, eta=eta)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"A_v = \eta \cdot \sum (h_{w0} \cdot t_{w0} + h_{w1} \cdot t_{w1}) = "
                r"1.000 \cdot (250.000 \cdot 8.000 + 300.000 \cdot 10.000) = 5000.000 \ mm^2",
            ),
            ("short", r"A_v = 5000.000 \ mm^2"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        hw = [250.0, 300.0]
        tw = [8.0, 10.0]
        eta = 1.0

        latex = Form6Dot18SubDWeldedIHandBoxSection(hw=hw, tw=tw, eta=eta).latex()

        actual = {
            "complete": latex.complete,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."


class TestForm6Dot18SubEWeldedIHandBoxSection:
    """Validation for formula 6.18sube from NEN-EN 1993-1-1+C2+A1:2016."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        a = 12000.0
        hw = [250.0, 300.0]
        tw = [8.0, 10.0]

        formula = Form6Dot18SubEWeldedIHandBoxSection(a=a, hw=hw, tw=tw)
        manually_calculated_result = 7000.0  # mm^2

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("a", "hw", "tw"),
        [
            (-12000.0, [250.0, 300.0], [8.0, 10.0]),  # a is negative
            (12000.0, [250.0, -300.0], [8.0, 10.0]),  # hw contains negative value
            (12000.0, [250.0, 300.0], [8.0, -10.0]),  # tw contains negative value
            (12000.0, [250.0, 300.0], [8.0, 10.0, 12.0]),  # hw and tw are not the same length
        ],
    )
    def test_raise_error_when_invalid_values_are_given(self, a: float, hw: list[float], tw: list[float]) -> None:
        """Test invalid values."""
        with pytest.raises((NegativeValueError, ListsNotSameLengthError)):
            Form6Dot18SubEWeldedIHandBoxSection(a=a, hw=hw, tw=tw)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"A_v = A - \sum (h_{w0} \cdot t_{w0} + h_{w1} \cdot t_{w1}) = "
                r"12000.000 - (250.000 \cdot 8.000 + 300.000 \cdot 10.000) = 7000.000 \ mm^2",
            ),
            ("short", r"A_v = 7000.000 \ mm^2"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        a = 12000.0
        hw = [250.0, 300.0]
        tw = [8.0, 10.0]

        latex = Form6Dot18SubEWeldedIHandBoxSection(a=a, hw=hw, tw=tw).latex()

        actual = {
            "complete": latex.complete,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."


class TestForm6Dot18SubF1RolledRectangularHollowSectionDepth:
    """Validation for formula 6.18subf1 from NEN-EN 1993-1-1+C2+A1:2016."""

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
    """Validation for formula 6.18subf2 from NEN-EN 1993-1-1+C2+A1:2016."""

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
    """Validation for formula 6.18subg from NEN-EN 1993-1-1+C2+A1:2016."""

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
