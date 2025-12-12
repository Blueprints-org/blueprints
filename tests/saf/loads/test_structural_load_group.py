"""Tests for StructuralLoadGroup dataclass."""

import pytest

from blueprints.saf.loads.structural_load_group import (
    LoadGroupType,
    Relation,
    StructuralLoadGroup,
)


class TestStructuralLoadGroup:
    """Tests for StructuralLoadGroup dataclass."""

    def test_permanent_with_standard_relation(self) -> None:
        """Test valid permanent load group with standard relation."""
        lg = StructuralLoadGroup(
            name="LG1",
            load_group_type=LoadGroupType.PERMANENT,
            relation=Relation.STANDARD,
        )

        assert lg.name == "LG1"
        assert lg.load_group_type == LoadGroupType.PERMANENT
        assert lg.relation == Relation.STANDARD
        assert lg.load_type == ""
        assert lg.id == ""

    def test_permanent_with_together_relation(self) -> None:
        """Test valid permanent load group with together relation."""
        lg = StructuralLoadGroup(
            name="LG_PERM",
            load_group_type=LoadGroupType.PERMANENT,
            relation=Relation.TOGETHER,
            id="uuid-123",
        )

        assert lg.name == "LG_PERM"
        assert lg.load_group_type == LoadGroupType.PERMANENT
        assert lg.relation == Relation.TOGETHER
        assert lg.id == "uuid-123"

    def test_variable_with_snow_load_type(self) -> None:
        """Test valid variable load group with Snow load type."""
        lg = StructuralLoadGroup(
            name="LG2",
            load_group_type=LoadGroupType.VARIABLE,
            relation=Relation.EXCLUSIVE,
            load_type="Snow",
        )

        assert lg.name == "LG2"
        assert lg.load_group_type == LoadGroupType.VARIABLE
        assert lg.relation == Relation.EXCLUSIVE
        assert lg.load_type == "Snow"

    def test_variable_with_wind_load_type(self) -> None:
        """Test valid variable load group with Wind load type."""
        lg = StructuralLoadGroup(
            name="LG_WIND",
            load_group_type=LoadGroupType.VARIABLE,
            relation=Relation.STANDARD,
            load_type="Wind",
        )

        assert lg.load_type == "Wind"
        assert lg.relation == Relation.STANDARD

    def test_variable_with_vehicle_30kn_load_type(self) -> None:
        """Test valid variable load group with Vehicle >30kN load type."""
        lg = StructuralLoadGroup(
            name="LG_VEHICLE",
            load_group_type=LoadGroupType.VARIABLE,
            relation=Relation.EXCLUSIVE,
            load_type="Vehicle >30kN",
        )

        assert lg.load_type == "Vehicle >30kN"

    def test_accidental_with_exclusive_relation(self) -> None:
        """Test valid accidental load group with exclusive relation."""
        lg = StructuralLoadGroup(
            name="LG_ACC",
            load_group_type=LoadGroupType.ACCIDENTAL,
            relation=Relation.EXCLUSIVE,
        )

        assert lg.load_group_type == LoadGroupType.ACCIDENTAL
        assert lg.relation == Relation.EXCLUSIVE

    def test_seismic_with_exclusive_relation(self) -> None:
        """Test valid seismic load group with exclusive relation."""
        lg = StructuralLoadGroup(
            name="LG_SEISMIC",
            load_group_type=LoadGroupType.SEISMIC,
            relation=Relation.EXCLUSIVE,
        )

        assert lg.load_group_type == LoadGroupType.SEISMIC

    def test_moving_with_exclusive_relation(self) -> None:
        """Test valid moving load group with exclusive relation."""
        lg = StructuralLoadGroup(
            name="LG_MOVING",
            load_group_type=LoadGroupType.MOVING,
            relation=Relation.EXCLUSIVE,
        )

        assert lg.load_group_type == LoadGroupType.MOVING

    def test_tensioning_with_standard_relation(self) -> None:
        """Test valid tensioning load group with standard relation."""
        lg = StructuralLoadGroup(
            name="LG_TENSION",
            load_group_type=LoadGroupType.TENSIONING,
            relation=Relation.STANDARD,
        )

        assert lg.load_group_type == LoadGroupType.TENSIONING

    def test_fire_with_exclusive_relation(self) -> None:
        """Test valid fire load group with exclusive relation."""
        lg = StructuralLoadGroup(
            name="LG_FIRE",
            load_group_type=LoadGroupType.FIRE,
            relation=Relation.EXCLUSIVE,
        )

        assert lg.load_group_type == LoadGroupType.FIRE

    def test_variable_without_load_type_raises_error(self) -> None:
        """Test that Variable load group without load_type raises ValueError."""
        with pytest.raises(
            ValueError,
            match=r"load_type must be specified when load_group_type = LoadGroupType\.VARIABLE",
        ):
            StructuralLoadGroup(
                name="LG_INVALID",
                load_group_type=LoadGroupType.VARIABLE,
                relation=Relation.EXCLUSIVE,
            )

    def test_together_on_variable_raises_error(self) -> None:
        """Test that Together relation on Variable load group raises ValueError."""
        with pytest.raises(
            ValueError,
            match=r"relation = Relation\.TOGETHER only valid for load_group_type = LoadGroupType\.PERMANENT",
        ):
            StructuralLoadGroup(
                name="LG_INVALID",
                load_group_type=LoadGroupType.VARIABLE,
                relation=Relation.TOGETHER,
                load_type="Snow",
            )

    def test_together_on_accidental_raises_error(self) -> None:
        """Test that Together relation on Accidental load group raises ValueError."""
        with pytest.raises(
            ValueError,
            match=r"relation = Relation\.TOGETHER only valid for load_group_type = LoadGroupType\.PERMANENT",
        ):
            StructuralLoadGroup(
                name="LG_INVALID",
                load_group_type=LoadGroupType.ACCIDENTAL,
                relation=Relation.TOGETHER,
            )

    def test_exclusive_on_permanent_raises_error(self) -> None:
        """Test that Exclusive relation on Permanent load group raises ValueError."""
        with pytest.raises(
            ValueError,
            match=r"relation = Relation\.EXCLUSIVE not valid for load_group_type = LoadGroupType\.PERMANENT",
        ):
            StructuralLoadGroup(
                name="LG_INVALID",
                load_group_type=LoadGroupType.PERMANENT,
                relation=Relation.EXCLUSIVE,
            )

    def test_invalid_load_type_raises_error(self) -> None:
        """Test that invalid load_type raises ValueError."""
        with pytest.raises(
            ValueError,
            match=r"load_type 'InvalidType' is not a valid SAF load type",
        ):
            StructuralLoadGroup(
                name="LG_INVALID",
                load_group_type=LoadGroupType.VARIABLE,
                relation=Relation.EXCLUSIVE,
                load_type="InvalidType",
            )

    def test_all_valid_load_types(self) -> None:
        """Test that all valid load types are accepted."""
        valid_types = [
            "Domestic",
            "Offices",
            "Congregation",
            "Shopping",
            "Storage",
            "Vehicle <30kN",
            "Vehicle >30kN",
            "Roofs",
            "Snow",
            "Wind",
            "Temperature",
        ]

        for load_type in valid_types:
            lg = StructuralLoadGroup(
                name="LG_TEST",
                load_group_type=LoadGroupType.VARIABLE,
                relation=Relation.EXCLUSIVE,
                load_type=load_type,
            )
            assert lg.load_type == load_type

    def test_load_group_equality(self) -> None:
        """Test that two load groups with same values are equal."""
        lg1 = StructuralLoadGroup(
            name="LG1",
            load_group_type=LoadGroupType.PERMANENT,
            relation=Relation.STANDARD,
        )
        lg2 = StructuralLoadGroup(
            name="LG1",
            load_group_type=LoadGroupType.PERMANENT,
            relation=Relation.STANDARD,
        )

        assert lg1 == lg2

    def test_load_group_inequality(self) -> None:
        """Test that load groups with different values are not equal."""
        lg1 = StructuralLoadGroup(
            name="LG1",
            load_group_type=LoadGroupType.PERMANENT,
            relation=Relation.STANDARD,
        )
        lg2 = StructuralLoadGroup(
            name="LG2",
            load_group_type=LoadGroupType.PERMANENT,
            relation=Relation.STANDARD,
        )

        assert lg1 != lg2

    def test_load_group_hashable(self) -> None:
        """Test that load groups are hashable (can be used in sets/dicts)."""
        lg1 = StructuralLoadGroup(
            name="LG1",
            load_group_type=LoadGroupType.PERMANENT,
            relation=Relation.STANDARD,
        )
        lg2 = StructuralLoadGroup(
            name="LG1",
            load_group_type=LoadGroupType.PERMANENT,
            relation=Relation.STANDARD,
        )

        lg_set = {lg1, lg2}
        assert len(lg_set) == 1

    def test_load_group_frozen(self) -> None:
        """Test that load group is immutable (frozen)."""
        lg = StructuralLoadGroup(
            name="LG1",
            load_group_type=LoadGroupType.PERMANENT,
            relation=Relation.STANDARD,
        )

        with pytest.raises(AttributeError):
            lg.name = "LG2"

    def test_load_type_optional_for_permanent(self) -> None:
        """Test that load_type is optional for Permanent load groups."""
        lg = StructuralLoadGroup(
            name="LG1",
            load_group_type=LoadGroupType.PERMANENT,
            relation=Relation.STANDARD,
        )

        assert lg.load_type == ""

    def test_id_optional_for_all_types(self) -> None:
        """Test that id is optional for all load group types."""
        lg = StructuralLoadGroup(
            name="LG1",
            load_group_type=LoadGroupType.VARIABLE,
            relation=Relation.EXCLUSIVE,
            load_type="Snow",
        )

        assert lg.id == ""

    def test_with_uuid_id(self) -> None:
        """Test that UUID id is properly stored."""
        uuid = "550e8400-e29b-41d4-a716-446655440000"
        lg = StructuralLoadGroup(
            name="LG1",
            load_group_type=LoadGroupType.PERMANENT,
            relation=Relation.STANDARD,
            id=uuid,
        )

        assert lg.id == uuid
