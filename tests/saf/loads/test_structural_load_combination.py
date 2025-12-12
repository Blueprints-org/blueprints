"""Tests for StructuralLoadCombination dataclass."""

import pytest

from blueprints.saf.loads.structural_load_combination import (
    Category,
    CombinationType,
    LoadCaseItem,
    NationalStandard,
    StructuralLoadCombination,
)


class TestLoadCaseItem:
    """Tests for LoadCaseItem NamedTuple."""

    def test_load_case_item_with_all_parameters(self) -> None:
        """Test LoadCaseItem creation with all parameters."""
        item = LoadCaseItem(load_case_name="LC1", load_factor=1.35, multiplier=0.9)

        assert item.load_case_name == "LC1"
        assert item.load_factor == 1.35
        assert item.multiplier == 0.9

    def test_load_case_item_with_default_factors(self) -> None:
        """Test LoadCaseItem creation with default factor values."""
        item = LoadCaseItem(load_case_name="LC1")

        assert item.load_case_name == "LC1"
        assert item.load_factor == 1.0
        assert item.multiplier == 1.0

    def test_load_case_item_immutability(self) -> None:
        """Test that LoadCaseItem is immutable."""
        item = LoadCaseItem(load_case_name="LC1")

        with pytest.raises(AttributeError):
            item.load_case_name = "LC2"


