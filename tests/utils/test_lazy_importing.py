"""Tests for lazy importing functionality."""

import pytest


class TestLazyImporting:
    """Test class for Lazy Importing."""

    def test_import_errors(self) -> None:
        """Test what happens when a module is not found."""
        with pytest.raises(ModuleNotFoundError):
            import blueprints.codes.eurocode.non_existing_module as non_existing  # noqa: F401

        with pytest.raises(ModuleNotFoundError):
            import blueprints.codes.non_existing_module as non_existing2  # noqa: F401

    def test_norm_items(self) -> None:
        """From all norms, test the inputs of at least 1 (edgecase) formula, to ensure the nen/__init__ works."""
        # Normal import
        import blueprints.codes.eurocode.en_1992_1_1_2004 as en
        from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_3_materials.formula_3_1 import Form3Dot1EstimationConcreteCompressiveStrength

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
        import blueprints.codes.eurocode.en_1992_1_1_2004 as en

        with pytest.raises(AttributeError):
            en.NotAForm(1, 1)

        import blueprints.codes.eurocode.en_1992_1_1_2004 as en

        with pytest.raises(AttributeError):
            en.Form999Dot999NonExistingFunction(1, 1)

        import blueprints.codes.eurocode.en_1992_1_1_2004 as en

        with pytest.raises(AttributeError):
            en.Form1Dothello_world(1, 1)

        import blueprints.codes.eurocode.en_1992_1_1_2004 as en

        with pytest.raises(AttributeError):
            en.Table3Dot123abcMyClass(1, 1)
