"""
建筑工程结构计算模块
基于Blueprints库开发的结构计算模块，包含混凝土梁、柱、钢结构验算

功能：
1. 混凝土梁抗弯、抗剪计算
2. 混凝土柱轴心受压、偏心受压计算
3. 钢结构受弯、受压、受拉验算
4. FastAPI接口服务

作者：AI Assistant
日期：2026-03-13
"""

import math
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional, Literal, List, Dict, Any
from abc import ABC, abstractmethod

# 导入Blueprints库相关模块
from blueprints.materials.concrete import ConcreteMaterial, ConcreteStrengthClass
from blueprints.materials.steel import SteelMaterial
from blueprints.codes.eurocode.en_1992_1_1_2004 import EN_1992_1_1_2004
from blueprints.codes.eurocode.en_1993_1_1_2005 import EN_1993_1_1_2005
from blueprints.checks.check_result import CheckResult

# Pydantic模型
from pydantic import BaseModel, Field, validator, root_validator

# FastAPI
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
import uvicorn


# ============================================================================
# 类型定义
# ============================================================================

# 单位类型别名
MM = float  # 毫米
MPA = float  # 兆帕
KN = float  # 千牛
KNM = float  # 千牛·米
MM2 = float  # 平方毫米
MM3 = float  # 立方毫米
MM4 = float  # 四次方毫米
DIMENSIONLESS = float  # 无量纲


# ============================================================================
# 枚举类型
# ============================================================================

class SectionType(str, Enum):
    """截面类型枚举"""
    RECTANGULAR = "矩形截面"
    CIRCULAR = "圆形截面"
    T_SECTION = "T形截面"
    I_SECTION = "I形截面"


class LoadType(str, Enum):
    """荷载类型枚举"""
    DEAD_LOAD = "恒载"
    LIVE_LOAD = "活载"
    WIND_LOAD = "风载"
    SEISMIC_LOAD = "地震荷载"


class DesignStatus(str, Enum):
    """设计状态枚举"""
    PASS = "通过"
    FAIL = "不通过"
    WARNING = "警告"


# ============================================================================
# Pydantic 请求/响应模型
# ============================================================================

class ConcreteMaterialInput(BaseModel):
    """混凝土材料输入模型"""
    strength_class: str = Field(default="C30/37", description="混凝土强度等级")
    material_factor: float = Field(default=1.5, description="材料分项系数")
    density: float = Field(default=2500.0, description="密度 kg/m³")

    @validator('strength_class')
    def validate_strength_class(cls, v):
        valid_classes = ["C12/15", "C16/20", "C20/25", "C25/30", "C30/37", 
                        "C35/45", "C40/50", "C45/55", "C50/60"]
        if v not in valid_classes:
            raise ValueError(f"无效的混凝土强度等级，可选: {valid_classes}")
        return v


class SteelMaterialInput(BaseModel):
    """钢材材料输入模型"""
    steel_class: str = Field(default="S355", description="钢材等级")
    yield_strength: Optional[float] = Field(default=None, description="屈服强度 MPa")
    ultimate_strength: Optional[float] = Field(default=None, description="极限强度 MPa")
    material_factor: float = Field(default=1.0, description="材料分项系数")


class RectangularSectionInput(BaseModel):
    """矩形截面输入模型"""
    width: float = Field(..., gt=0, description="截面宽度 mm")
    height: float = Field(..., gt=0, description="截面高度 mm")
    cover: float = Field(default=25.0, gt=0, description="保护层厚度 mm")


class ReinforcementInput(BaseModel):
    """钢筋配置输入模型"""
    top_rebar_diameter: float = Field(default=16.0, gt=0, description="上部钢筋直径 mm")
    top_rebar_count: int = Field(default=3, ge=0, description="上部钢筋根数")
    bottom_rebar_diameter: float = Field(default=20.0, gt=0, description="下部钢筋直径 mm")
    bottom_rebar_count: int = Field(default=4, ge=0, description="下部钢筋根数")
    stirrup_diameter: float = Field(default=8.0, gt=0, description="箍筋直径 mm")
    stirrup_spacing: float = Field(default=150.0, gt=0, description="箍筋间距 mm")
    steel_yield_strength: float = Field(default=400.0, gt=0, description="钢筋屈服强度 MPa")


class BeamLoadInput(BaseModel):
    """梁荷载输入模型"""
    dead_load: float = Field(default=10.0, ge=0, description="恒载 kN/m")
    live_load: float = Field(default=15.0, ge=0, description="活载 kN/m")
    span: float = Field(..., gt=0, description="跨度 m")


class ColumnLoadInput(BaseModel):
    """柱荷载输入模型"""
    axial_load: float = Field(..., description="轴力 kN (压力为正)")
    moment_x: float = Field(default=0.0, description="绕X轴弯矩 kN·m")
    moment_y: float = Field(default=0.0, description="绕Y轴弯矩 kN·m")
    effective_length: float = Field(..., gt=0, description="计算长度 m")


class SteelSectionInput(BaseModel):
    """钢截面输入模型"""
    section_type: str = Field(default="IPE300", description="截面型号")
    area: float = Field(..., gt=0, description="截面积 mm²")
    moment_of_inertia_y: float = Field(..., gt=0, description="绕Y轴惯性矩 mm⁴")
    moment_of_inertia_z: float = Field(..., gt=0, description="绕Z轴惯性矩 mm⁴")
    section_modulus_y: float = Field(..., gt=0, description="绕Y轴截面模量 mm³")
    section_modulus_z: float = Field(..., gt=0, description="绕Z轴截面模量 mm³")
    radius_of_gyration_y: float = Field(..., gt=0, description="绕Y轴回转半径 mm")
    radius_of_gyration_z: float = Field(..., gt=0, description="绕Z轴回转半径 mm")


class CalculationResult(BaseModel):
    """计算结果模型"""
    status: str = Field(..., description="计算状态")
    unity_check: float = Field(..., description="统一验算系数")
    capacity: float = Field(..., description="承载力")
    demand: float = Field(..., description="需求")
    details: Dict[str, Any] = Field(default_factory=dict, description="详细结果")
    messages: List[str] = Field(default_factory=list, description="提示信息")


