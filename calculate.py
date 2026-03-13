"""
建筑工程结构核心计算模块
包含混凝土梁、柱和钢结构的核心验算逻辑
"""

from dataclasses import dataclass
from enum import Enum
from typing import Optional

from blueprints.checks.check_result import CheckResult
from blueprints.codes.formula import Formula, LatexFormula
from blueprints.materials.concrete import ConcreteMaterial, ConcreteStrengthClass
from blueprints.materials.steel import SteelMaterial
from blueprints.materials.reinforcement_steel import ReinforcementSteelMaterial, ReinforcementSteelQualityClass
from blueprints.structural_sections.steel.steel_cross_section import SteelCrossSection
from blueprints.structural_sections.steel.standard_profiles.heb import HEB
from blueprints.structural_sections.steel.standard_profiles.hea import HEA
from blueprints.structural_sections.steel.standard_profiles.ipe import IPE
from blueprints.type_alias import DIMENSIONLESS, MM, MPA
from blueprints.unit_conversion import KN_TO_N, KNM_TO_NMM


class ConcreteGrade(str, Enum):
    """混凝土强度等级枚举"""
    C20 = "C20/25"
    C25 = "C25/30"
    C30 = "C30/37"
    C35 = "C35/45"
    C40 = "C40/50"
    C45 = "C45/55"
    C50 = "C50/60"


class SteelGrade(str, Enum):
    """钢材强度等级枚举"""
    S235 = "S235"
    S275 = "S275"
    S355 = "S355"
    S420 = "S420"
    S460 = "S460"


class RebarGrade(str, Enum):
    """钢筋强度等级枚举"""
    B400 = "B400"
    B500 = "B500"


class SteelProfileType(str, Enum):
    """钢截面类型枚举"""
    HEB = "HEB"
    HEA = "HEA"
    IPE = "IPE"


class FormConcreteFlexuralCapacity(Formula):
    """混凝土受弯承载力计算公式 (GB 50010-2010)"""
    
    def __new__(cls, f_cd: MPA, b: MM, x: MM, h0: MM, a_s: float, f_yd: MPA) -> "FormConcreteFlexuralCapacity":
        return super().__new__(cls, f_cd, b, x, h0, a_s, f_yd)
    
    @property
    def label(self) -> str:
        return "M_u"
    
    @property
    def source_document(self) -> str:
        return "GB 50010-2010"
    
    @staticmethod
    def _evaluate(f_cd: MPA, b: MM, x: MM, h0: MM, a_s: float, f_yd: MPA) -> float:
        return f_cd * b * x * (h0 - x / 2)
    
    def latex(self, n: int = 3) -> LatexFormula:
        return LatexFormula(
            return_symbol=r"M_u",
            result=f"{self:.{n}f}",
            equation=r"M_u = f_{cd} \cdot b \cdot x \cdot (h_0 - x/2)",
        )


class FormConcreteShearCapacity(Formula):
    """混凝土受剪承载力计算公式 (GB 50010-2010)"""
    
    def __new__(cls, f_t: MPA, b: MM, h0: MM, a_sv: float, f_yv: MPA, s: MM) -> "FormConcreteShearCapacity":
        return super().__new__(cls, f_t, b, h0, a_sv, f_yv, s)
    
    @property
    def label(self) -> str:
        return "V_u"
    
    @property
    def source_document(self) -> str:
        return "GB 50010-2010"
    
    @staticmethod
    def _evaluate(f_t: MPA, b: MM, h0: MM, a_sv: float, f_yv: MPA, s: MM) -> float:
        v_c = 0.7 * f_t * b * h0
        v_s = 1.25 * f_yv * a_sv * h0 / s
        return v_c + v_s
    
    def latex(self, n: int = 3) -> LatexFormula:
        return LatexFormula(
            return_symbol=r"V_u",
            result=f"{self:.{n}f}",
            equation=r"V_u = 0.7 f_t b h_0 + 1.25 f_{yv} \frac{A_{sv}}{s} h_0",
        )


