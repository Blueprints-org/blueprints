"""Subformula a trough g from 6.18 from EN 1993-1-1:2005: Chapter 6 - Ultimate Limit State."""

import numpy as np

from blueprints.codes.eurocode.en_1993_1_1_2005 import EN_1993_1_1_2005
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import DIMENSIONLESS, MM, MM2
from blueprints.validations import raise_if_less_or_equal_to_zero, raise_if_lists_differ_in_length, raise_if_negative


class Form6Dot18SubARolledIandHSection(Formula):
    r"""Class representing formula 6.18suba for the calculation of shear area for a rolled I and H section.

    The equations has been slightly modified to split effects of top and bottom flange.
    """

    label = "6.18suba"
    source_document = EN_1993_1_1_2005

    def __init__(
        self,
        a: MM2,
        b1: MM,
        b2: MM,
        hw: MM,
        r1: MM,
        r2: MM,
        tf1: MM,
        tf2: MM,
        tw: MM,
        eta: DIMENSIONLESS,
    ) -> None:
        r"""[$A_v$] Calculation of the shear area for a rolled I and H section with load parallel to web [$mm^2$].

        EN 1993-1-1:2005 art.6.2.6(3) - Formula (6.18suba)

        Parameters
        ----------
        a : MM2
            [$A$] Cross-sectional area [$mm^2$].
        b1 : MM
            [$b$] Overall breadth of flange 1 [$mm$].
        b2 : MM
            [$b$] Overall breadth of flange 2 [$mm$].
        hw : MM
            [$h_w$] Depth of the web [$mm$].
        r1 : MM
            [$r$] Root radius at flange 1 [$mm$].
        r2 : MM
            [$r$] Root radius at flange 2 [$mm$].
        tf1 : MM
            [$t_f$] Flange thickness 1 [$mm$].
        tf2 : MM
            [$t_f$] Flange thickness 2 [$mm$].
        tw : MM
            [$t_w$] Web thickness [$mm$]. If the web thickness is not constant, tw should be taken as the minimum thickness.
        eta : DIMENSIONLESS, optional
            [$\eta$] Dimensionless conversionfactor, see EN 1993-1-5 5.1. Note, $eta$ may be conservatively taken equal to 1.0.
        """
        super().__init__()
        self.a = a
        self.b1 = b1
        self.b2 = b2
        self.hw = hw
        self.r1 = r1
        self.r2 = r2
        self.tf1 = tf1
        self.tf2 = tf2
        self.tw = tw
        self.eta = eta

    @staticmethod
    def _evaluate(
        a: MM2,
        b1: MM,
        b2: MM,
        hw: MM,
        r1: MM,
        r2: MM,
        tf1: MM,
        tf2: MM,
        tw: MM,
        eta: DIMENSIONLESS,
    ) -> MM2:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(a=a, b1=b1, b2=b2, hw=hw, r1=r1, r2=r2, tf1=tf1, tf2=tf2, tw=tw, eta=eta)

        av = a - b1 * tf1 - b2 * tf2 + (tw + 2 * r1) * tf1 / 2 + (tw + 2 * r2) * tf2 / 2
        av_min = eta * hw * tw

        return max(0, av, av_min)

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 6.18suba."""
        _equation: str = (
            r"max(A - b_1 \cdot t_{f1} - b_2 \cdot t_{f2} + (t_w + 2 \cdot r_1) \cdot \frac{t_{f1}}{2} + "
            r"(t_w + 2 \cdot r_2) \cdot \frac{t_{f2}}{2}; \eta \cdot h_w \cdot t_w)"
        )
        _numeric_equation: str = latex_replace_symbols(
            _equation,
            {
                r"A": f"{self.a:.{n}f}",
                r"b_1": f"{self.b_1:.{n}f}",
                r"b_2": f"{self.b_2:.{n}f}",
                r"h_w": f"{self.hw:.{n}f}",
                r"r_1": f"{self.r_1:.{n}f}",
                r"r_2": f"{self.r_2:.{n}f}",
                r"t_{f1}": f"{self.tf_1:.{n}f}",
                r"t_{f2}": f"{self.tf_2:.{n}f}",
                r"t_w": f"{self.tw:.{n}f}",
                r"\eta": f"{self.eta:.{n}f}",
            },
            False,
        )
        return LatexFormula(
            return_symbol=r"A_v",
            result=f"{self:.{n}f}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            comparison_operator_label="=",
            unit="mm^2",
        )


class Form6Dot18SubBRolledChannelSection(Formula):
    r"""Class representing formula 6.18subb for the calculation of shear area for a rolled channel section."""

    label = "6.18subb"
    source_document = EN_1993_1_1_2005

    def __init__(
        self,
        a: MM2,
        b: MM,
        tf: MM,
        tw: MM,
        r: MM,
    ) -> None:
        r"""[$A_v$] Calculation of the shear area for a rolled channel section with load parallel to web [$mm^2$].

        EN 1993-1-1:2005 art.6.2.6(3) - Formula (6.18subb)

        Parameters
        ----------
        a : MM2
            [$A$] Cross-sectional area [$mm^2$].
        b : MM
            [$b$] Overall breadth [$mm$].
        tf : MM
            [$t_f$] Flange thickness [$mm$].
        tw : MM
            [$t_w$] Web thickness [$mm$]. If the web thickness is not constant, tw should be taken as the minimum thickness.
        r : MM
            [$r$] Root radius [$mm$].
        """
        super().__init__()
        self.a = a
        self.b = b
        self.tf = tf
        self.tw = tw
        self.r = r

    @staticmethod
    def _evaluate(
        a: MM2,
        b: MM,
        tf: MM,
        tw: MM,
        r: MM,
    ) -> MM2:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(a=a, b=b, tf=tf, tw=tw, r=r)

        return max(0, a - 2 * b * tf + (tw + r) * tf)

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 6.18subb."""
        _equation: str = r"A - 2 \cdot b \cdot t_f + (t_w + r) \cdot t_f"
        _numeric_equation: str = latex_replace_symbols(
            _equation,
            {
                r"A": f"{self.a:.{n}f}",
                r"b": f"{self.b:.{n}f}",
                r"t_f": f"{self.tf:.{n}f}",
                r"t_w": f"{self.tw:.{n}f}",
                r"r": f"{self.r:.{n}f}",
            },
            False,
        )
        return LatexFormula(
            return_symbol=r"A_v",
            result=f"{self:.{n}f}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            comparison_operator_label="=",
            unit="mm^2",
        )


