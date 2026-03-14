"""
建筑工程结构计算模块
===================
基于Blueprints库开发的建筑工程结构计算模块
包含：混凝土梁、柱、钢结构验算

作者：AI Assistant
日期：2026-03-14
"""

from __future__ import annotations

import sys
import os

# 添加本地site_packages到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'site_packages'))

import math
from dataclasses import dataclass, field
from enum import Enum
from typing import Literal, Optional, Union

from pydantic import BaseModel, Field, field_validator, model_validator
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# 导入Blueprints库组件
from blueprints.materials.concrete import ConcreteMaterial, ConcreteStrengthClass
from blueprints.materials.steel import SteelMaterial, SteelStrengthClass
from blueprints.materials.reinforcement_steel import ReinforcementSteelMaterial, ReinforcementSteelQuality
from blueprints.structural_sections.steel.standard_profiles import HEA, HEB, IPE, RHS, SHS
from blueprints.structural_sections.steel.steel_cross_section import SteelCrossSection, FabricationMethod
from blueprints.checks.check_result import CheckResult


# =============================================================================
# 枚举类型定义
# =============================================================================

class LoadType(str, Enum):
    """荷载类型枚举"""
    DEAD = "dead"           # 恒载
    LIVE = "live"           # 活载
    WIND = "wind"           # 风载
    SNOW = "snow"           # 雪载
    SEISMIC = "seismic"     # 地震荷载


class BeamSupportType(str, Enum):
    """梁支撑类型枚举"""
    SIMPLY_SUPPORTED = "simply_supported"   # 简支
    CONTINUOUS = "continuous"               # 连续
    CANTILEVER = "cantilever"               # 悬臂
    FIXED_BOTH = "fixed_both"               # 两端固定


class ColumnSupportType(str, Enum):
    """柱支撑类型枚举"""
    PINNED_TOP_BOTTOM = "pinned_top_bottom"     # 两端铰接
    FIXED_TOP_BOTTOM = "fixed_top_bottom"       # 两端固定
    FIXED_PINNED = "fixed_pinned"               # 下端固定上端铰接
    FIXED_FREE = "fixed_free"                   # 悬臂柱


class SteelProfileType(str, Enum):
    """型钢类型枚举"""
    HEA = "HEA"
    HEB = "HEB"
    IPE = "IPE"
    RHS = "RHS"
    SHS = "SHS"


# =============================================================================
# Pydantic 输入模型
# =============================================================================

class ConcreteMaterialInput(BaseModel):
    """混凝土材料输入模型"""
    strength_class: str = Field(default="C30/37", description="混凝土强度等级，如C30/37")
    density: float = Field(default=2500.0, description="密度 (kg/m³)")
    material_factor: float = Field(default=1.5, description="材料分项系数")

    @field_validator("strength_class")
    @classmethod
    def validate_strength_class(cls, v: str) -> str:
        valid_classes = ["C12/15", "C16/20", "C20/25", "C25/30", "C30/37", 
                        "C35/45", "C40/50", "C45/55", "C50/60", "C55/67", 
                        "C60/75", "C70/85", "C80/95", "C90/105"]
        if v not in valid_classes:
            raise ValueError(f"无效的混凝土强度等级，可选: {valid_classes}")
        return v


class SteelMaterialInput(BaseModel):
    """钢材材料输入模型"""
    steel_class: str = Field(default="S355", description="钢材等级，如S235, S355, S450")
    density: float = Field(default=7850.0, description="密度 (kg/m³)")

    @field_validator("steel_class")
    @classmethod
    def validate_steel_class(cls, v: str) -> str:
        valid_classes = ["S235", "S275", "S355", "S450"]
        if v not in valid_classes:
            raise ValueError(f"无效的钢材等级，可选: {valid_classes}")
        return v


class ReinforcementInput(BaseModel):
    """钢筋配置输入模型"""
    diameter: float = Field(..., gt=0, description="钢筋直径 (mm)")
    count: int = Field(..., gt=0, description="钢筋根数")
    grade: str = Field(default="B500B", description="钢筋等级")
    cover: float = Field(default=25.0, gt=0, description="保护层厚度 (mm)")


class ConcreteBeamInput(BaseModel):
    """混凝土梁计算输入模型"""
    # 几何参数
    width: float = Field(..., gt=0, description="梁宽 b (mm)")
    height: float = Field(..., gt=0, description="梁高 h (mm)")
    span: float = Field(..., gt=0, description="跨度 L (m)")
    support_type: BeamSupportType = Field(default=BeamSupportType.SIMPLY_SUPPORTED, description="支撑类型")
    
    # 材料参数
    concrete: ConcreteMaterialInput = Field(default_factory=ConcreteMaterialInput, description="混凝土材料")
    reinforcement: ReinforcementInput = Field(..., description="受拉钢筋配置")
    compression_reinforcement: Optional[ReinforcementInput] = Field(default=None, description="受压钢筋配置")
    
    # 荷载参数
    dead_load: float = Field(..., ge=0, description="恒载 (kN/m)")
    live_load: float = Field(..., ge=0, description="活载 (kN/m)")
    
    # 设计参数
    safety_factor_dead: float = Field(default=1.35, gt=0, description="恒载分项系数")
    safety_factor_live: float = Field(default=1.5, gt=0, description="活载分项系数")
    allowable_deflection_ratio: float = Field(default=250.0, gt=0, description="允许挠度比 L/xxx")

    @model_validator(mode="after")
    def validate_dimensions(self):
        if self.width >= self.height:
            raise ValueError("梁高应大于梁宽")
        return self


