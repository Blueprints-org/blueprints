"""Helper methods for building standardized report sections."""

from collections.abc import Sequence
from typing import Any

from blueprints.checks.check_protocol import CheckProtocol
from blueprints.codes.formula import Formula
from blueprints.saf.results.result_internal_force_1d import ResultInternalForce1D
from blueprints.structural_sections.steel.steel_cross_section import SteelCrossSection
from blueprints.utils.report import Report

# Mini dictionary of common property labels used in section reports
# please note: sectionproperties uses x-y coordinates, while Blueprints y-z as in structural analysis
PROPERTY_LABELS = {
    # mm^2
    "area": "Area $A$ in $mm^{2}$",
    "a_sx": "Shear area $A_{sy}$ in $mm^{2}$",
    "a_sy": "Shear area $A_{sz}$ in $mm^{2}$",
    # mm
    "perimeter": "Perimeter $P$ in $mm$",
    # kg/m
    "mass": "Mass $W$ in $kg/m$",
    # mm^3
    "zxx_plus": "Section modulus $W_{y,el+}$ in $mm^{3}$",
    "zxx_minus": "Section modulus $W_{y,el-}$ in $mm^{3}$",
    "zyy_plus": "Section modulus $W_{z,el+}$ in $mm^{3}$",
    "zyy_minus": "Section modulus $W_{z,el-}$ in $mm^{3}$",
    "sxx": "Plastic section modulus $W_{y,pl}$ in $mm^{3}$",
    "syy": "Plastic section modulus $W_{z,pl}$ in $mm^{3}$",
    # mm^4
    "ixx_c": "Second moment of area $I_{y}$ in $mm^{4}$",
    "iyy_c": "Second moment of area $I_{z}$ in $mm^{4}$",
    "J": "Torsion constant $J$ in $mm^{4}$",
}

FORCE_LABELS = {
    "n": "Normal force $N$ [kN]",
    "vz": "Shear force $V_z$ [kN]",
    "vy": "Shear force $V_y$ [kN]",
    "my": "Bending moment $M_y$ [kNm]",
    "mz": "Bending moment $M_z$ [kNm]",
    "mx": "Torsion $T$ [kNm]",
}