class Form6Dot18SubCTSectionRolled(Formula):
    r"""Class representing formula 6.18subc for the calculation of shear area for a rolled T-section with load parallel to web."""

    label = "6.18subc"
    source_document = EN_1993_1_1_2005

    def __init__(
        self,
        a: MM2,
        b: MM,
        tf: MM,
        tw: MM,
        r: MM,
    ) -> None:
        r"""[$A_v$] Calculation of the shear area for a T-section with load parallel to web [$mm^2$].

        EN 1993-1-1:2005 art.6.2.6(3) - Formula (6.18subc)

        Parameters
        ----------
        a : MM2
            [$A$] Cross-sectional area [$mm^2$].
        b : MM
            [$b$] Overall breadth [$mm$].
        tf : MM
            [$t_f$] Flange thickness [$mm$].
        tw : MM
            [$t_w$] Web thickness [$mm$]. If the web thickness is not constant, tw should be taken as the minimum thickness.
        r : MM
            [$r$] Root radius [$mm$].
        """
        super().__init__()
        self.a = a
        self.b = b
        self.tf = tf
        self.tw = tw
        self.r = r

    @staticmethod
    def _evaluate(
        a: MM2,
        b: MM,
        tf: MM,
        tw: MM,
        r: MM,
    ) -> MM2:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(a=a, b=b, tf=tf, tw=tw, r=r)

        return max(0, a - b * tf + (tw + 2 * r) * tf / 2)

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 6.18subc."""
        _equation: str = r"A - b \cdot t_f + (t_w + 2 \cdot r) \cdot \frac{t_f}{2}"
        _numeric_equation: str = latex_replace_symbols(
            _equation,
            {
                r"A": f"{self.a:.{n}f}",
                r"b": f"{self.b:.{n}f}",
                r"t_f": f"{self.tf:.{n}f}",
                r"t_w": f"{self.tw:.{n}f}",
                r" r": f" {self.r:.{n}f}",
            },
            False,
        )
        return LatexFormula(
            return_symbol=r"A_v",
            result=f"{self:.{n}f}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            comparison_operator_label="=",
            unit="mm^2",
        )


class Form6Dot18SubCTSectionWelded(Formula):
    r"""Class representing formula 6.18subc for the calculation of shear area for a welded T-section with load parallel to web."""

    label = "6.18subc"
    source_document = EN_1993_1_1_2005

    def __init__(
        self,
        tf: MM,
        tw: MM,
        h: MM,
    ) -> None:
        r"""[$A_v$] Calculation of the shear area for a T-section with load parallel to web [$mm^2$].

        EN 1993-1-1:2005 art.6.2.6(3) - Formula (6.18subc)

        Parameters
        ----------
        tf : MM
            [$t_f$] Flange thickness [$mm$].
        tw : MM
            [$t_w$] Web thickness [$mm$]. If the web thickness is not constant, tw should be taken as the minimum thickness.
        h : MM
            [$h$] Overall depth [$mm$].
        """
        super().__init__()
        self.tf = tf
        self.tw = tw
        self.h = h

    @staticmethod
    def _evaluate(
        tf: MM,
        tw: MM,
        h: MM,
    ) -> MM2:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(tf=tf, tw=tw, h=h)

        return max(0, tw * (h * tf / 2))

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 6.18subc."""
        _equation: str = r"t_w \cdot (h \cdot t_f / 2)"
        _numeric_equation: str = latex_replace_symbols(
            _equation,
            {
                r"t_f": f"{self.tf:.{n}f}",
                r"t_w": f"{self.tw:.{n}f}",
                r"h": f"{self.h:.{n}f}",
            },
            False,
        )
        return LatexFormula(
            return_symbol=r"A_v",
            result=f"{self:.{n}f}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            comparison_operator_label="=",
            unit="mm^2",
        )