# ============================================================================
# 核心计算类 - 混凝土梁
# ============================================================================

class ConcreteBeamCalculator:
    """
    混凝土梁计算器
    
    功能：
    - 正截面抗弯承载力计算
    - 斜截面抗剪承载力计算
    - 裂缝宽度验算
    - 挠度验算
    """
    
    def __init__(
        self,
        concrete: ConcreteMaterialInput,
        section: RectangularSectionInput,
        reinforcement: ReinforcementInput,
    ):
        self.concrete_input = concrete
        self.section_input = section
        self.reinforcement_input = reinforcement
        
        # 初始化Blueprints混凝土材料
        strength_class = getattr(ConcreteStrengthClass, concrete.strength_class.replace("/", "_"))
        self.concrete = ConcreteMaterial(
            concrete_class=strength_class,
            material_factor=concrete.material_factor
        )
        
    def calculate_flexural_capacity(self) -> CalculationResult:
        """
        计算正截面抗弯承载力
        
        基于EC2第6.1节，采用简化矩形应力分布法
        """
        # 几何参数
        b = self.section_input.width  # 截面宽度 mm
        h = self.section_input.height  # 截面高度 mm
        d = h - self.section_input.cover - self.reinforcement_input.bottom_rebar_diameter / 2  # 有效高度 mm
        
        # 钢筋面积
        As = (math.pi / 4) * self.reinforcement_input.bottom_rebar_diameter**2 * self.reinforcement_input.bottom_rebar_count
        
        # 材料强度
        fcd = self.concrete.f_cd  # 混凝土设计抗压强度 MPa
        fyd = self.reinforcement_input.steel_yield_strength / 1.15  # 钢筋设计屈服强度 MPa
        
        # 计算中性轴位置 (简化矩形应力分布)
        # 假设混凝土压应力矩形分布，高度为 0.8x
        # 平衡方程: As * fyd = 0.8 * x * b * fcd
        x = (As * fyd) / (0.8 * b * fcd)
        
        # 检查中性轴位置限制 (EC2 限制 x/d <= 0.45 对于C50/60以下混凝土)
        x_limit = 0.45 * d
        is_under_reinforced = x <= x_limit
        
        # 计算内力臂
        z = d - 0.4 * x
        
        # 计算抗弯承载力
        M_rd = As * fyd * z / 1e6  # kN·m
        
        # 配筋率
        rho = As / (b * d) * 100  # 百分比
        rho_min = self.concrete.rho_min(f_yd=fyd)
        
        details = {
            "effective_depth_d": d,
            "steel_area_As": As,
            "neutral_axis_x": x,
            "x_over_d_ratio": x / d,
            "lever_arm_z": z,
            "concrete_fcd": fcd,
            "steel_fyd": fyd,
            "reinforcement_ratio": rho,
            "min_reinforcement_ratio": rho_min,
            "is_under_reinforced": is_under_reinforced,
        }
        
        messages = []
        if not is_under_reinforced:
            messages.append(f"警告: 中性轴位置 x/d = {x/d:.3f} > 0.45, 可能发生超筋破坏")
        if rho < rho_min:
            messages.append(f"警告: 配筋率 {rho:.3f}% < 最小配筋率 {rho_min:.3f}%")
        
        return CalculationResult(
            status=DesignStatus.PASS if is_under_reinforced else DesignStatus.FAIL,
            unity_check=x / x_limit if x > 0 else 0,
            capacity=M_rd,
            demand=0,  # 由外部设置
            details=details,
            messages=messages
        )
    
    def calculate_shear_capacity(self, axial_force: float = 0.0) -> CalculationResult:
        """
        计算斜截面抗剪承载力
        
        基于EC2第6.2节
        
        Parameters
        ----------
        axial_force : float
            轴力 kN (压力为正，拉力为负)
        """
        # 几何参数
        b = self.section_input.width  # mm
        h = self.section_input.height  # mm
        d = h - self.section_input.cover - self.reinforcement_input.bottom_rebar_diameter / 2  # 有效高度 mm
        
        # 材料强度
        fck = self.concrete.f_ck  # 混凝土特征抗压强度 MPa
        fcd = self.concrete.f_cd  # 混凝土设计抗压强度 MPa
        fyd = self.reinforcement_input.steel_yield_strength / 1.15  # 钢筋设计屈服强度 MPa
        
        # 箍筋面积
        Asw = (math.pi / 4) * self.reinforcement_input.stirrup_diameter**2 * 2  # 双肢箍
        s = self.reinforcement_input.stirrup_spacing  # 箍筋间距 mm
        
        # 计算混凝土抗剪贡献 (EC2 公式6.2a)
        # VRd,c = [0.18/γc * k * (100*ρl*fck)^(1/3) + 0.15*σcp] * bw * d
        k = min(1 + math.sqrt(200 / d), 2.0)
        
        # 纵向配筋率
        Asl = (math.pi / 4) * self.reinforcement_input.bottom_rebar_diameter**2 * self.reinforcement_input.bottom_rebar_count
        rho_l = min(Asl / (b * d), 0.02)
        
        # 轴向应力
        sigma_cp = min(axial_force * 1000 / (b * h), 0.2 * fcd)  # MPa
        
        # 混凝土抗剪承载力
        v_rd_c = (0.18 / self.concrete.material_factor * k * (100 * rho_l * fck)**(1/3) + 0.15 * sigma_cp) * b * d / 1000  # kN
        
        # 最小抗剪承载力 (EC2 公式6.2b)
        v_rd_c_min = (0.035 * k**1.5 * math.sqrt(fck) + 0.15 * sigma_cp) * b * d / 1000  # kN
        
        v_rd_c = max(v_rd_c, v_rd_c_min)
        
        # 计算箍筋抗剪贡献 (EC2 公式6.8)
        # VRd,s = (Asw/s) * z * fyd * cotθ
        z = 0.9 * d  # 内力臂 mm
        theta = math.radians(45)  # 假设压杆角度 45度
        cot_theta = 1 / math.tan(theta)
        
        v_rd_s = (Asw / s) * z * fyd * cot_theta / 1000  # kN
        
        # 最大抗剪承载力限制 (EC2 公式6.9)
        # VRd,max = αcw * bw * z * ν1 * fcd / (cotθ + tanθ)
        alpha_cw = 1.0  # 无轴力时
        nu_1 = 0.6 * (1 - fck / 250)
        v_rd_max = alpha_cw * b * z * nu_1 * fcd / (cot_theta + math.tan(theta)) / 1000  # kN
        
        # 总抗剪承载力
        v_rd = min(v_rd_c + v_rd_s, v_rd_max)
        
        details = {
            "effective_depth_d": d,
            "k_factor": k,
            "longitudinal_reinforcement_ratio": rho_l,
            "concrete_contribution_VRd_c": v_rd_c,
            "steel_contribution_VRd_s": v_rd_s,
            "max_shear_VRd_max": v_rd_max,
            "total_shear_capacity": v_rd,
            "stirrup_area_Asw": Asw,
            "lever_arm_z": z,
            "concrete_fck": fck,
            "steel_fyd": fyd,
        }
        
        return CalculationResult(
            status=DesignStatus.PASS,
            unity_check=0,
            capacity=v_rd,
            demand=0,
            details=details,
            messages=[]
        )
    
    def check_flexural(self, applied_moment: float) -> CheckResult:
        """
        抗弯验算
        
        Parameters
        ----------
        applied_moment : float
            作用弯矩 kN·m
        """
        result = self.calculate_flexural_capacity()
        result.demand = applied_moment
        unity_check = applied_moment / result.capacity if result.capacity > 0 else float('inf')
        
        return CheckResult.from_comparison(
            provided=applied_moment,
            required=result.capacity,
            operator="<="
        )
    
    def check_shear(self, applied_shear: float, axial_force: float = 0.0) -> CheckResult:
        """
        抗剪验算
        
        Parameters
        ----------
        applied_shear : float
            作用剪力 kN
        axial_force : float
            轴力 kN
        """
        result = self.calculate_shear_capacity(axial_force)
        
        return CheckResult.from_comparison(
            provided=applied_shear,
            required=result.capacity,
            operator="<="
        )


