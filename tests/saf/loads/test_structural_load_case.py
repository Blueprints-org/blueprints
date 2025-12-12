"""Tests for StructuralLoadCase dataclass."""

import pytest

from blueprints.saf.loads.structural_load_case import (
    ActionType,
    StructuralLoadCase,
)


class TestStructuralLoadCase:
    """Tests for StructuralLoadCase dataclass."""

    # Valid Initialization Tests

    def test_permanent_with_self_weight(self) -> None:
        """Test permanent load case with Self weight."""
        lc = StructuralLoadCase(
            name="LC1",
            action_type=ActionType.PERMANENT,
            load_group="LG1",
            load_type="Self weight",
        )

        assert lc.name == "LC1"
        assert lc.action_type == ActionType.PERMANENT
        assert lc.load_group == "LG1"
        assert lc.load_type == "Self weight"
        assert lc.duration == ""

    def test_permanent_with_others(self) -> None:
        """Test permanent load case with Others."""
        lc = StructuralLoadCase(
            name="LC_PERM",
            action_type=ActionType.PERMANENT,
            load_group="LG1",
            load_type="Others",
        )

        assert lc.load_type == "Others"

    def test_permanent_with_prestress(self) -> None:
        """Test permanent load case with Prestress."""
        lc = StructuralLoadCase(
            name="LC_PREST",
            action_type=ActionType.PERMANENT,
            load_group="LG1",
            load_type="Prestress",
        )

        assert lc.load_type == "Prestress"

    def test_permanent_with_standard(self) -> None:
        """Test permanent load case with Standard."""
        lc = StructuralLoadCase(
            name="LC_STD",
            action_type=ActionType.PERMANENT,
            load_group="LG1",
            load_type="Standard",
        )

        assert lc.load_type == "Standard"

    def test_variable_with_snow_short_duration(self) -> None:
        """Test variable load case with Snow and Short duration."""
        lc = StructuralLoadCase(
            name="LC2",
            action_type=ActionType.VARIABLE,
            load_group="LG2",
            load_type="Snow",
            duration="Short",
        )

        assert lc.action_type == ActionType.VARIABLE
        assert lc.load_type == "Snow"
        assert lc.duration == "Short"

    def test_variable_with_wind_long_duration(self) -> None:
        """Test variable load case with Wind and Long duration."""
        lc = StructuralLoadCase(
            name="LC_WIND",
            action_type=ActionType.VARIABLE,
            load_group="LG2",
            load_type="Wind",
            duration="Long",
        )

        assert lc.load_type == "Wind"
        assert lc.duration == "Long"

    def test_variable_with_all_duration_values(self) -> None:
        """Test that all valid duration values are accepted for Variable."""
        durations = ["Long", "Medium", "Short", "Instantaneous"]

        for duration in durations:
            lc = StructuralLoadCase(
                name="LC_TEST",
                action_type=ActionType.VARIABLE,
                load_group="LG2",
                load_type="Snow",
                duration=duration,
            )
            assert lc.duration == duration

    def test_variable_with_temperature(self) -> None:
        """Test variable load case with Temperature."""
        lc = StructuralLoadCase(
            name="LC_TEMP",
            action_type=ActionType.VARIABLE,
            load_group="LG2",
            load_type="Temperature",
            duration="Medium",
        )

        assert lc.load_type == "Temperature"

    def test_variable_with_maintenance(self) -> None:
        """Test variable load case with Maintenance."""
        lc = StructuralLoadCase(
            name="LC_MAINT",
            action_type=ActionType.VARIABLE,
            load_group="LG2",
            load_type="Maintenance",
            duration="Medium",
        )

        assert lc.load_type == "Maintenance"

    def test_accidental_with_fire(self) -> None:
        """Test accidental load case with Fire."""
        lc = StructuralLoadCase(
            name="LC_FIRE",
            action_type=ActionType.ACCIDENTAL,
            load_group="LG3",
            load_type="Fire",
        )

        assert lc.action_type == ActionType.ACCIDENTAL
        assert lc.load_type == "Fire"

    def test_accidental_with_seismic(self) -> None:
        """Test accidental load case with Seismic."""
        lc = StructuralLoadCase(
            name="LC_SEISMIC",
            action_type=ActionType.ACCIDENTAL,
            load_group="LG3",
            load_type="Seismic",
        )

        assert lc.load_type == "Seismic"

    def test_variable_all_load_types(self) -> None:
        """Test that all valid load types for Variable are accepted."""
        load_types = [
            "Others",
            "Dynamic",
            "Static",
            "Temperature",
            "Wind",
            "Snow",
            "Maintenance",
            "Fire",
            "Moving",
            "Seismic",
            "Standard",
        ]

        for load_type in load_types:
            lc = StructuralLoadCase(
                name="LC_TEST",
                action_type=ActionType.VARIABLE,
                load_group="LG2",
                load_type=load_type,
                duration="Medium",
            )
            assert lc.load_type == load_type

    # Validation Tests

    def test_variable_without_duration_raises_error(self) -> None:
        """Test that Variable load case without duration raises ValueError."""
        with pytest.raises(
            ValueError,
            match=r"duration must be specified when action_type = ActionType\.VARIABLE",
        ):
            StructuralLoadCase(
                name="LC_INVALID",
                action_type=ActionType.VARIABLE,
                load_group="LG2",
                load_type="Snow",
            )

    def test_permanent_with_invalid_load_type_raises_error(self) -> None:
        """Test that Permanent with invalid load_type raises ValueError."""
        with pytest.raises(
            ValueError,
            match=r"load_type 'InvalidType' is not valid for action_type = Permanent",
        ):
            StructuralLoadCase(
                name="LC_INVALID",
                action_type=ActionType.PERMANENT,
                load_group="LG1",
                load_type="InvalidType",
            )

    def test_variable_with_invalid_load_type_raises_error(self) -> None:
        """Test that Variable with invalid load_type raises ValueError."""
        with pytest.raises(
            ValueError,
            match=r"load_type 'InvalidType' is not valid for action_type = Variable",
        ):
            StructuralLoadCase(
                name="LC_INVALID",
                action_type=ActionType.VARIABLE,
                load_group="LG2",
                load_type="InvalidType",
                duration="Short",
            )

    def test_accidental_with_invalid_load_type_raises_error(self) -> None:
        """Test that Accidental with invalid load_type raises ValueError."""
        with pytest.raises(
            ValueError,
            match=r"load_type 'InvalidType' is not valid for action_type = Accidental",
        ):
            StructuralLoadCase(
                name="LC_INVALID",
                action_type=ActionType.ACCIDENTAL,
                load_group="LG3",
                load_type="InvalidType",
            )

    def test_invalid_duration_value_raises_error(self) -> None:
        """Test that invalid duration value raises ValueError."""
        with pytest.raises(
            ValueError,
            match=r"duration 'InvalidDuration' is not valid",
        ):
            StructuralLoadCase(
                name="LC_INVALID",
                action_type=ActionType.VARIABLE,
                load_group="LG2",
                load_type="Snow",
                duration="InvalidDuration",
            )

    def test_permanent_with_variable_load_type_raises_error(self) -> None:
        """Test that Permanent can't use Variable-only load type."""
        with pytest.raises(
            ValueError,
            match=r"load_type 'Snow' is not valid for action_type = Permanent",
        ):
            StructuralLoadCase(
                name="LC_INVALID",
                action_type=ActionType.PERMANENT,
                load_group="LG1",
                load_type="Snow",
            )

    def test_variable_with_permanent_only_load_type_raises_error(self) -> None:
        """Test that Variable can't use Permanent-only load type."""
        with pytest.raises(
            ValueError,
            match=r"load_type 'Self weight' is not valid for action_type = Variable",
        ):
            StructuralLoadCase(
                name="LC_INVALID",
                action_type=ActionType.VARIABLE,
                load_group="LG2",
                load_type="Self weight",
                duration="Short",
            )

    # Edge Cases and Additional Tests

    def test_description_optional(self) -> None:
        """Test that description is optional."""
        lc = StructuralLoadCase(
            name="LC1",
            action_type=ActionType.PERMANENT,
            load_group="LG1",
            load_type="Standard",
        )

        assert lc.description == ""

    def test_description_with_value(self) -> None:
        """Test that description can have a value."""
        lc = StructuralLoadCase(
            name="LC1",
            action_type=ActionType.VARIABLE,
            load_group="LG2",
            load_type="Snow",
            duration="Short",
            description="Offices - Cat.B",
        )

        assert lc.description == "Offices - Cat.B"

    def test_id_optional(self) -> None:
        """Test that id is optional."""
        lc = StructuralLoadCase(
            name="LC1",
            action_type=ActionType.PERMANENT,
            load_group="LG1",
            load_type="Standard",
        )

        assert lc.id == ""

    def test_id_with_uuid(self) -> None:
        """Test that id can have UUID value."""
        uuid = "550e8400-e29b-41d4-a716-446655440000"
        lc = StructuralLoadCase(
            name="LC1",
            action_type=ActionType.PERMANENT,
            load_group="LG1",
            load_type="Standard",
            id=uuid,
        )

        assert lc.id == uuid

    def test_permanent_with_duration_allowed(self) -> None:
        """Test that duration can be specified for Permanent (but not required)."""
        lc = StructuralLoadCase(
            name="LC1",
            action_type=ActionType.PERMANENT,
            load_group="LG1",
            load_type="Standard",
            duration="Long",
        )

        assert lc.duration == "Long"

    def test_load_group_as_string_reference(self) -> None:
        """Test that load_group is a string reference (not validated)."""
        lc = StructuralLoadCase(
            name="LC1",
            action_type=ActionType.PERMANENT,
            load_group="NONEXISTENT_GROUP",
            load_type="Standard",
        )

        assert lc.load_group == "NONEXISTENT_GROUP"

    def test_load_case_equality(self) -> None:
        """Test that two load cases with same values are equal."""
        lc1 = StructuralLoadCase(
            name="LC1",
            action_type=ActionType.PERMANENT,
            load_group="LG1",
            load_type="Standard",
        )
        lc2 = StructuralLoadCase(
            name="LC1",
            action_type=ActionType.PERMANENT,
            load_group="LG1",
            load_type="Standard",
        )

        assert lc1 == lc2

    def test_load_case_inequality(self) -> None:
        """Test that load cases with different values are not equal."""
        lc1 = StructuralLoadCase(
            name="LC1",
            action_type=ActionType.PERMANENT,
            load_group="LG1",
            load_type="Standard",
        )
        lc2 = StructuralLoadCase(
            name="LC2",
            action_type=ActionType.PERMANENT,
            load_group="LG1",
            load_type="Standard",
        )

        assert lc1 != lc2

    def test_load_case_hashable(self) -> None:
        """Test that load cases are hashable (can be used in sets/dicts)."""
        lc1 = StructuralLoadCase(
            name="LC1",
            action_type=ActionType.PERMANENT,
            load_group="LG1",
            load_type="Standard",
        )
        lc2 = StructuralLoadCase(
            name="LC1",
            action_type=ActionType.PERMANENT,
            load_group="LG1",
            load_type="Standard",
        )

        lc_set = {lc1, lc2}
        assert len(lc_set) == 1

    def test_load_case_frozen(self) -> None:
        """Test that load case is immutable (frozen)."""
        lc = StructuralLoadCase(
            name="LC1",
            action_type=ActionType.PERMANENT,
            load_group="LG1",
            load_type="Standard",
        )

        with pytest.raises(AttributeError):
            lc.name = "LC2"

    def test_accidental_all_load_types(self) -> None:
        """Test that all valid load types for Accidental are accepted."""
        load_types = [
            "Others",
            "Dynamic",
            "Static",
            "Temperature",
            "Wind",
            "Snow",
            "Maintenance",
            "Fire",
            "Moving",
            "Seismic",
            "Standard",
        ]

        for load_type in load_types:
            lc = StructuralLoadCase(
                name="LC_TEST",
                action_type=ActionType.ACCIDENTAL,
                load_group="LG3",
                load_type=load_type,
            )
            assert lc.load_type == load_type
