"""Tests for the Blueprints CLI module."""

import importlib
import os
import subprocess
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from blueprints import cli

PROJECT_ROOT = Path(__file__).parent.parent


@pytest.mark.parametrize(
    "command",
    [
        "install",
        "lint",
        "formatting",
        "typecheck",
        "test",
        "check",
        "docs",
    ],
)
def test_cli_command_exists(command: str) -> None:
    """Test that all expected commands are available."""
    result = subprocess.run(
        args=[sys.executable, "-m", "blueprints.cli", command, "--help"],
        check=False,
        capture_output=True,
        text=True,
        cwd=PROJECT_ROOT,
        env=os.environ.copy(),
    )

    # Should show help, not "No such command"
    assert result.returncode == 0
    assert "No such command" not in result.stderr
    assert "Error" not in result.stderr or "Usage:" in result.stdout


def test_cli_can_be_imported() -> None:
    """Test that CLI module can be imported."""
    assert cli.app is not None


def test_cli_import_error_handling() -> None:
    """Test CLI behavior when typer is not available.

    This test verifies the import error message when dependencies are missing.
    """
    # Save original modules
    original_typer = sys.modules.pop("typer", None)
    original_rich = sys.modules.pop("rich", None)
    original_cli = sys.modules.pop("blueprints.cli", None)

    try:
        # Make typer unavailable
        sys.modules["typer"] = None

        # Try to import the cli module - should raise SystemExit
        with pytest.raises(SystemExit) as exc_info:
            importlib.import_module("blueprints.cli")

        assert exc_info.value.code == 1

    finally:
        # Restore original modules
        if original_typer is not None:
            sys.modules["typer"] = original_typer
        elif "typer" in sys.modules:
            del sys.modules["typer"]

        if original_rich is not None:
            sys.modules["rich"] = original_rich
        elif "rich" in sys.modules:
            del sys.modules["rich"]

        if original_cli is not None:
            sys.modules["blueprints.cli"] = original_cli
        elif "blueprints.cli" in sys.modules:
            del sys.modules["blueprints.cli"]

        # Re-import the working cli module for subsequent tests
        from blueprints import cli as cli_reloaded  # noqa: F401, PLC0415


# Tests using mocks to cover command implementations without executing them


def test_run_command_success() -> None:
    """Test run_command helper with successful execution."""
    with patch("blueprints.cli.subprocess.run") as mock_run:
        mock_run.return_value = MagicMock(returncode=0)

        with pytest.raises(SystemExit) as exc_info:
            cli.run_command(["test_cmd"], "Success message")

        assert exc_info.value.code == 0
        mock_run.assert_called_once_with(["test_cmd"], check=False, text=True)


def test_run_command_failure() -> None:
    """Test run_command helper with failed execution."""
    with patch("blueprints.cli.subprocess.run") as mock_run:
        mock_run.return_value = MagicMock(returncode=1)

        with pytest.raises(SystemExit) as exc_info:
            cli.run_command(["test_cmd"])

        assert exc_info.value.code == 1


def test_run_command_not_found() -> None:
    """Test run_command helper when command is not found."""
    with patch("blueprints.cli.subprocess.run") as mock_run:
        mock_run.side_effect = FileNotFoundError()

        with pytest.raises(SystemExit) as exc_info:
            cli.run_command(["nonexistent_cmd"])

        assert exc_info.value.code == 1


def test_run_command_keyboard_interrupt() -> None:
    """Test run_command helper with keyboard interrupt."""
    with patch("blueprints.cli.subprocess.run") as mock_run:
        mock_run.side_effect = KeyboardInterrupt()

        with pytest.raises(SystemExit) as exc_info:
            cli.run_command(["test_cmd"])

        assert exc_info.value.code == 130


def test_install_command() -> None:
    """Test install command mocked execution."""
    mock_ctx = MagicMock()
    mock_ctx.args = []

    with patch("blueprints.cli.subprocess.run") as mock_run:
        mock_run.return_value = MagicMock(returncode=0)

        with pytest.raises(SystemExit) as exc_info:
            cli.install(mock_ctx)

        assert exc_info.value.code == 0
        # Check that uv sync was called with correct flags
        mock_run.assert_called_once()
        call_cmd = mock_run.call_args[0][0]
        assert "uv" in call_cmd
        assert "sync" in call_cmd
        assert "--locked" in call_cmd
        assert "--all-groups" in call_cmd