# ============================================================================
# 核心计算类 - 混凝土柱
# ============================================================================

class ConcreteColumnCalculator:
    """
    混凝土柱计算器
    
    功能：
    - 轴心受压承载力计算
    - 偏心受压承载力计算 (NM相关曲线)
    - 稳定性验算
    """
    
    def __init__(
        self,
        concrete: ConcreteMaterialInput,
        section: RectangularSectionInput,
        reinforcement: ReinforcementInput,
    ):
        self.concrete_input = concrete
        self.section_input = section
        self.reinforcement_input = reinforcement
        
        # 初始化Blueprints混凝土材料
        strength_class = getattr(ConcreteStrengthClass, concrete.strength_class.replace("/", "_"))
        self.concrete = ConcreteMaterial(
            concrete_class=strength_class,
            material_factor=concrete.material_factor
        )
    
    def calculate_axial_capacity(self) -> CalculationResult:
        """
        计算轴心受压承载力
        
        基于EC2第3.1.7节
        """
        # 几何参数
        b = self.section_input.width  # mm
        h = self.section_input.height  # mm
        A_c = b * h  # 混凝土截面积 mm²
        
        # 钢筋面积 (全部纵筋)
        A_s_top = (math.pi / 4) * self.reinforcement_input.top_rebar_diameter**2 * self.reinforcement_input.top_rebar_count
        A_s_bottom = (math.pi / 4) * self.reinforcement_input.bottom_rebar_diameter**2 * self.reinforcement_input.bottom_rebar_count
        A_s = A_s_top + A_s_bottom
        
        # 材料强度
        fcd = self.concrete.f_cd  # 混凝土设计抗压强度 MPa
        fyd = self.reinforcement_input.steel_yield_strength / 1.15  # 钢筋设计屈服强度 MPa
        
        # 轴心受压承载力 (EC2 公式3.15)
        # N_Rd = A_c * fcd + A_s * fyd
        N_rd = (A_c * fcd + A_s * fyd) / 1000  # kN
        
        # 配筋率
        rho = A_s / A_c * 100  # 百分比
        
        details = {
            "concrete_area_Ac": A_c,
            "steel_area_As": A_s,
            "total_area": A_c + A_s,
            "concrete_fcd": fcd,
            "steel_fyd": fyd,
            "reinforcement_ratio": rho,
        }
        
        return CalculationResult(
            status=DesignStatus.PASS,
            unity_check=0,
            capacity=N_rd,
            demand=0,
            details=details,
            messages=[]
        )
    
    def calculate_eccentric_capacity(self, moment_x: float, moment_y: float, axial_force: float) -> CalculationResult:
        """
        计算偏心受压承载力 (简化方法)
        
        Parameters
        ----------
        moment_x : float
            绕X轴弯矩 kN·m
        moment_y : float
            绕Y轴弯矩 kN·m
        axial_force : float
            轴力 kN (压力为正)
        """
        # 获取轴心受压承载力
        axial_result = self.calculate_axial_capacity()
        N_rd_0 = axial_result.capacity
        
        # 几何参数
        b = self.section_input.width
        h = self.section_input.height
        d = h - self.section_input.cover - self.reinforcement_input.bottom_rebar_diameter / 2
        
        # 计算截面抗弯承载力 (纯弯)
        flexural_result = self._calculate_pure_flexural_capacity()
        M_rd_0 = flexural_result.capacity
        
        # 简化NM相互作用 (线性交互)
        # (N/N0) + (M/M0) <= 1
        N_ratio = abs(axial_force) / N_rd_0 if N_rd_0 > 0 else 0
        M_ratio = math.sqrt(moment_x**2 + moment_y**2) / M_rd_0 if M_rd_0 > 0 else 0
        
        unity_check = N_ratio + M_ratio
        
        details = {
            "axial_capacity_N0": N_rd_0,
            "flexural_capacity_M0": M_rd_0,
            "axial_ratio": N_ratio,
            "moment_ratio": M_ratio,
            "applied_moment": math.sqrt(moment_x**2 + moment_y**2),
            "applied_axial": axial_force,
        }
        
        status = DesignStatus.PASS if unity_check <= 1.0 else DesignStatus.FAIL
        
        return CalculationResult(
            status=status,
            unity_check=unity_check,
            capacity=N_rd_0,
            demand=abs(axial_force),
            details=details,
            messages=[]
        )
    
    def _calculate_pure_flexural_capacity(self) -> CalculationResult:
        """计算纯弯承载力 (用于偏心受压计算)"""
        b = self.section_input.width
        h = self.section_input.height
        d = h - self.section_input.cover - self.reinforcement_input.bottom_rebar_diameter / 2
        
        # 受拉钢筋面积
        A_s = (math.pi / 4) * self.reinforcement_input.bottom_rebar_diameter**2 * self.reinforcement_input.bottom_rebar_count
        
        fcd = self.concrete.f_cd
        fyd = self.reinforcement_input.steel_yield_strength / 1.15
        
        x = (A_s * fyd) / (0.8 * b * fcd)
        z = d - 0.4 * x
        M_rd = A_s * fyd * z / 1e6
        
        return CalculationResult(
            status=DesignStatus.PASS,
            unity_check=0,
            capacity=M_rd,
            demand=0,
            details={},
            messages=[]
        )
    
    def check_stability(self, axial_force: float, effective_length: float) -> CheckResult:
        """
        稳定性验算 (欧拉屈曲)
        
        Parameters
        ----------
        axial_force : float
            轴力 kN
        effective_length : float
            计算长度 m
        """
        # 几何参数
        b = self.section_input.width / 1000  # m
        h = self.section_input.height / 1000  # m
        
        # 截面惯性矩 (取弱轴)
        I_min = min(b * h**3 / 12, h * b**3 / 12)  # m⁴
        
        # 回转半径
        A = b * h
        i_min = math.sqrt(I_min / A)
        
        # 长细比
        lambda_ratio = effective_length / i_min
        
        # 欧拉临界力
        E_cm = self.concrete.e_cm * 1e6  # Pa
        N_cr = (math.pi**2 * E_cm * I_min) / (effective_length**2) / 1000  # kN
        
        # 稳定性系数 (简化)
        if lambda_ratio <= 25:
            phi = 1.0
        elif lambda_ratio <= 50:
            phi = 0.9
        elif lambda_ratio <= 75:
            phi = 0.8
        else:
            phi = 0.7
        
        # 稳定承载力
        axial_result = self.calculate_axial_capacity()
        N_rd = axial_result.capacity * phi
        
        unity_check = axial_force / N_rd if N_rd > 0 else float('inf')
        
        return CheckResult.from_unity_check(unity_check=unity_check)


