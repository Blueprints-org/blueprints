"""Tests for StructuralPointSupportDeformation class."""

import pytest

from blueprints.saf import StructuralPointSupportDeformation
from blueprints.saf.loads.structural_point_support_deformation import Direction


class TestStructuralPointSupportDeformationValidInitialization:
    """Test valid initialization of StructuralPointSupportDeformation."""

    def test_basic_x_translation(self) -> None:
        """Test basic X direction translation deformation."""
        deform = StructuralPointSupportDeformation(
            name="RS1",
            point_support="Sn6",
            direction=Direction.X,
            load_case="LC5",
            translation_value=10.0,
        )
        assert deform.name == "RS1"
        assert deform.point_support == "Sn6"
        assert deform.direction == Direction.X
        assert deform.load_case == "LC5"
        assert deform.translation_value == 10.0

    def test_y_translation_with_optional_id(self) -> None:
        """Test Y direction translation with optional id."""
        deform = StructuralPointSupportDeformation(
            name="RS2",
            point_support="Sn7",
            direction=Direction.Y,
            load_case="LC5",
            translation_value=15.5,
            id="uuid-1234",
        )
        assert deform.direction == Direction.Y
        assert deform.translation_value == 15.5
        assert deform.id == "uuid-1234"

    def test_z_translation(self) -> None:
        """Test Z direction translation deformation."""
        deform = StructuralPointSupportDeformation(
            name="RS3",
            point_support="Sn8",
            direction=Direction.Z,
            load_case="LC6",
            translation_value=-5.0,
        )
        assert deform.direction == Direction.Z
        assert deform.translation_value == -5.0

    def test_rx_rotation(self) -> None:
        """Test Rx direction rotation deformation."""
        deform = StructuralPointSupportDeformation(
            name="RS4",
            point_support="Sn9",
            direction=Direction.RX,
            load_case="LC5",
            rotation_value=3.5,
        )
        assert deform.direction == Direction.RX
        assert deform.rotation_value == 3.5

    def test_ry_rotation(self) -> None:
        """Test Ry direction rotation deformation."""
        deform = StructuralPointSupportDeformation(
            name="RS5",
            point_support="Sn10",
            direction=Direction.RY,
            load_case="LC5",
            rotation_value=5.0,
        )
        assert deform.direction == Direction.RY
        assert deform.rotation_value == 5.0

    def test_rz_rotation(self) -> None:
        """Test Rz direction rotation deformation."""
        deform = StructuralPointSupportDeformation(
            name="RS6",
            point_support="Sn11",
            direction=Direction.RZ,
            load_case="LC7",
            rotation_value=2.5,
        )
        assert deform.direction == Direction.RZ
        assert deform.rotation_value == 2.5

    def test_positive_translation_value(self) -> None:
        """Test with positive translation value."""
        deform = StructuralPointSupportDeformation(
            name="RS1",
            point_support="Sn6",
            direction=Direction.X,
            load_case="LC5",
            translation_value=25.0,
        )
        assert deform.translation_value == 25.0

    def test_negative_translation_value(self) -> None:
        """Test with negative translation value."""
        deform = StructuralPointSupportDeformation(
            name="RS1",
            point_support="Sn6",
            direction=Direction.X,
            load_case="LC5",
            translation_value=-15.0,
        )
        assert deform.translation_value == -15.0

    def test_zero_translation_value(self) -> None:
        """Test with zero translation value."""
        deform = StructuralPointSupportDeformation(
            name="RS1",
            point_support="Sn6",
            direction=Direction.X,
            load_case="LC5",
            translation_value=0.0,
        )
        assert deform.translation_value == 0.0

    def test_positive_rotation_value(self) -> None:
        """Test with positive rotation value."""
        deform = StructuralPointSupportDeformation(
            name="RS4",
            point_support="Sn9",
            direction=Direction.RX,
            load_case="LC5",
            rotation_value=10.0,
        )
        assert deform.rotation_value == 10.0

    def test_negative_rotation_value(self) -> None:
        """Test with negative rotation value."""
        deform = StructuralPointSupportDeformation(
            name="RS4",
            point_support="Sn9",
            direction=Direction.RX,
            load_case="LC5",
            rotation_value=-3.5,
        )
        assert deform.rotation_value == -3.5

    def test_zero_rotation_value(self) -> None:
        """Test with zero rotation value."""
        deform = StructuralPointSupportDeformation(
            name="RS4",
            point_support="Sn9",
            direction=Direction.RX,
            load_case="LC5",
            rotation_value=0.0,
        )
        assert deform.rotation_value == 0.0

    def test_decimal_translation_value(self) -> None:
        """Test with decimal translation value."""
        deform = StructuralPointSupportDeformation(
            name="RS1",
            point_support="Sn6",
            direction=Direction.X,
            load_case="LC5",
            translation_value=7.5,
        )
        assert deform.translation_value == 7.5

    def test_decimal_rotation_value(self) -> None:
        """Test with decimal rotation value."""
        deform = StructuralPointSupportDeformation(
            name="RS4",
            point_support="Sn9",
            direction=Direction.RX,
            load_case="LC5",
            rotation_value=2.75,
        )
        assert deform.rotation_value == 2.75

    def test_very_small_translation(self) -> None:
        """Test with very small translation value."""
        deform = StructuralPointSupportDeformation(
            name="RS1",
            point_support="Sn6",
            direction=Direction.Y,
            load_case="LC5",
            translation_value=0.001,
        )
        assert deform.translation_value == 0.001

    def test_very_small_rotation(self) -> None:
        """Test with very small rotation value."""
        deform = StructuralPointSupportDeformation(
            name="RS5",
            point_support="Sn10",
            direction=Direction.RY,
            load_case="LC5",
            rotation_value=0.0001,
        )
        assert deform.rotation_value == 0.0001


