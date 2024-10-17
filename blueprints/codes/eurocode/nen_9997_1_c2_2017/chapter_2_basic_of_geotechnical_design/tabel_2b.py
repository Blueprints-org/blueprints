
from dataclasses import dataclass
import math
from blueprints.codes.eurocode.nen_9997_1_c2_2017.chapter_2_basic_of_geotechnical_design.table_2b_soil_types import SoilTypesTable2b

        
@dataclass(frozen=True)
class SoilParametersTable2b:
    
    gamma_unsat: float
    """The unsaturated unit weight of the soil [kN/m^3]."""
    gamma_sat: float
    """The saturated unit weight of the soil [kN/m^3]."""
    qc_table: float
    """The representative cone resistance [MPa] after effective stress correction."""
    C_p: float
    """The Koppejan primary compression coefficient C'p for stresses above the preconsolidation stress."""
    C_s: float
    """The Koppejan secondary compression coefficient C's for stresses above the preconsolidation stress."""
    C_R: float
    """The Bjerrum compression ratio CR [-]. Note that CR = C_c / (1 + e0)."""
    C_alpha: float
    """The Bjerrum secondary compression index C_alpha [-]."""
    R_R: float
    """The Bjerrum recompression/swelling ratio RR [-]. Note that RR = C_sw / (1 + e0).""" 
    E_100: float
    """The elastic modulus of the soil [MPa] at a vertical stress of 100 kPa."""
    phi: float
    """The effective friction angle of the soil [deg]."""
    c: float
    """The drained cohesion of the soil [kPa]."""
    c_u: float | None
    """The undrained cohesion of the soil [kPa]."""
     


_LOWER_BOUND_MAP = {
    SoilTypesTable2b.GRAVEL_SL_LOOSE: SoilParametersTable2b(
        gamma_unsat=17.0,
        gamma_sat=19.0,
        qc_table=15.0,
        C_p=500.0,
        C_s=float("inf"),
        C_R=0.0046,
        C_alpha=0.0,
        R_R=0.0015,
        E_100=45.0,
        phi=32.5,
        c=0.0,
        c_u=None,
    ),
    SoilTypesTable2b.GRAVEL_SL_SILTY_MEDIUM_DENSE: SoilParametersTable2b(
        gamma_unsat=18.0,
        gamma_sat=20.0,
        qc_table=25.0,
        C_p=1000.0,
        C_s=float("inf"),
        C_R=0.0023,
        C_alpha=0.0,
        R_R=0.0008,
        E_100=75.0,
        phi=35.0,
        c=0.0,
        c_u=None,
    ),
    SoilTypesTable2b.GRAVEL_SL_SILTY_DENSE: SoilParametersTable2b(
        gamma_unsat=19.0,
        gamma_sat=21.0,
        qc_table=30.0,
        C_p=1200.0,
        C_s=float("inf"),
        C_R=0.0019,
        C_alpha=0.0,
        R_R=0.0006,
        E_100=90.0,
        phi=37.5,
        c=0.0,
        c_u=None,
    ),
    SoilTypesTable2b.GRAVEL_V_SILTY_LOOSE: SoilParametersTable2b(
        gamma_unsat=18.0,
        gamma_sat=20.0,
        qc_table=10.0,
        C_p=400.0,
        C_s=float("inf"),
        C_R=0.0058,
        C_alpha=0.0,
        R_R=0.0019,
        E_100=30.0,
        phi=30.0,
        c=0.0,
        c_u=None,
    ),
    SoilTypesTable2b.GRAVEL_V_SILTY_MEDIUM_DENSE: SoilParametersTable2b(
        gamma_unsat=19.0,
        gamma_sat=21.0,
        qc_table=15.0,
        C_p=600.0,
        C_s=float("inf"),
        C_R=0.0038,
        C_alpha=0.0,
        R_R=0.0013,
        E_100=45.0,
        phi=32.5,
        c=0.0,
        c_u=None,
    ),
    SoilTypesTable2b.GRAVEL_V_SILTY_DENSE: SoilParametersTable2b(
        gamma_unsat=20.0,
        gamma_sat=22.0,
        qc_table=20.0,
        C_p=1000.0,
        C_s=float("inf"),
        C_R=0.0029,
        C_alpha=0.0,
        R_R=0.0008,
        E_100=75.0,
        phi=35.0,
        c=0.0,
        c_u=None,
    ),
    SoilTypesTable2b.SAND_CLEAN_LOOSE: SoilParametersTable2b(
        gamma_unsat=17.0,
        gamma_sat=19.0,
        qc_table=5.0,
        C_p=200.0,
        C_s=float("inf"),
        C_R=0.0115,
        C_alpha=0.0,
        R_R=0.0038,
        E_100=15.0,
        phi=30.0,
        c=0.0,
        c_u=None,
    ),
    SoilTypesTable2b.SAND_CLEAN_MEDIUM_DENSE: SoilParametersTable2b(
        gamma_unsat=18.0,
        gamma_sat=20.0,
        qc_table=15.0,
        C_p=600.0,
        C_s=float("inf"),
        C_R=0.0038,
        C_alpha=0.0,
        R_R=0.0013,
        E_100=45.0,
        phi=32.5,
        c=0.0,
        c_u=None,
    ),
    SoilTypesTable2b.SAND_CLEAN_DENSE: SoilParametersTable2b(
        gamma_unsat=19.0,
        gamma_sat=21.0,
        qc_table=25.0,
        C_p=1000.0,
        C_s=float("inf"),
        C_R=0.0023,
        C_alpha=0.0,
        R_R=0.0008,
        E_100=75.0,
        phi=35.0,
        c=0.0,
        c_u=None,
    ),
    SoilTypesTable2b.SAND_SL_SILTY_CLAYEY: SoilParametersTable2b(
        gamma_unsat=18.0,
        gamma_sat=20.0,
        qc_table=12.0,
        C_p=450.0,
        C_s=float("inf"),
        C_R=0.0051,
        C_alpha=0.0,
        R_R=0.0017,
        E_100=35.0,
        phi=27.0,
        c=0.0,
        c_u=None,
    ),
    SoilTypesTable2b.SAND_V_SILTY_CLAYEY: SoilParametersTable2b(
        gamma_unsat=18.0,
        gamma_sat=20.0,
        qc_table=8.0,
        C_p=450.0,
        C_s=float("inf"),
        C_R=0.0051,
        C_alpha=0.0,
        R_R=0.0017,
        E_100=35.0,
        phi=27.0,
        c=0.0,
        c_u=None,
    ),
}

class Tabel2b(dict):
    _map_lower_bound: dict = {
        SoilTypesTable2b.GRAVEL_SL_LOOSE: 
    
    }

    def get_parameter(self, parameter: str, soil_type: SoilTypesTable2b) -> float:
        return self._map_lower_bound[soil_type][parameter]


SOIL_TABEL_2B = Tabel2b()

print(SOIL_TABEL_2B.get_parameter("phi", SoilTypesTable2b.GRAVEL_SL_LOOSE))
