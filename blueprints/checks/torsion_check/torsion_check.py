r"""Example for torsion calculation for a rectangular reinforced concrete cross-section.
Based on the calculation example from Technische Universiteit Delft:
https://www.studeersnel.nl/nl/document/technische-universiteit-delft/concrete-structures-2/torsion/29391885.
"""

from dataclasses import dataclass, field

from blueprints.structural_sections.concrete.reinforced_concrete_sections.rectangular import RectangularReinforcedCrossSection
from blueprints.type_alias import DEG, MM2, MPA, NMM, N

from .torsion_check_orchestrator import TorsionCheckOrchestrator
from .torsion_forces import TorsionForces
from .torsion_geometry import TorsionGeometry
from .torsion_materials import TorsionMaterials


@dataclass(frozen=True)
class TorsionCheck:
    """Class responsible for the torsion cross-section check according to art. 6.3.
    Includes the interaction between shear and torsion.

    Parameters
    ----------
    cs: RectangularReinforcedCrossSection
        The cross-section object containing geometry and reinforcement details.
    sigma_cp: MPA
        Mean compressive stress, measured positive, due to the design axial force [$MPa$].
    a_sl: MM2
        Area of the tensile reinforcement, which extends l_bd + d beyond the section considered (figure 6.3 EN 1992-1-1) [$mm²$].
    v_ed: N
        Shear force in the cross-section [$N$].
    t_ed: NMM
        Torsion moment in the cross-section [$Nmm$].
    alpha: DEG
        Angle between shear reinforcement and the beam axis perpendicular to the shear force [$°$].
        The default value is 90°.
    theta: DEG
        Angle between the concrete compression strut and the beam axis perpendicular to the shear force [$°$].
        The default value is 45°.
    """

    label = "Torsion according to art. 6.3"
    source_document = "EN 1992-1-1"

    cs: RectangularReinforcedCrossSection
    sigma_cp: MPA
    a_sl: MM2
    v_ed: N
    t_ed: NMM

    alpha: DEG = field(default=90)
    theta: DEG = field(default=45)

    def _get_orchestrator(self) -> TorsionCheckOrchestrator:
        """Create the orchestrator with refactored components."""
        geometry = TorsionGeometry(cs=self.cs)
        materials = TorsionMaterials(cs=self.cs)
        forces = TorsionForces(
            sigma_cp=self.sigma_cp,
            a_sl=self.a_sl,
            v_ed=self.v_ed,
            t_ed=self.t_ed,
            alpha=self.alpha,
            theta=self.theta,
        )
        return TorsionCheckOrchestrator(
            geometry=geometry,
            materials=materials,
            forces=forces,
        )

    def check(self) -> bool:
        """Perform the checks using the refactored structure."""
        orchestrator = self._get_orchestrator()
        return orchestrator.check()

    def latex(self, n: int = 1) -> str:
        """Returns the LaTeX string representation for the torsion check."""
        orchestrator = self._get_orchestrator()
        return orchestrator.latex(n)