class TestStructuralPointSupportDeformationValidation:
    """Test validation of StructuralPointSupportDeformation."""

    def test_x_direction_without_translation_value_raises_error(self) -> None:
        """Test that X direction without translation_value raises ValueError."""
        with pytest.raises(
            ValueError,
            match="translation_value must be specified when direction = X",
        ):
            StructuralPointSupportDeformation(
                name="RS1",
                point_support="Sn6",
                direction=Direction.X,
                load_case="LC5",
            )

    def test_y_direction_without_translation_value_raises_error(self) -> None:
        """Test that Y direction without translation_value raises ValueError."""
        with pytest.raises(
            ValueError,
            match="translation_value must be specified when direction = Y",
        ):
            StructuralPointSupportDeformation(
                name="RS2",
                point_support="Sn7",
                direction=Direction.Y,
                load_case="LC5",
            )

    def test_z_direction_without_translation_value_raises_error(self) -> None:
        """Test that Z direction without translation_value raises ValueError."""
        with pytest.raises(
            ValueError,
            match="translation_value must be specified when direction = Z",
        ):
            StructuralPointSupportDeformation(
                name="RS3",
                point_support="Sn8",
                direction=Direction.Z,
                load_case="LC6",
            )

    def test_rx_direction_without_rotation_value_raises_error(self) -> None:
        """Test that Rx direction without rotation_value raises ValueError."""
        with pytest.raises(
            ValueError,
            match="rotation_value must be specified when direction = Rx",
        ):
            StructuralPointSupportDeformation(
                name="RS4",
                point_support="Sn9",
                direction=Direction.RX,
                load_case="LC5",
            )

    def test_ry_direction_without_rotation_value_raises_error(self) -> None:
        """Test that Ry direction without rotation_value raises ValueError."""
        with pytest.raises(
            ValueError,
            match="rotation_value must be specified when direction = Ry",
        ):
            StructuralPointSupportDeformation(
                name="RS5",
                point_support="Sn10",
                direction=Direction.RY,
                load_case="LC5",
            )

    def test_rz_direction_without_rotation_value_raises_error(self) -> None:
        """Test that Rz direction without rotation_value raises ValueError."""
        with pytest.raises(
            ValueError,
            match="rotation_value must be specified when direction = Rz",
        ):
            StructuralPointSupportDeformation(
                name="RS6",
                point_support="Sn11",
                direction=Direction.RZ,
                load_case="LC7",
            )

    def test_x_direction_with_rotation_value_raises_error(self) -> None:
        """Test that X direction with rotation_value raises ValueError."""
        with pytest.raises(
            ValueError,
            match="rotation_value should not be specified when direction = X",
        ):
            StructuralPointSupportDeformation(
                name="RS1",
                point_support="Sn6",
                direction=Direction.X,
                load_case="LC5",
                translation_value=10.0,
                rotation_value=5.0,
            )

    def test_y_direction_with_rotation_value_raises_error(self) -> None:
        """Test that Y direction with rotation_value raises ValueError."""
        with pytest.raises(
            ValueError,
            match="rotation_value should not be specified when direction = Y",
        ):
            StructuralPointSupportDeformation(
                name="RS2",
                point_support="Sn7",
                direction=Direction.Y,
                load_case="LC5",
                translation_value=15.0,
                rotation_value=3.0,
            )

    def test_z_direction_with_rotation_value_raises_error(self) -> None:
        """Test that Z direction with rotation_value raises ValueError."""
        with pytest.raises(
            ValueError,
            match="rotation_value should not be specified when direction = Z",
        ):
            StructuralPointSupportDeformation(
                name="RS3",
                point_support="Sn8",
                direction=Direction.Z,
                load_case="LC6",
                translation_value=20.0,
                rotation_value=2.0,
            )

    def test_rx_direction_with_translation_value_raises_error(self) -> None:
        """Test that Rx direction with translation_value raises ValueError."""
        with pytest.raises(
            ValueError,
            match="translation_value should not be specified when direction = Rx",
        ):
            StructuralPointSupportDeformation(
                name="RS4",
                point_support="Sn9",
                direction=Direction.RX,
                load_case="LC5",
                translation_value=10.0,
                rotation_value=3.5,
            )

    def test_ry_direction_with_translation_value_raises_error(self) -> None:
        """Test that Ry direction with translation_value raises ValueError."""
        with pytest.raises(
            ValueError,
            match="translation_value should not be specified when direction = Ry",
        ):
            StructuralPointSupportDeformation(
                name="RS5",
                point_support="Sn10",
                direction=Direction.RY,
                load_case="LC5",
                translation_value=15.0,
                rotation_value=5.0,
            )

    def test_rz_direction_with_translation_value_raises_error(self) -> None:
        """Test that Rz direction with translation_value raises ValueError."""
        with pytest.raises(
            ValueError,
            match="translation_value should not be specified when direction = Rz",
        ):
            StructuralPointSupportDeformation(
                name="RS6",
                point_support="Sn11",
                direction=Direction.RZ,
                load_case="LC7",
                translation_value=8.0,
                rotation_value=2.5,
            )