class ConcreteColumnInput(BaseModel):
    """混凝土柱计算输入模型"""
    # 几何参数
    width: float = Field(..., gt=0, description="柱宽 b (mm)")
    depth: float = Field(..., gt=0, description="柱深 h (mm)")
    height: float = Field(..., gt=0, description="柱高 H (m)")
    support_type: ColumnSupportType = Field(default=ColumnSupportType.FIXED_TOP_BOTTOM, description="支撑类型")
    
    # 材料参数
    concrete: ConcreteMaterialInput = Field(default_factory=ConcreteMaterialInput, description="混凝土材料")
    longitudinal_reinforcement: ReinforcementInput = Field(..., description="纵向钢筋配置")
    stirrup_diameter: float = Field(default=8.0, gt=0, description="箍筋直径 (mm)")
    stirrup_spacing: float = Field(default=150.0, gt=0, description="箍筋间距 (mm)")
    
    # 荷载参数
    axial_load: float = Field(..., description="轴力设计值 N (kN)，压力为正")
    moment_x: float = Field(default=0.0, description="绕X轴弯矩设计值 Mx (kN·m)")
    moment_y: float = Field(default=0.0, description="绕Y轴弯矩设计值 My (kN·m)")


class SteelMemberInput(BaseModel):
    """钢结构构件计算输入模型"""
    # 截面参数
    profile_type: SteelProfileType = Field(..., description="型钢类型")
    profile_name: str = Field(..., description="型钢型号，如HEA200, IPE300")
    
    # 材料参数
    steel: SteelMaterialInput = Field(default_factory=SteelMaterialInput, description="钢材材料")
    fabrication_method: Optional[FabricationMethod] = Field(default=None, description="制造方法")
    
    # 几何参数
    length: float = Field(..., gt=0, description="构件长度 L (m)")
    effective_length_factor: float = Field(default=1.0, gt=0, description="计算长度系数")
    
    # 荷载参数
    axial_force: float = Field(default=0.0, description="轴力设计值 N (kN)，拉力为正")
    moment_y: float = Field(default=0.0, description="绕强轴弯矩设计值 My (kN·m)")
    moment_z: float = Field(default=0.0, description="绕弱轴弯矩设计值 Mz (kN·m)")
    shear_y: float = Field(default=0.0, description="Y向剪力设计值 Vy (kN)")
    shear_z: float = Field(default=0.0, description="Z向剪力设计值 Vz (kN)")


# =============================================================================
# Pydantic 输出模型
# =============================================================================

class CheckResultOutput(BaseModel):
    """验算结果输出模型"""
    check_name: str = Field(..., description="验算项目名称")
    provided: float = Field(..., description="实际值")
    required: float = Field(..., description="允许值")
    unity_check: float = Field(..., description="利用率")
    factor_of_safety: float = Field(..., description="安全系数")
    is_ok: bool = Field(..., description="是否通过")
    unit: str = Field(..., description="单位")
    message: str = Field(default="", description="结果说明")


class ConcreteBeamOutput(BaseModel):
    """混凝土梁计算输出模型"""
    # 基本信息
    beam_description: str = Field(..., description="梁描述")
    
    # 内力计算结果
    design_moment: float = Field(..., description="设计弯矩 M (kN·m)")
    design_shear: float = Field(..., description="设计剪力 V (kN)")
    
    # 抗弯验算
    flexural_check: CheckResultOutput = Field(..., description="抗弯验算结果")
    
    # 抗剪验算
    shear_check: CheckResultOutput = Field(..., description="抗剪验算结果")
    
    # 挠度验算
    deflection_check: CheckResultOutput = Field(..., description="挠度验算结果")
    max_deflection: float = Field(..., description="最大挠度 (mm)")
    allowable_deflection: float = Field(..., description="允许挠度 (mm)")
    
    # 配筋信息
    reinforcement_ratio: float = Field(..., description="配筋率 (%)")
    min_reinforcement_ratio: float = Field(..., description="最小配筋率 (%)")
    
    # 总体结果
    overall_status: bool = Field(..., description="总体验算结果")


class ConcreteColumnOutput(BaseModel):
    """混凝土柱计算输出模型"""
    # 基本信息
    column_description: str = Field(..., description="柱描述")
    
    # 承载力计算
    axial_capacity: float = Field(..., description="轴心受压承载力 Nc (kN)")
    moment_capacity_x: float = Field(..., description="X轴抗弯承载力 Mx (kN·m)")
    moment_capacity_y: float = Field(..., description="Y轴抗弯承载力 My (kN·m)")
    
    # 验算结果
    axial_check: CheckResultOutput = Field(..., description="轴心受压验算")
    biaxial_moment_check: CheckResultOutput = Field(..., description="双向偏心验算")
    slenderness_check: CheckResultOutput = Field(..., description="长细比验算")
    
    # 稳定系数
    stability_coefficient: float = Field(..., description="稳定系数 φ")
    slenderness_ratio: float = Field(..., description="长细比 λ")
    
    # 总体结果
    overall_status: bool = Field(..., description="总体验算结果")