class FormConcreteAxialCapacity(Formula):
    """混凝土轴心受压承载力计算公式 (GB 50010-2010)"""
    
    def __new__(cls, f_cd: MPA, a_c: float, f_yd: MPA, a_s: float, phi: float) -> "FormConcreteAxialCapacity":
        return super().__new__(cls, f_cd, a_c, f_yd, a_s, phi)
    
    @property
    def label(self) -> str:
        return "N_u"
    
    @property
    def source_document(self) -> str:
        return "GB 50010-2010"
    
    @staticmethod
    def _evaluate(f_cd: MPA, a_c: float, f_yd: MPA, a_s: float, phi: float) -> float:
        return phi * (f_cd * a_c + f_yd * a_s)
    
    def latex(self, n: int = 3) -> LatexFormula:
        return LatexFormula(
            return_symbol=r"N_u",
            result=f"{self:.{n}f}",
            equation=r"N_u = \varphi (f_{cd} A_c + f_y' A_s')",
        )


class FormSteelPlasticMomentCapacity(Formula):
    """钢截面塑性弯矩承载力计算公式 (EN 1993-1-1)"""
    
    def __new__(cls, w_pl: float, f_y: MPA, gamma_m0: DIMENSIONLESS) -> "FormSteelPlasticMomentCapacity":
        return super().__new__(cls, w_pl, f_y, gamma_m0)
    
    @property
    def label(self) -> str:
        return "M_pl_Rd"
    
    @property
    def source_document(self) -> str:
        return "EN 1993-1-1:2005"
    
    @staticmethod
    def _evaluate(w_pl: float, f_y: MPA, gamma_m0: DIMENSIONLESS) -> float:
        return w_pl * f_y / gamma_m0
    
    def latex(self, n: int = 3) -> LatexFormula:
        return LatexFormula(
            return_symbol=r"M_{pl,Rd}",
            result=f"{self:.{n}f}",
            equation=r"M_{pl,Rd} = \frac{W_{pl} f_y}{\gamma_{M0}}",
        )


class FormSteelCompressionCapacity(Formula):
    """钢截面受压承载力计算公式 (EN 1993-1-1)"""
    
    def __new__(cls, a: float, f_y: MPA, gamma_m0: DIMENSIONLESS) -> "FormSteelCompressionCapacity":
        return super().__new__(cls, a, f_y, gamma_m0)
    
    @property
    def label(self) -> str:
        return "N_c_Rd"
    
    @property
    def source_document(self) -> str:
        return "EN 1993-1-1:2005"
    
    @staticmethod
    def _evaluate(a: float, f_y: MPA, gamma_m0: DIMENSIONLESS) -> float:
        return a * f_y / gamma_m0
    
    def latex(self, n: int = 3) -> LatexFormula:
        return LatexFormula(
            return_symbol=r"N_{c,Rd}",
            result=f"{self:.{n}f}",
            equation=r"N_{c,Rd} = \frac{A f_y}{\gamma_{M0}}",
        )


class FormSteelBucklingCapacity(Formula):
    """钢截面稳定承载力计算公式 (EN 1993-1-1)"""
    
    def __new__(cls, a: float, f_y: MPA, phi: float, gamma_m1: DIMENSIONLESS) -> "FormSteelBucklingCapacity":
        return super().__new__(cls, a, f_y, phi, gamma_m1)
    
    @property
    def label(self) -> str:
        return "N_b_Rd"
    
    @property
    def source_document(self) -> str:
        return "EN 1993-1-1:2005"
    
    @staticmethod
    def _evaluate(a: float, f_y: MPA, phi: float, gamma_m1: DIMENSIONLESS) -> float:
        return phi * a * f_y / gamma_m1
    
    def latex(self, n: int = 3) -> LatexFormula:
        return LatexFormula(
            return_symbol=r"N_{b,Rd}",
            result=f"{self:.{n}f}",
            equation=r"N_{b,Rd} = \chi \frac{A f_y}{\gamma_{M1}}",
        )


class FormSteelShearCapacity(Formula):
    """钢截面受剪承载力计算公式 (EN 1993-1-1)"""
    
    def __new__(cls, a_v: float, f_y: MPA, gamma_m0: DIMENSIONLESS) -> "FormSteelShearCapacity":
        return super().__new__(cls, a_v, f_y, gamma_m0)
    
    @property
    def label(self) -> str:
        return "V_pl_Rd"
    
    @property
    def source_document(self) -> str:
        return "EN 1993-1-1:2005"
    
    @staticmethod
    def _evaluate(a_v: float, f_y: MPA, gamma_m0: DIMENSIONLESS) -> float:
        return a_v * f_y / (3 ** 0.5 * gamma_m0)
    
    def latex(self, n: int = 3) -> LatexFormula:
        return LatexFormula(
            return_symbol=r"V_{pl,Rd}",
            result=f"{self:.{n}f}",
            equation=r"V_{pl,Rd} = \frac{A_v f_y}{\sqrt{3} \gamma_{M0}}",
        )