class Form6Dot18SubDWeldedIHandBoxSection(Formula):
    r"""Class representing formula 6.18subd for the calculation of shear area for welded I, H, and box sections with load parallel to web."""

    label = "6.18subd"
    source_document = EN_1993_1_1_2005

    def __init__(
        self,
        hw_list: list[MM],
        tw_list: list[MM],
        eta: DIMENSIONLESS,
    ) -> None:
        r"""[$A_v$] Calculation of the shear area for welded I, H, and box sections with load parallel to web [$mm^2$].

        EN 1993-1-1:2005 art.6.2.6(3) - Formula (6.18subd)

        Parameters
        ----------
        hw_list : list[MM]
            [$h_w$] List of depths of the web [$mm$].
        tw_list : list[MM]
            [$t_w$] List of web thicknesses [$mm$]. If the web thickness is not constant, tw should be taken as the minimum thickness.
        eta : DIMENSIONLESS
            [$\eta$] See EN 1993-1-5. Note, $eta$ may be conservatively taken equal to 1.0.
        """
        super().__init__()
        self.hw_list: list[MM] = hw_list
        self.tw_list: list[MM] = tw_list
        self.eta = eta

    @staticmethod
    def _evaluate(
        hw_list: list[MM],
        tw_list: list[MM],
        eta: DIMENSIONLESS,
    ) -> MM2:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(eta=eta)
        for h, t in zip(hw_list, tw_list):
            raise_if_negative(h=h, t=t)
        raise_if_lists_differ_in_length(hw_list=hw_list, tw_list=tw_list)

        return max(0, eta * sum(h * t for h, t in zip(hw_list, tw_list)))

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 6.18subd."""
        _equation: str = r"\eta \cdot \sum (h_{w} \cdot t_{w})"
        _numeric_equation: str = rf"{self.eta:.{n}f} \cdot (" + rf"{self.hw_list[0]:.{n}f} \cdot {self.tw_list[0]:.{n}f}"
        for i in range(1, len(self.hw_list)):
            _numeric_equation += rf" + {self.hw_list[i]:.{n}f} \cdot {self.tw_list[i]:.{n}f}"
        _numeric_equation += ")"
        return LatexFormula(
            return_symbol=r"A_v",
            result=f"{self:.{n}f}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            comparison_operator_label="=",
            unit="mm^2",
        )


class Form6Dot18SubEWeldedIHandBoxSection(Formula):
    r"""Class representing formula 6.18sube for the calculation of shear area for welded I, H, channel, and box sections with
    load parallel to flanges.
    """

    label = "6.18sube"
    source_document = EN_1993_1_1_2005

    def __init__(
        self,
        a: MM2,
        hw_list: list[MM],
        tw_list: list[MM],
    ) -> None:
        r"""[$A_v$] Calculation of the shear area for welded I, H, channel, and box sections with load parallel to flanges [$mm^2$].

        EN 1993-1-1:2005 art.6.2.6(3) - Formula (6.18sube)

        Parameters
        ----------
        a : MM2
            [$A$] Cross-sectional area [$mm^2$].
        hw_list : list[MM]
            [$h_w$] List of depths of the web [$mm$].
        tw_list : list[MM]
            [$t_w$] List of web thicknesses [$mm$]. If the web thickness is not constant, tw should be taken as the minimum thickness.
        """
        super().__init__()
        self.a = a
        self.hw_list: list[MM] = hw_list
        self.tw_list: list[MM] = tw_list

    @staticmethod
    def _evaluate(
        a: MM2,
        hw_list: list[MM],
        tw_list: list[MM],
    ) -> MM2:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(a=a)
        for h, t in zip(hw_list, tw_list):
            raise_if_negative(h=h, t=t)
        raise_if_lists_differ_in_length(hw=hw_list, tw_list=tw_list)

        return max(0, a - sum(h * t for h, t in zip(hw_list, tw_list)))

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 6.18sube."""
        _equation: str = r"A - \sum (h_{w} \cdot t_{w})"
        _numeric_equation: str = rf"{self.a:.{n}f} - (" + rf"{self.hw_list[0]:.{n}f} \cdot {self.tw_list[0]:.{n}f}"
        for i in range(1, len(self.hw_list)):
            _numeric_equation += rf" + {self.hw_list[i]:.{n}f} \cdot {self.tw_list[i]:.{n}f}"
        _numeric_equation += ")"
        return LatexFormula(
            return_symbol=r"A_v",
            result=f"{self:.{n}f}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            comparison_operator_label="=",
            unit="mm^2",
        )


