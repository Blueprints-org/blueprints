"""Subformula a trough g from 6.18 from NEN-EN 1993-1-1+C2+A1:2016: Chapter 6 - Ultimate Limit State."""

import numpy as np

from blueprints.codes.eurocode.nen_en_1993_1_1_c2_a1_2016 import NEN_EN_1993_1_1_C2_A1_2016
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import DIMENSIONLESS, MM, MM2
from blueprints.validations import raise_if_lists_differ_in_length, raise_if_negative


class Form6Dot18SubARolledIandHSection(Formula):
    r"""Class representing formula 6.18suba for the calculation of shear area for a rolled I and H section."""

    label = "6.18suba"
    source_document = NEN_EN_1993_1_1_C2_A1_2016

    def __init__(
        self,
        a: MM2,
        b: MM,
        hw: MM,
        r: MM,
        tf: MM,
        tw: MM,
        eta: DIMENSIONLESS,
    ) -> None:
        r"""[$A_v$] Calculation of the shear area for a rolled I and H section with load parallel to web [$mm^2$].

        NEN-EN 1993-1-1+C2+A1:2016 art.6.2.6(3) - Formula (6.18suba)

        Parameters
        ----------
        a : MM2
            [$A$] Cross-sectional area [$mm^2$].
        b : MM
            [$b$] Overall breadth [$mm$].
        hw : MM
            [$h_w$] Depth of the web [$mm$].
        r : MM
            [$r$] Root radius [$mm$].
        tf : MM
            [$t_f$] Flange thickness [$mm$].
        tw : MM
            [$t_w$] Web thickness [$mm$]. If the web thickness is not constant, tw should be taken as the minimum thickness.
        eta : DIMENSIONLESS, optional
            [$\eta$] See EN 1993-1-5. Note, $eta$ may be conservatively taken equal to 1.0.
        """
        super().__init__()
        self.a = a
        self.b = b
        self.hw = hw
        self.r = r
        self.tf = tf
        self.tw = tw
        self.eta = eta

    @staticmethod
    def _evaluate(
        a: MM2,
        b: MM,
        hw: MM,
        r: MM,
        tf: MM,
        tw: MM,
        eta: DIMENSIONLESS,
    ) -> MM2:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(a=a, b=b, hw=hw, r=r, tf=tf, tw=tw, eta=eta)

        av = a - 2 * b * tf + (tw + 2 * r) * tf
        av_min = eta * hw * tw

        return max(av, av_min)

    def latex(self) -> LatexFormula:
        """Returns LatexFormula object for formula 6.18suba."""
        _equation: str = r"max(A - 2 \cdot b \cdot t_f + (t_w + 2 \cdot r) \cdot t_f; \eta \cdot h_w \cdot t_w)"
        _numeric_equation: str = latex_replace_symbols(
            _equation,
            {
                r"A": f"{self.a:.3f}",
                r"b": f"{self.b:.3f}",
                r"h_w": f"{self.hw:.3f}",
                r"r": f"{self.r:.3f}",
                r"t_f": f"{self.tf:.3f}",
                r"t_w": f"{self.tw:.3f}",
                r"\eta": f"{self.eta:.3f}",
            },
            False,
        )
        return LatexFormula(
            return_symbol=r"A_v",
            result=f"{self:.3f}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            comparison_operator_label="=",
            unit="mm^2",
        )