def get_concrete_class(grade: ConcreteGrade) -> ConcreteStrengthClass:
    """根据混凝土等级获取Blueprints混凝土强度类"""
    mapping = {
        ConcreteGrade.C20: ConcreteStrengthClass.C20_25,
        ConcreteGrade.C25: ConcreteStrengthClass.C25_30,
        ConcreteGrade.C30: ConcreteStrengthClass.C30_37,
        ConcreteGrade.C35: ConcreteStrengthClass.C35_45,
        ConcreteGrade.C40: ConcreteStrengthClass.C40_50,
        ConcreteGrade.C45: ConcreteStrengthClass.C45_55,
        ConcreteGrade.C50: ConcreteStrengthClass.C50_60,
    }
    return mapping[grade]


def get_rebar_class(grade: RebarGrade) -> ReinforcementSteelQualityClass:
    """根据钢筋等级获取Blueprints钢筋强度类"""
    mapping = {
        RebarGrade.B400: ReinforcementSteelQualityClass.B400,
        RebarGrade.B500: ReinforcementSteelQualityClass.B500,
    }
    return mapping[grade]


def get_steel_class(grade: SteelGrade):
    """根据钢材等级获取Blueprints钢材强度类"""
    from blueprints.codes.eurocode.en_1993_1_1_2005.chapter_3_materials.table_3_1 import SteelStrengthClass as EC3SteelClass
    mapping = {
        SteelGrade.S235: EC3SteelClass.S235,
        SteelGrade.S275: EC3SteelClass.S275,
        SteelGrade.S355: EC3SteelClass.S355,
        SteelGrade.S420: EC3SteelClass.S420,
        SteelGrade.S460: EC3SteelClass.S460,
    }
    return mapping[grade]


def get_steel_profile(profile_type: SteelProfileType, profile_name: str):
    """根据截面类型和名称获取钢截面"""
    profile_mapping = {
        SteelProfileType.HEB: HEB,
        SteelProfileType.HEA: HEA,
        SteelProfileType.IPE: IPE,
    }
    
    profile_class = profile_mapping[profile_type]
    profile_enum = getattr(profile_class, profile_name.upper(), None)
    
    if profile_enum is None:
        raise ValueError(f"未找到截面类型: {profile_type.value} {profile_name}")
    
    return profile_enum.with_corrosion(0)


def calculate_rebar_area(diameter: MM, count: int) -> float:
    """计算钢筋总面积"""
    return count * 3.14159 * (diameter / 2) ** 2


def calculate_stability_coefficient(slenderness: float, steel_grade: SteelGrade) -> float:
    """计算稳定系数（基于中国规范简化方法）"""
    if slenderness <= 0:
        return 1.0
    
    lambda_limit = {
        SteelGrade.S235: 100,
        SteelGrade.S275: 95,
        SteelGrade.S355: 85,
        SteelGrade.S420: 80,
        SteelGrade.S460: 75,
    }.get(steel_grade, 85)
    
    if slenderness < lambda_limit * 0.3:
        return 1.0
    elif slenderness < lambda_limit * 0.6:
        return 0.95 - 0.1 * (slenderness - lambda_limit * 0.3) / (lambda_limit * 0.3)
    elif slenderness < lambda_limit:
        return 0.85 - 0.15 * (slenderness - lambda_limit * 0.6) / (lambda_limit * 0.4)
    else:
        return max(0.7 - 0.3 * (slenderness - lambda_limit) / lambda_limit, 0.3)


def calculate_phi_by_slenderness(slenderness: float) -> float:
    """根据长细比计算混凝土柱稳定系数（GB 50010-2010）"""
    if slenderness < 8:
        return 1.0
    elif slenderness < 10:
        return 0.98
    elif slenderness < 12:
        return 0.95
    elif slenderness < 14:
        return 0.92
    elif slenderness < 16:
        return 0.87
    elif slenderness < 18:
        return 0.81
    elif slenderness < 20:
        return 0.75
    elif slenderness < 22:
        return 0.70
    elif slenderness < 24:
        return 0.65
    elif slenderness < 26:
        return 0.60
    elif slenderness < 28:
        return 0.56
    else:
        return 0.52