class TestStructuralPointSupportDeformationEnums:
    """Test enum values and functionality."""

    def test_direction_translation_enum_values(self) -> None:
        """Test translation Direction enum values."""
        assert Direction.X.value == "X"
        assert Direction.Y.value == "Y"
        assert Direction.Z.value == "Z"

    def test_direction_rotation_enum_values(self) -> None:
        """Test rotation Direction enum values."""
        assert Direction.RX.value == "Rx"
        assert Direction.RY.value == "Ry"
        assert Direction.RZ.value == "Rz"


class TestStructuralPointSupportDeformationImmutability:
    """Test immutability of StructuralPointSupportDeformation."""

    def test_frozen_dataclass(self) -> None:
        """Test that instances are frozen and immutable."""
        deform = StructuralPointSupportDeformation(
            name="RS1",
            point_support="Sn6",
            direction=Direction.X,
            load_case="LC5",
            translation_value=10.0,
        )
        with pytest.raises(AttributeError):
            deform.name = "RS2"  # type: ignore

    def test_hash_support(self) -> None:
        """Test that frozen instances are hashable."""
        deform1 = StructuralPointSupportDeformation(
            name="RS1",
            point_support="Sn6",
            direction=Direction.X,
            load_case="LC5",
            translation_value=10.0,
        )
        deform_dict = {deform1: "first"}
        assert deform_dict[deform1] == "first"