class Form6Dot18SubBRolledChannelSection(Formula):
    r"""Class representing formula 6.18subb for the calculation of shear area for a rolled channel section."""

    label = "6.18subb"
    source_document = NEN_EN_1993_1_1_C2_A1_2016

    def __init__(
        self,
        a: MM2,
        b: MM,
        tf: MM,
        tw: MM,
        r: MM,
    ) -> None:
        r"""[$A_v$] Calculation of the shear area for a rolled channel section with load parallel to web [$mm^2$].

        NEN-EN 1993-1-1+C2+A1:2016 art.6.2.6(3) - Formula (6.18subb)

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

        return a - 2 * b * tf + (tw + r) * tf

    def latex(self) -> LatexFormula:
        """Returns LatexFormula object for formula 6.18subb."""
        _equation: str = r"A - 2 \cdot b \cdot t_f + (t_w + r) \cdot t_f"
        _numeric_equation: str = latex_replace_symbols(
            _equation,
            {
                r"A": f"{self.a:.3f}",
                r"b": f"{self.b:.3f}",
                r"t_f": f"{self.tf:.3f}",
                r"t_w": f"{self.tw:.3f}",
                r"r": f"{self.r:.3f}",
            },
            False,
        )
        return LatexFormula(
            return_symbol=r"A_v",
            result=f"{self:.3f}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            comparison_operator_label="=",
            unit="mm^2",
        )


class Form6Dot18SubCTSection(Formula):
    r"""Class representing formula 6.18subc for the calculation of shear area for a T-section with load parallel to web."""

    label = "6.18subc"
    source_document = NEN_EN_1993_1_1_C2_A1_2016

    def __init__(
        self,
        a: MM2,
        b: MM,
        tf: MM,
    ) -> None:
        r"""[$A_v$] Calculation of the shear area for a T-section with load parallel to web [$mm^2$].

        NEN-EN 1993-1-1+C2+A1:2016 art.6.2.6(3) - Formula (6.18subc)

        Parameters
        ----------
        a : MM2
            [$A$] Cross-sectional area [$mm^2$].
        b : MM
            [$b$] Overall breadth [$mm$].
        tf : MM
            [$t_f$] Flange thickness [$mm$].
        """
        super().__init__()
        self.a = a
        self.b = b
        self.tf = tf

    @staticmethod
    def _evaluate(
        a: MM2,
        b: MM,
        tf: MM,
    ) -> MM2:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(a=a, b=b, tf=tf)

        return 0.9 * (a - b * tf)

    def latex(self) -> LatexFormula:
        """Returns LatexFormula object for formula 6.18subc."""
        _equation: str = r"0.9 \cdot (A - b \cdot t_f)"
        _numeric_equation: str = latex_replace_symbols(
            _equation,
            {
                r"A": f"{self.a:.3f}",
                r"b": f"{self.b:.3f}",
                r"t_f": f"{self.tf:.3f}",
            },
            False,
        )
        return LatexFormula(
            return_symbol=r"A_v",
            result=f"{self:.3f}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            comparison_operator_label="=",
            unit="mm^2",
        )


class Form6Dot18SubDWeldedIHandBoxSection(Formula):
    r"""Class representing formula 6.18subd for the calculation of shear area for welded I, H, and box sections with load parallel to web."""

    label = "6.18subd"
    source_document = NEN_EN_1993_1_1_C2_A1_2016

    def __init__(
        self,
        hw: list[MM],
        tw: list[MM],
        eta: DIMENSIONLESS,
    ) -> None:
        r"""[$A_v$] Calculation of the shear area for welded I, H, and box sections with load parallel to web [$mm^2$].

        NEN-EN 1993-1-1+C2+A1:2016 art.6.2.6(3) - Formula (6.18subd)

        Parameters
        ----------
        hw : list[MM]
            [$h_w$] List of depths of the web [$mm$].
        tw : list[MM]
            [$t_w$] List of web thicknesses [$mm$]. If the web thickness is not constant, tw should be taken as the minimum thickness.
        eta : DIMENSIONLESS
            [$\eta$] See EN 1993-1-5. Note, $eta$ may be conservatively taken equal to 1.0.
        """
        super().__init__()
        self.hw = hw
        self.tw = tw
        self.eta = eta

    @staticmethod
    def _evaluate(
        hw: list[MM],
        tw: list[MM],
        eta: DIMENSIONLESS,
    ) -> MM2:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(eta=eta)
        for h, t in zip(hw, tw):
            raise_if_negative(h=h, t=t)
        raise_if_lists_differ_in_length(hw=hw, tw=tw)

        return eta * sum(h * t for h, t in zip(hw, tw))

    def latex(self) -> LatexFormula:
        """Returns LatexFormula object for formula 6.18subd."""
        _equation: str = r"\eta \cdot \sum (h_{w0} \cdot t_{w0}"
        for i in range(1, len(self.hw)):
            _equation += rf" + h_{{w{i}}} \cdot t_{{w{i}}}"
        _equation += ")"
        _numeric_equation: str = rf"{self.eta:.3f} \cdot (" + rf"{self.hw[0]:.3f} \cdot {self.tw[0]:.3f}"
        for i in range(1, len(self.hw)):
            _numeric_equation += rf" + {self.hw[i]:.3f} \cdot {self.tw[i]:.3f}"
        _numeric_equation += ")"
        return LatexFormula(
            return_symbol=r"A_v",
            result=f"{self:.3f}",
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
    source_document = NEN_EN_1993_1_1_C2_A1_2016

    def __init__(
        self,
        a: MM2,
        hw: list[MM],
        tw: list[MM],
    ) -> None:
        r"""[$A_v$] Calculation of the shear area for welded I, H, channel, and box sections with load parallel to flanges [$mm^2$].

        NEN-EN 1993-1-1+C2+A1:2016 art.6.2.6(3) - Formula (6.18sube)

        Parameters
        ----------
        a : MM2
            [$A$] Cross-sectional area [$mm^2$].
        hw : list[MM]
            [$h_w$] List of depths of the web [$mm$].
        tw : list[MM]
            [$t_w$] List of web thicknesses [$mm$]. If the web thickness is not constant, tw should be taken as the minimum thickness.
        """
        super().__init__()
        self.a = a
        self.hw = hw
        self.tw = tw

    @staticmethod
    def _evaluate(
        a: MM2,
        hw: list[MM],
        tw: list[MM],
    ) -> MM2:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(a=a)
        for h, t in zip(hw, tw):
            raise_if_negative(h=h, t=t)
        raise_if_lists_differ_in_length(hw=hw, tw=tw)

        return a - sum(h * t for h, t in zip(hw, tw))

    def latex(self) -> LatexFormula:
        """Returns LatexFormula object for formula 6.18sube."""
        _equation: str = r"A - \sum (h_{w0} \cdot t_{w0}"
        for i in range(1, len(self.hw)):
            _equation += rf" + h_{{w{i}}} \cdot t_{{w{i}}}"
        _equation += ")"
        _numeric_equation: str = rf"{self.a:.3f} - (" + rf"{self.hw[0]:.3f} \cdot {self.tw[0]:.3f}"
        for i in range(1, len(self.hw)):
            _numeric_equation += rf" + {self.hw[i]:.3f} \cdot {self.tw[i]:.3f}"
        _numeric_equation += ")"
        return LatexFormula(
            return_symbol=r"A_v",
            result=f"{self:.3f}",
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
    source_document = NEN_EN_1993_1_1_C2_A1_2016

    def __init__(
        self,
        a: MM2,
        b: MM,
        h: MM,
    ) -> None:
        r"""[$A_v$] Calculation of the shear area for rolled rectangular hollow sections of uniform thickness with load parallel to depth [$mm^2$].

        NEN-EN 1993-1-1+C2+A1:2016 art.6.2.6(3) - Formula (6.18subf1)

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

        return a * h / (b + h)

    def latex(self) -> LatexFormula:
        """Returns LatexFormula object for formula 6.18subf1."""
        _equation: str = r"\frac{A \cdot h}{b + h}"
        _numeric_equation: str = latex_replace_symbols(
            _equation,
            {
                r"A": f"{self.a:.3f}",
                r"b": f"{self.b:.3f}",
                r"h": f"{self.h:.3f}",
            },
            False,
        )
        return LatexFormula(
            return_symbol=r"A_v",
            result=f"{self:.3f}",
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
    source_document = NEN_EN_1993_1_1_C2_A1_2016

    def __init__(
        self,
        a: MM2,
        b: MM,
        h: MM,
    ) -> None:
        r"""[$A_v$] Calculation of the shear area for rolled rectangular hollow sections of uniform thickness with load parallel to width [$mm^2$].

        NEN-EN 1993-1-1+C2+A1:2016 art.6.2.6(3) - Formula (6.18subf2)

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

        return a * b / (b + h)

    def latex(self) -> LatexFormula:
        """Returns LatexFormula object for formula 6.18subf2."""
        _equation: str = r"\frac{A \cdot b}{b + h}"
        _numeric_equation: str = latex_replace_symbols(
            _equation,
            {
                r"A": f"{self.a:.3f}",
                r"b": f"{self.b:.3f}",
                r"h": f"{self.h:.3f}",
            },
            False,
        )
        return LatexFormula(
            return_symbol=r"A_v",
            result=f"{self:.3f}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            comparison_operator_label="=",
            unit="mm^2",
        )


class Form6Dot18SubGCircularHollowSection(Formula):
    r"""Class representing formula 6.18subg for the calculation of shear area for circular hollow sections and tubes of uniform thickness."""

    label = "6.18subg"
    source_document = NEN_EN_1993_1_1_C2_A1_2016

    def __init__(
        self,
        a: MM2,
    ) -> None:
        r"""[$A_v$] Calculation of the shear area for circular hollow sections and tubes of uniform thickness [$mm^2$].

        NEN-EN 1993-1-1+C2+A1:2016 art.6.2.6(3) - Formula (6.18subg)

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

        return 2 * a / np.pi

    def latex(self) -> LatexFormula:
        """Returns LatexFormula object for formula 6.18subg."""
        _equation: str = r"\frac{2 \cdot A}{\pi}"
        _numeric_equation: str = latex_replace_symbols(
            _equation,
            {
                r"A": f"{self.a:.3f}",
            },
            False,
        )
        return LatexFormula(
            return_symbol=r"A_v",
            result=f"{self:.3f}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            comparison_operator_label="=",
            unit="mm^2",
        )
