"""Implementation of SAF (Structural Analysis Format) on Blueprints.

 https://www.saf.guide/en/stable/

 We try to keep our implementation up to date with the latest SAF but will make our own choices if needed.

**This is not a full implementation of SAF, but rather a focused one for our use cases.**
"""

from blueprints.saf.loads.structural_curve_action import (
    Distribution,
    Extent,
    Location,
    StructuralCurveAction,
)
from blueprints.saf.loads.structural_curve_action_free import (
    Segment,
    StructuralCurveActionFree,
)
from blueprints.saf.loads.structural_curve_action_thermal import (
    StructuralCurveActionThermal,
)
from blueprints.saf.loads.structural_curve_moment import (
    MomentDirection,
    StructuralCurveMoment,
)
from blueprints.saf.loads.structural_load_case import (
    ActionType,
    StructuralLoadCase,
)
from blueprints.saf.loads.structural_load_combination import (
    Category,
    CombinationType,
    LoadCaseItem,
    NationalStandard,
    StructuralLoadCombination,
)
from blueprints.saf.loads.structural_load_group import (
    LoadGroupType,
    Relation,
    StructuralLoadGroup,
)
from blueprints.saf.loads.structural_point_action import (
    CoordinateDefinition,
    CoordinateSystem,
    Direction,
    ForceAction,
    Origin,
    StructuralPointAction,
)
from blueprints.saf.loads.structural_point_action_free import (
    StructuralPointActionFree,
)
from blueprints.saf.loads.structural_point_moment import (
    StructuralPointMoment,
)
from blueprints.saf.loads.structural_point_support_deformation import (
    StructuralPointSupportDeformation,
)
from blueprints.saf.loads.structural_surface_action import (
    StructuralSurfaceAction,
)
from blueprints.saf.loads.structural_surface_action_distribution import (
    StructuralSurfaceActionDistribution,
)
from blueprints.saf.loads.structural_surface_action_free import (
    StructuralSurfaceActionFree,
)
from blueprints.saf.loads.structural_surface_action_thermal import (
    StructuralSurfaceActionThermal,
    Variation,
)
from blueprints.saf.results.result_internal_force_1d import (
    ResultFor,
    ResultInternalForce1D,
    ResultOn,
)
from blueprints.saf.results.result_internal_force_2d_edge import (
    ResultInternalForce2DEdge,
    ResultOn2DEdge,
)
from blueprints.saf.structural_analysis_elements.composite_shape_def import (
    CompositeShapeDef,
    PolygonContour,
)
from blueprints.saf.structural_analysis_elements.structural_cross_section import (
    CrossSectionType,
    FormCode,
    ShapeType,
    StructuralCrossSection,
)
from blueprints.saf.structural_analysis_elements.structural_curve_edge import (
    SegmentType as CurveEdgeSegmentType,
)
from blueprints.saf.structural_analysis_elements.structural_curve_edge import (
    StructuralCurveEdge,
)
from blueprints.saf.structural_analysis_elements.structural_curve_member import (
    BehaviourType,
    GeometricalShapeType,
    LCSType,
    StructuralCurveMember,
    SystemLineType,
)
from blueprints.saf.structural_analysis_elements.structural_curve_member import (
    SegmentType as CurveMemberSegmentType,
)
from blueprints.saf.structural_analysis_elements.structural_curve_member_rib import (
    RibAlignmentType,
    RibBehaviourType,
    RibConnectionType,
    RibEffectiveWidthType,
    RibShapeType,
    StructuralCurveMemberRib,
)
from blueprints.saf.structural_analysis_elements.structural_curve_member_rib import (
    SegmentType as RibSegmentType,
)
from blueprints.saf.structural_analysis_elements.structural_curve_member_varying import (
    AlignmentType as VaryingAlignmentType,
)
from blueprints.saf.structural_analysis_elements.structural_curve_member_varying import (
    StructuralCurveMemberVarying,
    VaryingSegment,
)
from blueprints.saf.structural_analysis_elements.structural_material import (
    MaterialType,
    StructuralMaterial,
)
from blueprints.saf.structural_analysis_elements.structural_point_connection import (
    StructuralPointConnection,
)
from blueprints.saf.structural_analysis_elements.structural_proxy_element import (
    Face,
    StructuralProxyElement,
    Vertex,
)
from blueprints.saf.structural_analysis_elements.structural_storey import (
    StructuralStorey,
)
from blueprints.saf.structural_analysis_elements.structural_surface_member import (
    BehaviourType as SurfaceBehaviourType,
)
from blueprints.saf.structural_analysis_elements.structural_surface_member import (
    LCSType as SurfaceLCSType,
)
from blueprints.saf.structural_analysis_elements.structural_surface_member import (
    StructuralSurfaceMember,
    SurfaceEdgeType,
    SystemPlaneType,
    ThicknessType,
)
from blueprints.saf.structural_analysis_elements.structural_surface_member_opening import (
    EdgeType as OpeningEdgeType,
)
from blueprints.saf.structural_analysis_elements.structural_surface_member_opening import (
    StructuralSurfaceMemberOpening,
)
from blueprints.saf.structural_analysis_elements.structural_surface_member_region import (
    EdgeType as RegionEdgeType,
)
from blueprints.saf.structural_analysis_elements.structural_surface_member_region import (
    StructuralSurfaceMemberRegion,
)
from blueprints.saf.structural_analysis_elements.structural_surface_member_region import (
    SystemPlaneType as RegionSystemPlaneType,
)
from blueprints.saf.supports_and_hinges.rel_connects_rigid_cross import (
    RelConnectsRigidCross,
)
from blueprints.saf.supports_and_hinges.rel_connects_rigid_link import (
    RelConnectsRigidLink,
)
from blueprints.saf.supports_and_hinges.rel_connects_rigid_member import (
    RelConnectsRigidMember,
)
from blueprints.saf.supports_and_hinges.rel_connects_structural_member import (
    RelConnectsStructuralMember,
)
from blueprints.saf.supports_and_hinges.rel_connects_surface_edge import (
    RelConnectsSurfaceEdge,
)
from blueprints.saf.supports_and_hinges.structural_curve_connection import (
    StructuralCurveConnection,
)
from blueprints.saf.supports_and_hinges.structural_edge_connection import (
    StructuralEdgeConnection,
)
from blueprints.saf.supports_and_hinges.structural_point_support import (
    BoundaryCondition,
    RotationConstraint,
    StructuralPointSupport,
    SupportType,
    TranslationConstraint,
)
from blueprints.saf.supports_and_hinges.structural_surface_connection import (
    StructuralSurfaceConnection,
)

