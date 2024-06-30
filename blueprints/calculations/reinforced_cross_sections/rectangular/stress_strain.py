"""Stress-strain calculations for rectangular reinforced concrete sections."""
import functools
from cmath import isclose
from enum import Enum
from typing import Literal, Protocol

from icecream import ic

from blueprints.structural_sections.concrete.rebar import Rebar
from blueprints.structural_sections.concrete.reinforced_concrete_sections.rectangular_rcs import RectangularReinforcedCrossSection
from blueprints.type_alias import KN, KNM, DIMENSIONLESS, MM
from blueprints.unit_conversion import KN_TO_N, KNM_TO_NMM


class RectangularEdge(Enum):
    """Enumeration of edges of square or rectangular cross-sections. X direction is in the length axis of the cross-section."""

    UPPER_SIDE = "UPPER (+Z)"
    RIGHT_SIDE = "RIGHT (+Y)"
    LOWER_SIDE = "LOWER (-Z)"
    LEFT_SIDE = "LEFT (-Y)"


class StressStrainCalculationsRectangular:
    """Class for stress-strain calculations for rectangular reinforced concrete sections."""

    def __init__(
        self,
        reinforced_cross_section: RectangularReinforcedCrossSection,
        n_x: KN | None = None,
        m_y: KNM | None = None,
        design_situation: Literal["permanent/temporary", "extraordinary"] = "permanent/temporary",
        gamma_s: DIMENSIONLESS | None = None,
        gamma_c: DIMENSIONLESS | None = None,
    ) -> None:
        """Stress-strain calculations for rectangular reinforced concrete sections.

        Parameters
        ----------
        reinforced_cross_section: RectangularReinforcedCrossSection
            Reinforced cross-section
        n_x: KN, optional
            Axial force. (negative is compression)
        m_y: KNM, optional
            Bending moment around the y-axis.
            Positive is from X to Z (positive moment gives compression in Z-positive domain)
            Deviates from right-hand rule
        design_situation: Literal["permanent/temporary", "extraordinary"]
            Design situation, default is "permanent/temporary"
        """
        if n_x is None and m_y is None:
            msg = "Either n_x and/or m_y should be given"
            raise ValueError(msg)
        self.reinforced_cross_section = reinforced_cross_section
        self.n_x = n_x * KN_TO_N
        self.m_y = m_y * KNM_TO_NMM
        self._design_situation = design_situation
        self._gamma_s = gamma_s
        self._gamma_c = gamma_c
        self._x_u_calculated = False
        self._x_u = 0.0

    @property
    def get_x_u_chatgpt(self) -> MM:
        """
        Get Xu for the cross-section based on the input given [mm].

        Returns
        -------
        MM
            Distance from the top of the cross-section to the neutral axis.
        """
        if self._x_u_calculated:
            return self._x_u

        # Constants
        MAX_ITERATIONS = 20
        TOLERANCE = 1e-5
        DEFAULT_FACTOR = 1.0 if self.most_strained_side == RectangularEdge.LOWER_SIDE else -1.0

        # Initial guess for the neutral axis position
        initial_x_u = self.reinforced_cross_section.height * 0.5

        # Cross-section properties
        e_cm = self.reinforced_cross_section.concrete_material.e_cm
        b = self.reinforced_cross_section.width
        h = self.reinforced_cross_section.height

        @functools.lru_cache
        def point_zero(x_u: 'MM') -> float:
            """
            Calculate the value of the equation at a given x_u.
            This represents the distance where the neutral axis is located.

            Parameters
            ----------
            x_u : MM
                Distance from the top of the cross-section to the neutral axis.

            Returns
            -------
            float
                Result of the equation at x_u.
            """
            part_1 = (self.n_x * e_cm / 6 * b) * x_u ** 2
            part_2 = (-e_cm * b * self.n_x * h / 4 - (DEFAULT_FACTOR * self.m_y) * 0.5 * e_cm * b) * x_u
            part_3 = sum(self.n_x * rebar.material.e_s * rebar.area * (self._d_distance_rebar(rebar.y) - h / 2.0)
                         for rebar in self.reinforced_cross_section.longitudinal_rebars)
            part_4 = sum((DEFAULT_FACTOR * self.m_y) * rebar.material.e_s * rebar.area
                         for rebar in self.reinforced_cross_section.longitudinal_rebars)
            part_5 = sum(-self.n_x * rebar.material.e_s * rebar.area * (self._d_distance_rebar(rebar.y) - h / 2.0) *
                         self._d_distance_rebar(rebar.y)
                         for rebar in self.reinforced_cross_section.longitudinal_rebars)
            part_6 = sum((DEFAULT_FACTOR * self.m_y) * rebar.material.e_s * rebar.area * self._d_distance_rebar(rebar.y)
                         for rebar in self.reinforced_cross_section.longitudinal_rebars)
            return part_1 + part_2 + part_3 - part_4 + (part_5 + part_6) / x_u

        initial_point_zero = point_zero(initial_x_u)
        last_x_u = initial_x_u - initial_x_u / 2 if initial_point_zero < 0 else initial_x_u + initial_x_u / 2
        iterations = 0

        while iterations < MAX_ITERATIONS:
            if not isclose(last_x_u - initial_x_u, 0.0, abs_tol=TOLERANCE):
                current_point_zero = point_zero(last_x_u)
                try:
                    next_x_u = last_x_u - current_point_zero / ((current_point_zero - initial_point_zero) / (last_x_u - initial_x_u))
                except ZeroDivisionError:
                    next_x_u = last_x_u - current_point_zero / 1e25

                initial_x_u = last_x_u
                initial_point_zero = point_zero(last_x_u)
                last_x_u = abs(next_x_u)
            else:
                break

            iterations += 1

        if last_x_u > h or last_x_u < 0:
            last_x_u = 0.0

        self._x_u = max(0.0, last_x_u)
        self._x_u_calculated = True
        return self._x_u

    @property
    def get_x_u_old(self) -> MM:
        """Get Xu for the cross-section based on the input given [mm].

        Returns
        -------
        MM
            distance from the top of the cross-section to the neutral axis.
        """
        if self._x_u_calculated:
            return self._x_u
        # initial guess for the neutral axis
        initial_x_u = self.reinforced_cross_section.height * 0.5

        # get the properties of the cross-section
        e_cm = self.reinforced_cross_section.concrete_material.e_cm
        b = self.reinforced_cross_section.width
        h = self.reinforced_cross_section.height
        factor = 1.0 if self.most_strained_side == RectangularEdge.LOWER_SIDE else -1.0

        @functools.lru_cache
        def point_zero(x_u: MM) -> MM:
            """Get the point where the equation is zero."""
            part_1 = (self.n_x * e_cm / 6 * b) * x_u ** 2
            part_2 = (-e_cm * b * self.n_x * h / 4 - (factor * self.m_y) * 0.5 * e_cm * b) * x_u
            part_3 = 0.0
            part_4 = 0.0
            part_5 = 0.0
            part_6 = 0.0
            for rebar in self.reinforced_cross_section.longitudinal_rebars:
                d = self._d_distance_rebar(rebar.y)
                e_s = rebar.material.e_s
                part_3 += self.n_x * e_s * rebar.area * (d - h / 2.0)
                part_4 += (factor * self.m_y) * e_s * rebar.area
                part_5 += -self.n_x * e_s * rebar.area * (d - h / 2.0) * d
                part_6 += (factor * self.m_y) * e_s * rebar.area * d
            return part_1 + part_2 + part_3 - part_4 + (part_5 + part_6) / x_u

        initial_point_zero = point_zero(x_u=initial_x_u)

        last_x_u = initial_x_u - initial_x_u / 2 if initial_point_zero < 0 else initial_x_u + initial_x_u / 2

        raised = [initial_point_zero ** 2, point_zero(last_x_u) ** 2]

        iterations = 0
        while iterations < 20:
            if not isclose(a=last_x_u - initial_x_u, b=0.0, abs_tol=1e-5):
                point_0 = point_zero(last_x_u)
                try:
                    vergelijking = last_x_u - point_0 / ((point_0 - initial_point_zero) / (last_x_u - initial_x_u))
                except ZeroDivisionError:
                    vergelijking = last_x_u - point_0 / 1e25
                initial_x_u = last_x_u
                initial_point_zero = point_zero(last_x_u)
                last_x_u = abs(vergelijking)
            else:
                raised.append(0)
                break
            raised.append(point_zero(last_x_u) ** 2)
            iterations += 1

        if min(raised):
            last_x_u = 0.0

        if last_x_u > self.reinforced_cross_section.height or last_x_u < 0:
            last_x_u = 0.0
        self._x_u = max(0.0, last_x_u)
        self._x_u_calculated = True
        return self._x_u

    @property
    def x_u(self) -> MM:
        """Get Xu for the cross-section based on the input given [mm].

        Returns
        -------
        MM
            distance from the top of the cross-section to the neutral axis.
        """
        if self._x_u_calculated:
            return self._x_u

        # Constants
        max_iterations = 20
        tolerance = 1e-5
        default_factor = 1.0 if self.most_strained_side == RectangularEdge.LOWER_SIDE else -1.0

        # initial guess for the neutral axis position
        initial_x_u = self.reinforced_cross_section.height * 0.5

        # cross-section properties
        e_cm = self.reinforced_cross_section.concrete_material.e_cm
        width = self.reinforced_cross_section.width
        height = self.reinforced_cross_section.height

        @functools.lru_cache
        def point_zero(x_u: MM) -> MM:
            """Get the point where the equation is zero."""
            part_1 = (self.n_x * e_cm / 6 * width) * x_u ** 2
            part_2 = (-e_cm * width * self.n_x * height / 4 - (default_factor * self.m_y) * 0.5 * e_cm * width) * x_u
            part_3 = 0.0
            part_4 = 0.0
            part_5 = 0.0
            part_6 = 0.0
            for rebar in self.reinforced_cross_section.longitudinal_rebars:
                d = self._d_distance_rebar(rebar.y)
                e_s = rebar.material.e_s
                part_3 += self.n_x * e_s * rebar.area * (d - height / 2.0)
                part_4 += (default_factor * self.m_y) * e_s * rebar.area
                part_5 += -self.n_x * e_s * rebar.area * (d - height / 2.0) * d
                part_6 += (default_factor * self.m_y) * e_s * rebar.area * d
            return part_1 + part_2 + part_3 - part_4 + (part_5 + part_6) / x_u

        initial_point_zero = point_zero(x_u=initial_x_u)

        last_x_u = initial_x_u - initial_x_u / 2 if initial_point_zero < 0 else initial_x_u + initial_x_u / 2

        raised = [initial_point_zero ** 2, point_zero(last_x_u) ** 2]

        iterations = 0
        while iterations < max_iterations:
            if not isclose(a=last_x_u - initial_x_u, b=0.0, abs_tol=tolerance):
                point_0 = point_zero(last_x_u)
                try:
                    vergelijking = last_x_u - point_0 / ((point_0 - initial_point_zero) / (last_x_u - initial_x_u))
                except ZeroDivisionError:
                    vergelijking = last_x_u - point_0 / 1e25
                initial_x_u = last_x_u
                initial_point_zero = point_zero(last_x_u)
                last_x_u = abs(vergelijking)
            else:
                raised.append(0)
                break
            raised.append(point_zero(last_x_u) ** 2)

            iterations += 1

        if min(raised):
            last_x_u = 0.0

        if last_x_u > self.reinforced_cross_section.height or last_x_u < 0:
            last_x_u = 0.0

        self._x_u = max(0.0, last_x_u)
        self._x_u_calculated = True
        return self._x_u

    @property
    def gamma_s(self) -> float:
        """Get the partial safety factor for the reinforcement [-]."""
        if self._gamma_s:
            return self._gamma_s
        y_s_permanent_temporary = 1.15
        y_s_extraordinary = 1.0
        return y_s_permanent_temporary if self.design_situation == "permanent/temporary" else y_s_extraordinary

    @property
    def gamma_c(self) -> float:
        """Get the partial safety factor for the concrete [-]."""
        if self._gamma_c:
            return self._gamma_c
        y_c_permanent_temporary = 1.5
        y_c_extraordinary = 1.2
        return y_c_permanent_temporary if self.design_situation == "permanent/temporary" else y_c_extraordinary

    @property
    def design_situation(self) -> Literal["permanent/temporary", "extraordinary"]:
        """Get the design situation."""
        if self._design_situation.lower() not in ["permanent/temporary", "extraordinary"]:
            msg = f"Design situation '{self._design_situation}' is not supported"
            raise ValueError(msg)
        return self._design_situation

    @property
    def most_strained_side(self) -> RectangularEdge:
        """Get the most strained side of the cross-section.

        Returns
        -------
        RectangularEdge
            Most strained side
        """
        if self.m_y >= 0:
            return RectangularEdge.LOWER_SIDE
        return RectangularEdge.UPPER_SIDE

    @property
    def stretch_concrete_pressure_side(self) -> float:
        """Maximal concrete stretch on the pressure edge [-].

        Returns
        -------
        float
        """
        return self._stretch_pressure_side_eps_c(x_u=self.x_u)

    @property
    def strain_concrete_pressure_side(self) -> float:
        """Maximal concrete strain on the pressure edge [N/mm2].

        Returns
        -------
        float
        """
        return self.stretch_concrete_pressure_side * self.reinforced_cross_section.concrete_material.e_cm

    @property
    def resulting_force_concrete_pressure_side(self) -> float:
        """Maximal resulting force of the concrete on the pressure edge [N].

        Returns
        -------
        float
        """
        return self.strain_concrete_pressure_side * self.reinforced_cross_section.width * (self.x_u / 2)

    def stretch_in_rebars(self) -> dict[float, Rebar]:
        """Get the stretch in the rebars [-].

        Returns
        -------
        dict[float, Rebar]
            Stretch in the rebars
        """
        results = {}

        if not self.reinforced_cross_section.longitudinal_rebars:
            msg = f"No rebars present in {self.reinforced_cross_section.longitudinal_rebars}"
            raise ValueError(msg)

        for rebar in self.reinforced_cross_section.longitudinal_rebars:
            results[self.stretch_rebar(rebar.y)] = rebar
        return results

    @property
    def get_rebar_max_stretch(self) -> Rebar:
        """Get the rebar with the maximum stretch [-].

        Returns
        -------
        Rebar
            Rebar with the maximum stretch
        """
        stretch_in_rebars = self.stretch_in_rebars()
        results = list(stretch_in_rebars.keys())
        max_stretch = max(results, key=abs)
        return stretch_in_rebars[max_stretch]

    def get_rebar_max_stretch_on_side(self, side: RectangularEdge) -> Rebar:
        """Get the rebar with the maximum stretch on the given side [-].

        Parameters
        ----------
        side: RectangularEdge
            Side of the cross-section

        Returns
        -------
        Rebar
            Rebar with the maximum stretch on the given side
        """
        rebar_max_stretch = None

        if side == RectangularEdge.UPPER_SIDE:
            rebars_on_side = [rebar for rebar in self.reinforced_cross_section.longitudinal_rebars if rebar.y >= 0]
        elif side == RectangularEdge.LOWER_SIDE:
            rebars_on_side = [rebar for rebar in self.reinforced_cross_section.longitudinal_rebars if rebar.y <= 0]
        else:
            msg = f"Lateral sides are not supported with this method ({side})"
            raise ValueError(msg)

        for rebar in rebars_on_side:
            if not rebar_max_stretch:
                rebar_max_stretch = rebar
            if abs(self.stretch_rebar(rebar.y)) >= abs(self.stretch_rebar(rebar_max_stretch.y)):
                rebar_max_stretch = rebar
        if not rebar_max_stretch:
            msg = f"No rebars present in {side} ({self.reinforced_cross_section.longitudinal_rebars})"
            raise ValueError(msg)
        return rebar_max_stretch

    @functools.lru_cache
    def stretch_rebar(self, rebar_y: float) -> float:
        """Get the stretch in the rebar at rebar_y.

        Parameters
        ----------
        rebar_y: float
            Rebar y position

        Returns
        -------
        float
            Stretch in the rebar
        """
        d = self._d_distance_rebar(rebar_y)
        concrete_stretch = self.stretch_concrete_pressure_side
        x_u = self.x_u

        if concrete_stretch:
            return concrete_stretch / x_u * (x_u - d)
        h = self.reinforced_cross_section.height
        e_s = self.reinforced_cross_section.steel_material.e_s
        area_reinforcement = sum(rebar.area for rebar in self.reinforced_cross_section.longitudinal_rebars)
        part_1 = sum(rebar.area * (self._d_distance_rebar(rebar.y) - h / 2) for rebar in self.reinforced_cross_section.longitudinal_rebars)
        part_2 = sum(rebar.area * (self._d_distance_rebar(rebar.y) - h / 2) ** 2 for rebar in self.reinforced_cross_section.longitudinal_rebars)
        k_u = (self.m_y / e_s - self.n_x / e_s / area_reinforcement * part_1) / ((part_1 ** 2) / area_reinforcement - part_2)
        e = (self.n_x / e_s + k_u * part_1) / area_reinforcement
        return e - k_u * (d - h / 2)

    @staticmethod
    def strain_rebar(rebar: Rebar, stretch_rebar: float) -> float:
        """Get the strain in the rebar.

        Parameters
        ----------
        rebar: Rebar
            Rebar
        stretch_rebar: float
            Stretch in the rebar

        Returns
        -------
        float
            Strain in the rebar
        """
        if not isinstance(rebar.material, ReinforcementSteelMaterial):
            msg = f"Rebar {rebar.name} should be made of ReinforcedSteelMaterial"
            raise ValueError(msg)
        if abs(stretch_rebar) <= rebar.material.f_yk / rebar.material.e_s:
            return stretch_rebar * rebar.material.e_s
        return (stretch_rebar / abs(stretch_rebar)) * rebar.material.f_yk

    @functools.lru_cache
    def _d_distance_rebar(self, rebar_y: float) -> float:
        """Get the distance from the center of the cross-section to the rebar."""
        if self.most_strained_side == RectangularEdge.LOWER_SIDE:
            if rebar_y >= 0:
                return (self.reinforced_cross_section.height / 2) - rebar_y
            return (self.reinforced_cross_section.height / 2) + abs(rebar_y)
        if self.most_strained_side == RectangularEdge.UPPER_SIDE:
            return (self.reinforced_cross_section.height / 2) + rebar_y
        msg = "Use RectangularEdge.UPPER_SIDE or LOWER_SIDE"
        raise ValueError(msg)

    @functools.lru_cache
    def _stretch_pressure_side_eps_c(self, x_u: float) -> float:
        """Maximal concrete stretch on the pressure edge for the given Xu.

        Parameters
        ----------
        x_u: float
            Xu [mm]

        Returns
        -------
        float
            stretch eu for a given Xu in the context of the given reinforced cross-section [-]
        """
        e_cm = self.reinforced_cross_section.concrete_material.e_cm
        b = self.reinforced_cross_section.width
        rebars = self.reinforced_cross_section.longitudinal_rebars

        share_rebars_in_eps_c = 0.0
        if self.n_x:
            for rebar in rebars:
                d = self._d_distance_rebar(rebar.y)
                share_rebars_in_eps_c += 2 * rebar.material.e_s * rebar.area * (d - x_u)
            return (-2 * self.n_x * x_u) / ((-1 * x_u ** 2 * e_cm * b) + share_rebars_in_eps_c)
        for rebar in rebars:
            d = self._d_distance_rebar(rebar.y)
            share_rebars_in_eps_c += rebar.material.e_s * rebar.area * (d - x_u / 3) * (d / x_u - 1)
        factor = 1 if self.most_strained_side == RectangularEdge.LOWER_SIDE else -1
        return (-self.m_y / share_rebars_in_eps_c) * factor