@dataclass(frozen=True)
class ConcreteBeamResult:
    """混凝土梁验算结果"""
    flexural_capacity: float
    shear_capacity: float
    flexural_check: CheckResult
    shear_check: CheckResult
    effective_depth: float
    compression_zone_depth: float
    tension_rebar_area: float
    stirrup_area: float


@dataclass(frozen=True)
class ConcreteColumnResult:
    """混凝土柱验算结果"""
    axial_capacity: float
    axial_check: CheckResult
    combined_check: Optional[CheckResult]
    slenderness: float
    stability_coefficient: float
    concrete_area: float
    rebar_area: float


@dataclass(frozen=True)
class SteelBeamResult:
    """钢梁验算结果"""
    plastic_moment_capacity_y: float
    plastic_moment_capacity_z: Optional[float]
    shear_capacity: Optional[float]
    bending_check_y: CheckResult
    bending_check_z: Optional[CheckResult]
    shear_check: Optional[CheckResult]
    section_area: float
    yield_strength: float


@dataclass(frozen=True)
class SteelColumnResult:
    """钢柱验算结果"""
    compression_capacity: float
    buckling_capacity_y: float
    buckling_capacity_z: float
    compression_check: CheckResult
    buckling_check_y: CheckResult
    buckling_check_z: CheckResult
    combined_check: Optional[CheckResult]
    slenderness_y: float
    slenderness_z: float
    stability_coefficient_y: float
    stability_coefficient_z: float


class ConcreteBeamCalculator:
    """混凝土梁计算器"""
    
    def __init__(
        self,
        width: MM,
        height: MM,
        concrete_grade: ConcreteGrade,
        rebar_grade: RebarGrade,
        cover: MM,
        tension_rebar_diameter: MM,
        tension_rebar_count: int,
        compression_rebar_diameter: MM = 0,
        compression_rebar_count: int = 0,
        stirrup_diameter: MM = 8,
        stirrup_spacing: MM = 200,
    ):
        self.width = width
        self.height = height
        self.concrete_grade = concrete_grade
        self.rebar_grade = rebar_grade
        self.cover = cover
        self.tension_rebar_diameter = tension_rebar_diameter
        self.tension_rebar_count = tension_rebar_count
        self.compression_rebar_diameter = compression_rebar_diameter
        self.compression_rebar_count = compression_rebar_count
        self.stirrup_diameter = stirrup_diameter
        self.stirrup_spacing = stirrup_spacing
        
        self._concrete_material = ConcreteMaterial(
            concrete_class=get_concrete_class(concrete_grade),
        )
        self._rebar_material = ReinforcementSteelMaterial(
            steel_class=get_rebar_class(rebar_grade),
        )
    
    @property
    def f_cd(self) -> MPA:
        """混凝土轴心抗压设计值"""
        return self._concrete_material.f_cd
    
    @property
    def f_t(self) -> MPA:
        """混凝土抗拉强度"""
        return self._concrete_material.f_ctm
    
    @property
    def f_yd(self) -> MPA:
        """钢筋抗拉设计值"""
        return self._rebar_material.f_yd
    
    @property
    def effective_depth(self) -> MM:
        """截面有效高度"""
        return self.height - self.cover - self.stirrup_diameter - self.tension_rebar_diameter / 2
    
    @property
    def tension_rebar_area(self) -> float:
        """受拉钢筋面积"""
        return calculate_rebar_area(self.tension_rebar_diameter, self.tension_rebar_count)
    
    @property
    def stirrup_area(self) -> float:
        """箍筋面积（双肢）"""
        return 2 * 3.14159 * (self.stirrup_diameter / 2) ** 2
    
    def calculate_compression_zone_depth(self) -> MM:
        """计算受压区高度"""
        x = (self.f_yd * self.tension_rebar_area) / (self.f_cd * self.width)
        x_lim = 0.35 * self.effective_depth
        return min(x, x_lim)
    
    def calculate_flexural_capacity(self) -> FormConcreteFlexuralCapacity:
        """计算受弯承载力"""
        x = self.calculate_compression_zone_depth()
        return FormConcreteFlexuralCapacity(
            f_cd=self.f_cd,
            b=self.width,
            x=x,
            h0=self.effective_depth,
            a_s=self.tension_rebar_area,
            f_yd=self.f_yd,
        )
    
    def calculate_shear_capacity(self) -> FormConcreteShearCapacity:
        """计算受剪承载力"""
        return FormConcreteShearCapacity(
            f_t=self.f_t,
            b=self.width,
            h0=self.effective_depth,
            a_sv=self.stirrup_area,
            f_yv=self.f_yd,
            s=self.stirrup_spacing,
        )
    
    def check(self, design_moment: float, design_shear: float) -> ConcreteBeamResult:
        """执行验算"""
        design_moment_nmm = design_moment * KNM_TO_NMM
        design_shear_n = design_shear * KN_TO_N
        
        flexural_capacity = self.calculate_flexural_capacity()
        shear_capacity = self.calculate_shear_capacity()
        
        return ConcreteBeamResult(
            flexural_capacity=float(flexural_capacity),
            shear_capacity=float(shear_capacity),
            flexural_check=CheckResult.from_comparison(
                provided=design_moment_nmm,
                required=float(flexural_capacity),
            ),
            shear_check=CheckResult.from_comparison(
                provided=design_shear_n,
                required=float(shear_capacity),
            ),
            effective_depth=self.effective_depth,
            compression_zone_depth=self.calculate_compression_zone_depth(),
            tension_rebar_area=self.tension_rebar_area,
            stirrup_area=self.stirrup_area,
        )


