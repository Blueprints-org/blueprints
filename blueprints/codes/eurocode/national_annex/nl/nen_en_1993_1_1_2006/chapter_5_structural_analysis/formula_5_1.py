"""Formula 5.1 from NEN-EN 1993-1-1:2006: Chapter 5 - Structural Analysis."""

from typing import Literal

from blueprints.codes.eurocode.en_1993_1_1_2005.chapter_5_structural_analysis.formula_5_1 import Form5Dot1CriteriumDisregardSecondOrderEffects
from blueprints.codes.eurocode.national_annex.nl.nen_en_1993_1_1_2006 import NEN_EN_1993_1_1_2006_A1_2014_NB_2016
from blueprints.type_alias import N


class Form5Dot1NLCriteriumDisregardSecondOrderEffects(Form5Dot1CriteriumDisregardSecondOrderEffects):
    r"""Class representing formula 5.1 to check whether second order effects of a structure can be disregarded
    or not.

    This is the Dutch National Annex version which modifies the base Eurocode values.

    Source: NEN-EN 1993-1-1:2006+A1:2014+NB:2016 - Formula 5.1

    Notes
    -----
    This formula is based on NEN-EN 1993-1-1:2006+A1:2014+NB:2016.
    Previous versions (NEN-EN 1993-1-1:2006) may have different values.
    """

    label = "5.1"
    source_document = NEN_EN_1993_1_1_2006_A1_2014_NB_2016

    def __init__(self, f_cr: N, f_ed: N, analysis_type: Literal["elastic", "plastic"]) -> None:
        r"""Check if second order effects of a structure can be disregarded.

        NEN-EN 1993-1-1:2006 - Formula (5.1)

        Parameters
        ----------
        f_cr: N
            [$F_{cr}$] Elastic critical buckling load for global instability mode based on initial elastic stiffness.
        f_ed: N
            [$F_{Ed}$] Design loading on the structure.
        analysis_type: Literal["elastic", "plastic"]
            Type of analysis being performed (elastic or plastic).
        """
        super().__init__(f_cr, f_ed, analysis_type)

    @staticmethod
    def _limit(analysis_type: Literal["elastic", "plastic"]) -> float:
        """Returns the limit value for the comparison based on the analysis type."""
        analysis_type_map = {
            "elastic": 10,
            "plastic": 10,
        }

        limit = analysis_type_map.get(analysis_type.lower())

        if limit is None:
            raise ValueError(f"Invalid analysis type: {analysis_type}. Must be 'elastic' or 'plastic'.")
        return limit

    @staticmethod
    def _evaluate_rhs(analysis_type: Literal["elastic", "plastic"], *_args, **_kwargs) -> float:
        """Evaluates the right-hand side of the comparison. See __init__ for details."""
        return Form5Dot1NLCriteriumDisregardSecondOrderEffects._limit(analysis_type=analysis_type)