class SteelMemberOutput(BaseModel):
    """钢结构构件计算输出模型"""
    # 基本信息
    member_description: str = Field(..., description="构件描述")
    profile_properties: dict = Field(..., description="截面特性")
    
    # 强度验算
    tension_check: Optional[CheckResultOutput] = Field(default=None, description="抗拉强度验算")
    compression_check: Optional[CheckResultOutput] = Field(default=None, description="抗压强度验算")
    bending_y_check: CheckResultOutput = Field(..., description="强轴抗弯验算")
    bending_z_check: CheckResultOutput = Field(..., description="弱轴抗弯验算")
    shear_y_check: CheckResultOutput = Field(..., description="Y向抗剪验算")
    shear_z_check: CheckResultOutput = Field(..., description="Z向抗剪验算")
    
    # 稳定验算
    buckling_y_check: CheckResultOutput = Field(..., description="强轴屈曲验算")
    buckling_z_check: CheckResultOutput = Field(..., description="弱轴屈曲验算")
    lateral_torsional_buckling_check: CheckResultOutput = Field(..., description="弯扭屈曲验算")
    
    # 组合验算
    combined_axial_bending_check: CheckResultOutput = Field(..., description="轴力-弯矩组合验算")
    
    # 总体结果
    overall_status: bool = Field(..., description="总体验算结果")


# =============================================================================
# 核心计算类
# =============================================================================

@dataclass
class ConcreteBeamCalculator:
    """混凝土梁计算器"""
    
    def calculate(self, input_data: ConcreteBeamInput) -> ConcreteBeamOutput:
        """执行混凝土梁验算"""
        
        # 创建混凝土材料对象
        concrete_class = getattr(ConcreteStrengthClass, input_data.concrete.strength_class.replace("/", "_"))
        concrete = ConcreteMaterial(
            concrete_class=concrete_class,
            density=input_data.concrete.density,
            material_factor=input_data.concrete.material_factor
        )
        
        # 计算截面特性
        b = input_data.width  # mm
        h = input_data.height  # mm
        L = input_data.span  # m
        
        # 有效高度
        d = h - input_data.reinforcement.cover - input_data.reinforcement.diameter / 2
        
        # 钢筋面积
        As = math.pi * (input_data.reinforcement.diameter / 2) ** 2 * input_data.reinforcement.count
        
        # 计算设计荷载
        q_dead = input_data.dead_load  # kN/m
        q_live = input_data.live_load  # kN/m
        q_design = input_data.safety_factor_dead * q_dead + input_data.safety_factor_live * q_live
        
        # 计算内力
        if input_data.support_type == BeamSupportType.SIMPLY_SUPPORTED:
            M_design = q_design * L ** 2 / 8  # kN·m
            V_design = q_design * L / 2  # kN
            deflection_coeff = 5 / 384
        elif input_data.support_type == BeamSupportType.CANTILEVER:
            M_design = q_design * L ** 2 / 2
            V_design = q_design * L
            deflection_coeff = 1 / 8
        elif input_data.support_type == BeamSupportType.FIXED_BOTH:
            M_design = q_design * L ** 2 / 12
            V_design = q_design * L / 2
            deflection_coeff = 1 / 384
        else:
            M_design = q_design * L ** 2 / 8
            V_design = q_design * L / 2
            deflection_coeff = 5 / 384
        
        # 材料强度
        fcd = concrete.f_cd  # MPa
        fyd = 435  # MPa (假设使用B500B钢筋)
        
        # 抗弯验算 (简化矩形应力块法)
        # x = (As * fyd) / (0.8 * b * fcd)
        # Mu = As * fyd * (d - 0.4 * x) / 1e6  # kN·m
        
        # 简化计算
        rho = As / (b * d)  # 配筋率
        rho_bal = 0.8 * fcd / fyd * 0.5  # 平衡配筋率近似
        
        if rho <= rho_bal:
            # 适筋梁
            xi = (rho * fyd) / (0.8 * fcd)
            Mu = As * fyd * (d - 0.4 * xi * d) / 1e6
        else:
            # 超筋梁，按混凝土压碎控制
            Mu = 0.8 * fcd * b * 0.5 * d * (d - 0.4 * 0.5 * d) / 1e6
        
        flexural_check = CheckResult.from_comparison(
            provided=M_design,
            required=Mu,
            operator="<="
        )
        
        # 抗剪验算
        # 混凝土抗剪贡献
        k = min(1 + math.sqrt(200 / d), 2.0)
        rho_l = min(As / (b * d), 0.02)
        VRd_c = 0.12 * k * (100 * rho_l * concrete.f_ck) ** (1/3) * b * d / 1000  # kN
        
        shear_check = CheckResult.from_comparison(
            provided=V_design,
            required=VRd_c,
            operator="<="
        )
        
        # 挠度验算
        Ecm = concrete.e_cm  # MPa
        I = b * h ** 3 / 12  # mm^4
        EI = Ecm * I  # N·mm²
        
        # 使用特征荷载组合计算挠度
        q_char = q_dead + q_live
        delta_max = deflection_coeff * q_char * (L * 1000) ** 4 / EI  # mm
        delta_allow = L * 1000 / input_data.allowable_deflection_ratio
        
        deflection_check = CheckResult.from_comparison(
            provided=delta_max,
            required=delta_allow,
            operator="<="
        )
        
        # 最小配筋率
        rho_min = 0.26 * concrete.f_ctm / fyd * 100  # %
        rho_actual = As / (b * h) * 100
        
        # 构建输出
        beam_desc = f"混凝土梁 {b}×{h}mm, 跨度{L}m, {input_data.concrete.strength_class}"
        
        return ConcreteBeamOutput(
            beam_description=beam_desc,
            design_moment=round(M_design, 2),
            design_shear=round(V_design, 2),
            flexural_check=CheckResultOutput(
                check_name="抗弯承载力验算",
                provided=round(M_design, 2),
                required=round(Mu, 2),
                unity_check=round(flexural_check.unity_check, 3),
                factor_of_safety=round(flexural_check.factor_of_safety, 3),
                is_ok=flexural_check.is_ok if flexural_check.is_ok is not None else False,
                unit="kN·m",
                message="满足" if flexural_check.is_ok else "不满足"
            ),
            shear_check=CheckResultOutput(
                check_name="抗剪承载力验算",
                provided=round(V_design, 2),
                required=round(VRd_c, 2),
                unity_check=round(shear_check.unity_check, 3),
                factor_of_safety=round(shear_check.factor_of_safety, 3),
                is_ok=shear_check.is_ok if shear_check.is_ok is not None else False,
                unit="kN",
                message="满足" if shear_check.is_ok else "不满足"
            ),
            deflection_check=CheckResultOutput(
                check_name="挠度验算",
                provided=round(delta_max, 2),
                required=round(delta_allow, 2),
                unity_check=round(deflection_check.unity_check, 3),
                factor_of_safety=round(deflection_check.factor_of_safety, 3),
                is_ok=deflection_check.is_ok if deflection_check.is_ok is not None else False,
                unit="mm",
                message="满足" if deflection_check.is_ok else "不满足"
            ),
            max_deflection=round(delta_max, 2),
            allowable_deflection=round(delta_allow, 2),
            reinforcement_ratio=round(rho_actual, 3),
            min_reinforcement_ratio=round(rho_min, 3),
            overall_status=(flexural_check.is_ok and shear_check.is_ok and deflection_check.is_ok)
        )