class ConcreteColumnCalculator:
    """混凝土柱计算器"""
    
    def __init__(
        self,
        width: MM,
        height: MM,
        concrete_grade: ConcreteGrade,
        rebar_grade: RebarGrade,
        cover: MM,
        rebar_diameter: MM,
        rebar_count: int,
        effective_length: MM,
    ):
        self.width = width
        self.height = height
        self.concrete_grade = concrete_grade
        self.rebar_grade = rebar_grade
        self.cover = cover
        self.rebar_diameter = rebar_diameter
        self.rebar_count = rebar_count
        self.effective_length = effective_length
        
        self._concrete_material = ConcreteMaterial(
            concrete_class=get_concrete_class(concrete_grade),
        )
        self._rebar_material = ReinforcementSteelMaterial(
            steel_class=get_rebar_class(rebar_grade),
        )
    
    @property
    def f_cd(self) -> MPA:
        """混凝土轴心抗压设计值"""
        return self._concrete_material.f_cd
    
    @property
    def f_yd(self) -> MPA:
        """钢筋抗压设计值"""
        return self._rebar_material.f_yd
    
    @property
    def concrete_area(self) -> float:
        """混凝土面积"""
        return self.width * self.height
    
    @property
    def rebar_area(self) -> float:
        """钢筋面积"""
        return calculate_rebar_area(self.rebar_diameter, self.rebar_count)
    
    @property
    def slenderness(self) -> float:
        """长细比"""
        b = min(self.width, self.height)
        return self.effective_length / b
    
    @property
    def stability_coefficient(self) -> float:
        """稳定系数"""
        return calculate_phi_by_slenderness(self.slenderness)
    
    def calculate_axial_capacity(self) -> FormConcreteAxialCapacity:
        """计算轴心受压承载力"""
        return FormConcreteAxialCapacity(
            f_cd=self.f_cd,
            a_c=self.concrete_area,
            f_yd=self.f_yd,
            a_s=self.rebar_area,
            phi=self.stability_coefficient,
        )
    
    def check(self, design_axial_force: float, design_moment_y: float = 0, design_moment_z: float = 0) -> ConcreteColumnResult:
        """执行验算"""
        design_axial_n = design_axial_force * KN_TO_N
        
        axial_capacity = self.calculate_axial_capacity()
        
        combined_check = None
        if design_moment_y > 0 or design_moment_z > 0:
            h0 = min(self.width, self.height) - self.cover - self.rebar_diameter / 2
            moment_capacity = self.f_cd * self.width * 0.35 * h0 * (h0 - 0.35 * h0 / 2)
            total_moment = (design_moment_y ** 2 + design_moment_z ** 2) ** 0.5
            combined_check = CheckResult.from_comparison(
                provided=total_moment * KNM_TO_NMM,
                required=moment_capacity,
            )
        
        return ConcreteColumnResult(
            axial_capacity=float(axial_capacity),
            axial_check=CheckResult.from_comparison(
                provided=design_axial_n,
                required=float(axial_capacity),
            ),
            combined_check=combined_check,
            slenderness=self.slenderness,
            stability_coefficient=self.stability_coefficient,
            concrete_area=self.concrete_area,
            rebar_area=self.rebar_area,
        )


