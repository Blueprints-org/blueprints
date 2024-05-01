"""Formula 5.7a from NEN-EN 1992-1-1+C2:2011: Chapter 5 - Structural Analysis."""

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011 import NEN_EN_1992_1_1_C2_2011
from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011.chapter_5_structural_analysis.formula_5_7ab import Form5Dot7abFlangeEffectiveFlangeWidth


class Form5Dot7aFlangeEffectiveFlangeWidth(Form5Dot7abFlangeEffectiveFlangeWidth):
    """Class representing formula 5.7a for the calculation of effective flange width of the i-th flange [:math:`b_{eff,i}`].
    See Figure 5.3.
    """

    label = "5.7a"
    source_document = NEN_EN_1992_1_1_C2_2011