def test_install_command_sync_failure() -> None:
    """Test install command when sync fails."""
    mock_ctx = MagicMock()
    mock_ctx.args = []

    with patch("blueprints.cli.subprocess.run") as mock_run:
        mock_run.return_value = MagicMock(returncode=1, stderr="sync error")

        with pytest.raises(SystemExit) as exc_info:
            cli.install(mock_ctx)

        assert exc_info.value.code == 1


def test_lint_command() -> None:
    """Test lint command mocked execution."""
    mock_ctx = MagicMock()
    mock_ctx.args = []

    with patch("blueprints.cli.run_command") as mock_run:
        cli.lint(mock_ctx)
        mock_run.assert_called_once()


def test_format_command() -> None:
    """Test format command mocked execution."""
    mock_ctx = MagicMock()
    mock_ctx.args = []

    with patch("blueprints.cli.run_command") as mock_run:
        cli.formatting(mock_ctx)
        mock_run.assert_called_once()


def test_typecheck_command() -> None:
    """Test typecheck command mocked execution."""
    mock_ctx = MagicMock()
    mock_ctx.args = []

    with patch("blueprints.cli.run_command") as mock_run:
        cli.typecheck(mock_ctx)
        mock_run.assert_called_once()


def test_test_command() -> None:
    """Test test command mocked execution."""
    mock_ctx = MagicMock()
    mock_ctx.args = []

    with patch("blueprints.cli.run_command") as mock_run:
        cli.test(mock_ctx)
        mock_run.assert_called_once()


def test_test_light_command() -> None:
    """Test test command with --light flag."""
    mock_ctx = MagicMock()
    mock_ctx.args = []

    with patch("blueprints.cli.run_command") as mock_run:
        cli.test(mock_ctx, light=True)
        mock_run.assert_called_once()
        # Verify it includes the -m not slow filter for lightweight tests
        call_args = mock_run.call_args[0][0]
        assert "not slow" in call_args


def test_coverage_command() -> None:
    """Test coverage command with default terminal report."""
    mock_ctx = MagicMock()
    mock_ctx.args = []

    with patch("blueprints.cli.run_command") as mock_run:
        cli.coverage(mock_ctx)
        mock_run.assert_called_once()
        # Verify it includes coverage flags
        call_args = mock_run.call_args[0][0]
        assert "--cov=./blueprints" in call_args
        assert "--cov-fail-under=100" in call_args


def test_coverage_command_with_xml() -> None:
    """Test coverage command with --xml flag."""
    mock_ctx = MagicMock()
    mock_ctx.args = []

    with patch("blueprints.cli.run_command") as mock_run:
        cli.coverage(mock_ctx, xml=True)
        mock_run.assert_called_once()
        # Verify it includes coverage flags
        call_args = mock_run.call_args[0][0]
        assert "--cov=./blueprints" in call_args
        assert "xml" in call_args
        assert "--cov-fail-under=100" in call_args


def test_coverage_command_with_html() -> None:
    """Test coverage command with --html flag."""
    mock_ctx = MagicMock()
    mock_ctx.args = []

    with patch("blueprints.cli.run_command") as mock_run:
        cli.coverage(mock_ctx, html=True)
        mock_run.assert_called_once()
        # Verify it includes coverage flags
        call_args = mock_run.call_args[0][0]
        assert "--cov=./blueprints" in call_args
        assert "html" in call_args
        assert "--cov-fail-under=100" in call_args


def test_coverage_command_with_no_check() -> None:
    """Test coverage command with --no-check flag."""
    mock_ctx = MagicMock()
    mock_ctx.args = []

    with patch("blueprints.cli.run_command") as mock_run:
        cli.coverage(mock_ctx, check=False)
        mock_run.assert_called_once()
        # Verify it does NOT include enforcement flag
        call_args = mock_run.call_args[0][0]
        assert "--cov=./blueprints" in call_args
        assert "--cov-fail-under=100" not in call_args


def test_coverage_command_failure() -> None:
    """Test coverage command with failure."""
    mock_ctx = MagicMock()
    mock_ctx.args = []

    with patch("blueprints.cli.run_command") as mock_run:
        # Make run_command raise SystemExit with code 1 to simulate failure
        mock_run.side_effect = SystemExit(1)

        with pytest.raises(SystemExit) as exc_info:
            cli.coverage(mock_ctx)

        assert exc_info.value.code == 1