@dataclass
class ConcreteColumnCalculator:
    """混凝土柱计算器"""
    
    def calculate(self, input_data: ConcreteColumnInput) -> ConcreteColumnOutput:
        """执行混凝土柱验算"""
        
        # 创建混凝土材料对象
        concrete_class = getattr(ConcreteStrengthClass, input_data.concrete.strength_class.replace("/", "_"))
        concrete = ConcreteMaterial(
            concrete_class=concrete_class,
            density=input_data.concrete.density,
            material_factor=input_data.concrete.material_factor
        )
        
        # 几何参数
        b = input_data.width  # mm
        h = input_data.depth  # mm
        H = input_data.height  # m
        
        # 计算长度
        effective_length_factors = {
            ColumnSupportType.PINNED_TOP_BOTTOM: 1.0,
            ColumnSupportType.FIXED_TOP_BOTTOM: 0.5,
            ColumnSupportType.FIXED_PINNED: 0.7,
            ColumnSupportType.FIXED_FREE: 2.0
        }
        l0 = effective_length_factors.get(input_data.support_type, 1.0) * H
        
        # 钢筋面积
        As = (math.pi * (input_data.longitudinal_reinforcement.diameter / 2) ** 2 * 
              input_data.longitudinal_reinforcement.count)
        
        # 材料强度
        fcd = concrete.f_cd  # MPa
        fyd = 435  # MPa
        
        # 轴心受压承载力
        Ac = b * h - As  # 混凝土面积
        Nc = 0.8 * (fcd * Ac + fyd * As) / 1000  # kN
        
        axial_check = CheckResult.from_comparison(
            provided=abs(input_data.axial_load),
            required=Nc,
            operator="<="
        )
        
        # 长细比计算
        i_min = min(b, h) / math.sqrt(12)  # 最小回转半径 mm
        lambda_slender = l0 * 1000 / i_min
        lambda_limit = 25  # 简化限制值
        
        slenderness_check = CheckResult.from_comparison(
            provided=lambda_slender,
            required=lambda_limit,
            operator="<="
        )
        
        # 稳定系数 (简化计算)
        if lambda_slender <= lambda_limit:
            phi = 1.0
        else:
            phi = max(0.5, 1 - (lambda_slender - lambda_limit) / 100)
        
        # 抗弯承载力 (简化计算)
        d = h - input_data.longitudinal_reinforcement.cover - input_data.longitudinal_reinforcement.diameter / 2
        Mux = As * fyd * (d - h / 2) / 2 / 1e6  # kN·m
        Muy = Mux * b / h if h > b else Mux
        
        # 双向偏心验算 (简化方法)
        if input_data.moment_x == 0 and input_data.moment_y == 0:
            biaxial_unity = 0
        else:
            ratio_x = abs(input_data.moment_x) / Mux if Mux > 0 else 0
            ratio_y = abs(input_data.moment_y) / Muy if Muy > 0 else 0
            biaxial_unity = ratio_x + ratio_y
        
        biaxial_check = CheckResult.from_unity_check(unity_check=biaxial_unity)
        
        # 构建输出
        column_desc = f"混凝土柱 {b}×{h}mm, 高{H}m, {input_data.concrete.strength_class}"
        
        return ConcreteColumnOutput(
            column_description=column_desc,
            axial_capacity=round(Nc, 2),
            moment_capacity_x=round(Mux, 2),
            moment_capacity_y=round(Muy, 2),
            axial_check=CheckResultOutput(
                check_name="轴心受压验算",
                provided=round(abs(input_data.axial_load), 2),
                required=round(Nc, 2),
                unity_check=round(axial_check.unity_check, 3),
                factor_of_safety=round(axial_check.factor_of_safety, 3),
                is_ok=axial_check.is_ok if axial_check.is_ok is not None else False,
                unit="kN",
                message="满足" if axial_check.is_ok else "不满足"
            ),
            biaxial_moment_check=CheckResultOutput(
                check_name="双向偏心验算",
                provided=round(biaxial_unity, 3),
                required=1.0,
                unity_check=round(biaxial_check.unity_check, 3),
                factor_of_safety=round(biaxial_check.factor_of_safety, 3),
                is_ok=biaxial_check.is_ok if biaxial_check.is_ok is not None else False,
                unit="-",
                message="满足" if biaxial_check.is_ok else "不满足"
            ),
            slenderness_check=CheckResultOutput(
                check_name="长细比验算",
                provided=round(lambda_slender, 2),
                required=lambda_limit,
                unity_check=round(slenderness_check.unity_check, 3),
                factor_of_safety=round(slenderness_check.factor_of_safety, 3),
                is_ok=slenderness_check.is_ok if slenderness_check.is_ok is not None else False,
                unit="-",
                message="满足" if slenderness_check.is_ok else "不满足"
            ),
            stability_coefficient=round(phi, 3),
            slenderness_ratio=round(lambda_slender, 2),
            overall_status=(axial_check.is_ok and biaxial_check.is_ok and slenderness_check.is_ok)
        )


