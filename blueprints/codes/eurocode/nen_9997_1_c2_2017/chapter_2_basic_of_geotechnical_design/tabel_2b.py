
from copy import deepcopy
from dataclasses import dataclass
from functools import cached_property

import pandas as pd

from blueprints.codes.eurocode.nen_9997_1_c2_2017.chapter_2_basic_of_geotechnical_design.table_2b_soil_types import \
    SoilTypesTable2b


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
     

    @cached_property
    def as_dict(self) -> dict:
        return {
            "gamma_unsat": self.gamma_unsat,
            "gamma_sat": self.gamma_sat,
            "qc_table": self.qc_table,
            "C_p": self.C_p,
            "C_s": self.C_s,
            "C_R": self.C_R,
            "C_alpha": self.C_alpha,
            "R_R": self.R_R,
            "E_100": self.E_100,
            "phi": self.phi,
            "c": self.c,
            "c_u": self.c_u,
        }


class Tabel2b:
    
    _LOW_CHARACTERISTIC_MAP = {
        SoilTypesTable2b.GRAVEL_SL_SILTY_LOOSE: SoilParametersTable2b(
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
            C_p=200.0,
            C_s=float("inf"),
            C_R=0.0115,
            C_alpha=0.0,
            R_R=0.0038,
            E_100=15.0,
            phi=25.0,
            c=0.0,
            c_u=None,
        ),
        SoilTypesTable2b.LOAM_SL_SANDY_SOFT: SoilParametersTable2b(
            gamma_unsat=19.0,
            gamma_sat=19.0,
            qc_table=1.0,
            C_p=25.0,
            C_s=650.0,
            C_R=0.0920,
            C_alpha=0.0037,
            R_R=0.0307,
            E_100=2.0,
            phi=27.5,
            c=0.0,
            c_u=50.0,
        ),
        SoilTypesTable2b.LOAM_SL_SANDY_MEDIUM_STIFF: SoilParametersTable2b(
            gamma_unsat=20.0,
            gamma_sat=20.0,
            qc_table=2.0,
            C_p=45.0,
            C_s=1300.0,
            C_R=0.0511,
            C_alpha=0.0020,
            R_R=0.0170,
            E_100=3.0,
            phi=27.5,
            c=1.0,
            c_u=100.0,
        ),
        SoilTypesTable2b.LOAM_SL_SANDY_STIFF: SoilParametersTable2b(
            gamma_unsat=21.0,
            gamma_sat=21.0,
            qc_table=3.0,
            C_p=70.0,
            C_s=1900.0,
            C_R=0.0329,
            C_alpha=0.0013,
            R_R=0.0110,
            E_100=5.0,
            phi=27.5,
            c=2.5,
            c_u=200.0,
        ),
        SoilTypesTable2b.LOAM_V_SANDY: SoilParametersTable2b(
            gamma_unsat=19.0,
            gamma_sat=19.0,
            qc_table=2.0,
            C_p=45.0,
            C_s=1300.0,
            C_R=0.0511,
            C_alpha=0.0020,
            R_R=0.0170,
            E_100=3.0,
            phi=27.5,
            c=0.0,
            c_u=50.0,
        ),
        SoilTypesTable2b.CLAY_CLEAN_SOFT: SoilParametersTable2b(
            gamma_unsat=14.0,
            gamma_sat=14.0,
            qc_table=0.5,
            C_p=7.0,
            C_s=80.0,
            C_R=0.3286,
            C_alpha=0.0131,
            R_R=0.1095,
            E_100=1.0,
            phi=17.5,
            c=0.0,
            c_u=25.0,
        ),
        SoilTypesTable2b.CLAY_CLEAN_MEDIUM_STIFF: SoilParametersTable2b(
            gamma_unsat=17.0,
            gamma_sat=17.0,
            qc_table=1.0,
            C_p=15.0,
            C_s=160.0,
            C_R=0.1533,
            C_alpha=0.0061,
            R_R=0.0511,
            E_100=2.0,
            phi=17.5,
            c=5.0,
            c_u=50.0,
        ),
        SoilTypesTable2b.CLAY_CLEAN_STIFF: SoilParametersTable2b(
            gamma_unsat=19.0,
            gamma_sat=19.0,
            qc_table=2.0,
            C_p=25.0,
            C_s=320.0,
            C_R=0.0920,
            C_alpha=0.0037,
            R_R=0.0307,
            E_100=4.0,
            phi=17.5,
            c=13.0,
            c_u=100.0,
        ),
        SoilTypesTable2b.CLAY_SL_SANDY_SOFT: SoilParametersTable2b(
            gamma_unsat=15.0,
            gamma_sat=15.0,
            qc_table=0.7,
            C_p=10.0,
            C_s=110.0,
            C_R=0.2300,
            C_alpha=0.0092,
            R_R=0.0767,
            E_100=1.5,
            phi=22.5,
            c=0.0,
            c_u=40.0,
        ),
        SoilTypesTable2b.CLAY_SL_SANDY_MEDIUM_STIFF: SoilParametersTable2b(
            gamma_unsat=18.0,
            gamma_sat=18.0,
            qc_table=1.5,
            C_p=20.0,
            C_s=240.0,
            C_R=0.1150,
            C_alpha=0.0046,
            R_R=0.0383,
            E_100=3.0,
            phi=22.5,
            c=5.0,
            c_u=80.0,
        ),
        SoilTypesTable2b.CLAY_SL_SANDY_STIFF: SoilParametersTable2b(
            gamma_unsat=20.0,
            gamma_sat=20.0,
            qc_table=2.5,
            C_p=30.0,
            C_s=400.0,
            C_R=0.0767,
            C_alpha=0.0031,
            R_R=0.0256,
            E_100=5.0,
            phi=22.5,
            c=13.0,
            c_u=120.0,
        ),
        SoilTypesTable2b.CLAY_V_SANDY: SoilParametersTable2b(
            gamma_unsat=18.0,
            gamma_sat=18.0,
            qc_table=1.0,
            C_p=25.0,
            C_s=320.0,
            C_R=0.0920,
            C_alpha=0.0037,
            R_R=0.0307,
            E_100=2.0,
            phi=27.5,
            c=0.0,
            c_u=0.0,
        ),
        SoilTypesTable2b.CLAY_ORGANIC_SOFT: SoilParametersTable2b(
            gamma_unsat=13.0,
            gamma_sat=13.0,
            qc_table=0.2,
            C_p=7.5,
            C_s=30.0,
            C_R=0.3067,
            C_alpha=0.0153,
            R_R=0.1022,
            E_100=0.5,
            phi=15.0,
            c=0.0,
            c_u=10.0,
        ),
        SoilTypesTable2b.CLAY_ORGANIC_MEDIUM_STIFF: SoilParametersTable2b(
            gamma_unsat=15.0,
            gamma_sat=15.0,
            qc_table=0.5,
            C_p=10.0,
            C_s=40.0,
            C_R=0.230,
            C_alpha=0.0115,
            R_R=0.0767,
            E_100=1.0,
            phi=15.0,
            c=0.0,
            c_u=25.0,
        ),
        SoilTypesTable2b.PEAT_NC: SoilParametersTable2b(
            gamma_unsat=10.0,
            gamma_sat=10.0,
            qc_table=0.1,
            C_p=5.0,
            C_s=20.0,
            C_R=0.460,
            C_alpha=0.0230,
            R_R=0.1533,
            E_100=0.2,
            phi=15.0,
            c=1.0,
            c_u=10.0,
        ),
        SoilTypesTable2b.PEAT_OC: SoilParametersTable2b(
            gamma_unsat=12.0,
            gamma_sat=12.0,
            qc_table=0.2,
            C_p=7.5,
            C_s=30.0,
            C_R=0.3067,
            C_alpha=0.0153,
            R_R=0.1022,
            E_100=0.5,
            phi=15.0,
            c=2.5,
            c_u=20.0,
        ),
    }


    _HIGH_CHARACTERISTIC_MAP = {
        SoilTypesTable2b.GRAVEL_SL_SILTY_LOOSE: SoilParametersTable2b(
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
        SoilTypesTable2b.GRAVEL_SL_SILTY_MEDIUM_DENSE: SoilParametersTable2b(
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
        SoilTypesTable2b.GRAVEL_SL_SILTY_DENSE: SoilParametersTable2b(
            gamma_unsat=20.0,
            gamma_sat=22.0,
            qc_table=30.0,
            C_p=1400.0,
            C_s=float("inf"),
            C_R=0.0016,
            C_alpha=0.0,
            R_R=0.0005,
            E_100=105.0,
            phi=40.0,
            c=0.0,
            c_u=None,
        ),
        SoilTypesTable2b.GRAVEL_V_SILTY_LOOSE: SoilParametersTable2b(
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
        SoilTypesTable2b.GRAVEL_V_SILTY_MEDIUM_DENSE: SoilParametersTable2b(
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
        SoilTypesTable2b.GRAVEL_V_SILTY_DENSE: SoilParametersTable2b(
            gamma_unsat=21.0,
            gamma_sat=22.5,
            qc_table=25.0,
            C_p=1500.0,
            C_s=float("inf"),
            C_R=0.0015,
            C_alpha=0.0,
            R_R=0.0005,
            E_100=110.0,
            phi=40.0,
            c=0.0,
            c_u=None,
        ),
        SoilTypesTable2b.SAND_CLEAN_LOOSE: SoilParametersTable2b(
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
        SoilTypesTable2b.SAND_CLEAN_MEDIUM_DENSE: SoilParametersTable2b(
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
        SoilTypesTable2b.SAND_CLEAN_DENSE: SoilParametersTable2b(
            gamma_unsat=20.0,
            gamma_sat=22.0,
            qc_table=25.0,
            C_p=1500.0,
            C_s=float("inf"),
            C_R=0.0015,
            C_alpha=0.0,
            R_R=0.0005,
            E_100=110.0,
            phi=40.0,
            c=0.0,
            c_u=None,
        ),
        SoilTypesTable2b.SAND_SL_SILTY_CLAYEY: SoilParametersTable2b(
            gamma_unsat=19.0,
            gamma_sat=21.0,
            qc_table=12.0,
            C_p=650.0,
            C_s=float("inf"),
            C_R=0.0035,
            C_alpha=0.0,
            R_R=0.0012,
            E_100=50.0,
            phi=32.5,
            c=0.0,
            c_u=None,
        ),
        SoilTypesTable2b.SAND_V_SILTY_CLAYEY: SoilParametersTable2b(
            gamma_unsat=19.0,
            gamma_sat=21.0,
            qc_table=8.0,
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
        SoilTypesTable2b.LOAM_SL_SANDY_SOFT: SoilParametersTable2b(
            gamma_unsat=20.0,
            gamma_sat=20.0,
            qc_table=2.0,
            C_p=45.0,
            C_s=1300.0,
            C_R=0.0511,
            C_alpha=0.0020,
            R_R=0.0170,
            E_100=3.0,
            phi=27.5,
            c=1.0,
            c_u=100.0,
        ),
        SoilTypesTable2b.LOAM_SL_SANDY_MEDIUM_STIFF: SoilParametersTable2b(
            gamma_unsat=21.0,
            gamma_sat=21.0,
            qc_table=3.0,
            C_p=70.0,
            C_s=1900.0,
            C_R=0.0329,
            C_alpha=0.0013,
            R_R=0.0110,
            E_100=5.0,
            phi=27.5,
            c=2.5,
            c_u=200.0,
        ),
        SoilTypesTable2b.LOAM_SL_SANDY_STIFF: SoilParametersTable2b(
            gamma_unsat=22.0,
            gamma_sat=22.0,
            qc_table=3.0,
            C_p=100.0,
            C_s=2500.0,
            C_R=0.0230,
            C_alpha=0.0009,
            R_R=0.0077,
            E_100=7.0,
            phi=35.0,
            c=3.8,
            c_u=300.0,
        ),
        SoilTypesTable2b.LOAM_V_SANDY: SoilParametersTable2b(
            gamma_unsat=20.0,
            gamma_sat=20.0,
            qc_table=2.0,
            C_p=70.0,
            C_s=2000.0,
            C_R=0.0329,
            C_alpha=0.0013,
            R_R=0.0110,
            E_100=5.0,
            phi=35.0,
            c=1.0,
            c_u=100.0,
        ),
        SoilTypesTable2b.CLAY_CLEAN_SOFT: SoilParametersTable2b(
            gamma_unsat=17.0,
            gamma_sat=17.0,
            qc_table=1.0,
            C_p=15.0,
            C_s=160.0,
            C_R=0.1533,
            C_alpha=0.0061,
            R_R=0.0511,
            E_100=2.0,
            phi=17.5,
            c=5.0,
            c_u=50.0,
        ),
        SoilTypesTable2b.CLAY_CLEAN_MEDIUM_STIFF: SoilParametersTable2b(
            gamma_unsat=19.0,
            gamma_sat=19.0,
            qc_table=2.0,
            C_p=25.0,
            C_s=320.0,
            C_R=0.0920,
            C_alpha=0.0037,
            R_R=0.0307,
            E_100=4.0,
            phi=17.5,
            c=13.0,
            c_u=100.0,
        ),
        SoilTypesTable2b.CLAY_CLEAN_STIFF: SoilParametersTable2b(
            gamma_unsat=20.0,
            gamma_sat=20.0,
            qc_table=2.0,
            C_p=30.0,
            C_s=500.0,
            C_R=0.0767,
            C_alpha=0.0031,
            R_R=0.0256,
            E_100=10.0,
            phi=25.0,
            c=15.0,
            c_u=200.0,
        ),
        SoilTypesTable2b.CLAY_SL_SANDY_SOFT: SoilParametersTable2b(
            gamma_unsat=18.0,
            gamma_sat=18.0,
            qc_table=1.5,
            C_p=20.0,
            C_s=240.0,
            C_R=0.1150,
            C_alpha=0.0046,
            R_R=0.0383,
            E_100=3.0,
            phi=22.5,
            c=5.0,
            c_u=80.0,
        ),
        SoilTypesTable2b.CLAY_SL_SANDY_MEDIUM_STIFF: SoilParametersTable2b(
            gamma_unsat=20.0,
            gamma_sat=20.0,
            qc_table=2.5,
            C_p=30.0,
            C_s=400.0,
            C_R=0.0767,
            C_alpha=0.0031,
            R_R=0.0256,
            E_100=5.0,
            phi=22.5,
            c=13.0,
            c_u=120.0,
        ),
        SoilTypesTable2b.CLAY_SL_SANDY_STIFF: SoilParametersTable2b(
            gamma_unsat=21.0,
            gamma_sat=21.0,
            qc_table=2.5,
            C_p=50.0,
            C_s=600.0,
            C_R=0.0460,
            C_alpha=0.0018,
            R_R=0.0153,
            E_100=10.0,
            phi=27.5,
            c=15.0,
            c_u=170.0,
        ),
        SoilTypesTable2b.CLAY_V_SANDY: SoilParametersTable2b(
            gamma_unsat=20.0,
            gamma_sat=20.0,
            qc_table=1.0,
            C_p=140.0,
            C_s=1680.0,
            C_R=0.0164,
            C_alpha=0.0007,
            R_R=0.0055,
            E_100=5.0,
            phi=32.5,
            c=1.0,
            c_u=10.0,
        ),
        SoilTypesTable2b.CLAY_ORGANIC_SOFT: SoilParametersTable2b(
            gamma_unsat=15.0,
            gamma_sat=15.0,
            qc_table=0.5,
            C_p=10.0,
            C_s=40.0,
            C_R=0.230,
            C_alpha=0.0115,
            R_R=0.0767,
            E_100=1.0,
            phi=15.0,
            c=0.0,
            c_u=25.0,
        ),
        SoilTypesTable2b.CLAY_ORGANIC_MEDIUM_STIFF: SoilParametersTable2b(
            gamma_unsat=16.0,
            gamma_sat=16.0,
            qc_table=0.5,
            C_p=15.0,
            C_s=60.0,
            C_R=0.1533,
            C_alpha=0.0077,
            R_R=0.0511,
            E_100=2.0,
            phi=15.0,
            c=1.0,
            c_u=30.0,
        ),
        SoilTypesTable2b.PEAT_NC: SoilParametersTable2b(
            gamma_unsat=12.0,
            gamma_sat=12.0,
            qc_table=0.1,
            C_p=7.5,
            C_s=30.0,
            C_R=0.3067,
            C_alpha=0.0153,
            R_R=0.1022,
            E_100=0.5,
            phi=15.0,
            c=2.5,
            c_u=20.0,
        ),
        SoilTypesTable2b.PEAT_OC: SoilParametersTable2b(
            gamma_unsat=13.0,
            gamma_sat=13.0,
            qc_table=0.2,
            C_p=10.0,
            C_s=40.0,
            C_R=0.2300,
            C_alpha=0.0115,
            R_R=0.0767,
            E_100=1.0,
            phi=15.0,
            c=5.0,
            c_u=30.0,
        ),
    }
    

    def get_low_characteristic_parameters(self, soil_type_or_name: SoilTypesTable2b | str) -> SoilParametersTable2b:
        """Get the low characteristic parameters of the soil type.
        
        Parameters
        ----------
        soil_type_or_name : SoilTypesTable2b | str
            The soil type or name (English or Dutch).
            
        Returns
        -------
        SoilParametersTable2b
            The low characteristic parameters of the soil type.
        
        Raises
        ------
        TypeError
            If `soil_type_or_name` is not of type SoilTypesTable2b or str.
        """

        # Parse soil type based on input
        match soil_type_or_name:
            case str():
                soil_type = SoilTypesTable2b.CLAY_CLEAN_MEDIUM_STIFF.get_soil_type_by_name(soil_type_or_name)
            case SoilTypesTable2b():
                soil_type = soil_type_or_name
            case _:
                raise TypeError(f"`soil_type_or_name` must be of type SoilTypesTable2b or str, not '{type(soil_type_or_name)}'")
        
        return self._LOW_CHARACTERISTIC_MAP[soil_type]
        

    def get_high_characteristic_parameters(self, soil_type_or_name: SoilTypesTable2b | str) -> SoilParametersTable2b:
        """Get the high characteristic parameters of the soil type.
        
        Parameters
        ----------
        soil_type_or_name : SoilTypesTable2b | str
            The soil type or name (English or Dutch).
            
        Returns
        -------
        SoilParametersTable2b
            The high characteristic parameters of the soil type.
        
        Raises
        ------
        TypeError
            If `soil_type_or_name` is not of type SoilTypesTable2b or str.
        """

        # Parse soil type based on input
        match soil_type_or_name:
            case str():
                soil_type = SoilTypesTable2b.CLAY_CLEAN_MEDIUM_STIFF.get_soil_type_by_name(soil_type_or_name)
            case SoilTypesTable2b():
                soil_type = soil_type_or_name
            case _:
                raise TypeError(f"`soil_type_or_name` must be of type SoilTypesTable2b or str, not '{type(soil_type_or_name)}'")
        
        return self._HIGH_CHARACTERISTIC_MAP[soil_type]

    
    @cached_property
    def low_characteristic_dataframe(self) -> pd.DataFrame:
        """Returns the low characteristic parameters of all soil types in a DataFrame."""
        records = []
        for soil_type in SoilTypesTable2b:
            records.append(soil_type.value.as_dict | self.get_low_characteristic_parameters(soil_type).as_dict)
            
        return pd.DataFrame.from_records(records)

    @cached_property
    def high_characteristic_dataframe(self) -> pd.DataFrame:
        """Returns the high characteristic parameters of all soil types in a DataFrame."""
        records = []
        for soil_type in SoilTypesTable2b:
            records.append(soil_type.value.as_dict | self.get_high_characteristic_parameters(soil_type).as_dict)
            
        return pd.DataFrame.from_records(records)



SOIL_TABEL_2B = Tabel2b()



print()