class TestStructuralLoadCombination:
    """Tests for StructuralLoadCombination dataclass."""

    # Valid Initialization Tests

    def test_uls_with_single_load_case(self) -> None:
        """Test ULS combination with single load case."""
        combo = StructuralLoadCombination(
            name="COM1",
            category=Category.ULS,
            load_cases=(LoadCaseItem("LC1", 1.35, 1.0),),
        )

        assert combo.name == "COM1"
        assert combo.category == Category.ULS
        assert len(combo.load_cases) == 1
        assert combo.national_standard is None

    def test_sls_with_multiple_load_cases(self) -> None:
        """Test SLS combination with multiple load cases."""
        combo = StructuralLoadCombination(
            name="COM2",
            category=Category.SLS,
            load_cases=(
                LoadCaseItem("LC1", 1.0, 1.0),
                LoadCaseItem("LC2", 1.0, 0.6),
            ),
        )

        assert combo.category == Category.SLS
        assert len(combo.load_cases) == 2

    def test_als_combination(self) -> None:
        """Test ALS (Accidental Limit State) combination."""
        combo = StructuralLoadCombination(
            name="COM3",
            category=Category.ALS,
            load_cases=(LoadCaseItem("LC_FIRE", 1.0, 1.0),),
        )

        assert combo.category == Category.ALS

    def test_not_defined_combination(self) -> None:
        """Test combination with Not defined category."""
        combo = StructuralLoadCombination(
            name="COM4",
            category=Category.NOT_DEFINED,
            load_cases=(LoadCaseItem("LC1", 1.0, 1.0),),
        )

        assert combo.category == Category.NOT_DEFINED

    def test_according_national_standard_with_en_standard(self) -> None:
        """Test According national standard with EN standard."""
        combo = StructuralLoadCombination(
            name="COM5",
            category=Category.ACCORDING_NATIONAL_STANDARD,
            load_cases=(LoadCaseItem("LC1", 1.35, 1.0),),
            national_standard=NationalStandard.EN_ULS_STR_GEO_SET_B,
        )

        assert combo.category == Category.ACCORDING_NATIONAL_STANDARD
        assert combo.national_standard == NationalStandard.EN_ULS_STR_GEO_SET_B

    def test_according_national_standard_with_ibc_standard(self) -> None:
        """Test According national standard with IBC standard."""
        combo = StructuralLoadCombination(
            name="COM6",
            category=Category.ACCORDING_NATIONAL_STANDARD,
            load_cases=(LoadCaseItem("LC1", 1.2, 1.0),),
            national_standard=NationalStandard.IBC_LRFD_ULTIMATE,
        )

        assert combo.national_standard == NationalStandard.IBC_LRFD_ULTIMATE

    def test_with_envelope_combination_type(self) -> None:
        """Test combination with Envelope type."""
        combo = StructuralLoadCombination(
            name="COM7",
            category=Category.ULS,
            load_cases=(LoadCaseItem("LC1", 1.35, 1.0),),
            combination_type=CombinationType.ENVELOPE,
        )

        assert combo.combination_type == CombinationType.ENVELOPE

    def test_with_linear_combination_type(self) -> None:
        """Test combination with Linear type."""
        combo = StructuralLoadCombination(
            name="COM8",
            category=Category.ULS,
            load_cases=(LoadCaseItem("LC1", 1.35, 1.0),),
            combination_type=CombinationType.LINEAR,
        )

        assert combo.combination_type == CombinationType.LINEAR

    def test_with_nonlinear_combination_type(self) -> None:
        """Test combination with Nonlinear type."""
        combo = StructuralLoadCombination(
            name="COM9",
            category=Category.ULS,
            load_cases=(LoadCaseItem("LC1", 1.35, 1.0),),
            combination_type=CombinationType.NONLINEAR,
        )

        assert combo.combination_type == CombinationType.NONLINEAR

    def test_with_description(self) -> None:
        """Test combination with description."""
        combo = StructuralLoadCombination(
            name="COM10",
            category=Category.ULS,
            load_cases=(LoadCaseItem("LC1", 1.35, 1.0),),
            description="Ultimate Limit State - Permanent + Variable",
        )

        assert combo.description == "Ultimate Limit State - Permanent + Variable"

    def test_with_uuid_id(self) -> None:
        """Test combination with UUID id."""
        uuid = "550e8400-e29b-41d4-a716-446655440000"
        combo = StructuralLoadCombination(
            name="COM11",
            category=Category.ULS,
            load_cases=(LoadCaseItem("LC1", 1.35, 1.0),),
            id=uuid,
        )

        assert combo.id == uuid

    def test_multiple_load_cases_with_different_factors(self) -> None:
        """Test combination with multiple load cases and varying factors."""
        combo = StructuralLoadCombination(
            name="COM12",
            category=Category.ULS,
            load_cases=(
                LoadCaseItem("LC_PERM", 1.35, 1.0),
                LoadCaseItem("LC_SNOW", 1.5, 0.0),
                LoadCaseItem("LC_WIND", 1.5, 0.6),
            ),
        )

        assert len(combo.load_cases) == 3
        assert combo.load_cases[0].load_factor == 1.35
        assert combo.load_cases[1].load_factor == 1.5
        assert combo.load_cases[2].multiplier == 0.6

    # Validation Tests

    def test_empty_load_cases_raises_error(self) -> None:
        """Test that empty load_cases raises ValueError."""
        with pytest.raises(ValueError, match=r"load_cases must contain at least one LoadCaseItem"):
            StructuralLoadCombination(
                name="COM_INVALID",
                category=Category.ULS,
                load_cases=(),
            )

    def test_load_case_with_empty_name_raises_error(self) -> None:
        """Test that load case with empty name raises ValueError."""
        with pytest.raises(ValueError, match=r"load_case_name at index 0 cannot be empty"):
            StructuralLoadCombination(
                name="COM_INVALID",
                category=Category.ULS,
                load_cases=(LoadCaseItem("", 1.35, 1.0),),
            )

    def test_according_national_standard_without_national_standard_raises_error(
        self,
    ) -> None:
        """Test that ACCORDING_NATIONAL_STANDARD without national_standard raises error."""
        with pytest.raises(
            ValueError,
            match=r"national_standard must be specified when category = Category.ACCORDING_NATIONAL_STANDARD",
        ):
            StructuralLoadCombination(
                name="COM_INVALID",
                category=Category.ACCORDING_NATIONAL_STANDARD,
                load_cases=(LoadCaseItem("LC1", 1.35, 1.0),),
            )

    def test_national_standard_with_uls_raises_error(self) -> None:
        """Test that national_standard with ULS category raises error."""
        with pytest.raises(
            ValueError,
            match=r"national_standard should only be specified when category = Category.ACCORDING_NATIONAL_STANDARD",
        ):
            StructuralLoadCombination(
                name="COM_INVALID",
                category=Category.ULS,
                load_cases=(LoadCaseItem("LC1", 1.35, 1.0),),
                national_standard=NationalStandard.EN_ULS_STR_GEO_SET_B,
            )

    def test_national_standard_with_sls_raises_error(self) -> None:
        """Test that national_standard with SLS category raises error."""
        with pytest.raises(
            ValueError,
            match=r"national_standard should only be specified when category = Category.ACCORDING_NATIONAL_STANDARD",
        ):
            StructuralLoadCombination(
                name="COM_INVALID",
                category=Category.SLS,
                load_cases=(LoadCaseItem("LC1", 1.0, 1.0),),
                national_standard=NationalStandard.EN_SLS_CHARACTERISTIC,
            )

    def test_national_standard_with_als_raises_error(self) -> None:
        """Test that national_standard with ALS category raises error."""
        with pytest.raises(
            ValueError,
            match=r"national_standard should only be specified when category = Category.ACCORDING_NATIONAL_STANDARD",
        ):
            StructuralLoadCombination(
                name="COM_INVALID",
                category=Category.ALS,
                load_cases=(LoadCaseItem("LC1", 1.0, 1.0),),
                national_standard=NationalStandard.EN_ACCIDENTAL_1,
            )

    def test_national_standard_with_not_defined_raises_error(self) -> None:
        """Test that national_standard with NOT_DEFINED category raises error."""
        with pytest.raises(
            ValueError,
            match=r"national_standard should only be specified when category = Category.ACCORDING_NATIONAL_STANDARD",
        ):
            StructuralLoadCombination(
                name="COM_INVALID",
                category=Category.NOT_DEFINED,
                load_cases=(LoadCaseItem("LC1", 1.0, 1.0),),
                national_standard=NationalStandard.IBC_LRFD_ULTIMATE,
            )

    def test_multiple_empty_load_case_names_detected(self) -> None:
        """Test detection of empty load case names in sequence."""
        with pytest.raises(ValueError, match=r"load_case_name at index 0 cannot be empty"):
            StructuralLoadCombination(
                name="COM_INVALID",
                category=Category.ULS,
                load_cases=(
                    LoadCaseItem("", 1.35, 1.0),
                    LoadCaseItem("LC2", 1.5, 1.0),
                ),
            )

    # Edge Cases and Properties

    def test_combination_equality(self) -> None:
        """Test that two combinations with same values are equal."""
        combo1 = StructuralLoadCombination(
            name="COM1",
            category=Category.ULS,
            load_cases=(LoadCaseItem("LC1", 1.35, 1.0),),
        )
        combo2 = StructuralLoadCombination(
            name="COM1",
            category=Category.ULS,
            load_cases=(LoadCaseItem("LC1", 1.35, 1.0),),
        )

        assert combo1 == combo2

    def test_combination_inequality(self) -> None:
        """Test that combinations with different values are not equal."""
        combo1 = StructuralLoadCombination(
            name="COM1",
            category=Category.ULS,
            load_cases=(LoadCaseItem("LC1", 1.35, 1.0),),
        )
        combo2 = StructuralLoadCombination(
            name="COM2",
            category=Category.ULS,
            load_cases=(LoadCaseItem("LC1", 1.35, 1.0),),
        )

        assert combo1 != combo2

    def test_combination_hashable(self) -> None:
        """Test that combinations are hashable (can be used in sets/dicts)."""
        combo1 = StructuralLoadCombination(
            name="COM1",
            category=Category.ULS,
            load_cases=(LoadCaseItem("LC1", 1.35, 1.0),),
        )
        combo2 = StructuralLoadCombination(
            name="COM1",
            category=Category.ULS,
            load_cases=(LoadCaseItem("LC1", 1.35, 1.0),),
        )

        combo_set = {combo1, combo2}
        assert len(combo_set) == 1

    def test_combination_frozen(self) -> None:
        """Test that combination is immutable (frozen)."""
        combo = StructuralLoadCombination(
            name="COM1",
            category=Category.ULS,
            load_cases=(LoadCaseItem("LC1", 1.35, 1.0),),
        )

        with pytest.raises(AttributeError):
            combo.name = "COM2"

    def test_description_optional(self) -> None:
        """Test that description is optional."""
        combo = StructuralLoadCombination(
            name="COM1",
            category=Category.ULS,
            load_cases=(LoadCaseItem("LC1", 1.35, 1.0),),
        )

        assert combo.description == ""

    def test_id_optional(self) -> None:
        """Test that id is optional."""
        combo = StructuralLoadCombination(
            name="COM1",
            category=Category.ULS,
            load_cases=(LoadCaseItem("LC1", 1.35, 1.0),),
        )

        assert combo.id == ""

    def test_combination_type_optional(self) -> None:
        """Test that combination_type is optional."""
        combo = StructuralLoadCombination(
            name="COM1",
            category=Category.ULS,
            load_cases=(LoadCaseItem("LC1", 1.35, 1.0),),
        )

        assert combo.combination_type is None

    def test_national_standard_optional_for_uls(self) -> None:
        """Test that national_standard is optional for ULS category."""
        combo = StructuralLoadCombination(
            name="COM1",
            category=Category.ULS,
            load_cases=(LoadCaseItem("LC1", 1.35, 1.0),),
        )

        assert combo.national_standard is None

    # National Standard Coverage Tests

    def test_all_en_national_standards_accepted(self) -> None:
        """Test that all EN national standards are accepted."""
        en_standards = [
            NationalStandard.EN_ULS_STR_GEO_SET_B,
            NationalStandard.EN_ULS_STR_GEO_SET_C,
            NationalStandard.EN_ACCIDENTAL_1,
            NationalStandard.EN_ACCIDENTAL_2,
            NationalStandard.EN_SEISMIC,
            NationalStandard.EN_SLS_CHARACTERISTIC,
            NationalStandard.EN_SLS_FREQUENT,
            NationalStandard.EN_SLS_QUASI_PERMANENT,
        ]

        for standard in en_standards:
            combo = StructuralLoadCombination(
                name="COM_TEST",
                category=Category.ACCORDING_NATIONAL_STANDARD,
                load_cases=(LoadCaseItem("LC1", 1.35, 1.0),),
                national_standard=standard,
            )
            assert combo.national_standard == standard

    def test_all_ibc_national_standards_accepted(self) -> None:
        """Test that all IBC national standards are accepted."""
        ibc_standards = [
            NationalStandard.IBC_LRFD_ULTIMATE,
            NationalStandard.IBC_ASD_ULTIMATE,
            NationalStandard.IBC_ASD_SERVICEABILITY,
            NationalStandard.IBC_ASD_SEISMIC,
            NationalStandard.IBC_LRFD_SEISMIC,
        ]

        for standard in ibc_standards:
            combo = StructuralLoadCombination(
                name="COM_TEST",
                category=Category.ACCORDING_NATIONAL_STANDARD,
                load_cases=(LoadCaseItem("LC1", 1.35, 1.0),),
                national_standard=standard,
            )
            assert combo.national_standard == standard

    def test_all_category_values(self) -> None:
        """Test that all Category enum values are accepted."""
        categories_without_national_standard = [
            Category.ULS,
            Category.SLS,
            Category.ALS,
            Category.NOT_DEFINED,
        ]

        for category in categories_without_national_standard:
            combo = StructuralLoadCombination(
                name="COM_TEST",
                category=category,
                load_cases=(LoadCaseItem("LC1", 1.35, 1.0),),
            )
            assert combo.category == category

    def test_all_combination_type_values(self) -> None:
        """Test that all CombinationType enum values are accepted."""
        for combo_type in CombinationType:
            combo = StructuralLoadCombination(
                name="COM_TEST",
                category=Category.ULS,
                load_cases=(LoadCaseItem("LC1", 1.35, 1.0),),
                combination_type=combo_type,
            )
            assert combo.combination_type == combo_type

    def test_many_load_cases(self) -> None:
        """Test combination with many load cases (testing scalability)."""
        load_cases = tuple(LoadCaseItem(f"LC{i}", 1.0, 1.0) for i in range(1, 11))
        combo = StructuralLoadCombination(
            name="COM_MANY",
            category=Category.ULS,
            load_cases=load_cases,
        )

        assert len(combo.load_cases) == 10

    def test_load_cases_with_zero_factors(self) -> None:
        """Test load cases with zero factors (e.g., for envelope analysis)."""
        combo = StructuralLoadCombination(
            name="COM_ZERO",
            category=Category.ULS,
            load_cases=(
                LoadCaseItem("LC1", 1.35, 1.0),
                LoadCaseItem("LC2", 0.0, 1.0),
            ),
        )

        assert combo.load_cases[1].load_factor == 0.0

    def test_load_cases_with_fractional_factors(self) -> None:
        """Test load cases with fractional multipliers."""
        combo = StructuralLoadCombination(
            name="COM_FRAC",
            category=Category.ULS,
            load_cases=(
                LoadCaseItem("LC1", 1.35, 1.0),
                LoadCaseItem("LC2", 1.5, 0.7),
                LoadCaseItem("LC3", 1.5, 0.5),
            ),
        )

        assert combo.load_cases[1].multiplier == 0.7
        assert combo.load_cases[2].multiplier == 0.5
