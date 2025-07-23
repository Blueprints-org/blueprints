"""Tests for the ABCEnumMeta class."""
import importlib
import pkgutil
from abc import ABCMeta, abstractmethod
from enum import Enum, EnumMeta
from types import ModuleType

import pytest

from blueprints.utils.abc_enum_meta import ABCEnumMeta


def get_first_submodule(package):
    """Returns the first submodule if the input is a package."""
    if not hasattr(package, '__path__'):
        print(f"⚠️ {package.__name__} is not a package, stopping here.")
        return None  # Not a package
    submodules = list(pkgutil.iter_modules(package.__path__))
    if not submodules:
        print(f"⚠️ {package.__name__} has no submodules.")
        return None
    first = sorted(submodules, key=lambda x: x.name)[0]
    full_name = f"{package.__name__}.{first.name}"
    return importlib.import_module(full_name)


class TestLazyImporting:
    """Test class for ABCEnumMeta."""

    def test_eurocode_skip(self) -> None:
        """Test if imports are properly working when the eurocode module is skipped"""
        import blueprints.codes.eurocode.en_1992_2_2005 as en
        assert en is not None
        import blueprints.codes.en_1992_2_2005 as en2
        assert en == en2

    def test_norm_items(self) -> None:
        """From all norms, test the inputs of at least 1 (edgecase) formula, to ensure the nen/__init__ works"""

        # Normal import
        import blueprints.codes.eurocode.en_1992_1_1_2004 as en
        from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_3_materials.formula_3_1 import (
            Form3Dot1EstimationConcreteCompressiveStrength
        )
        assert en.Form3Dot1EstimationConcreteCompressiveStrength == Form3Dot1EstimationConcreteCompressiveStrength

        # Import table and import with n
        assert en.Form4Dot4nCheckExecutionTolerances is not None

        # Import with large dot number
        import blueprints.codes.eurocode.en_1992_2_2005 as en
        assert en.Form5Dot101Imperfections is not None

        # Normal import
        import blueprints.codes.eurocode.en_1993_1_1_2005 as en
        assert en.Form6Dot23CheckTorsionalMoment is not None

        # Normal import
        import blueprints.codes.eurocode.en_1993_1_8_2005 as en
        assert en.Form4Dot2CheckWeldedConnection is not None

        # Import annex form
        print("THIS SHOULD TRIGGER D")
        import blueprints.codes.eurocode.en_1993_1_9_2005 as en
        assert en.FormADot1DamageDuringDesignLife is not None

        # Normal import
        import blueprints.codes.eurocode.en_1993_5_2007 as en
        assert en.Form5Dot20ReducedMomentResistanceClass2ZProfiles is not None

        # Normal import
        import blueprints.codes.eurocode.en_1995_1_1_2004 as en
        assert en.Form7Dot5NaturalFrequency is not None

        # Import with b
        import blueprints.codes.eurocode.nen_9997_1_c2_2017 as en
        assert en.Form2Dot1bRepresentativeValue is not None

        # Normal import
        import blueprints.codes.eurocode.nen_en_1992_1_1_a1_2020 as en
        assert en.Form8Dot14EquivalentDiameterBundledBars is not None

    def test_lazy_import_errors(self) -> None:
        """Test if lazy importing raises the right errors."""

        # Calculate attribute error when poorly importing
        with pytest.raises(AttributeError):
            import blueprints.codes.eurocode.en_1992_1_1_2004 as en
            en.NotAForm(1, 1)

        with pytest.raises(AttributeError):
            import blueprints.codes.eurocode.en_1992_1_1_2004 as en
            en.Form999Dot999NonExistingFunction(1, 1)

        with pytest.raises(AttributeError):
            import blueprints.codes.eurocode.en_1992_1_1_2004 as en
            en.Form1Dothello_world(1, 1)

        with pytest.raises(AttributeError):
            import blueprints.codes.eurocode.en_1992_1_1_2004 as en
            en.Table3Dot123abcMyClass(1, 1)