class SteelBeamCalculator:
    """钢梁计算器"""
    
    def __init__(
        self,
        profile_type: SteelProfileType,
        profile_name: str,
        steel_grade: SteelGrade,
        gamma_m0: DIMENSIONLESS = 1.0,
    ):
        self.profile_type = profile_type
        self.profile_name = profile_name
        self.steel_grade = steel_grade
        self.gamma_m0 = gamma_m0
        
        self._profile = get_steel_profile(profile_type, profile_name)
        self._steel_material = SteelMaterial(
            steel_class=get_steel_class(steel_grade),
        )
        self._steel_section = SteelCrossSection(
            profile=self._profile,
            material=self._steel_material,
        )
    
    @property
    def section_properties(self):
        """截面属性"""
        return self._profile.section_properties()
    
    @property
    def yield_strength(self) -> MPA:
        """屈服强度"""
        return self._steel_material.yield_strength(thickness=20)
    
    @property
    def section_area(self) -> float:
        """截面面积"""
        return float(self.section_properties.area or 0)
    
    @property
    def plastic_modulus_y(self) -> float:
        """塑性截面模量（绕Y轴）"""
        return float(self.section_properties.sxx or 0)
    
    @property
    def plastic_modulus_z(self) -> float:
        """塑性截面模量（绕Z轴）"""
        return float(self.section_properties.syy or 0)
    
    def calculate_plastic_moment_capacity_y(self) -> FormSteelPlasticMomentCapacity:
        """计算塑性弯矩承载力（绕Y轴）"""
        return FormSteelPlasticMomentCapacity(
            w_pl=self.plastic_modulus_y,
            f_y=self.yield_strength,
            gamma_m0=self.gamma_m0,
        )
    
    def calculate_plastic_moment_capacity_z(self) -> FormSteelPlasticMomentCapacity:
        """计算塑性弯矩承载力（绕Z轴）"""
        return FormSteelPlasticMomentCapacity(
            w_pl=self.plastic_modulus_z,
            f_y=self.yield_strength,
            gamma_m0=self.gamma_m0,
        )
    
    def calculate_shear_capacity(self) -> FormSteelShearCapacity:
        """计算受剪承载力"""
        a_v = self.section_area * 0.5
        return FormSteelShearCapacity(
            a_v=a_v,
            f_y=self.yield_strength,
            gamma_m0=self.gamma_m0,
        )
    
    def check(
        self,
        design_moment_y: float,
        design_moment_z: float = 0,
        design_shear: float = 0,
    ) -> SteelBeamResult:
        """执行验算"""
        design_moment_y_nmm = design_moment_y * KNM_TO_NMM
        design_moment_z_nmm = design_moment_z * KNM_TO_NMM
        design_shear_n = design_shear * KN_TO_N
        
        m_pl_rd_y = self.calculate_plastic_moment_capacity_y()
        m_pl_rd_z = self.calculate_plastic_moment_capacity_z()
        v_pl_rd = self.calculate_shear_capacity()
        
        bending_check_z = None
        if design_moment_z > 0:
            bending_check_z = CheckResult.from_comparison(
                provided=design_moment_z_nmm,
                required=float(m_pl_rd_z),
            )
        
        shear_check = None
        if design_shear > 0:
            shear_check = CheckResult.from_comparison(
                provided=design_shear_n,
                required=float(v_pl_rd),
            )
        
        return SteelBeamResult(
            plastic_moment_capacity_y=float(m_pl_rd_y),
            plastic_moment_capacity_z=float(m_pl_rd_z) if design_moment_z > 0 else None,
            shear_capacity=float(v_pl_rd) if design_shear > 0 else None,
            bending_check_y=CheckResult.from_comparison(
                provided=design_moment_y_nmm,
                required=float(m_pl_rd_y),
            ),
            bending_check_z=bending_check_z,
            shear_check=shear_check,
            section_area=self.section_area,
            yield_strength=self.yield_strength,
        )