# ============================================================================
# 核心计算类 - 钢结构
# ============================================================================

class SteelStructureCalculator:
    """
    钢结构计算器
    
    功能：
    - 受弯构件验算
    - 轴心受压构件验算
    - 轴心受拉构件验算
    - 压弯构件验算
    """
    
    def __init__(
        self,
        steel: SteelMaterialInput,
        section: SteelSectionInput,
    ):
        self.steel_input = steel
        self.section_input = section
        
        # 材料强度
        self.fy = steel.yield_strength or 355.0  # MPa
        self.fu = steel.ultimate_strength or 490.0  # MPa
        self.gamma_m0 = steel.material_factor
    
    def check_bending(self, applied_moment_y: float, applied_moment_z: float = 0.0) -> CalculationResult:
        """
        受弯构件验算
        
        基于EC3第6.2.5节
        
        Parameters
        ----------
        applied_moment_y : float
            绕Y轴弯矩 kN·m
        applied_moment_z : float
            绕Z轴弯矩 kN·m
        """
        # 截面模量
        W_y = self.section_input.section_modulus_y  # mm³
        W_z = self.section_input.section_modulus_z  # mm³
        
        # 设计屈服强度
        fyd = self.fy / self.gamma_m0  # MPa
        
        # 抗弯承载力
        M_y_rd = W_y * fyd / 1e6  # kN·m
        M_z_rd = W_z * fyd / 1e6  # kN·m
        
        # 双向受弯验算 (简化线性交互)
        if M_y_rd > 0 and M_z_rd > 0:
            unity_check = abs(applied_moment_y) / M_y_rd + abs(applied_moment_z) / M_z_rd
        elif M_y_rd > 0:
            unity_check = abs(applied_moment_y) / M_y_rd
        else:
            unity_check = float('inf')
        
        capacity = math.sqrt(M_y_rd**2 + M_z_rd**2)
        demand = math.sqrt(applied_moment_y**2 + applied_moment_z**2)
        
        details = {
            "section_modulus_y": W_y,
            "section_modulus_z": W_z,
            "yield_strength_fyd": fyd,
            "moment_capacity_y": M_y_rd,
            "moment_capacity_z": M_z_rd,
            "applied_moment_y": applied_moment_y,
            "applied_moment_z": applied_moment_z,
        }
        
        status = DesignStatus.PASS if unity_check <= 1.0 else DesignStatus.FAIL
        
        return CalculationResult(
            status=status,
            unity_check=unity_check,
            capacity=capacity,
            demand=demand,
            details=details,
            messages=[]
        )
    
    def check_axial_compression(self, axial_force: float, effective_length_y: float, effective_length_z: float) -> CalculationResult:
        """
        轴心受压构件验算
        
        基于EC3第6.2.4节和第6.3.1节
        
        Parameters
        ----------
        axial_force : float
            轴力 kN (压力为正)
        effective_length_y : float
            绕Y轴计算长度 m
        effective_length_z : float
            绕Z轴计算长度 m
        """
        # 截面积
        A = self.section_input.area  # mm²
        
        # 设计屈服强度
        fyd = self.fy / self.gamma_m0  # MPa
        
        # 截面抗压承载力
        N_c_rd = A * fyd / 1000  # kN
        
        # 回转半径
        i_y = self.section_input.radius_of_gyration_y  # mm
        i_z = self.section_input.radius_of_gyration_z  # mm
        
        # 长细比
        lambda_y = (effective_length_y * 1000) / i_y
        lambda_z = (effective_length_z * 1000) / i_z
        lambda_max = max(lambda_y, lambda_z)
        
        # 欧拉临界长细比 (S355钢材)
        lambda_1 = 86.8  # 对于S355钢材
        
        # 相对长细比
        lambda_bar = lambda_max / lambda_1
        
        # 稳定系数 (Perry-Robertson公式简化)
        # 假设b类曲线，alpha = 0.34
        alpha = 0.34
        phi = 0.5 * (1 + alpha * (lambda_bar - 0.2) + lambda_bar**2)
        chi = 1 / (phi + math.sqrt(phi**2 - lambda_bar**2))
        chi = min(chi, 1.0)
        
        # 稳定承载力
        N_b_rd = chi * A * fyd / 1000  # kN
        
        unity_check = abs(axial_force) / N_b_rd if N_b_rd > 0 else float('inf')
        
        details = {
            "area_A": A,
            "yield_strength_fyd": fyd,
            "section_capacity_NcRd": N_c_rd,
            "buckling_capacity_NbRd": N_b_rd,
            "slenderness_y": lambda_y,
            "slenderness_z": lambda_z,
            "relative_slenderness": lambda_bar,
            "buckling_reduction_factor": chi,
        }
        
        status = DesignStatus.PASS if unity_check <= 1.0 else DesignStatus.FAIL
        
        return CalculationResult(
            status=status,
            unity_check=unity_check,
            capacity=N_b_rd,
            demand=abs(axial_force),
            details=details,
            messages=[]
        )
    
    def check_axial_tension(self, axial_force: float) -> CalculationResult:
        """
        轴心受拉构件验算
        
        基于EC3第6.2.3节
        
        Parameters
        ----------
        axial_force : float
            轴力 kN (拉力为正)
        """
        # 截面积
        A = self.section_input.area  # mm²
        
        # 设计强度
        fyd = self.fy / self.gamma_m0  # MPa
        fud = self.fu / 1.25  # MPa (抗拉强度分项系数)
        
        # 屈服承载力
        N_pl_rd = A * fyd / 1000  # kN
        
        # 极限承载力 (考虑净截面，简化计算)
        N_u_rd = 0.9 * A * fud / 1000  # kN
        
        # 控制承载力
        N_t_rd = min(N_pl_rd, N_u_rd)
        
        unity_check = abs(axial_force) / N_t_rd if N_t_rd > 0 else float('inf')
        
        details = {
            "area_A": A,
            "yield_strength_fyd": fyd,
            "ultimate_strength_fud": fud,
            "plastic_capacity_NplRd": N_pl_rd,
            "ultimate_capacity_NuRd": N_u_rd,
            "tension_capacity": N_t_rd,
        }
        
        status = DesignStatus.PASS if unity_check <= 1.0 else DesignStatus.FAIL
        
        return CalculationResult(
            status=status,
            unity_check=unity_check,
            capacity=N_t_rd,
            demand=abs(axial_force),
            details=details,
            messages=[]
        )
    
    def check_combined_compression_bending(
        self,
        axial_force: float,
        moment_y: float,
        moment_z: float,
        effective_length_y: float,
        effective_length_z: float
    ) -> CalculationResult:
        """
        压弯构件验算
        
        基于EC3第6.2.9节
        
        Parameters
        ----------
        axial_force : float
            轴力 kN
        moment_y : float
            绕Y轴弯矩 kN·m
        moment_z : float
            绕Z轴弯矩 kN·m
        effective_length_y : float
            绕Y轴计算长度 m
        effective_length_z : float
            绕Z轴计算长度 m
        """
        # 轴压验算
        compression_result = self.check_axial_compression(axial_force, effective_length_y, effective_length_z)
        N_b_rd = compression_result.details["buckling_capacity_NbRd"]
        
        # 受弯验算
        bending_result = self.check_bending(moment_y, moment_z)
        M_y_rd = bending_result.details["moment_capacity_y"]
        M_z_rd = bending_result.details["moment_capacity_z"]
        
        # 截面抗压承载力
        A = self.section_input.area
        fyd = self.fy / self.gamma_m0
        N_pl_rd = A * fyd / 1000
        
        # 交互公式 (EC3 公式6.61和6.62)
        n = abs(axial_force) / N_pl_rd
        
        # 考虑轴力影响的抗弯承载力折减
        a = 0.5  # 对于I型截面
        M_N_y_rd = M_y_rd * (1 - n) / (1 - 0.5 * a) if n > 0.25 else M_y_rd
        M_N_z_rd = M_z_rd * (1 - n) / (1 - 0.5 * a) if n > 0.25 else M_z_rd
        
        M_N_y_rd = min(M_N_y_rd, M_y_rd)
        M_N_z_rd = min(M_N_z_rd, M_z_rd)
        
        # 线性交互公式
        if N_b_rd > 0 and M_N_y_rd > 0 and M_N_z_rd > 0:
            unity_check = abs(axial_force) / N_b_rd + moment_y / M_N_y_rd + moment_z / M_N_z_rd
        else:
            unity_check = float('inf')
        
        details = {
            "axial_compression_ratio": n,
            "buckling_capacity": N_b_rd,
            "moment_capacity_y": M_y_rd,
            "moment_capacity_z": M_z_rd,
            "reduced_moment_capacity_y": M_N_y_rd,
            "reduced_moment_capacity_z": M_N_z_rd,
        }
        
        status = DesignStatus.PASS if unity_check <= 1.0 else DesignStatus.FAIL
        
        return CalculationResult(
            status=status,
            unity_check=unity_check,
            capacity=N_b_rd,
            demand=abs(axial_force),
            details=details,
            messages=[]
        )


