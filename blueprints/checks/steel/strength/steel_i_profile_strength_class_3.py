"""Steel I-Profile strength check according to Eurocode 3."""

import numpy as np
from sectionproperties.post.post import SectionProperties

from blueprints.checks.loads.load_combination import LoadCombination
from blueprints.codes.eurocode.en_1993_1_1_2005.chapter_3_materials.table_3_1 import SteelStrengthClass
from blueprints.codes.eurocode.en_1993_1_1_2005.chapter_6_ultimate_limit_state import formula_6_5, formula_6_6, formula_6_9, formula_6_10
from blueprints.structural_sections.steel.steel_cross_sections.i_profile import ISteelProfile
from blueprints.structural_sections.steel.steel_cross_sections.standard_profiles.heb import HEB
from blueprints.type_alias import DIMENSIONLESS
from blueprints.unit_conversion import KN_TO_N


class SteelIProfileStrengthClass3:
    """Steel I-Profile strength check for class 3.

    This class performs strength checks on steel I-profiles according to Eurocode 3, for class 3 profiles.

    Parameters
    ----------
    profile : ISteelProfile
        The steel I-profile to check.
    load_combination : LoadCombination
        The load combination to apply to the profile.
    """

    def __init__(
        self, profile: ISteelProfile, properties: SectionProperties, load_combination: LoadCombination, gamma_m0: DIMENSIONLESS = 1.0
    ) -> None:
        """Initialize the steel I-profile strength check.

        Parameters
        ----------
        profile : ISteelProfile
            The steel I-profile to check.
        properties: SectionProperties
            The section properties of the profile.
        load_combination : LoadCombination
            The load combination to apply to the profile.
        gamma_m0 : DIMENSIONLESS
            Partial safety factor for resistance of cross-sections, default is 1.0.
        """
        self.profile = profile
        self.properties = properties
        self.load_combination = load_combination
        self.gamma_m0 = gamma_m0

    def check_normal_force(self) -> bool:
        """Check normal force resistance.

        Returns
        -------
        bool
            True if the normal force check passes, False otherwise.
        """
        if self.load_combination.normal_force == 0:
            return True
        if self.load_combination.normal_force > 0:  # tension, based on chapter 6.2.3
            # load
            n_ed = self.load_combination.normal_force * KN_TO_N

            # resistance
            a = self.properties.area
            f_y = np.inf
            for element in self.profile.elements:
                f_y = element.yield_strength if f_y > element.yield_strength else f_y
            n_t_rd = formula_6_6.Form6Dot6DesignPlasticRestistanceGrossCrossSection(a=a, f_y=f_y, gamma_m0=self.gamma_m0)

            # check
            return bool(formula_6_5.Form6Dot5UnityCheckTensileStrength(n_ed=n_ed, n_t_rd=n_t_rd))

        # compression
        # load
        n_ed = -self.load_combination.normal_force * KN_TO_N

        # resistance
        a = self.properties.area
        f_y = np.inf
        for element in self.profile.elements:
            f_y = element.yield_strength if f_y > element.yield_strength else f_y
        n_c_rd = formula_6_10.Form6Dot10NcRdClass1And2And3(a=a, f_y=f_y, gamma_m0=self.gamma_m0)

        # check
        return bool(formula_6_9.Form6Dot9CheckCompressionForce(n_ed=n_ed, n_c_rd=n_c_rd))

    def check_shear_force(self) -> float:
        """Check shear force resistance.

        Returns
        -------
        float
            Unity check ratio for shear force.
        """
        # Placeholder implementation
        raise NotImplementedError("Shear force check not yet implemented.")

    def check_bending_moment(self) -> float:
        """Check bending moment resistance.

        Returns
        -------
        float
            Unity check ratio for bending moment.
        """
        # Placeholder implementation
        raise NotImplementedError("Bending moment check not yet implemented.")

    def check_torsion(self) -> float:
        """Check torsional resistance.

        Returns
        -------
        float
            Unity check ratio for torsion.
        """
        # Placeholder implementation
        raise NotImplementedError("Torsion check not yet implemented.")

    def check_bending_and_shear(self) -> float:
        """Check combined bending and shear resistance.

        Returns
        -------
        float
            Unity check ratio for combined bending and shear.
        """
        # Placeholder implementation
        raise NotImplementedError("Bending and shear combination check not yet implemented.")

    def check_bending_and_axial_force(self) -> float:
        """Check combined bending and axial force resistance.

        Returns
        -------
        float
            Unity check ratio for combined bending and axial force.
        """
        # Placeholder implementation
        raise NotImplementedError("Bending and axial force combination check not yet implemented.")

    def check_bending_shear_and_axial_force(self) -> float:
        """Check combined bending, shear, and axial force resistance.

        Returns
        -------
        float
            Unity check ratio for combined bending, shear, and axial force.
        """
        # Placeholder implementation
        raise NotImplementedError("Bending, shear, and axial force combination check not yet implemented.")

    def overall_unity_check(self) -> float:
        """Calculate overall unity check ratio.

        Returns
        -------
        float
            Overall unity check ratio for the profile under the given load combination.
        """
        # Placeholder implementation
        raise NotImplementedError("Overall unity check not yet implemented.")


if __name__ == "__main__":
    """Example usage of SteelIProfileStrengthClass3 with HEB300 and S355 steel.

    This example demonstrates how to create a steel profile check using
    a HEB300 profile with S355 steel grade.
    """

    from blueprints.codes.eurocode.en_1993_1_1_2005.chapter_3_materials.table_3_1 import SteelStrengthClass
    from blueprints.materials.steel import SteelMaterial
    from blueprints.structural_sections.steel.steel_cross_sections.i_profile import ISteelProfile
    from blueprints.structural_sections.steel.steel_cross_sections.standard_profiles.heb import HEB

    # Create S355 steel material from Table 3.1 (assuming flange thickness for HEB300)
    steel_material = SteelMaterial(steel_class=SteelStrengthClass.S355)

    # Create  the HEB300 profile
    heb_profile = ISteelProfile.from_standard_profile(
        profile=HEB.HEB300,
        steel_material=steel_material,
        corrosion=0,  # mm
    )
    heb_properties = heb_profile.section_properties(geometric=True, plastic=False, warping=False)

    # Create simple load combinations (example values)
    example_load_tension = LoadCombination(100, 50, 30, 25, 15, 5)
    example_load_compression = LoadCombination(-100, 50, 30, 25, 15, 5)

    # Perform strength check
    strength_check_tension = SteelIProfileStrengthClass3(heb_profile, heb_properties, example_load_tension, gamma_m0=1.0)
    check_normal_tension = strength_check_tension.check_normal_force()

    strength_check_compression = SteelIProfileStrengthClass3(heb_profile, heb_properties, example_load_compression, gamma_m0=1.0)
    check_normal_compression = strength_check_compression.check_normal_force()
