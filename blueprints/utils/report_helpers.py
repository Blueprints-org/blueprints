"""Helper methods for building standardized report sections."""

from collections.abc import Sequence
from typing import Any

from blueprints.checks.check_protocol import CheckProtocol
from blueprints.codes.formula import Formula
from blueprints.saf.results.result_internal_force_1d import ResultInternalForce1D
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
        """Add applied code documents section to the report."""
        report.add_heading("Applied code documents")
        report.add_paragraph("The following documents were applied in this check:")
        report.add_list(docs)

    @staticmethod
    def add_applied_forces(report: Report, forces: ResultInternalForce1D, n: int = 2) -> None:
        """Add applied forces section to the report.
        Args:
            report: Report object
            forces: ResultInternalForce1D object
            n: Number of decimals.
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
    def add_material_steel_info(report: Report, steel_cross_section: object, n: int = 2) -> None:
        """Add material and steel info to the report."""
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
        """Add section properties to the report.
        Args:
            report: Report object
            section_properties: SectionProperties object
            profile: Optional profile object for name
            n: Number of decimals
            properties: List of property names to include (e.g., ["area", "zxx_plus"]).
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
        """Add a summary table of unity checks to the report.
        Args:
            report: Report object
            calculation_steps: Iterable of (check_name, check_instance) tuples
            n: Number of decimals.
        """
        check_results = list(calculation_steps.items()) if isinstance(calculation_steps, dict) else list(calculation_steps)
        report.add_heading("Utilization summary")
        rows = []
        overall_ok = True
        for check_name, check in check_results:
            if hasattr(check, "result"):
                res = check.result()
                uc = getattr(res, "unity_check", None)
                utilization = f"{uc:.{n}f}" if uc is not None else "N/A"
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
