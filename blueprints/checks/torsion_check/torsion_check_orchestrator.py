"""Orchestrates all torsion checks and coordinates the analysis."""

import logging
from dataclasses import dataclass

from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_6_ultimate_limit_state.formula_6_18 import Form6Dot18AdditionalTensileForce
from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_6_ultimate_limit_state.formula_6_28 import (
    Form6Dot28RequiredCrossSectionalArea,
)
from blueprints.unit_conversion import KN_TO_N, N_TO_KN

from .check_result import CheckResult
from .individual_checks import (
    ConcreteStrutCapacityCheck,
    MaxLongitudinalReinforcementCheck,
    MaxShearStirrupSpacingCheck,
    MaxTorsionStirrupSpacingCheck,
    MinShearReinforcementRatioCheck,
    MinTensileReinforcementCheck,
    ShearAndTorsionStirrupAreaCheck,
    TorsionMomentCapacityCheck,
)
from .torsion_forces import TorsionForces
from .torsion_geometry import TorsionGeometry
from .torsion_materials import TorsionMaterials


@dataclass(frozen=True)
class TorsionCheckResults:
    """Comprehensive results container for torsional resistance verification.

    Aggregates all individual check results from the complete torsional analysis
    according to EN 1992-1-1:2004 art. 6.3. Provides both individual check
    outcomes and overall pass/fail status with utilization summaries.

    Attributes
    ----------
    concrete_strut_capacity : CheckResult
        Result of concrete compression strut capacity check (most critical).
    torsion_moment_capacity : CheckResult
        Result of torsion moment capacity check with minimum reinforcement.
    max_longitudinal_reinforcement : CheckResult
        Result of maximum longitudinal reinforcement limit check (4%).
    min_tensile_reinforcement : CheckResult
        Result of minimum tensile reinforcement requirement check.
    max_shear_stirrup_spacing : CheckResult
        Result of maximum shear stirrup spacing limit check.
    max_torsion_stirrup_spacing : CheckResult
        Result of maximum torsion stirrup spacing limit check.
    shear_and_torsion_stirrup_area : CheckResult
        Result of combined shear and torsion stirrup area requirement check.
    min_shear_reinforcement_ratio : CheckResult
        Result of minimum shear reinforcement ratio check.
    additional_longitudinal_reinforcement_shear : float
        Required additional longitudinal reinforcement due to shear [mm²].
    additional_longitudinal_reinforcement_torsion : float | None
        Required additional longitudinal reinforcement due to torsion [mm²],
        None if torsion capacity check passes.

    Notes
    -----
    - Frozen dataclass ensures immutable results
    - All checks must pass for safe structural performance
    - Utilization ratios help identify critical design aspects
    - Additional reinforcement is calculated based on Eurocode formulas

    Examples
    --------
    >>> orchestrator = TorsionCheckOrchestrator(geometry, materials, forces)
    >>> results = orchestrator.execute_all_checks()
    >>> if results.all_checks_pass():
    ...     print("All torsion checks pass")
    >>> max_util = max(results.get_check_summary().values())
    >>> print(f"Maximum utilization: {max_util:.1%}")
    """

    concrete_strut_capacity: CheckResult
    torsion_moment_capacity: CheckResult
    max_longitudinal_reinforcement: CheckResult
    min_tensile_reinforcement: CheckResult
    max_shear_stirrup_spacing: CheckResult
    max_torsion_stirrup_spacing: CheckResult
    shear_and_torsion_stirrup_area: CheckResult
    min_shear_reinforcement_ratio: CheckResult

    additional_longitudinal_reinforcement_shear: float
    additional_longitudinal_reinforcement_torsion: float | None = None

    def all_checks_pass(self) -> bool:
        """Evaluate overall torsional resistance adequacy.

        Performs comprehensive evaluation of all individual structural checks
        to determine if the cross-section can safely resist the applied
        combination of shear and torsion forces.

        Returns
        -------
        bool
            True if all individual structural checks pass, indicating safe
            structural performance. False if any check fails, requiring
            design modifications.

        Notes
        -----
        - All individual checks must pass for True result
        - Critical for determining structural adequacy
        - Failure of any check requires design action
        - Most critical: concrete strut capacity cannot be fixed with more reinforcement

        Examples
        --------
        >>> if results.all_checks_pass():
        ...     print("Design is adequate")
        ... else:
        ...     print("Design modifications required")
        ...     # Identify which specific checks failed
        """
        return all(
            [
                self.concrete_strut_capacity.is_ok,
                self.torsion_moment_capacity.is_ok,
                self.max_longitudinal_reinforcement.is_ok,
                self.min_tensile_reinforcement.is_ok,
                self.max_shear_stirrup_spacing.is_ok,
                self.max_torsion_stirrup_spacing.is_ok,
                self.shear_and_torsion_stirrup_area.is_ok,
                self.min_shear_reinforcement_ratio.is_ok,
            ]
        )

    def get_check_summary(self) -> dict[str, float]:
        """Generate utilization summary for all structural checks.

        Creates a comprehensive overview of all check utilization ratios,
        providing insight into which aspects of the design are most critical
        and how close the section is to its limits.

        Returns
        -------
        dict[str, float]
            Dictionary mapping check names to their utilization ratios.
            Ratios > 1.0 indicate check failure. Higher values indicate
            higher demand relative to capacity.

        Notes
        -----
        - Utilization ratio = demand/capacity (or required/provided)
        - Values close to 1.0 indicate efficient but near-limit design
        - Values >> 1.0 indicate significant over-demand requiring design changes
        - Useful for identifying bottlenecks in structural performance

        Examples
        --------
        >>> summary = results.get_check_summary()
        >>> critical_check = max(summary, key=summary.get)
        >>> print(f"Most critical: {critical_check} at {summary[critical_check]:.1%}")
        >>> for check, ratio in summary.items():
        ...     status = "FAIL" if ratio > 1.0 else "PASS"
        ...     print(f"{check}: {ratio:.2f} ({status})")
        """
        return {
            "Concrete strut capacity": self.concrete_strut_capacity.utilization,
            "Torsion moment capacity": self.torsion_moment_capacity.utilization,
            "Max longitudinal reinforcement": self.max_longitudinal_reinforcement.utilization,
            "Min tensile reinforcement": self.min_tensile_reinforcement.utilization,
            "Max shear stirrup spacing": self.max_shear_stirrup_spacing.utilization,
            "Max torsion stirrup spacing": self.max_torsion_stirrup_spacing.utilization,
            "Shear and torsion stirrup area": self.shear_and_torsion_stirrup_area.utilization,
            "Min shear reinforcement ratio": self.min_shear_reinforcement_ratio.utilization,
        }