class SteelColumnCalculator:
    """钢柱计算器"""
    
    def __init__(
        self,
        profile_type: SteelProfileType,
        profile_name: str,
        steel_grade: SteelGrade,
        effective_length_y: MM,
        effective_length_z: MM,
        gamma_m0: DIMENSIONLESS = 1.0,
        gamma_m1: DIMENSIONLESS = 1.0,
    ):
        self.profile_type = profile_type
        self.profile_name = profile_name
        self.steel_grade = steel_grade
        self.effective_length_y = effective_length_y
        self.effective_length_z = effective_length_z
        self.gamma_m0 = gamma_m0
        self.gamma_m1 = gamma_m1
        
        self._profile = get_steel_profile(profile_type, profile_name)
        self._steel_material = SteelMaterial(
            steel_class=get_steel_class(steel_grade),
        )
        self._steel_section = SteelCrossSection(
            profile=self._profile,
            material=self._steel_material,
        )
    
    @property
    def section_properties(self):
        """截面属性"""
        return self._profile.section_properties()
    
    @property
    def yield_strength(self) -> MPA:
        """屈服强度"""
        return self._steel_material.yield_strength(thickness=20)
    
    @property
    def elastic_modulus(self) -> float:
        """弹性模量"""
        return self._steel_material.e_modulus
    
    @property
    def section_area(self) -> float:
        """截面面积"""
        return float(self.section_properties.area or 0)
    
    @property
    def inertia_y(self) -> float:
        """惯性矩（绕Y轴）"""
        return float(self.section_properties.ixx or 0)
    
    @property
    def inertia_z(self) -> float:
        """惯性矩（绕Z轴）"""
        return float(self.section_properties.iyy or 0)
    
    @property
    def radius_of_gyration_y(self) -> float:
        """回转半径（绕Y轴）"""
        return (self.inertia_y / self.section_area) ** 0.5 if self.section_area > 0 else 0
    
    @property
    def radius_of_gyration_z(self) -> float:
        """回转半径（绕Z轴）"""
        return (self.inertia_z / self.section_area) ** 0.5 if self.section_area > 0 else 0
    
    @property
    def slenderness_y(self) -> float:
        """长细比（绕Y轴）"""
        return self.effective_length_y / self.radius_of_gyration_y if self.radius_of_gyration_y > 0 else 0
    
    @property
    def slenderness_z(self) -> float:
        """长细比（绕Z轴）"""
        return self.effective_length_z / self.radius_of_gyration_z if self.radius_of_gyration_z > 0 else 0
    
    @property
    def stability_coefficient_y(self) -> float:
        """稳定系数（绕Y轴）"""
        return calculate_stability_coefficient(self.slenderness_y, self.steel_grade)
    
    @property
    def stability_coefficient_z(self) -> float:
        """稳定系数（绕Z轴）"""
        return calculate_stability_coefficient(self.slenderness_z, self.steel_grade)
    
    def calculate_compression_capacity(self) -> FormSteelCompressionCapacity:
        """计算受压承载力"""
        return FormSteelCompressionCapacity(
            a=self.section_area,
            f_y=self.yield_strength,
            gamma_m0=self.gamma_m0,
        )
    
    def calculate_buckling_capacity_y(self) -> FormSteelBucklingCapacity:
        """计算稳定承载力（绕Y轴）"""
        return FormSteelBucklingCapacity(
            a=self.section_area,
            f_y=self.yield_strength,
            phi=self.stability_coefficient_y,
            gamma_m1=self.gamma_m1,
        )
    
    def calculate_buckling_capacity_z(self) -> FormSteelBucklingCapacity:
        """计算稳定承载力（绕Z轴）"""
        return FormSteelBucklingCapacity(
            a=self.section_area,
            f_y=self.yield_strength,
            phi=self.stability_coefficient_z,
            gamma_m1=self.gamma_m1,
        )
    
    @property
    def plastic_modulus_y(self) -> float:
        """塑性截面模量（绕Y轴）"""
        return float(self.section_properties.sxx or 0)
    
    @property
    def plastic_modulus_z(self) -> float:
        """塑性截面模量（绕Z轴）"""
        return float(self.section_properties.syy or 0)
    
    def check(
        self,
        design_axial_force: float,
        design_moment_y: float = 0,
        design_moment_z: float = 0,
    ) -> SteelColumnResult:
        """执行验算"""
        design_axial_n = abs(design_axial_force) * KN_TO_N
        design_moment_y_nmm = design_moment_y * KNM_TO_NMM
        design_moment_z_nmm = design_moment_z * KNM_TO_NMM
        
        n_c_rd = self.calculate_compression_capacity()
        n_b_rd_y = self.calculate_buckling_capacity_y()
        n_b_rd_z = self.calculate_buckling_capacity_z()
        
        combined_check = None
        if design_moment_y > 0 or design_moment_z > 0:
            m_pl_rd_y = self.plastic_modulus_y * self.yield_strength / self.gamma_m0
            m_pl_rd_z = self.plastic_modulus_z * self.yield_strength / self.gamma_m0
            
            utilization = (
                design_axial_n / float(n_b_rd_y) +
                design_moment_y_nmm / m_pl_rd_y +
                design_moment_z_nmm / m_pl_rd_z
            )
            combined_check = CheckResult.from_unity_check(utilization)
        
        return SteelColumnResult(
            compression_capacity=float(n_c_rd),
            buckling_capacity_y=float(n_b_rd_y),
            buckling_capacity_z=float(n_b_rd_z),
            compression_check=CheckResult.from_comparison(
                provided=design_axial_n,
                required=float(n_c_rd),
            ),
            buckling_check_y=CheckResult.from_comparison(
                provided=design_axial_n,
                required=float(n_b_rd_y),
            ),
            buckling_check_z=CheckResult.from_comparison(
                provided=design_axial_n,
                required=float(n_b_rd_z),
            ),
            combined_check=combined_check,
            slenderness_y=self.slenderness_y,
            slenderness_z=self.slenderness_z,
            stability_coefficient_y=self.stability_coefficient_y,
            stability_coefficient_z=self.stability_coefficient_z,
        )