class TestStructuralPointSupportDeformationEquality:
    """Test equality comparison of StructuralPointSupportDeformation."""

    def test_equal_translation_instances(self) -> None:
        """Test that identical translation instances are equal."""
        deform1 = StructuralPointSupportDeformation(
            name="RS1",
            point_support="Sn6",
            direction=Direction.X,
            load_case="LC5",
            translation_value=10.0,
        )
        deform2 = StructuralPointSupportDeformation(
            name="RS1",
            point_support="Sn6",
            direction=Direction.X,
            load_case="LC5",
            translation_value=10.0,
        )
        assert deform1 == deform2

    def test_equal_rotation_instances(self) -> None:
        """Test that identical rotation instances are equal."""
        deform1 = StructuralPointSupportDeformation(
            name="RS4",
            point_support="Sn9",
            direction=Direction.RX,
            load_case="LC5",
            rotation_value=3.5,
        )
        deform2 = StructuralPointSupportDeformation(
            name="RS4",
            point_support="Sn9",
            direction=Direction.RX,
            load_case="LC5",
            rotation_value=3.5,
        )
        assert deform1 == deform2

    def test_unequal_instances_different_name(self) -> None:
        """Test that instances with different names are not equal."""
        deform1 = StructuralPointSupportDeformation(
            name="RS1",
            point_support="Sn6",
            direction=Direction.X,
            load_case="LC5",
            translation_value=10.0,
        )
        deform2 = StructuralPointSupportDeformation(
            name="RS2",
            point_support="Sn6",
            direction=Direction.X,
            load_case="LC5",
            translation_value=10.0,
        )
        assert deform1 != deform2

    def test_unequal_instances_different_direction(self) -> None:
        """Test that instances with different directions are not equal."""
        deform1 = StructuralPointSupportDeformation(
            name="RS1",
            point_support="Sn6",
            direction=Direction.X,
            load_case="LC5",
            translation_value=10.0,
        )
        deform2 = StructuralPointSupportDeformation(
            name="RS1",
            point_support="Sn6",
            direction=Direction.Y,
            load_case="LC5",
            translation_value=10.0,
        )
        assert deform1 != deform2

    def test_unequal_instances_different_value(self) -> None:
        """Test that instances with different values are not equal."""
        deform1 = StructuralPointSupportDeformation(
            name="RS1",
            point_support="Sn6",
            direction=Direction.X,
            load_case="LC5",
            translation_value=10.0,
        )
        deform2 = StructuralPointSupportDeformation(
            name="RS1",
            point_support="Sn6",
            direction=Direction.X,
            load_case="LC5",
            translation_value=15.0,
        )
        assert deform1 != deform2


class TestStructuralPointSupportDeformationEdgeCases:
    """Test edge cases and special scenarios."""

    def test_large_translation_value(self) -> None:
        """Test with large translation value."""
        deform = StructuralPointSupportDeformation(
            name="RS1",
            point_support="Sn6",
            direction=Direction.Z,
            load_case="LC5",
            translation_value=1000.0,
        )
        assert deform.translation_value == 1000.0

    def test_large_rotation_value(self) -> None:
        """Test with large rotation value."""
        deform = StructuralPointSupportDeformation(
            name="RS4",
            point_support="Sn9",
            direction=Direction.RX,
            load_case="LC5",
            rotation_value=100.0,
        )
        assert deform.rotation_value == 100.0

    def test_empty_id_default(self) -> None:
        """Test that empty id is default."""
        deform = StructuralPointSupportDeformation(
            name="RS1",
            point_support="Sn6",
            direction=Direction.X,
            load_case="LC5",
            translation_value=10.0,
        )
        assert deform.id == ""

    def test_all_translation_directions(self) -> None:
        """Test that all translation directions work."""
        for direction in [Direction.X, Direction.Y, Direction.Z]:
            deform = StructuralPointSupportDeformation(
                name="RS1",
                point_support="Sn6",
                direction=direction,
                load_case="LC5",
                translation_value=10.0,
            )
            assert deform.direction == direction

    def test_all_rotation_directions(self) -> None:
        """Test that all rotation directions work."""
        for direction in [Direction.RX, Direction.RY, Direction.RZ]:
            deform = StructuralPointSupportDeformation(
                name="RS4",
                point_support="Sn9",
                direction=direction,
                load_case="LC5",
                rotation_value=5.0,
            )
            assert deform.direction == direction

    def test_scientific_notation_translation(self) -> None:
        """Test with translation value in scientific notation."""
        deform = StructuralPointSupportDeformation(
            name="RS1",
            point_support="Sn6",
            direction=Direction.X,
            load_case="LC5",
            translation_value=1e-3,
        )
        assert deform.translation_value == 0.001

    def test_scientific_notation_rotation(self) -> None:
        """Test with rotation value in scientific notation."""
        deform = StructuralPointSupportDeformation(
            name="RS4",
            point_support="Sn9",
            direction=Direction.RX,
            load_case="LC5",
            rotation_value=1e-2,
        )
        assert deform.rotation_value == 0.01