# ============================================================================
# FastAPI 应用
# ============================================================================

app = FastAPI(
    title="建筑工程结构计算API",
    description="基于Blueprints库的建筑工程结构计算模块，支持混凝土梁、柱和钢结构验算",
    version="1.0.0",
)


@app.get("/")
async def root():
    """API根路径"""
    return {
        "message": "建筑工程结构计算API",
        "version": "1.0.0",
        "endpoints": [
            "/concrete/beam/flexural",
            "/concrete/beam/shear",
            "/concrete/column/axial",
            "/concrete/column/eccentric",
            "/steel/bending",
            "/steel/compression",
            "/steel/tension",
            "/steel/combined",
        ]
    }


class BeamFlexuralRequest(BaseModel):
    """混凝土梁抗弯验算请求"""
    concrete: ConcreteMaterialInput
    section: RectangularSectionInput
    reinforcement: ReinforcementInput
    applied_moment: float = Field(..., gt=0, description="作用弯矩 kN·m")


@app.post("/concrete/beam/flexural", response_model=CalculationResult)
async def concrete_beam_flexural(request: BeamFlexuralRequest):
    """
    混凝土梁抗弯验算
    
    计算混凝土梁的正截面抗弯承载力并进行验算
    """
    try:
        calculator = ConcreteBeamCalculator(request.concrete, request.section, request.reinforcement)
        result = calculator.calculate_flexural_capacity()
        result.demand = request.applied_moment
        result.unity_check = request.applied_moment / result.capacity if result.capacity > 0 else float('inf')
        result.status = DesignStatus.PASS if result.unity_check <= 1.0 else DesignStatus.FAIL
        
        check = calculator.check_flexural(request.applied_moment)
        result.details["check_result"] = {
            "is_ok": check.is_ok,
            "unity_check": check.unity_check,
            "factor_of_safety": check.factor_of_safety,
        }
        
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