# Tests for CLI callback and new features


def test_version_flag() -> None:
    """Test --version flag displays version."""
    result = subprocess.run(
        args=[sys.executable, "-m", "blueprints.cli", "--version"],
        check=False,
        capture_output=True,
        text=True,
        cwd=PROJECT_ROOT,
        env=os.environ.copy(),
    )
    assert result.returncode == 0
    assert "version" in result.stdout.lower()


def test_version_short_flag() -> None:
    """Test -v shorthand flag displays version."""
    result = subprocess.run(
        args=[sys.executable, "-m", "blueprints.cli", "-v"],
        check=False,
        capture_output=True,
        text=True,
        cwd=PROJECT_ROOT,
        env=os.environ.copy(),
    )
    assert result.returncode == 0
    assert "version" in result.stdout.lower()


def test_version_retrieval() -> None:
    """Test __version__ can be retrieved."""
    from blueprints.cli import __version__  # noqa: PLC0415

    assert __version__ is not None
    assert isinstance(__version__, str)
    assert len(__version__) > 0


def test_banner_shows_current_version() -> None:
    """Test banner displays the correct version."""
    result = subprocess.run(
        args=[sys.executable, "-m", "blueprints.cli", "--version"],
        check=False,
        capture_output=True,
        text=True,
        cwd=PROJECT_ROOT,
        env=os.environ.copy(),
    )

    assert result.returncode == 0
    # Check that version appears in banner
    assert "Blueprints CLI - v" in result.stdout


# Tests for Pass-Through Arguments


def test_install_with_pass_through_args() -> None:
    """Test install command passes extra arguments to uv sync."""
    mock_ctx = MagicMock()
    mock_ctx.args = ["--upgrade"]

    with patch("blueprints.cli.subprocess.run") as mock_run:
        mock_run.return_value = MagicMock(returncode=0)

        with pytest.raises(SystemExit) as exc_info:
            cli.install(mock_ctx)

        assert exc_info.value.code == 0
        # Check that --upgrade was passed to uv sync
        mock_run.assert_called_once()
        call_cmd = mock_run.call_args[0][0]
        assert "--upgrade" in call_cmd


def test_install_with_python_version() -> None:
    """Test install command passes --python flag to uv sync."""
    mock_ctx = MagicMock()
    mock_ctx.args = ["--python", "3.11"]

    with patch("blueprints.cli.subprocess.run") as mock_run:
        mock_run.return_value = MagicMock(returncode=0)

        with pytest.raises(SystemExit) as exc_info:
            cli.install(mock_ctx)

        assert exc_info.value.code == 0
        mock_run.assert_called_once()
        call_cmd = mock_run.call_args[0][0]
        assert "--python" in call_cmd
        assert "3.11" in call_cmd


def test_test_with_pass_through_args() -> None:
    """Test test command passes extra arguments to pytest."""
    mock_ctx = MagicMock()
    mock_ctx.args = ["-k", "test_cli"]

    with patch("blueprints.cli.run_command") as mock_run:
        cli.test(mock_ctx)
        # Verify run_command was called with the extra args
        call_args = mock_run.call_args[0][0]
        assert "-k" in call_args
        assert "test_cli" in call_args


def test_test_with_verbose_flag() -> None:
    """Test test command passes --verbose flag."""
    mock_ctx = MagicMock()
    mock_ctx.args = ["--verbose"]

    with patch("blueprints.cli.run_command") as mock_run:
        cli.test(mock_ctx)
        call_args = mock_run.call_args[0][0]
        assert "--verbose" in call_args


def test_lint_with_fix_flag() -> None:
    """Test lint command passes --fix flag."""
    mock_ctx = MagicMock()
    mock_ctx.args = ["--fix"]

    with patch("blueprints.cli.run_command") as mock_run:
        cli.lint(mock_ctx)
        call_args = mock_run.call_args[0][0]
        assert "--fix" in call_args


def test_format_with_pass_through_args() -> None:
    """Test format command passes extra arguments."""
    mock_ctx = MagicMock()
    mock_ctx.args = ["--line-length", "100"]

    with patch("blueprints.cli.run_command") as mock_run:
        cli.formatting(mock_ctx)
        call_args = mock_run.call_args[0][0]
        assert "--line-length" in call_args
        assert "100" in call_args


