"""Steel I-Profile strength check according to Eurocode 3."""

from blueprints.checks.loads.load_combination import LoadCombination
from blueprints.structural_sections.steel.steel_cross_sections.i_profile import ISteelProfile


class SteelIProfileStrength:
    """Steel I-Profile strength check.

    This class performs strength checks on steel I-profiles according to Eurocode 3.

    Parameters
    ----------
    profile : ISteelProfile
        The steel I-profile to check.
    load_combination : LoadCombination
        The load combination to apply to the profile.
    """

    def __init__(self, profile: ISteelProfile, load_combination: LoadCombination) -> None:
        """Initialize the steel I-profile strength check.

        Parameters
        ----------
        profile : ISteelProfile
            The steel I-profile to check.
        load_case : LoadCase
            The load case to apply to the profile.
        """
        self.profile = profile
        self.load_combination = load_combination

    def check_normal_force(self) -> float:
        """Check normal force resistance.

        Returns
        -------
        float
            Unity check ratio for normal force.
        """
        # Placeholder implementation
        raise NotImplementedError("Normal force check not yet implemented.")

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

    def check_combined(self) -> float:
        """Check combined resistance.

        Returns
        -------
        float
            Unity check ratio for combined loading.
        """
        # Placeholder implementation
        raise NotImplementedError("Combined check not yet implemented.")