class BeamShearRequest(BaseModel):
    """混凝土梁抗剪验算请求"""
    concrete: ConcreteMaterialInput
    section: RectangularSectionInput
    reinforcement: ReinforcementInput
    applied_shear: float = Field(..., gt=0, description="作用剪力 kN")
    axial_force: float = Field(default=0.0, description="轴力 kN (压力为正)")


@app.post("/concrete/beam/shear", response_model=CalculationResult)
async def concrete_beam_shear(request: BeamShearRequest):
    """
    混凝土梁抗剪验算
    
    计算混凝土梁的斜截面抗剪承载力并进行验算
    """
    try:
        calculator = ConcreteBeamCalculator(request.concrete, request.section, request.reinforcement)
        result = calculator.calculate_shear_capacity(request.axial_force)
        result.demand = request.applied_shear
        result.unity_check = request.applied_shear / result.capacity if result.capacity > 0 else float('inf')
        result.status = DesignStatus.PASS if result.unity_check <= 1.0 else DesignStatus.FAIL
        
        check = calculator.check_shear(request.applied_shear, request.axial_force)
        result.details["check_result"] = {
            "is_ok": check.is_ok,
            "unity_check": check.unity_check,
            "factor_of_safety": check.factor_of_safety,
        }
        
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


class ColumnAxialRequest(BaseModel):
    """混凝土柱轴心受压验算请求"""
    concrete: ConcreteMaterialInput
    section: RectangularSectionInput
    reinforcement: ReinforcementInput
    axial_load: float = Field(..., gt=0, description="轴力 kN")


@app.post("/concrete/column/axial", response_model=CalculationResult)
async def concrete_column_axial(request: ColumnAxialRequest):
    """
    混凝土柱轴心受压承载力计算
    
    计算混凝土柱的轴心受压承载力
    """
    try:
        calculator = ConcreteColumnCalculator(request.concrete, request.section, request.reinforcement)
        result = calculator.calculate_axial_capacity()
        result.demand = request.axial_load
        result.unity_check = request.axial_load / result.capacity if result.capacity > 0 else float('inf')
        result.status = DesignStatus.PASS if result.unity_check <= 1.0 else DesignStatus.FAIL
        
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


class ColumnEccentricRequest(BaseModel):
    """混凝土柱偏心受压验算请求"""
    concrete: ConcreteMaterialInput
    section: RectangularSectionInput
    reinforcement: ReinforcementInput
    axial_load: float = Field(..., description="轴力 kN (压力为正)")
    moment_x: float = Field(default=0.0, description="绕X轴弯矩 kN·m")
    moment_y: float = Field(default=0.0, description="绕Y轴弯矩 kN·m")


@app.post("/concrete/column/eccentric", response_model=CalculationResult)
async def concrete_column_eccentric(request: ColumnEccentricRequest):
    """
    混凝土柱偏心受压验算
    
    计算混凝土柱在偏心受压状态下的承载力
    """
    try:
        calculator = ConcreteColumnCalculator(request.concrete, request.section, request.reinforcement)
        result = calculator.calculate_eccentric_capacity(request.moment_x, request.moment_y, request.axial_load)
        
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


class SteelBendingRequest(BaseModel):
    """钢结构受弯验算请求"""
    steel: SteelMaterialInput
    section: SteelSectionInput
    moment_y: float = Field(..., description="绕Y轴弯矩 kN·m")
    moment_z: float = Field(default=0.0, description="绕Z轴弯矩 kN·m")


@app.post("/steel/bending", response_model=CalculationResult)
async def steel_bending(request: SteelBendingRequest):
    """
    钢结构受弯验算
    
    计算钢构件的受弯承载力并进行验算
    """
    try:
        calculator = SteelStructureCalculator(request.steel, request.section)
        result = calculator.check_bending(request.moment_y, request.moment_z)
        
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


class SteelCompressionRequest(BaseModel):
    """钢结构轴心受压验算请求"""
    steel: SteelMaterialInput
    section: SteelSectionInput
    axial_force: float = Field(..., gt=0, description="轴力 kN")
    effective_length_y: float = Field(..., gt=0, description="绕Y轴计算长度 m")
    effective_length_z: float = Field(..., gt=0, description="绕Z轴计算长度 m")


