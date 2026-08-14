"""Tests for report_helpers.py helpers."""

import pytest

from blueprints.checks.check_result import CheckResult
from blueprints.utils.report import Report, report_helpers


@pytest.fixture
def fixture_report() -> Report:
    """Fixture for a real Report instance."""
    return Report()


def test_add_applied_documents(fixture_report: Report) -> None:
    """Test add_applied_documents helper."""
    docs = ["EN 1993-1-1", "EN 1990"]
    report_helpers.add_applied_documents(fixture_report, docs)
    content = fixture_report.content
    assert "Applied code documents" in content
    assert "The following documents were applied" in content
    for doc in docs:
        assert str(doc) in content


def test_add_applied_forces(fixture_report: Report) -> None:
    """Test add_applied_forces helper."""

    class DummyForces:
        n = 100.1234
        vy = 50.5678
        vz = 25.4321
        mx = 10.0
        my = 5.0
        mz = 1.0

    forces = DummyForces()
    report_helpers.add_applied_forces(fixture_report, forces, n=1)
    content = fixture_report.content
    assert "internal forces" in content.lower()
    assert "internal forces were applied" in content
    assert "Internal Force" in content
    assert "Normal force" in content
    assert "100.1" in content


def test_add_material_steel_info(fixture_report: Report) -> None:
    """Test add_material_steel_info helper."""

    class DummyMat:
        name = "S355"
        e_modulus = 210000

    class DummySteel:
        material = DummyMat()
        yield_strength = 355.5
        ultimate_strength = 510.2

    steel = DummySteel()
    report_helpers.add_material_steel_info(fixture_report, steel, n=0)
    content = fixture_report.content
    assert "material" in content.lower()
    assert "material properties" in content
    assert "Material" in content
    assert "S355" in content
    assert "Yield Strength" in content
    assert "356 MPa" in content
    assert "Elastic Modulus" in content
    assert "210000 MPa" in content


def test_add_section_properties_with_profile(fixture_report: Report) -> None:
    """Test add_section_properties with profile."""

    class DummySection:
        area = 123.456
        perimeter = 42.0

    class DummyProfile:
        name = "IPE 200"

    section = DummySection()
    profile = DummyProfile()
    report_helpers.add_section_properties(fixture_report, section, profile=profile, n=1, properties=["area", "perimeter", "not_existing"])
    content = fixture_report.content
    assert "section properties" in content
    assert "Profile" in content
    assert "IPE 200" in content
    assert "Area" in content
    assert "123.5" in content
    assert "Perimeter" in content
    assert "42.0" in content
    assert "Not_existing" in content
    assert "Not calculated" in content


def test_add_section_properties_without_profile(fixture_report: Report) -> None:
    """Test add_section_properties without profile."""

    class DummySection:
        area = 10.0

    section = DummySection()
    report_helpers.add_section_properties(fixture_report, section, profile=None, n=2, properties=["area"])
    content = fixture_report.content
    assert "Area" in content
    assert "10.00" in content


def test_add_unity_check_summary(fixture_report: Report) -> None:
    """Test add_unity_check_summary helper."""

    class DummyResult:
        def __init__(self, uc: float, ok: bool) -> None:
            self.unity_check = uc
            self.is_ok = ok

    class DummyCheck:
        def __init__(self, uc: float, ok: bool) -> None:
            self._res = DummyResult(uc, ok)

        def result(self) -> "DummyResult":
            return self._res

    checks = {
        "bending": DummyCheck(0.95, True),
        "shear": DummyCheck(1.05, False),
        "none": None,
        "check_result": CheckResult(is_ok=True),
    }
    report_helpers.add_unity_check_summary(report=fixture_report, calculations=checks, n=2)
    content = fixture_report.content
    assert "utilization" in content.lower()
    assert "Check" in content
    assert "Utilization" in content
    assert "Status" in content
    assert "Bending" in content
    assert "0.95" in content
    assert "OK" in content
    assert "Shear" in content
    assert "1.05" in content
    assert "NOT OK" in content
    assert "Overall result: NOT OK" in content


def test_add_unity_check_summary_empty(fixture_report: Report) -> None:
    """Test add_unity_check_summary with empty input."""
    report_helpers.add_unity_check_summary(fixture_report, {}, n=2)
    content = fixture_report.content
    assert "No checks were performed" in content