if __name__ == "__main__":
    print("=" * 60)
    print("建筑工程结构核心计算模块 - 示例")
    print("=" * 60)
    
    print("\n【混凝土梁验算示例】")
    beam_calc = ConcreteBeamCalculator(
        width=300,
        height=500,
        concrete_grade=ConcreteGrade.C30,
        rebar_grade=RebarGrade.B500,
        cover=30,
        tension_rebar_diameter=20,
        tension_rebar_count=3,
        stirrup_diameter=8,
        stirrup_spacing=150,
    )
    beam_result = beam_calc.check(design_moment=150, design_shear=80)
    print(f"  受弯承载力: {beam_result.flexural_capacity/1e6:.2f} kNm")
    print(f"  受剪承载力: {beam_result.shear_capacity/1e3:.2f} kN")
    print(f"  受弯验算: {'通过' if beam_result.flexural_check.is_ok else '不通过'}")
    print(f"  受剪验算: {'通过' if beam_result.shear_check.is_ok else '不通过'}")
    
    print("\n【混凝土柱验算示例】")
    column_calc = ConcreteColumnCalculator(
        width=400,
        height=400,
        concrete_grade=ConcreteGrade.C35,
        rebar_grade=RebarGrade.B500,
        cover=30,
        rebar_diameter=20,
        rebar_count=8,
        effective_length=4000,
    )
    column_result = column_calc.check(design_axial_force=2000, design_moment_y=50)
    print(f"  轴压承载力: {column_result.axial_capacity/1e3:.2f} kN")
    print(f"  长细比: {column_result.slenderness:.1f}")
    print(f"  稳定系数: {column_result.stability_coefficient:.3f}")
    print(f"  轴压验算: {'通过' if column_result.axial_check.is_ok else '不通过'}")
    
    print("\n【钢梁验算示例】")
    steel_beam_calc = SteelBeamCalculator(
        profile_type=SteelProfileType.HEB,
        profile_name="HEB300",
        steel_grade=SteelGrade.S355,
    )
    steel_beam_result = steel_beam_calc.check(design_moment_y=300, design_shear=200)
    print(f"  塑性弯矩承载力: {steel_beam_result.plastic_moment_capacity_y/1e6:.2f} kNm")
    print(f"  受弯验算: {'通过' if steel_beam_result.bending_check_y.is_ok else '不通过'}")
    
    print("\n【钢柱验算示例】")
    steel_column_calc = SteelColumnCalculator(
        profile_type=SteelProfileType.HEB,
        profile_name="HEB300",
        steel_grade=SteelGrade.S355,
        effective_length_y=4000,
        effective_length_z=4000,
    )
    steel_column_result = steel_column_calc.check(design_axial_force=-1500, design_moment_y=50)
    print(f"  受压承载力: {steel_column_result.compression_capacity/1e3:.2f} kN")
    print(f"  稳定承载力(Y轴): {steel_column_result.buckling_capacity_y/1e3:.2f} kN")
    print(f"  稳定验算: {'通过' if steel_column_result.buckling_check_y.is_ok else '不通过'}")
    
    print("\n" + "=" * 60)
    print("计算完成")
    print("=" * 60)
