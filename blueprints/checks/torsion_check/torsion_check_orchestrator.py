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
    _check_instances : dict
        Internal storage of executed check instances for accessing explanations.

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
    _check_instances: dict = None  # type: ignore[assignment]

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
        logging.info("Results:")

        for check_name, utilization in self.get_check_summary().items():
            logging.info(f"{check_name}: {utilization:.2f}")

        if not self.concrete_strut_capacity.is_ok:
            logging.warning("Concrete strut capacity is not enough. Increase cross-section or concrete class.")
            return False

        if self.torsion_moment_capacity.is_ok:
            logging.info("The combination of shear and torsion forces can be resisted with provided reinforcement.")
        else:
            logging.warning(
                "Torsion moment capacity is not enough. Additional reinforcement is required to resist this combination of shear and torsion forces."
            )
            if self.additional_longitudinal_reinforcement_torsion is not None:
                logging.info(
                    "Required additional longitudinal reinforcement for torsion (to be distributed along beam edges): "
                    f"{self.additional_longitudinal_reinforcement_torsion:.2f} mm²"
                )

        logging.info(
            f"The required area of the additional longitudinal reinforcement due to shear: {self.additional_longitudinal_reinforcement_shear:.2f} mm²"
        )

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

    def latex(self, n: int = 1, standalone: bool = False) -> str:  # noqa: C901, PLR0912, PLR0915
        """Generate LaTeX documentation for the torsion check results.

        Creates detailed LaTeX output documenting all individual check results,
        calculations, and conclusions from the torsional resistance verification
        according to EN 1992-1-1:2004 art. 6.3.

        Parameters
        ----------
        n : int, default=1
            Section numbering level for LaTeX document structure.
        standalone : bool, default=False
            If True, generates a complete LaTeX document with preamble and document environment.
            If False, generates only the content body for inclusion in another document.

        Returns
        -------
        str
            LaTeX string representation of the torsion check results, including:

            - Individual check results with utilization ratios
            - Calculations and formulas used
            - Overall conclusions and recommendations

        Notes
        -----
        - Future implementation will include complete EN 1992-1-1:2004 references
        - Will support customizable formatting and section numbering
        - Intended for integration with automated reporting systems
        """
        # Build document preamble if standalone
        preamble = (
            r"""\documentclass{article}
\usepackage{amsmath}
\usepackage{booktabs}
\usepackage{geometry}
\geometry{a4paper, margin=1in}

% Increase spacing throughout document
\usepackage{setspace}
\setstretch{1.3}  % Increase line spacing by 30%

% Add space between paragraphs
\setlength{\parskip}{0.5em}

% Add space around equations
\setlength{\abovedisplayskip}{12pt}
\setlength{\belowdisplayskip}{12pt}

\begin{document}

\title{Torsion Check Results}
\date{}
\maketitle

"""
            if standalone
            else ""
        )

        # Create section header
        heading = "\\" + "sub" * (n - 1) + "section"
        output = f"{heading}{{Torsion Check Results}}\n\n" if not standalone else ""

        # Move Utilization Summary to the top for standalone documents
        if standalone:
            output += "\\section{Utilization Summary}\n\n"
            output += "\\begin{table}[h]\n"
            output += "\\centering\n"
            output += "\\begin{tabular}{lcc}\n"
            output += "\\toprule\n"
            output += "Check & Utilization & Status \\\\\n"
            output += "\\midrule\n"

            for check_name, utilization in self.get_check_summary().items():
                status = "PASS" if utilization <= 1.0 else "FAIL"
                output += f"{check_name} & {utilization:.3f} & {status} \\\\\n"

            output += "\\bottomrule\n"
            output += "\\end{tabular}\n"
            output += "\\end{table}\n\n"

        # Overall result summary
        all_pass = self.all_checks_pass()
        output += "\\textbf{Overall Result: "
        output += "PASS" if all_pass else "FAIL"
        output += "}\\\\[0.5em]\n\n"

        # Individual check results
        section_heading = "\\section" if standalone else heading
        output += f"{section_heading}{{Individual Checks}}\n\n"

        # Map check names to their results and stored instances
        if self._check_instances:
            checks_map = {
                "Concrete Strut Capacity": (self.concrete_strut_capacity, self._check_instances.get("concrete_strut")),
                "Torsion Moment Capacity": (self.torsion_moment_capacity, self._check_instances.get("torsion_moment")),
                "Maximum Longitudinal Reinforcement": (self.max_longitudinal_reinforcement, self._check_instances.get("max_longitudinal")),
                "Minimum Tensile Reinforcement": (self.min_tensile_reinforcement, self._check_instances.get("min_tensile")),
                "Maximum Shear Stirrup Spacing": (self.max_shear_stirrup_spacing, self._check_instances.get("max_shear_spacing")),
                "Maximum Torsion Stirrup Spacing": (self.max_torsion_stirrup_spacing, self._check_instances.get("max_torsion_spacing")),
                "Shear and Torsion Stirrup Area": (self.shear_and_torsion_stirrup_area, self._check_instances.get("stirrup_area")),
                "Minimum Shear Reinforcement Ratio": (self.min_shear_reinforcement_ratio, self._check_instances.get("min_shear_ratio")),
            }

            subsection_heading = "\\subsection" if standalone else heading
            for check_name, (result, check_obj) in checks_map.items():
                output += f"{subsection_heading}{{{check_name}}}\n\n"

                # Add explanation if available from executed check
                if check_obj and hasattr(check_obj, "explanation") and check_obj.explanation:
                    # Format the explanation - remove "Result:" line as we'll add it separately
                    explanation_lines = check_obj.explanation.strip().split("\n")
                    output += "\n".join(explanation_lines) + "\n\n"
                else:
                    # Fallback to basic result info
                    output += f"Utilization: {result.utilization:.1%}\\\\[0.3em]\n"
                    output += f"Status: {'PASS' if result.is_ok else 'FAIL'}\\\\[0.5em]\n\n"
        else:
            # Fallback if check instances not available
            output += "Check details not available. Please re-run the analysis.\n\n"

        # Additional reinforcement requirements
        output += f"{section_heading}{{Additional Reinforcement Requirements}}\n\n"
        output += "\\textbf{Shear:}\\\\[0.3em]\n"
        output += (
            f"Additional longitudinal reinforcement due to shear: $A_{{sl,shear}} = "
            f"{self.additional_longitudinal_reinforcement_shear:.2f}$ mm²\\\\[0.5em]\n\n"
        )

        if self.additional_longitudinal_reinforcement_torsion is not None:
            output += "\\textbf{Torsion:}\\\\[0.3em]\n"
            output += (
                f"Additional longitudinal reinforcement due to torsion: $A_{{sl,torsion}} = "
                f"{self.additional_longitudinal_reinforcement_torsion:.2f}$ mm²\\\\\n"
            )
            output += "(To be distributed along beam edges)\\\\[0.5em]\n\n"

        # Summary table of utilizations (skip for standalone as it's already at the top)
        if not standalone:
            output += f"{heading}{{Utilization Summary}}\n\n"
            output += "\\begin{table}[h]\n"
            output += "\\centering\n"
            output += "\\begin{tabular}{lcc}\n"
            output += "\\hline\n"
            output += "Check & Utilization & Status \\\\\n"
            output += "\\hline\n"

            for check_name, utilization in self.get_check_summary().items():
                status = "PASS" if utilization <= 1.0 else "FAIL"
                output += f"{check_name} & {utilization:.3f} & {status} \\\\\n"

            output += "\\hline\n"
            output += "\\end{tabular}\n"
            output += "\\end{table}\n\n"

        # Conclusions
        output += f"{section_heading}{{Conclusions}}\n\n"

        if all_pass:
            output += (
                "All torsion checks pass. The cross-section can safely resist the applied combination "
                "of shear and torsion forces with the provided reinforcement.\n\n"
            )
        else:
            output += "\\textbf{Warning:} One or more checks have failed.\\\\[0.5em]\n\n"

            if not self.concrete_strut_capacity.is_ok:
                output += (
                    "\\textbf{Critical:} Concrete strut capacity is insufficient. This cannot be "
                    "resolved by adding more reinforcement. Required actions:\n"
                )
                output += "\\begin{itemize}\n"
                output += "  \\item Increase cross-section dimensions, or\n"
                output += "  \\item Use higher strength concrete, or\n"
                output += "  \\item Reduce applied loads\n"
                output += "\\end{itemize}\n\n"

            if not self.torsion_moment_capacity.is_ok:
                output += (
                    "\\textbf{Note:} Torsion moment capacity is insufficient with "
                    "minimum reinforcement. Additional torsion-specific reinforcement is "
                    "required as specified above.\\\\[0.5em]\n\n"
                )

        # Add closing document tag for standalone
        if standalone:
            output += "\\end{document}\n"

        return preamble + output


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
        # Execute individual checks - store instances to preserve explanations
        concrete_strut_check = ConcreteStrutCapacityCheck()
        concrete_strut = concrete_strut_check.execute(
            geometry=self.geometry,
            materials=self.materials,
            forces=self.forces,
        )

        torsion_moment_check = TorsionMomentCapacityCheck()
        torsion_moment = torsion_moment_check.execute(
            geometry=self.geometry,
            forces=self.forces,
        )

        max_longitudinal_check = MaxLongitudinalReinforcementCheck()
        max_longitudinal = max_longitudinal_check.execute(geometry=self.geometry)

        min_tensile_check = MinTensileReinforcementCheck()
        min_tensile = min_tensile_check.execute(
            geometry=self.geometry,
            materials=self.materials,
        )

        max_shear_spacing_check = MaxShearStirrupSpacingCheck()
        max_shear_spacing = max_shear_spacing_check.execute(
            geometry=self.geometry,
            forces=self.forces,
        )

        max_torsion_spacing_check = MaxTorsionStirrupSpacingCheck()
        max_torsion_spacing = max_torsion_spacing_check.execute(
            geometry=self.geometry,
            forces=self.forces,
        )

        stirrup_area_check = ShearAndTorsionStirrupAreaCheck()
        stirrup_area = stirrup_area_check.execute(
            geometry=self.geometry,
            materials=self.materials,
            forces=self.forces,
        )

        min_shear_ratio_check = MinShearReinforcementRatioCheck()
        min_shear_ratio = min_shear_ratio_check.execute(
            geometry=self.geometry,
            materials=self.materials,
            forces=self.forces,
        )

        # Store check instances for accessing explanations in latex method
        check_instances = {
            "concrete_strut": concrete_strut_check,
            "torsion_moment": torsion_moment_check,
            "max_longitudinal": max_longitudinal_check,
            "min_tensile": min_tensile_check,
            "max_shear_spacing": max_shear_spacing_check,
            "max_torsion_spacing": max_torsion_spacing_check,
            "stirrup_area": stirrup_area_check,
            "min_shear_ratio": min_shear_ratio_check,
        }

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
            _check_instances=check_instances,
        )