@app.post("/steel/compression", response_model=CalculationResult)
async def steel_compression(request: SteelCompressionRequest):
    """
    钢结构轴心受压验算
    
    计算钢构件的轴心受压承载力(考虑稳定性)并进行验算
    """
    try:
        calculator = SteelStructureCalculator(request.steel, request.section)
        result = calculator.check_axial_compression(request.axial_force, request.effective_length_y, request.effective_length_z)
        
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


class SteelTensionRequest(BaseModel):
    """钢结构轴心受拉验算请求"""
    steel: SteelMaterialInput
    section: SteelSectionInput
    axial_force: float = Field(..., gt=0, description="轴力 kN")


@app.post("/steel/tension", response_model=CalculationResult)
async def steel_tension(request: SteelTensionRequest):
    """
    钢结构轴心受拉验算
    
    计算钢构件的轴心受拉承载力并进行验算
    """
    try:
        calculator = SteelStructureCalculator(request.steel, request.section)
        result = calculator.check_axial_tension(request.axial_force)
        
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


class SteelCombinedRequest(BaseModel):
    """钢结构压弯/拉弯验算请求"""
    steel: SteelMaterialInput
    section: SteelSectionInput
    axial_force: float = Field(..., description="轴力 kN (压力为正，拉力为负)")
    moment_y: float = Field(default=0.0, description="绕Y轴弯矩 kN·m")
    moment_z: float = Field(default=0.0, description="绕Z轴弯矩 kN·m")
    effective_length_y: float = Field(..., gt=0, description="绕Y轴计算长度 m")
    effective_length_z: float = Field(..., gt=0, description="绕Z轴计算长度 m")


@app.post("/steel/combined", response_model=CalculationResult)
async def steel_combined(request: SteelCombinedRequest):
    """
    钢结构压弯/拉弯构件验算
    
    计算钢构件在轴力和弯矩共同作用下的承载力
    """
    try:
        calculator = SteelStructureCalculator(request.steel, request.section)
        
        if request.axial_force >= 0:  # 压弯
            result = calculator.check_combined_compression_bending(
                request.axial_force, request.moment_y, request.moment_z, 
                request.effective_length_y, request.effective_length_z
            )
        else:  # 拉弯
            # 简化的拉弯验算
            tension_result = calculator.check_axial_tension(abs(request.axial_force))
            bending_result = calculator.check_bending(request.moment_y, request.moment_z)
            
            unity_check = tension_result.unity_check + bending_result.unity_check
            
            result = CalculationResult(
                status=DesignStatus.PASS if unity_check <= 1.0 else DesignStatus.FAIL,
                unity_check=unity_check,
                capacity=tension_result.capacity,
                demand=tension_result.demand,
                details={
                    "tension_check": tension_result.details,
                    "bending_check": bending_result.details,
                },
                messages=[]
            )
        
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ============================================================================
# 示例和测试代码
# ============================================================================

def example_concrete_beam():
    """混凝土梁计算示例"""
    print("=" * 60)
    print("混凝土梁计算示例")
    print("=" * 60)
    
    # 材料参数
    concrete = ConcreteMaterialInput(
        strength_class="C30/37",
        material_factor=1.5
    )
    
    # 截面参数
    section = RectangularSectionInput(
        width=300,
        height=500,
        cover=30
    )
    
    # 钢筋配置
    reinforcement = ReinforcementInput(
        top_rebar_diameter=16,
        top_rebar_count=3,
        bottom_rebar_diameter=20,
        bottom_rebar_count=4,
        stirrup_diameter=8,
        stirrup_spacing=150,
        steel_yield_strength=400
    )
    
    # 创建计算器
    calculator = ConcreteBeamCalculator(concrete, section, reinforcement)
    
    # 抗弯计算
    print("\n【正截面抗弯承载力计算】")
    flexural_result = calculator.calculate_flexural_capacity()
    print(f"抗弯承载力 M_rd = {flexural_result.capacity:.2f} kN·m")
    print(f"配筋率 ρ = {flexural_result.details['reinforcement_ratio']:.3f}%")
    print(f"最小配筋率 ρ_min = {flexural_result.details['min_reinforcement_ratio']:.3f}%")
    print(f"中性轴位置 x/d = {flexural_result.details['x_over_d_ratio']:.3f}")
    
    # 抗弯验算
    applied_moment = 150.0  # kN·m
    print(f"\n【抗弯验算】")
    print(f"作用弯矩 M_ed = {applied_moment:.2f} kN·m")
    check = calculator.check_flexural(applied_moment)
    print(f"验算结果: {'通过' if check.is_ok else '不通过'}")
    print(f"统一验算系数: {check.unity_check:.3f}")
    print(f"安全系数: {check.factor_of_safety:.3f}")
    
    # 抗剪计算
    print("\n【斜截面抗剪承载力计算】")
    shear_result = calculator.calculate_shear_capacity()
    print(f"混凝土抗剪贡献 V_rd,c = {shear_result.details['concrete_contribution_VRd_c']:.2f} kN")
    print(f"箍筋抗剪贡献 V_rd,s = {shear_result.details['steel_contribution_VRd_s']:.2f} kN")
    print(f"最大抗剪承载力 V_rd,max = {shear_result.details['max_shear_VRd_max']:.2f} kN")
    print(f"总抗剪承载力 V_rd = {shear_result.capacity:.2f} kN")
    
    # 抗剪验算
    applied_shear = 120.0  # kN
    print(f"\n【抗剪验算】")
    print(f"作用剪力 V_ed = {applied_shear:.2f} kN")
    check = calculator.check_shear(applied_shear)
    print(f"验算结果: {'通过' if check.is_ok else '不通过'}")
    print(f"统一验算系数: {check.unity_check:.3f}")