def test_typecheck_with_pass_through_args() -> None:
    """Test typecheck command passes extra arguments."""
    mock_ctx = MagicMock()
    mock_ctx.args = ["--strict"]

    with patch("blueprints.cli.run_command") as mock_run:
        cli.typecheck(mock_ctx)
        call_args = mock_run.call_args[0][0]
        assert "--strict" in call_args


def test_test_light_with_pass_through_args() -> None:
    """Test test command with --light flag passes extra arguments."""
    mock_ctx = MagicMock()
    mock_ctx.args = ["--pdb"]

    with patch("blueprints.cli.run_command") as mock_run:
        cli.test(mock_ctx, light=True)
        call_args = mock_run.call_args[0][0]
        assert "--pdb" in call_args
        # Also verify it's using the lightweight filter
        assert "not slow" in call_args


def test_coverage_with_pass_through_args() -> None:
    """Test coverage command passes extra arguments."""
    mock_ctx = MagicMock()
    mock_ctx.args = ["-x"]

    with patch("blueprints.cli.run_command") as mock_run:
        cli.coverage(mock_ctx)
        # Verify run_command was called with the pass-through arg
        call_args = mock_run.call_args[0][0]
        assert "-x" in call_args


def test_coverage_with_xml_and_pass_through_args() -> None:
    """Test coverage command with --xml flag and pass-through arguments."""
    mock_ctx = MagicMock()
    mock_ctx.args = ["-k", "test_important"]

    with patch("blueprints.cli.run_command") as mock_run:
        cli.coverage(mock_ctx, xml=True)
        # Verify run_command was called with the pass-through args
        call_args = mock_run.call_args[0][0]
        assert "-k" in call_args
        assert "test_important" in call_args
        assert "xml" in call_args


def test_commands_work_without_extra_args() -> None:
    """Test backward compatibility - commands work without extra arguments."""
    mock_ctx = MagicMock()
    mock_ctx.args = []

    with patch("blueprints.cli.run_command") as mock_run:
        cli.lint(mock_ctx)
        mock_run.assert_called_once()

    with patch("blueprints.cli.run_command") as mock_run:
        cli.test(mock_ctx)
        mock_run.assert_called_once()


def test_multiple_pass_through_args() -> None:
    """Test commands handle multiple pass-through arguments."""
    mock_ctx = MagicMock()
    mock_ctx.args = ["-k", "test_pattern", "--verbose", "-x"]

    with patch("blueprints.cli.run_command") as mock_run:
        cli.test(mock_ctx)
        call_args = mock_run.call_args[0][0]
        assert "-k" in call_args
        assert "test_pattern" in call_args
        assert "--verbose" in call_args
        assert "-x" in call_args


# Tests for Check Command


def test_check_command_all_pass() -> None:
    """Test check command when all checks pass."""
    mock_ctx = MagicMock()
    mock_ctx.args = []

    with patch("blueprints.cli.subprocess.run") as mock_run:
        # All checks return 0 (success)
        mock_run.return_value = MagicMock(returncode=0)

        with pytest.raises(SystemExit) as exc_info:
            cli.check(mock_ctx)

        # Should exit with 0 (success)
        assert exc_info.value.code == 0
        # Should have called subprocess.run 4 times (lint, format, typecheck, coverage)
        assert mock_run.call_count == 4


def test_check_command_lint_fails() -> None:
    """Test check command when lint fails."""
    mock_ctx = MagicMock()
    mock_ctx.args = []

    with patch("blueprints.cli.subprocess.run") as mock_run:
        # First call (lint) fails, rest pass
        mock_run.side_effect = [
            MagicMock(returncode=1),  # Lint fails
            MagicMock(returncode=0),  # Format passes
            MagicMock(returncode=0),  # Typecheck passes
            MagicMock(returncode=0),  # Coverage passes
        ]

        with pytest.raises(SystemExit) as exc_info:
            cli.check(mock_ctx)

        # Should exit with 1 (failure)
        assert exc_info.value.code == 1
        # Should still run all checks
        assert mock_run.call_count == 4