@dataclass
class SteelMemberCalculator:
    """钢结构构件计算器"""
    
    def _get_profile(self, profile_type: SteelProfileType, profile_name: str):
        """获取型钢截面"""
        profile_classes = {
            SteelProfileType.HEA: HEA,
            SteelProfileType.HEB: HEB,
            SteelProfileType.IPE: IPE,
            SteelProfileType.RHS: RHS,
            SteelProfileType.SHS: SHS
        }
        
        profile_class = profile_classes.get(profile_type)
        if not profile_class:
            raise ValueError(f"不支持的型钢类型: {profile_type}")
        
        try:
            return getattr(profile_class, profile_name.replace("-", "_").replace(".", "_"))
        except AttributeError:
            raise ValueError(f"未找到型钢型号: {profile_name}")
    
    def calculate(self, input_data: SteelMemberInput) -> SteelMemberOutput:
        """执行钢结构构件验算"""
        
        # 获取型钢截面
        profile = self._get_profile(input_data.profile_type, input_data.profile_name)
        
        # 创建钢材材料
        steel_class = getattr(SteelStrengthClass, input_data.steel.steel_class)
        steel = SteelMaterial(steel_class=steel_class, density=input_data.steel.density)
        
        # 创建钢截面对象
        cross_section = SteelCrossSection(
            profile=profile,
            material=steel,
            fabrication_method=input_data.fabrication_method
        )
        
        # 截面特性
        A = profile.area  # mm²
        
        # 通过section_properties方法获取截面特性
        section_props = profile.section_properties(geometric=True, plastic=True, warping=False)
        Iy = section_props.i_xx if hasattr(section_props, 'i_xx') else 1e6  # mm⁴
        Iz = section_props.i_yy if hasattr(section_props, 'i_yy') else 1e6  # mm⁴
        
        # 计算截面模量 (近似值)
        h = getattr(profile, 'total_height', profile.profile_height)
        b = getattr(profile, 'top_flange_width', getattr(profile, 'total_width', profile.profile_width))
        Wy = Iy / (h / 2) if h > 0 else 1e4  # mm³
        Wz = Iz / (b / 2) if b > 0 else 1e4  # mm³
        
        # 材料强度
        fy = cross_section.yield_strength  # MPa
        fu = cross_section.ultimate_strength  # MPa
        E = steel.e_modulus  # MPa
        
        # 计算长度
        L = input_data.length  # m
        Leff = input_data.effective_length_factor * L  # m
        
        # 强度验算
        # 抗拉/抗压强度
        Npl = A * fy / 1000  # kN
        
        tension_check = None
        compression_check = None
        
        if input_data.axial_force > 0:  # 拉力
            tension_check = CheckResultOutput(
                check_name="抗拉强度验算",
                provided=round(input_data.axial_force, 2),
                required=round(Npl, 2),
                unity_check=round(input_data.axial_force / Npl, 3),
                factor_of_safety=round(Npl / input_data.axial_force, 3) if input_data.axial_force > 0 else float('inf'),
                is_ok=input_data.axial_force <= Npl,
                unit="kN",
                message="满足" if input_data.axial_force <= Npl else "不满足"
            )
        elif input_data.axial_force < 0:  # 压力
            compression_check = CheckResultOutput(
                check_name="抗压强度验算",
                provided=round(abs(input_data.axial_force), 2),
                required=round(Npl, 2),
                unity_check=round(abs(input_data.axial_force) / Npl, 3),
                factor_of_safety=round(Npl / abs(input_data.axial_force), 3) if input_data.axial_force != 0 else float('inf'),
                is_ok=abs(input_data.axial_force) <= Npl,
                unit="kN",
                message="满足" if abs(input_data.axial_force) <= Npl else "不满足"
            )
        
        # 抗弯强度验算
        Mply = Wy * fy / 1e6  # kN·m
        Mplz = Wz * fy / 1e6  # kN·m
        
        bending_y_check = CheckResultOutput(
            check_name="强轴抗弯验算",
            provided=round(abs(input_data.moment_y), 2),
            required=round(Mply, 2),
            unity_check=round(abs(input_data.moment_y) / Mply, 3) if Mply > 0 else 0,
            factor_of_safety=round(Mply / abs(input_data.moment_y), 3) if input_data.moment_y != 0 else float('inf'),
            is_ok=abs(input_data.moment_y) <= Mply,
            unit="kN·m",
            message="满足" if abs(input_data.moment_y) <= Mply else "不满足"
        )
        
        bending_z_check = CheckResultOutput(
            check_name="弱轴抗弯验算",
            provided=round(abs(input_data.moment_z), 2),
            required=round(Mplz, 2),
            unity_check=round(abs(input_data.moment_z) / Mplz, 3) if Mplz > 0 else 0,
            factor_of_safety=round(Mplz / abs(input_data.moment_z), 3) if input_data.moment_z != 0 else float('inf'),
            is_ok=abs(input_data.moment_z) <= Mplz,
            unit="kN·m",
            message="满足" if abs(input_data.moment_z) <= Mplz else "不满足"
        )
        
        # 抗剪强度验算
        Avy = A * 0.6  # 简化假设
        Avz = A * 0.6
        Vply = Avy * fy / math.sqrt(3) / 1000  # kN
        Vplz = Avz * fy / math.sqrt(3) / 1000
        
        shear_y_check = CheckResultOutput(
            check_name="Y向抗剪验算",
            provided=round(abs(input_data.shear_y), 2),
            required=round(Vply, 2),
            unity_check=round(abs(input_data.shear_y) / Vply, 3) if Vply > 0 else 0,
            factor_of_safety=round(Vply / abs(input_data.shear_y), 3) if input_data.shear_y != 0 else float('inf'),
            is_ok=abs(input_data.shear_y) <= Vply,
            unit="kN",
            message="满足" if abs(input_data.shear_y) <= Vply else "不满足"
        )
        
        shear_z_check = CheckResultOutput(
            check_name="Z向抗剪验算",
            provided=round(abs(input_data.shear_z), 2),
            required=round(Vplz, 2),
            unity_check=round(abs(input_data.shear_z) / Vplz, 3) if Vplz > 0 else 0,
            factor_of_safety=round(Vplz / abs(input_data.shear_z), 3) if input_data.shear_z != 0 else float('inf'),
            is_ok=abs(input_data.shear_z) <= Vplz,
            unit="kN",
            message="满足" if abs(input_data.shear_z) <= Vplz else "不满足"
        )
        
        # 屈曲验算
        # 强轴屈曲
        lambda_y = Leff * 1000 / math.sqrt(Iy / A)
        lambda_1 = 93.9 * math.sqrt(235 / fy)
        lambda_bar_y = lambda_y / lambda_1
        
        # 屈曲曲线b的折减系数
        phi_y = 0.5 * (1 + 0.34 * (lambda_bar_y - 0.2) + lambda_bar_y ** 2)
        chi_y = min(1.0, 1 / (phi_y + math.sqrt(phi_y ** 2 - lambda_bar_y ** 2)))
        
        Nb_y = chi_y * Npl
        
        buckling_y_check = CheckResultOutput(
            check_name="强轴屈曲验算",
            provided=round(abs(input_data.axial_force), 2) if input_data.axial_force != 0 else 0,
            required=round(Nb_y, 2),
            unity_check=round(abs(input_data.axial_force) / Nb_y, 3) if Nb_y > 0 else 0,
            factor_of_safety=round(Nb_y / abs(input_data.axial_force), 3) if input_data.axial_force != 0 else float('inf'),
            is_ok=abs(input_data.axial_force) <= Nb_y,
            unit="kN",
            message="满足" if abs(input_data.axial_force) <= Nb_y else "不满足"
        )
        
        # 弱轴屈曲
        lambda_z = Leff * 1000 / math.sqrt(Iz / A)
        lambda_bar_z = lambda_z / lambda_1
        
        phi_z = 0.5 * (1 + 0.49 * (lambda_bar_z - 0.2) + lambda_bar_z ** 2)
        chi_z = min(1.0, 1 / (phi_z + math.sqrt(phi_z ** 2 - lambda_bar_z ** 2)))
        
        Nb_z = chi_z * Npl
        
        buckling_z_check = CheckResultOutput(
            check_name="弱轴屈曲验算",
            provided=round(abs(input_data.axial_force), 2) if input_data.axial_force != 0 else 0,
            required=round(Nb_z, 2),
            unity_check=round(abs(input_data.axial_force) / Nb_z, 3) if Nb_z > 0 else 0,
            factor_of_safety=round(Nb_z / abs(input_data.axial_force), 3) if input_data.axial_force != 0 else float('inf'),
            is_ok=abs(input_data.axial_force) <= Nb_z,
            unit="kN",
            message="满足" if abs(input_data.axial_force) <= Nb_z else "不满足"
        )
        
        # 弯扭屈曲验算 (简化)
        lambda_lt = lambda_bar_y  # 简化假设
        phi_lt = 0.5 * (1 + 0.21 * (lambda_lt - 0.2) + lambda_lt ** 2)
        chi_lt = min(1.0, 1 / (phi_lt + math.sqrt(phi_lt ** 2 - lambda_lt ** 2)))
        
        Mb = chi_lt * Mply
        
        lateral_torsional_buckling_check = CheckResultOutput(
            check_name="弯扭屈曲验算",
            provided=round(abs(input_data.moment_y), 2),
            required=round(Mb, 2),
            unity_check=round(abs(input_data.moment_y) / Mb, 3) if Mb > 0 else 0,
            factor_of_safety=round(Mb / abs(input_data.moment_y), 3) if input_data.moment_y != 0 else float('inf'),
            is_ok=abs(input_data.moment_y) <= Mb,
            unit="kN·m",
            message="满足" if abs(input_data.moment_y) <= Mb else "不满足"
        )
        
        # 轴力-弯矩组合验算 (Eurocode 3 6.2.1)
        n = abs(input_data.axial_force) / Npl if Npl > 0 else 0
        my = abs(input_data.moment_y) / Mply if Mply > 0 else 0
        mz = abs(input_data.moment_z) / Mplz if Mplz > 0 else 0
        
        combined_unity = n + my + mz
        
        combined_check = CheckResultOutput(
            check_name="轴力-弯矩组合验算",
            provided=round(combined_unity, 3),
            required=1.0,
            unity_check=round(combined_unity, 3),
            factor_of_safety=round(1 / combined_unity, 3) if combined_unity > 0 else float('inf'),
            is_ok=combined_unity <= 1.0,
            unit="-",
            message="满足" if combined_unity <= 1.0 else "不满足"
        )
        
        # 截面特性字典
        profile_props = {
            "area_mm2": A,
            "height_mm": getattr(profile, 'total_height', 0),
            "width_mm": getattr(profile, 'top_flange_width', 0),
            "web_thickness_mm": getattr(profile, 'web_thickness', 0),
            "flange_thickness_mm": getattr(profile, 'top_flange_thickness', 0),
            "weight_kg_m": round(cross_section.weight_per_meter, 2)
        }
        
        # 构建输出
        member_desc = f"{input_data.profile_type.value} {input_data.profile_name}, {input_data.steel.steel_class}, L={L}m"
        
        # 总体验算结果
        all_checks = [
            bending_y_check.is_ok,
            bending_z_check.is_ok,
            shear_y_check.is_ok,
            shear_z_check.is_ok,
            buckling_y_check.is_ok,
            buckling_z_check.is_ok,
            lateral_torsional_buckling_check.is_ok,
            combined_check.is_ok
        ]
        
        # 如果有拉压验算也加入
        if tension_check:
            all_checks.append(tension_check.is_ok)
        if compression_check:
            all_checks.append(compression_check.is_ok)
        
        overall_status = all(all_checks)
        
        return SteelMemberOutput(
            member_description=member_desc,
            profile_properties=profile_props,
            tension_check=tension_check,
            compression_check=compression_check,
            bending_y_check=bending_y_check,
            bending_z_check=bending_z_check,
            shear_y_check=shear_y_check,
            shear_z_check=shear_z_check,
            buckling_y_check=buckling_y_check,
            buckling_z_check=buckling_z_check,
            lateral_torsional_buckling_check=lateral_torsional_buckling_check,
            combined_axial_bending_check=combined_check,
            overall_status=overall_status
        )