class ReportHelpers:
    """Helper methods for building standardized report sections."""

    @staticmethod
    def add_applied_documents(report: Report, docs: Sequence[Any]) -> None:
        """
        Add applied code documents section to the report.

        report : Report
            The report object to which the calculation steps will be added.
        docs : Sequence[Any]
            The list of applied code documents.
        """
        report.add_heading("Applied code documents")
        report.add_paragraph("The following documents were applied in this check:")
        report.add_list(docs)

    @staticmethod
    def add_applied_forces(report: Report, forces: ResultInternalForce1D, n: int = 2) -> None:
        """
        Add applied forces section to the report.

        report : Report
            The report object to which the calculation steps will be added.
        forces : ResultInternalForce1D
            The internal forces object.
        n : int, optional
            Number of decimals (default is 2).
        """
        report.add_heading("Applied internal forces")
        report.add_paragraph("The following internal forces were applied in this check:")
        rows = []
        for force_attr in ["n", "vy", "vz", "mx", "my", "mz"]:
            value = getattr(forces, force_attr, None)
            if value is not None:
                label = FORCE_LABELS[force_attr] if FORCE_LABELS and force_attr in FORCE_LABELS else force_attr.upper()
                rows.append([label, f"{value:.{n}f}"])
        report.add_table(headers=["Internal Force", "Value"], rows=rows)

    @staticmethod
    def add_material_steel_info(report: Report, steel_cross_section: SteelCrossSection, n: int = 2) -> None:
        """
        Add material and steel info to the report.

        report : Report
            The report object to which the calculation steps will be added.
        steel_cross_section : SteelCrossSection
            The steel cross section object.
        n : int, optional
            Number of decimals (default is 2).
        """
        report.add_heading("Applied material and profile")
        report.add_paragraph("The following material properties were used in this check:")
        mat = steel_cross_section.material
        report.add_table(
            headers=["Property", "Value"],
            rows=[
                ["Material", str(getattr(mat, "name", mat))],
                ["Yield Strength $f_y$", f"{getattr(steel_cross_section, 'yield_strength', 0):.{n}f} MPa"],
                ["Ultimate Strength $f_u$", f"{getattr(steel_cross_section, 'ultimate_strength', 0):.{n}f} MPa"],
                ["Elastic Modulus $E$", f"{getattr(mat, 'e_modulus', 0):.{n}f} MPa"],
            ],
        )

    @staticmethod
    def add_section_properties(
        report: Report,
        section_properties: object,
        profile: object = None,
        n: int = 2,
        properties: Sequence[str] = ("area",),
    ) -> None:
        """
        Add section properties to the report.

        report : Report
            The report object to which the calculation steps will be added.
        section_properties : object
            The section properties object.
        profile : object, optional
            Optional profile object for name.
        n : int, optional
            Number of decimals (default is 2).
        properties : Sequence[str], optional
            List of property names to include (default is ("area",)).
        """
        report.add_paragraph("The following section properties were used in this check:")
        rows = []
        if profile is not None:
            rows.append(["Profile", str(getattr(profile, "name", profile))])
        for prop in properties:
            label = PROPERTY_LABELS[prop] if PROPERTY_LABELS and prop in PROPERTY_LABELS else prop.capitalize()
            value = getattr(section_properties, prop, None)
            if value is None:
                rows.append([label, "Not calculated"])
            else:
                value_str = f"{value:.{n}f}" if isinstance(value, float) else str(value)
                rows.append([label, value_str])

        report.add_table(headers=["Property", "Value"], rows=rows)

    @staticmethod
    def add_unity_check_summary(report: Report, calculation_steps: dict[str, CheckProtocol | Formula | None], n: int = 2) -> None:
        """
        Add a summary table of unity checks to the report.

        report : Report
            The report object to which the calculation steps will be added.
        calculation_steps : dict[str, CheckProtocol | Formula | None]
            Iterable of (check_name, check_instance) tuples.
        n : int, optional
            Number of decimals (default is 2).
        """
        check_results = list(calculation_steps.items()) if isinstance(calculation_steps, dict) else list(calculation_steps)
        report.add_heading("Utilization summary")
        rows = []
        overall_ok = True
        for check_name, check in check_results:
            if hasattr(check, "result"):
                res = check.result if not callable(check.result) else check.result()
                uc = getattr(res, "unity_check", None)
                utilization = f"{uc:.{n}f}" if uc is not None else "Not calculated"
                status = "OK" if getattr(res, "is_ok", False) else "NOT OK"
                if not getattr(res, "is_ok", False):
                    overall_ok = False
            else:
                utilization = "Not implemented"
                status = "NOT OK"
                overall_ok = False
            rows.append([check_name.capitalize(), utilization, status])
        report.add_table(headers=["Check", "Utilization", "Status"], rows=rows)
        report.add_paragraph(f"Overall result: {'OK' if overall_ok else 'NOT OK'}", bold=True)

    @staticmethod
    def add_calculation_steps_formula(report: Report, calculation_steps: dict[str, CheckProtocol | Formula | None], n: int = 2) -> None:
        """
        Add calculation steps formula to the report.

        report : Report
            The report object to which the calculation steps will be added.
        calculation_steps : dict[str, CheckProtocol | Formula | None]
            Iterable of (step_name, step_instance) tuples.
        n : int, optional
            Number of decimals (default is 2).
        """
        steps = list(calculation_steps.items()) if isinstance(calculation_steps, dict) else list(calculation_steps)
        for step_name, step in steps:
            if isinstance(step, Formula):
                report.add_heading(f"Calculation Step: {step_name.capitalize()}")
                report.add_formula(step, n=n)

    @staticmethod
    def add_calculation_steps_subchecks(
        report: Report, calculation_steps: dict[str, CheckProtocol | Formula | None], n: int = 2, level: int = 2
    ) -> None:
        """
        Add calculation steps for sub-checks to the report.

        report : Report
            The report object to which the calculation steps will be added.
        calculation_steps : dict[str, CheckProtocol | Formula | None]
            Iterable of (check_name, check_instance) tuples.
        n : int, optional
            Formula numbering for LaTeX output (default is 2).
        level : int, optional
            Heading level for the report sections (default is 2).
        """
        for check_name, check in calculation_steps().items():
            report.add_heading(f"Checking: {check_name}", level=level)
            method = getattr(check, "report_calculation_steps", None)
            if callable(method):
                method(report, n=n)
            else:
                report.add_paragraph("This check does not support detailed calculation steps.")