@dataclass(frozen=True)
class TorsionCheckOrchestrator:
    """Comprehensive orchestrator for torsional resistance verification according to EN 1992-1-1:2004.

    This class coordinates the complete torsional analysis workflow, executing all
    required structural checks and calculating additional reinforcement requirements.
    It implements the full scope of torsion verification according to Eurocode 2
    art. 6.3, ensuring compliance with all safety and serviceability requirements.

    Attributes
    ----------
    label : str
        Description of the check type for reporting purposes.
    source_document : str
        Reference standard (EN 1992-1-1) for traceability.
    geometry : TorsionGeometry
        Cross-sectional geometry and dimensional properties.
    materials : TorsionMaterials
        Material properties and design coefficients.
    forces : TorsionForces
        Applied loads and design parameters.

    Notes
    -----
    - Implements complete EN 1992-1-1:2004 art. 6.3 torsion verification
    - Coordinates individual torsion checks
    - Calculates additional reinforcement requirements per Eurocode formulas
    - Provides both detailed results and simplified pass/fail evaluation
    - Frozen dataclass ensures consistent input parameters throughout analysis

    Examples
    --------
    >>> geometry = TorsionGeometry(cross_section)
    >>> materials = TorsionMaterials(cross_section)
    >>> forces = TorsionForces(v_ed=150.0, t_ed=50.0, ...)
    >>> orchestrator = TorsionCheckOrchestrator(geometry, materials, forces)
    >>> results = orchestrator.execute_all_checks()
    >>> print(f"Design adequate: {results.all_checks_pass()}")
    """

    label = "Torsion according to art. 6.3"
    source_document = "EN 1992-1-1"

    geometry: TorsionGeometry
    materials: TorsionMaterials
    forces: TorsionForces

    def execute_all_checks(self) -> TorsionCheckResults:
        """Execute complete torsional resistance verification analysis.

        Performs all individual structural checks required for torsional
        resistance verification according to EN 1992-1-1:2004 art. 6.3, and
        calculates additional reinforcement requirements based on Eurocode formulas.

        Returns
        -------
        TorsionCheckResults
            Comprehensive results object containing all individual check outcomes,
            utilization ratios, and additional reinforcement requirements.

        Notes
        -----
        Executes the following checks in sequence:

        1. **Concrete Strut Capacity** - Most critical, cannot be fixed with more steel
        2. **Torsion Moment Capacity** - Determines if minimum reinforcement suffices
        3. **Max Longitudinal Reinforcement** - 4% limit to prevent over-reinforcement
        4. **Min Tensile Reinforcement** - Safety against brittle failure
        5. **Max Shear Stirrup Spacing** - Spacing limits for shear resistance
        6. **Max Torsion Stirrup Spacing** - Stricter spacing limits for torsion
        7. **Shear and Torsion Stirrup Area** - Combined stirrup requirement check
        8. **Min Shear Reinforcement Ratio** - Minimum stirrup ratio requirement

        Additional reinforcement calculations:

        - **Shear longitudinal reinforcement** per formula 6.18
        - **Torsion longitudinal reinforcement** per formula 6.28 (if needed)

        Examples
        --------
        >>> results = orchestrator.execute_all_checks()
        >>> if not results.all_checks_pass():
        ...     for name, util in results.get_check_summary().items():
        ...         if util > 1.0:
        ...             print(f"Failed: {name} (utilization: {util:.2f})")
        >>> print(f"Additional shear reinforcement: {results.additional_longitudinal_reinforcement_shear:.1f} mm²")
        """
        # Execute individual checks
        concrete_strut = ConcreteStrutCapacityCheck().execute(
            geometry=self.geometry,
            materials=self.materials,
            forces=self.forces,
        )
        torsion_moment = TorsionMomentCapacityCheck().execute(
            geometry=self.geometry,
            forces=self.forces,
        )
        max_longitudinal = MaxLongitudinalReinforcementCheck().execute(geometry=self.geometry)
        min_tensile = MinTensileReinforcementCheck().execute(
            geometry=self.geometry,
            materials=self.materials,
        )
        max_shear_spacing = MaxShearStirrupSpacingCheck().execute(
            geometry=self.geometry,
            forces=self.forces,
        )
        max_torsion_spacing = MaxTorsionStirrupSpacingCheck().execute(
            geometry=self.geometry,
            forces=self.forces,
        )
        stirrup_area = ShearAndTorsionStirrupAreaCheck().execute(
            geometry=self.geometry,
            materials=self.materials,
            forces=self.forces,
        )
        min_shear_ratio = MinShearReinforcementRatioCheck().execute(
            geometry=self.geometry,
            materials=self.materials,
            forces=self.forces,
        )

        # Calculate additional reinforcement requirements
        f_yd = self.materials.get_tension_rebar_material().f_yd

        # Additional tensile force due to shear
        delta_f_td = Form6Dot18AdditionalTensileForce(
            v_ed=self.forces.v_ed * N_TO_KN,
            theta=self.forces.theta,
            alpha=self.forces.alpha,
        )
        a_sl_shear = delta_f_td * KN_TO_N / f_yd

        # Additional longitudinal reinforcement for torsion (if torsion check fails)
        a_sl_torsion = None
        if not torsion_moment.is_ok:
            a_sl_torsion = Form6Dot28RequiredCrossSectionalArea(
                u_k=self.geometry.perimeter(),
                f_yd=f_yd,
                t_ed=self.forces.t_ed,
                a_k=self.geometry.enclosed_area(),
                theta=self.forces.theta,
            )

        return TorsionCheckResults(
            concrete_strut_capacity=concrete_strut,
            torsion_moment_capacity=torsion_moment,
            max_longitudinal_reinforcement=max_longitudinal,
            min_tensile_reinforcement=min_tensile,
            max_shear_stirrup_spacing=max_shear_spacing,
            max_torsion_stirrup_spacing=max_torsion_spacing,
            shear_and_torsion_stirrup_area=stirrup_area,
            min_shear_reinforcement_ratio=min_shear_ratio,
            additional_longitudinal_reinforcement_shear=a_sl_shear,
            additional_longitudinal_reinforcement_torsion=a_sl_torsion,
        )

    def check(self) -> bool:
        """Execute analysis with console output for interactive use and backward compatibility.

        Performs complete torsional analysis and prints detailed results to console.
        This method provides immediate feedback on structural adequacy and specific
        failure modes, making it suitable for interactive analysis and debugging.

        Returns
        -------
        bool
            True if all structural checks pass and design is adequate.
            False if any check fails, indicating required design modifications.

        Notes
        -----
        - Provides immediate console feedback for each check
        - Reports utilization ratios for all structural checks
        - Identifies specific failure modes and required actions
        - Calculates and reports additional reinforcement requirements
        - Maintained for backward compatibility with existing workflows

        Examples
        --------
        >>> orchestrator = TorsionCheckOrchestrator(geometry, materials, forces)
        >>> is_adequate = orchestrator.check()
        >>> if not is_adequate:
        ...     print("Design requires modifications")
        """
        results = self.execute_all_checks()

        logging.info("Results:")

        for check_name, utilization in results.get_check_summary().items():
            logging.info(f"{check_name}: {utilization:.2f}")

        if not results.concrete_strut_capacity.is_ok:
            logging.warning("Concrete strut capacity is not enough. Increase cross-section or concrete class.")
            return False

        if results.torsion_moment_capacity.is_ok:
            logging.info("The combination of shear and torsion forces can be resisted with provided reinforcement.")
        else:
            logging.warning(
                "Torsion moment capacity is not enough. Additional reinforcement is required to resist this combination of shear and torsion forces."
            )
            if results.additional_longitudinal_reinforcement_torsion is not None:
                logging.info(
                    "Required additional longitudinal reinforcement for torsion (to be distributed along beam edges): "
                    f"{results.additional_longitudinal_reinforcement_torsion:.2f} mm²"
                )

        logging.info(
            "The required area of the additional longitudinal reinforcement due to shear: "
            f"{results.additional_longitudinal_reinforcement_shear:.2f} mm²"
        )

        return results.all_checks_pass()

    def latex(self, n: int = 1) -> str:  # noqa: ARG002
        """Generate LaTeX documentation for the complete torsional analysis.

        Creates comprehensive LaTeX output documenting all aspects of the torsional
        resistance verification, including input parameters, individual check results,
        calculations, and conclusions. Suitable for engineering reports and documentation.

        Parameters
        ----------
        n : int, default=1
            Section numbering level for LaTeX document structure.

        Returns
        -------
        str
            Complete LaTeX string representation of the analysis, including:

            - Input parameters and cross-section properties
            - Individual check calculations and results
            - Utilization ratios and safety factors
            - Additional reinforcement requirements
            - Overall conclusions and recommendations

        Notes
        -----
        - Currently not implemented (placeholder)
        - Future implementation will include complete EN 1992-1-1:2004 references
        - Will support customizable formatting and section numbering
        - Intended for integration with automated reporting systems

        Examples
        --------
        >>> latex_report = orchestrator.latex(n=3)
        >>> with open("torsion_analysis.tex", "w") as f:
        ...     f.write(latex_report)
        """
        # TODO: To be implemented  #noqa: FIX002, TD002, TD003
        return ""