__all__ = [
    "ActionType",
    "AlignmentType",
    "BehaviourType",
    "BoundaryCondition",
    "Category",
    "CombinationType",
    "CompositeShapeDef",
    "CoordinateDefinition",
    "CoordinateSystem",
    "CrossSectionType",
    "CurveEdgeSegmentType",
    "CurveMemberSegmentType",
    "Direction",
    "Distribution",
    "EdgeType",
    "Extent",
    "Face",
    "ForceAction",
    "FormCode",
    "GeometricalShapeType",
    "LCSType",
    "LoadCaseItem",
    "LoadGroupType",
    "Location",
    "MaterialType",
    "MomentDirection",
    "NationalStandard",
    "OpeningEdgeType",
    "Origin",
    "PolygonContour",
    "RegionEdgeType",
    "RegionSystemPlaneType",
    "RelConnectsRigidCross",
    "RelConnectsRigidLink",
    "RelConnectsRigidMember",
    "RelConnectsStructuralMember",
    "RelConnectsSurfaceEdge",
    "Relation",
    "ResultFor",
    "ResultInternalForce1D",
    "ResultInternalForce2DEdge",
    "ResultOn",
    "ResultOn2DEdge",
    "RibAlignmentType",
    "RibBehaviourType",
    "RibConnectionType",
    "RibEffectiveWidthType",
    "RibSegmentType",
    "RibShapeType",
    "RotationConstraint",
    "Segment",
    "ShapeType",
    "StructuralCrossSection",
    "StructuralCurveAction",
    "StructuralCurveActionFree",
    "StructuralCurveActionThermal",
    "StructuralCurveConnection",
    "StructuralCurveEdge",
    "StructuralCurveMember",
    "StructuralCurveMemberRib",
    "StructuralCurveMemberVarying",
    "StructuralCurveMoment",
    "StructuralEdgeConnection",
    "StructuralLoadCase",
    "StructuralLoadCombination",
    "StructuralLoadGroup",
    "StructuralMaterial",
    "StructuralPointAction",
    "StructuralPointActionFree",
    "StructuralPointConnection",
    "StructuralPointMoment",
    "StructuralPointSupport",
    "StructuralPointSupportDeformation",
    "StructuralProxyElement",
    "StructuralStorey",
    "StructuralSurfaceAction",
    "StructuralSurfaceActionDistribution",
    "StructuralSurfaceActionFree",
    "StructuralSurfaceActionThermal",
    "StructuralSurfaceConnection",
    "StructuralSurfaceMember",
    "StructuralSurfaceMemberOpening",
    "StructuralSurfaceMemberRegion",
    "SupportType",
    "SurfaceBehaviourType",
    "SurfaceEdgeType",
    "SurfaceLCSType",
    "SystemLineType",
    "SystemPlaneType",
    "ThicknessType",
    "TranslationConstraint",
    "Variation",
    "VaryingAlignmentType",
    "VaryingSegment",
    "Vertex",
]