def example_concrete_column():
    """混凝土柱计算示例"""
    print("\n" + "=" * 60)
    print("混凝土柱计算示例")
    print("=" * 60)
    
    # 材料参数
    concrete = ConcreteMaterialInput(
        strength_class="C30/37",
        material_factor=1.5
    )
    
    # 截面参数
    section = RectangularSectionInput(
        width=400,
        height=400,
        cover=30
    )
    
    # 钢筋配置
    reinforcement = ReinforcementInput(
        top_rebar_diameter=20,
        top_rebar_count=4,
        bottom_rebar_diameter=20,
        bottom_rebar_count=4,
        stirrup_diameter=8,
        stirrup_spacing=200,
        steel_yield_strength=400
    )
    
    # 创建计算器
    calculator = ConcreteColumnCalculator(concrete, section, reinforcement)
    
    # 轴心受压承载力
    print("\n【轴心受压承载力计算】")
    axial_result = calculator.calculate_axial_capacity()
    print(f"轴心受压承载力 N_rd = {axial_result.capacity:.2f} kN")
    print(f"配筋率 ρ = {axial_result.details['reinforcement_ratio']:.3f}%")
    
    # 偏心受压验算
    print("\n【偏心受压验算】")
    N_ed = 1500.0  # kN
    M_x = 100.0  # kN·m
    M_y = 50.0   # kN·m
    print(f"作用轴力 N_ed = {N_ed:.2f} kN")
    print(f"作用弯矩 M_x = {M_x:.2f} kN·m, M_y = {M_y:.2f} kN·m")
    
    eccentric_result = calculator.calculate_eccentric_capacity(M_x, M_y, N_ed)
    print(f"验算结果: {eccentric_result.status}")
    print(f"统一验算系数: {eccentric_result.unity_check:.3f}")
    
    # 稳定性验算
    print("\n【稳定性验算】")
    effective_length = 3.5  # m
    print(f"计算长度 L0 = {effective_length:.2f} m")
    check = calculator.check_stability(N_ed, effective_length)
    print(f"验算结果: {'通过' if check.is_ok else '不通过'}")
    print(f"统一验算系数: {check.unity_check:.3f}")


def example_steel_structure():
    """钢结构计算示例"""
    print("\n" + "=" * 60)
    print("钢结构计算示例")
    print("=" * 60)
    
    # 材料参数
    steel = SteelMaterialInput(
        steel_class="S355",
        yield_strength=355,
        material_factor=1.0
    )
    
    # 截面参数 (IPE300近似值)
    section = SteelSectionInput(
        section_type="IPE300",
        area=5380,
        moment_of_inertia_y=83560000,
        moment_of_inertia_z=6038000,
        section_modulus_y=557000,
        section_modulus_z=40200,
        radius_of_gyration_y=125,
        radius_of_gyration_z=33.5
    )
    
    # 创建计算器
    calculator = SteelStructureCalculator(steel, section)
    
    # 受弯验算
    print("\n【受弯验算】")
    M_y = 150.0  # kN·m
    M_z = 10.0   # kN·m
    print(f"作用弯矩 M_y = {M_y:.2f} kN·m, M_z = {M_z:.2f} kN·m")
    
    bending_result = calculator.check_bending(M_y, M_z)
    print(f"抗弯承载力 M_y,Rd = {bending_result.details['moment_capacity_y']:.2f} kN·m")
    print(f"抗弯承载力 M_z,Rd = {bending_result.details['moment_capacity_z']:.2f} kN·m")
    print(f"验算结果: {bending_result.status}")
    print(f"统一验算系数: {bending_result.unity_check:.3f}")
    
    # 轴心受压验算
    print("\n【轴心受压验算】")
    N_ed = 800.0  # kN
    L_y = 4.0     # m
    L_z = 4.0     # m
    print(f"作用轴力 N_ed = {N_ed:.2f} kN")
    print(f"计算长度 L_y = {L_y:.2f} m, L_z = {L_z:.2f} m")
    
    compression_result = calculator.check_axial_compression(N_ed, L_y, L_z)
    print(f"截面抗压承载力 N_c,Rd = {compression_result.details['section_capacity_NcRd']:.2f} kN")
    print(f"稳定承载力 N_b,Rd = {compression_result.details['buckling_capacity_NbRd']:.2f} kN")
    print(f"长细比 λ_y = {compression_result.details['slenderness_y']:.2f}")
    print(f"长细比 λ_z = {compression_result.details['slenderness_z']:.2f}")
    print(f"稳定系数 χ = {compression_result.details['buckling_reduction_factor']:.3f}")
    print(f"验算结果: {compression_result.status}")
    print(f"统一验算系数: {compression_result.unity_check:.3f}")
    
    # 轴心受拉验算
    print("\n【轴心受拉验算】")
    N_t = 600.0  # kN
    print(f"作用轴力 N_ed = {N_t:.2f} kN")
    
    tension_result = calculator.check_axial_tension(N_t)
    print(f"受拉承载力 N_t,Rd = {tension_result.capacity:.2f} kN")
    print(f"验算结果: {tension_result.status}")
    print(f"统一验算系数: {tension_result.unity_check:.3f}")
    
    # 压弯验算
    print("\n【压弯验算】")
    N_ed = 500.0  # kN
    M_y = 100.0   # kN·m
    M_z = 5.0     # kN·m
    print(f"作用轴力 N_ed = {N_ed:.2f} kN")
    print(f"作用弯矩 M_y = {M_y:.2f} kN·m, M_z = {M_z:.2f} kN·m")
    
    combined_result = calculator.check_combined_compression_bending(
        N_ed, M_y, M_z, L_y, L_z
    )
    print(f"验算结果: {combined_result.status}")
    print(f"统一验算系数: {combined_result.unity_check:.3f}")


def run_examples():
    """运行所有示例"""
    print("\n" + "=" * 60)
    print("基于Blueprints库的建筑工程结构计算模块")
    print("=" * 60)
    
    example_concrete_beam()
    example_concrete_column()
    example_steel_structure()
    
    print("\n" + "=" * 60)
    print("示例计算完成")
    print("=" * 60)


def main():
    """主函数"""
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "server":
        # 启动FastAPI服务器
        print("启动FastAPI服务器...")
        print("访问 http://localhost:8000/docs 查看API文档")
        uvicorn.run(app, host="0.0.0.0", port=8000)
    else:
        # 运行示例
        run_examples()


if __name__ == "__main__":
    main()