class Form6Dot18SubF1RolledRectangularHollowSectionDepth(Formula):
    r"""Class representing formula 6.18subf1 for the calculation of shear area for rolled rectangular hollow sections of uniform thickness with
    load parallel to depth.
    """

    label = "6.18subf1"
    source_document = EN_1993_1_1_2005

    def __init__(
        self,
        a: MM2,
        b: MM,
        h: MM,
    ) -> None:
        r"""[$A_v$] Calculation of the shear area for rolled rectangular hollow sections of uniform thickness with load parallel to depth [$mm^2$].

        EN 1993-1-1:2005 art.6.2.6(3) - Formula (6.18subf1)

        Parameters
        ----------
        a : MM2
            [$A$] Cross-sectional area [$mm^2$].
        b : MM
            [$b$] Overall breadth [$mm$].
        h : MM
            [$h$] Overall depth [$mm$].
        """
        super().__init__()
        self.a = a
        self.b = b
        self.h = h

    @staticmethod
    def _evaluate(
        a: MM2,
        b: MM,
        h: MM,
    ) -> MM2:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(a=a, b=b, h=h)
        denominator = b + h
        raise_if_less_or_equal_to_zero(denominator=denominator)
        return max(0, a * h / (b + h))

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 6.18subf1."""
        _equation: str = r"\frac{A \cdot h}{b + h}"
        _numeric_equation: str = latex_replace_symbols(
            _equation,
            {
                r"A": f"{self.a:.{n}f}",
                r"b": f"{self.b:.{n}f}",
                r"h": f"{self.h:.{n}f}",
            },
            False,
        )
        return LatexFormula(
            return_symbol=r"A_v",
            result=f"{self:.{n}f}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            comparison_operator_label="=",
            unit="mm^2",
        )


class Form6Dot18SubF2RolledRectangularHollowSectionWidth(Formula):
    r"""Class representing formula 6.18subf2 for the calculation of shear area for rolled rectangular hollow sections of uniform thickness with
    load parallel to width.
    """

    label = "6.18subf2"
    source_document = EN_1993_1_1_2005

    def __init__(
        self,
        a: MM2,
        b: MM,
        h: MM,
    ) -> None:
        r"""[$A_v$] Calculation of the shear area for rolled rectangular hollow sections of uniform thickness with load parallel to width [$mm^2$].

        EN 1993-1-1:2005 art.6.2.6(3) - Formula (6.18subf2)

        Parameters
        ----------
        a : MM2
            [$A$] Cross-sectional area [$mm^2$].
        b : MM
            [$b$] Overall breadth [$mm$].
        h : MM
            [$h$] Overall depth [$mm$].
        """
        super().__init__()
        self.a = a
        self.b = b
        self.h = h

    @staticmethod
    def _evaluate(
        a: MM2,
        b: MM,
        h: MM,
    ) -> MM2:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(a=a, b=b, h=h)
        denominator = b + h
        raise_if_less_or_equal_to_zero(denominator=denominator)
        return max(0, a * b / (b + h))

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 6.18subf2."""
        _equation: str = r"\frac{A \cdot b}{b + h}"
        _numeric_equation: str = latex_replace_symbols(
            _equation,
            {
                r"A": f"{self.a:.{n}f}",
                r"b": f"{self.b:.{n}f}",
                r"h": f"{self.h:.{n}f}",
            },
            False,
        )
        return LatexFormula(
            return_symbol=r"A_v",
            result=f"{self:.{n}f}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            comparison_operator_label="=",
            unit="mm^2",
        )


class Form6Dot18SubGCircularHollowSection(Formula):
    r"""Class representing formula 6.18subg for the calculation of shear area for circular hollow sections and tubes of uniform thickness."""

    label = "6.18subg"
    source_document = EN_1993_1_1_2005

    def __init__(
        self,
        a: MM2,
    ) -> None:
        r"""[$A_v$] Calculation of the shear area for circular hollow sections and tubes of uniform thickness [$mm^2$].

        EN 1993-1-1:2005 art.6.2.6(3) - Formula (6.18subg)

        Parameters
        ----------
        a : MM2
            [$A$] Cross-sectional area [$mm^2$].
        """
        super().__init__()
        self.a = a

    @staticmethod
    def _evaluate(
        a: MM2,
    ) -> MM2:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(a=a)

        return max(0, 2 * a / np.pi)

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 6.18subg."""
        _equation: str = r"\frac{2 \cdot A}{\pi}"
        _numeric_equation: str = latex_replace_symbols(
            _equation,
            {
                r"A": f"{self.a:.{n}f}",
            },
            False,
        )
        return LatexFormula(
            return_symbol=r"A_v",
            result=f"{self:.{n}f}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            comparison_operator_label="=",
            unit="mm^2",
        )