if __name__ == '__main__':
    from blueprints.materials.concrete import ConcreteMaterial, ConcreteStrengthClass
    from blueprints.materials.reinforcement_steel import ReinforcementSteelMaterial, ReinforcementSteelQuality
    from blueprints.structural_sections.concrete.reinforced_concrete_sections.covers import CoversRectangular
    from blueprints.structural_sections.concrete.reinforced_concrete_sections.cross_sections_shapes import Edges
    from blueprints.structural_sections.concrete.reinforced_concrete_sections.rectangular_rcs import RectangularReinforcedCrossSection

    # Define a concrete material
    concrete = ConcreteMaterial(concrete_class=ConcreteStrengthClass.C35_45)

    # Define a reinforcement steel material
    steel = ReinforcementSteelMaterial(steel_quality=ReinforcementSteelQuality.B500B)

    # Define a rectangular reinforced cross-section
    cs = RectangularReinforcedCrossSection(
        width=1000,
        height=800,
        covers=CoversRectangular(upper=30, lower=30, left=30, right=30),
        concrete_material=concrete,
        steel_material=steel,
    )

    # Change the covers of the cross-section ( if necessary )
    cs.set_covers(upper=60, lower=45)

    # Add reinforcement to the cross-section
    cs.add_longitudinal_reinforcement_by_quantity_on_edge(
        n=5,
        diameter=14,
        edge=Edges.UPPER_SIDE,
        material=steel,
    )
    cs.add_longitudinal_reinforcement_by_quantity_on_edge(
        n=4,
        diameter=20,
        edge=Edges.LOWER_SIDE,
        material=steel,
    )

    # Add stirrups to the cross-section
    cs.add_stirrup_along_edges(
        diameter=8,
        distance=150,
        material=steel,
    )

    # Add a longitudinal rebar to the cross-section
    cs.add_longitudinal_rebar(
        diameter=16,
        x=-250,
        y=-100,
        material=steel,
    )
    cs.add_longitudinal_rebar(
        diameter=32,
        x=200,
        y=150,
        material=steel,
    )

    # start calculations
    stress_strain = StressStrainCalculationsRectangular(
        reinforced_cross_section=cs,
        n_x=50 * KN_TO_N,
        m_y=450 * KNM_TO_NMM,
        design_situation="permanent/temporary",
    )

    ic(stress_strain.x_u)
    ic(stress_strain.gamma_s)
    ic(stress_strain.gamma_c)
    ic(stress_strain.design_situation)
    ic(stress_strain.most_strained_side)
    ic(stress_strain.stretch_concrete_pressure_side)
    ic(stress_strain.strain_concrete_pressure_side)
    ic(stress_strain.resulting_force_concrete_pressure_side)

    bar_max_stretch_upper = stress_strain.get_rebar_max_stretch_on_side(side=RectangularEdge.UPPER_SIDE)
    bar_max_stretch_lower = stress_strain.get_rebar_max_stretch_on_side(side=RectangularEdge.LOWER_SIDE)
    bar_max_stretch_overall = stress_strain.get_rebar_max_stretch

    max_stretch_upper = stress_strain.stretch_rebar(rebar_y=bar_max_stretch_upper.y)
    max_stretch_lower = stress_strain.stretch_rebar(rebar_y=bar_max_stretch_lower.y)
    max_stretch_overall = stress_strain.stretch_rebar(rebar_y=bar_max_stretch_overall.y)

    max_strain_upper = stress_strain.strain_rebar(rebar=bar_max_stretch_upper, stretch_rebar=max_stretch_upper)
    max_strain_lower = stress_strain.strain_rebar(rebar=bar_max_stretch_lower, stretch_rebar=max_stretch_lower)
    max_strain_overall = stress_strain.strain_rebar(rebar=bar_max_stretch_overall, stretch_rebar=max_stretch_overall)

    ic(bar_max_stretch_upper, bar_max_stretch_lower, bar_max_stretch_overall)
    ic(max_stretch_upper, max_stretch_lower, max_stretch_overall)
    ic(max_strain_upper, max_strain_lower, max_strain_overall)

    # cs.plot(show=True)