# =============================================================================
# FastAPI 应用
# =============================================================================

# 创建FastAPI应用实例
app = FastAPI(
    title="建筑工程结构计算API",
    description="基于Blueprints库的建筑工程结构计算模块，包含混凝土梁、柱、钢结构验算",
    version="1.0.0",
    contact={
        "name": "结构计算API",
        "email": "structural@example.com"
    }
)

# 添加CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 创建计算器实例
beam_calculator = ConcreteBeamCalculator()
column_calculator = ConcreteColumnCalculator()
steel_calculator = SteelMemberCalculator()


@app.get("/")
async def root():
    """API根路径"""
    return {
        "message": "建筑工程结构计算API",
        "version": "1.0.0",
        "endpoints": [
            "/api/beam/calculate",
            "/api/column/calculate",
            "/api/steel/calculate",
            "/docs"
        ]
    }


@app.get("/health")
async def health_check():
    """健康检查端点"""
    return {"status": "healthy", "service": "structural-calculation-api"}


@app.post("/api/beam/calculate", response_model=ConcreteBeamOutput)
async def calculate_beam(input_data: ConcreteBeamInput):
    """
    混凝土梁计算端点
    
    执行混凝土梁的抗弯、抗剪、挠度验算
    
    - **width**: 梁宽 (mm)
    - **height**: 梁高 (mm)
    - **span**: 跨度 (m)
    - **concrete**: 混凝土材料参数
    - **reinforcement**: 钢筋配置
    - **dead_load**: 恒载 (kN/m)
    - **live_load**: 活载 (kN/m)
    """
    try:
        result = beam_calculator.calculate(input_data)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/api/column/calculate", response_model=ConcreteColumnOutput)