def test_check_command_format_fails() -> None:
    """Test check command when format fails."""
    mock_ctx = MagicMock()
    mock_ctx.args = []

    with patch("blueprints.cli.subprocess.run") as mock_run:
        # Second call (format) fails
        mock_run.side_effect = [
            MagicMock(returncode=0),  # Lint passes
            MagicMock(returncode=1),  # Format fails
            MagicMock(returncode=0),  # Typecheck passes
            MagicMock(returncode=0),  # Coverage passes
        ]

        with pytest.raises(SystemExit) as exc_info:
            cli.check(mock_ctx)

        assert exc_info.value.code == 1
        assert mock_run.call_count == 4


def test_check_command_typecheck_fails() -> None:
    """Test check command when typecheck fails."""
    mock_ctx = MagicMock()
    mock_ctx.args = []

    with patch("blueprints.cli.subprocess.run") as mock_run:
        # Third call (typecheck) fails
        mock_run.side_effect = [
            MagicMock(returncode=0),  # Lint passes
            MagicMock(returncode=0),  # Format passes
            MagicMock(returncode=1),  # Typecheck fails
            MagicMock(returncode=0),  # Coverage passes
        ]

        with pytest.raises(SystemExit) as exc_info:
            cli.check(mock_ctx)

        assert exc_info.value.code == 1
        assert mock_run.call_count == 4


def test_check_command_coverage_fails() -> None:
    """Test check command when coverage fails."""
    mock_ctx = MagicMock()
    mock_ctx.args = []

    with patch("blueprints.cli.subprocess.run") as mock_run:
        # Fourth call (coverage) fails
        mock_run.side_effect = [
            MagicMock(returncode=0),  # Lint passes
            MagicMock(returncode=0),  # Format passes
            MagicMock(returncode=0),  # Typecheck passes
            MagicMock(returncode=1),  # Coverage fails
        ]

        with pytest.raises(SystemExit) as exc_info:
            cli.check(mock_ctx)

        assert exc_info.value.code == 1
        assert mock_run.call_count == 4


def test_check_command_with_pass_through_args() -> None:
    """Test check command passes extra arguments to sub-commands."""
    mock_ctx = MagicMock()
    mock_ctx.args = ["-x"]

    with patch("blueprints.cli.subprocess.run") as mock_run:
        mock_run.return_value = MagicMock(returncode=0)

        with pytest.raises(SystemExit) as exc_info:
            cli.check(mock_ctx)

        assert exc_info.value.code == 0
        # Check that all calls include the extra args
        assert len(mock_run.call_args_list) == 4  # 4 checks: lint, format, typecheck, coverage

        # All calls use args= keyword argument
        for call in mock_run.call_args_list:
            call_args = call[1]["args"]
            assert "-x" in call_args


def test_check_command_multiple_failures() -> None:
    """Test check command when multiple checks fail."""
    mock_ctx = MagicMock()
    mock_ctx.args = []

    with patch("blueprints.cli.subprocess.run") as mock_run:
        # Lint and coverage fail
        mock_run.side_effect = [
            MagicMock(returncode=1),  # Lint fails
            MagicMock(returncode=0),  # Format passes
            MagicMock(returncode=0),  # Typecheck passes
            MagicMock(returncode=1),  # Coverage fails
        ]

        with pytest.raises(SystemExit) as exc_info:
            cli.check(mock_ctx)

        assert exc_info.value.code == 1
        assert mock_run.call_count == 4


def test_check_command_missing_uv() -> None:
    """Test check command when uv is not found."""
    mock_ctx = MagicMock()
    mock_ctx.args = []

    with patch("blueprints.cli.subprocess.run") as mock_run:
        mock_run.side_effect = FileNotFoundError()

        with pytest.raises(SystemExit) as exc_info:
            cli.check(mock_ctx)

        assert exc_info.value.code == 1


# Tests for Docs Command


def test_docs_command() -> None:
    """Test docs command mocked execution."""
    with patch("blueprints.cli.run_command") as mock_run:
        cli.docs()
        mock_run.assert_called_once()


def test_docs_command_calls_mkdocs() -> None:
    """Test that docs command calls mkdocs serve with livereload."""
    with patch("blueprints.cli.run_command") as mock_run:
        cli.docs()
        # Get the command that was passed to run_command
        call_args = mock_run.call_args[0][0]
        assert "mkdocs" in call_args
        assert "serve" in call_args
        assert "--livereload" in call_args
