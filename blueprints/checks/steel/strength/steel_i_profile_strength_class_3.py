"""Steel I-Profile strength check according to Eurocode 3.

This module provides strength checks for steel I-profiles of class 3 cross-sections according to Eurocode 3.
"""

from sectionproperties.post.post import SectionProperties

from blueprints.codes.eurocode.en_1993_1_1_2005.chapter_6_ultimate_limit_state import (
    formula_6_5,
    formula_6_6,
    formula_6_9,
    formula_6_10,
    formula_6_12,
    formula_6_14,
)
from blueprints.codes.formula import Formula
from blueprints.saf.results.result_internal_force_1d import ResultInternalForce1D
from blueprints.structural_sections.steel.steel_cross_sections.i_profile import ISteelProfile
from blueprints.type_alias import DIMENSIONLESS
from blueprints.unit_conversion import KN_TO_N, KNM_TO_NMM


class SteelIProfileStrengthClass3:
    """Steel I-Profile strength check for class 3.

    Performs strength checks on steel I-profiles according to Eurocode 3, for class 3 cross-sections.

    Parameters
    ----------
    profile : ISteelProfile
        The steel I-profile to check.
    properties : SectionProperties
        The section properties of the profile.
    result_internal_force_1d : ResultInternalForce1D
        The load combination to apply to the profile.
    gamma_m0 : DIMENSIONLESS, optional
        Partial safety factor for resistance of cross-sections, default is 1.0.
    """

    def __init__(
        self, profile: ISteelProfile, properties: SectionProperties, result_internal_force_1d: ResultInternalForce1D, gamma_m0: DIMENSIONLESS = 1.0
    ) -> None:
        self.profile = profile
        self.properties = properties
        self.result_internal_force_1d = result_internal_force_1d
        self.gamma_m0 = gamma_m0

    class NormalForce:
        """Class to perform normal force resistance check.

        Checks normal force resistance for steel I-profiles according to Eurocode 3, chapter 6.2.3 (tension) and 6.2.4 (compression).

        Parameters
        ----------
        profile : ISteelProfile
            The steel I-profile to check.
        properties : SectionProperties
            The section properties of the profile.
        result_internal_force_1d : ResultInternalForce1D
            The load combination to apply to the profile.
        gamma_m0 : DIMENSIONLESS, optional
            Partial safety factor for resistance of cross-sections, default is 1.0.
        """

        def __init__(
            self,
            profile: ISteelProfile,
            properties: SectionProperties,
            result_internal_force_1d: ResultInternalForce1D,
            gamma_m0: DIMENSIONLESS = 1.0,
        ) -> None:
            self.profile = profile
            self.properties = properties
            self.result_internal_force_1d = result_internal_force_1d
            self.gamma_m0 = gamma_m0

        def calculation_steps(self) -> list[Formula]:
            """Perform calculation steps for normal force resistance check.

            Returns
            -------
            list of Formula
                Calculation results. Returns an empty list if no bending moment is applied.
            """
            if self.result_internal_force_1d.n == 0:
                return []
            if self.result_internal_force_1d.n > 0:  # tension, based on chapter 6.2.3
                a = self.properties.area if self.properties.area is not None else 0
                f_y = min(element.yield_strength for element in self.profile.elements)
                n_ed = self.result_internal_force_1d.n * KN_TO_N
                n_t_rd = formula_6_6.Form6Dot6DesignPlasticRestistanceGrossCrossSection(a=a, f_y=f_y, gamma_m0=self.gamma_m0)
                check_tension = formula_6_5.Form6Dot5UnityCheckTensileStrength(n_ed=n_ed, n_t_rd=n_t_rd)
                return [n_t_rd, check_tension]

            # compression, based on chapter 6.2.4
            a = self.properties.area if self.properties.area is not None else 0
            f_y = min(element.yield_strength for element in self.profile.elements)
            n_ed = -self.result_internal_force_1d.n * KN_TO_N
            n_c_rd = formula_6_10.Form6Dot10NcRdClass1And2And3(a=a, f_y=f_y, gamma_m0=self.gamma_m0)
            check_compression = formula_6_9.Form6Dot9CheckCompressionForce(n_ed=n_ed, n_c_rd=n_c_rd)
            return [n_c_rd, check_compression]

        def check(self) -> bool:
            """Check normal force resistance.

            Returns
            -------
            bool
                True if the normal force check passes, False otherwise.
            """
            if len(self.calculation_steps()) == 0:
                return True
            return bool(self.calculation_steps()[-1])

        def latex(self, n: int = 1, summary: bool = False) -> str:
            """Returns the LaTeX string representation for the normal force check.

            Parameters
            ----------
            n : int, optional
                Formula numbering for LaTeX output (default is 1).
            summary : bool, optional
                If True, returns a summary LaTeX output; otherwise, returns detailed output (default is False).

            Returns
            -------
            str
                LaTeX representation of the normal force check.
            """
            if self.result_internal_force_1d.n == 0:
                text = r"\text{Checking normal force not needed as no normal force applied.} \\ CHECK \to OK"
            elif self.result_internal_force_1d.n > 0:
                text = r"\text{Checking normal force (tension) using chapter 6.2.3.}"
            elif self.result_internal_force_1d.n < 0:
                text = r"\text{Checking normal force (compression) using chapter 6.2.4.}"

            if self.result_internal_force_1d.n != 0:
                if summary:
                    text += f"\\\\{self.calculation_steps()[-1].latex(n=n)}"
                else:
                    for step in self.calculation_steps():
                        text += f"\\\\\\text{{With formula {step.label}:}}\\\\{step.latex(n=n)}"
            return text

    class SingleAxisBendingMoment:
        """Class to perform single axis bending moment resistance check.

        Checks single axis bending moment resistance for steel I-profiles according to Eurocode 3, chapter 6.2.5. For multiple axis bending use 6.2.9.

        Parameters
        ----------
        profile : ISteelProfile
            The steel I-profile to check.
        properties : SectionProperties
            The section properties of the profile.
        result_internal_force_1d : ResultInternalForce1D
            The load combination to apply to the profile.
        axis : str
            The axis to check ('My' or 'Mz'), default is 'My'.
            Usually, the strong axis corresponds to My bending moment, weak axis to Mz bending moment.
        gamma_m0 : DIMENSIONLESS, optional
            Partial safety factor for resistance of cross-sections, default is 1.0.
        """

        def __init__(
            self,
            profile: ISteelProfile,
            properties: SectionProperties,
            result_internal_force_1d: ResultInternalForce1D,
            axis: str = "My",
            gamma_m0: DIMENSIONLESS = 1.0,
        ) -> None:
            # Validate the axis parameter
            allowed_axes = ["My", "Mz"]
            if axis not in allowed_axes:
                raise ValueError(f"Invalid axis '{axis}'. Allowed checks are {allowed_axes}.")

            self.profile = profile
            self.properties = properties
            self.result_internal_force_1d = result_internal_force_1d
            self.axis = axis
            self.gamma_m0 = gamma_m0
            self.moment = self.result_internal_force_1d.my if self.axis == "My" else self.result_internal_force_1d.mz

        def calculation_steps(self) -> list[Formula]:
            """Perform calculation steps for single axis bending moment resistance check.

            Returns
            -------
            list of Formula
                Calculation results. Returns an empty list if no bending moment is applied.
            """
            if self.moment == 0:
                return []

            # Based on chapter 6.2.5
            w_z = (
                min(self.properties.zyy_plus, self.properties.zyy_minus)
                if (self.properties.zyy_plus is not None and self.properties.zyy_minus is not None)
                else 0
            )
            w_y = (
                min(self.properties.zxx_plus, self.properties.zxx_minus)
                if (self.properties.zxx_plus is not None and self.properties.zxx_minus is not None)
                else 0
            )
            section_modulus = w_y if self.axis == "My" else w_z
            f_y = min(element.yield_strength for element in self.profile.elements)

            m_ed = abs(self.moment) * KNM_TO_NMM
            m_c_rd = formula_6_14.Form6Dot14MCRdClass3(w_el_min=section_modulus, f_y=f_y, gamma_m0=self.gamma_m0)
            check_moment = formula_6_12.Form6Dot12CheckBendingMoment(m_ed=m_ed, m_c_rd=m_c_rd)
            return [m_c_rd, check_moment]

        def check(self) -> bool:
            """Check bending moment resistance.

            Returns
            -------
            bool
                True if the bending moment check passes, False otherwise.
            """
            if len(self.calculation_steps()) == 0:
                return True
            return bool(self.calculation_steps()[-1])

        def latex(self, n: int = 1, summary: bool = False) -> str:
            """Returns the LaTeX string representation for the normal force check.

            Parameters
            ----------
            n : int, optional
                Formula numbering for LaTeX output (default is 1).
            summary : bool, optional
                If True, returns a summary LaTeX output; otherwise, returns detailed output (default is False).

            Returns
            -------
            str
                LaTeX representation of the normal force check.
            """
            if self.moment == 0:
                return f"\\text{{Checking bending moment around {self.axis}-axis not needed as no bending moment was applied.}} \\\\ CHECK \to OK"

            text = f"\\text{{Checking bending moments around {self.axis}-axis using chapter 6.2.5.}}"
            if summary:
                text += f"\\\\ {self.calculation_steps()[-1].latex(n=n)}"
            else:
                for step in self.calculation_steps():
                    text += f"\\\\ \\text{{With formula {step.label}:}}\\\\{step.latex(n=n)}"
            return text

    class ShearForce:
        """Class to perform shear force resistance check.

        Checks shear force resistance for steel I-profiles according to Eurocode 3, chapter 6.2.6.
        """

        def __init__(self) -> None:
            raise NotImplementedError("Shear force check not yet implemented.")

    class Torsion:
        """Class to perform torsion resistance check.

        Checks torsion resistance for steel I-profiles according to Eurocode 3, chapter 6.2.7.
        """

        def __init__(self) -> None:
            raise NotImplementedError("Torsion check not yet implemented.")

    class BendingAndShear:
        """Class to perform bending and shear interaction resistance check.

        Checks bending and shear interaction resistance for steel I-profiles according to Eurocode 3, chapter 6.2.8.
        """

        def __init__(self) -> None:
            raise NotImplementedError("Bending and shear interaction check not yet implemented.")

    class MultiBendingAndAxialForce:
        """Class to perform (multi-axis) bending and axial force interaction resistance check.

        Checks (multi-axis) bending and axial force interaction resistance for steel I-profiles according to Eurocode 3, chapter 6.2.9.
        """

        def __init__(self) -> None:
            raise NotImplementedError("(Multi-axis) bending and axial force interaction check not yet implemented.")

    class MultiBendingShearAndAxialForce:
        """Class to perform (multi-axis) bending, shear, and axial force interaction resistance check.

        Checks (multi-axis) bending, shear, and axial force interaction resistance for steel I-profiles according to Eurocode 3, chapter 6.2.10.
        """

        def __init__(self) -> None:
            raise NotImplementedError("(Multi-axis) bending, shear, and axial force interaction check not yet implemented.")

    def check(self) -> bool:
        """Returns True if all strength criteria for the steel I-profile pass, False otherwise.

        Warning: Currently only normal force and single axis bending moment checks are implemented.
        """
        # check normal force
        normal_force_check = self.NormalForce(self.profile, self.properties, self.result_internal_force_1d, self.gamma_m0).check()

        # check bending moments
        bending_moment_w_y_axis_check = self.SingleAxisBendingMoment(
            self.profile, self.properties, self.result_internal_force_1d, axis="My", gamma_m0=self.gamma_m0
        ).check()
        bending_moment_w_z_axis_check = self.SingleAxisBendingMoment(
            self.profile, self.properties, self.result_internal_force_1d, axis="Mz", gamma_m0=self.gamma_m0
        ).check()

        return normal_force_check and bending_moment_w_y_axis_check and bending_moment_w_z_axis_check

    def latex(self, n: int = 1, summary: bool = False) -> str:  # noqa: C901, PLR0912
        """
        Returns the combined LaTeX string representation for all strength checks.

        Parameters
        ----------
        n : int, optional
            Formula numbering for LaTeX output (default is 1).
        summary : bool, optional
            If True, returns a summary LaTeX output; otherwise, returns detailed output (default is False).

        Returns
        -------
        str
            Combined LaTeX representation of all strength checks.
        """
        all_latex = ""

        # Check normal force
        if self.result_internal_force_1d.n != 0:
            all_latex += self.NormalForce(self.profile, self.properties, self.result_internal_force_1d, self.gamma_m0).latex(n=n, summary=summary)

        # Check My axis bending moment (usually strong axis)
        if self.result_internal_force_1d.my != 0 and self.result_internal_force_1d.mz == 0:
            all_latex += r"\\ " + self.SingleAxisBendingMoment(
                self.profile, self.properties, self.result_internal_force_1d, axis="My", gamma_m0=self.gamma_m0
            ).latex(n=n, summary=summary)

        # Check Mz axis bending moment (usually weak axis)
        if self.result_internal_force_1d.mz != 0 and self.result_internal_force_1d.my == 0:
            all_latex += r"\\ " + self.SingleAxisBendingMoment(
                self.profile, self.properties, self.result_internal_force_1d, axis="Mz", gamma_m0=self.gamma_m0
            ).latex(n=n, summary=summary)

        # Check single axis shear force Vz (not yet implemented)
        if self.result_internal_force_1d.vz != 0:
            all_latex += r"\\ \\ \text{Warning: single axis shear force Vz check not yet implemented.}"

        # Check single axis shear force Vy (not yet implemented)
        if self.result_internal_force_1d.vy != 0:
            all_latex += r"\\ \\ \text{Warning: single axis shear force Vy check not yet implemented.}"

        # Check torsion (not yet implemented)
        if self.result_internal_force_1d.mx != 0:
            all_latex += r"\\ \\ \text{Warning: torsion check not yet implemented.}"

        # Check (multiple axis) bending and shear interaction (not yet implemented)
        if (
            max(abs(self.result_internal_force_1d.my), abs(self.result_internal_force_1d.mz)) > 0
            and max(abs(self.result_internal_force_1d.vy), abs(self.result_internal_force_1d.vz)) > 0
        ):
            all_latex += r"\\ \\ \text{Warning: bending and shear interaction check not yet implemented.}"

        # Check bending and axial force interaction (not yet implemented)
        if (max(abs(self.result_internal_force_1d.my), abs(self.result_internal_force_1d.mz)) > 0 and abs(self.result_internal_force_1d.n) > 0) or (
            self.result_internal_force_1d.mz != 0 and self.result_internal_force_1d.my != 0
        ):
            all_latex += r"\\ \\ \text{Warning: (multiple axis) bending and axial force interaction check not yet implemented.}"

        # Check bending, shear and axial force interaction (not yet implemented)
        if (
            max(abs(self.result_internal_force_1d.my), abs(self.result_internal_force_1d.mz)) > 0
            and max(abs(self.result_internal_force_1d.vy), abs(self.result_internal_force_1d.vz)) > 0
            and abs(self.result_internal_force_1d.n) > 0
        ):
            all_latex += r"\\ \\ \text{Warning: bending, shear and axial force interaction check not yet implemented.}"

        if all_latex == "":
            all_latex += r"\text{No internal forces applied.} \\ CHECK \to OK"

        # If the LaTeX string starts with return (\\), remove it for cleaner output
        while all_latex.startswith((r"\\", " ")):
            if all_latex.startswith(r"\\"):
                all_latex = all_latex[2:]
            if all_latex.startswith(" "):
                all_latex = all_latex[1:]

        return all_latex