async def calculate_column(input_data: ConcreteColumnInput):
    """
    混凝土柱计算端点
    
    执行混凝土柱的轴心受压、偏心受压、长细比验算
    
    - **width**: 柱宽 (mm)
    - **depth**: 柱深 (mm)
    - **height**: 柱高 (m)
    - **concrete**: 混凝土材料参数
    - **axial_load**: 轴力设计值 (kN)
    - **moment_x**: 绕X轴弯矩 (kN·m)
    - **moment_y**: 绕Y轴弯矩 (kN·m)
    """
    try:
        result = column_calculator.calculate(input_data)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/api/steel/calculate", response_model=SteelMemberOutput)
async def calculate_steel(input_data: SteelMemberInput):
    """
    钢结构构件计算端点
    
    执行钢结构构件的强度、稳定性验算
    
    - **profile_type**: 型钢类型 (HEA, HEB, IPE, RHS, SHS)
    - **profile_name**: 型钢型号 (如HEA200, IPE300)
    - **steel**: 钢材材料参数
    - **length**: 构件长度 (m)
    - **axial_force**: 轴力设计值 (kN)
    - **moment_y**: 绕强轴弯矩 (kN·m)
    - **moment_z**: 绕弱轴弯矩 (kN·m)
    """
    try:
        result = steel_calculator.calculate(input_data)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/api/materials/concrete-classes")
async def get_concrete_classes():
    """获取支持的混凝土强度等级列表"""
    return {
        "concrete_classes": [
            "C12/15", "C16/20", "C20/25", "C25/30", "C30/37",
            "C35/45", "C40/50", "C45/55", "C50/60", "C55/67",
            "C60/75", "C70/85", "C80/95", "C90/105"
        ]
    }


@app.get("/api/materials/steel-classes")
async def get_steel_classes():
    """获取支持的钢材等级列表"""
    return {
        "steel_classes": ["S235", "S275", "S355", "S450"]
    }


@app.get("/api/profiles/{profile_type}")
async def get_available_profiles(profile_type: SteelProfileType):
    """获取指定类型的可用型钢型号列表"""
    profile_databases = {
        SteelProfileType.HEA: HEA,
        SteelProfileType.HEB: HEB,
        SteelProfileType.IPE: IPE,
        SteelProfileType.RHS: RHS,
        SteelProfileType.SHS: SHS
    }
    
    db = profile_databases.get(profile_type)
    if db and hasattr(db, '_database'):
        profiles = list(getattr(db, '_database').keys())
        return {"profile_type": profile_type.value, "available_profiles": profiles}
    
    return {"profile_type": profile_type.value, "available_profiles": []}


# =============================================================================
# 示例用法
# =============================================================================

def example_usage():
    """示例用法演示"""
    
    print("=" * 60)
    print("建筑工程结构计算模块 - 示例用法")
    print("=" * 60)
    
    # 示例1: 混凝土梁计算
    print("\n【示例1】混凝土梁计算")
    print("-" * 40)
    
    beam_input = ConcreteBeamInput(
        width=250,
        height=500,
        span=6.0,
        support_type=BeamSupportType.SIMPLY_SUPPORTED,
        concrete=ConcreteMaterialInput(strength_class="C30/37"),
        reinforcement=ReinforcementInput(
            diameter=20,
            count=4,
            grade="B500B",
            cover=30
        ),
        dead_load=15.0,
        live_load=10.0
    )
    
    beam_result = beam_calculator.calculate(beam_input)
    print(f"梁描述: {beam_result.beam_description}")
    print(f"设计弯矩: {beam_result.design_moment} kN·m")
    print(f"设计剪力: {beam_result.design_shear} kN")
    print(f"抗弯验算: {beam_result.flexural_check.message} (利用率: {beam_result.flexural_check.unity_check})")
    print(f"抗剪验算: {beam_result.shear_check.message} (利用率: {beam_result.shear_check.unity_check})")
    print(f"挠度验算: {beam_result.deflection_check.message} (最大挠度: {beam_result.max_deflection} mm)")
    print(f"配筋率: {beam_result.reinforcement_ratio}%")
    print(f"总体结果: {'通过' if beam_result.overall_status else '不通过'}")
    
    # 示例2: 混凝土柱计算
    print("\n【示例2】混凝土柱计算")
    print("-" * 40)
    
    column_input = ConcreteColumnInput(
        width=400,
        depth=400,
        height=3.5,
        support_type=ColumnSupportType.FIXED_TOP_BOTTOM,
        concrete=ConcreteMaterialInput(strength_class="C30/37"),
        longitudinal_reinforcement=ReinforcementInput(
            diameter=20,
            count=8,
            grade="B500B",
            cover=30
        ),
        stirrup_diameter=8,
        stirrup_spacing=150,
        axial_load=1500,
        moment_x=50,
        moment_y=30
    )
    
    column_result = column_calculator.calculate(column_input)
    print(f"柱描述: {column_result.column_description}")
    print(f"轴心受压承载力: {column_result.axial_capacity} kN")
    print(f"轴心受压验算: {column_result.axial_check.message} (利用率: {column_result.axial_check.unity_check})")
    print(f"双向偏心验算: {column_result.biaxial_moment_check.message} (利用率: {column_result.biaxial_moment_check.unity_check})")
    print(f"长细比: {column_result.slenderness_ratio}")
    print(f"稳定系数: {column_result.stability_coefficient}")
    print(f"总体结果: {'通过' if column_result.overall_status else '不通过'}")
    
    # 示例3: 钢结构构件计算
    print("\n【示例3】钢结构构件计算")
    print("-" * 40)
    
    steel_input = SteelMemberInput(
        profile_type=SteelProfileType.HEA,
        profile_name="HEA200",
        steel=SteelMaterialInput(steel_class="S355"),
        length=4.0,
        effective_length_factor=1.0,
        axial_force=-500,  # 压力
        moment_y=80,
        moment_z=10,
        shear_y=50,
        shear_z=5
    )
    
    steel_result = steel_calculator.calculate(steel_input)
    print(f"构件描述: {steel_result.member_description}")
    print(f"截面面积: {steel_result.profile_properties['area_mm2']} mm²")
    print(f"单位重量: {steel_result.profile_properties['weight_kg_m']} kg/m")
    print(f"强轴抗弯验算: {steel_result.bending_y_check.message} (利用率: {steel_result.bending_y_check.unity_check})")
    print(f"弱轴抗弯验算: {steel_result.bending_z_check.message} (利用率: {steel_result.bending_z_check.unity_check})")
    print(f"强轴屈曲验算: {steel_result.buckling_y_check.message} (利用率: {steel_result.buckling_y_check.unity_check})")
    print(f"弱轴屈曲验算: {steel_result.buckling_z_check.message} (利用率: {steel_result.buckling_z_check.unity_check})")
    print(f"组合验算: {steel_result.combined_axial_bending_check.message} (利用率: {steel_result.combined_axial_bending_check.unity_check})")
    print(f"总体结果: {'通过' if steel_result.overall_status else '不通过'}")
    
    print("\n" + "=" * 60)
    print("示例运行完成")
    print("=" * 60)


# =============================================================================
# 主程序入口
# =============================================================================

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--example":
        # 运行示例
        example_usage()
    else:
        # 启动FastAPI服务器
        print("启动建筑工程结构计算API服务器...")
        print("访问 http://localhost:8000/docs 查看API文档")
        uvicorn.run(app, host="0.0.0.0", port=8000)
