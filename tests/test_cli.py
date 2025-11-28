"""Tests for the Blueprints CLI module."""

import importlib
import subprocess
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from blueprints import cli

PROJECT_ROOT = Path(__file__).parent.parent


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
        from blueprints import cli as cli_reloaded  # noqa: F401


def test_cli_help_command() -> None:
    """Test that CLI help command works."""
    result = subprocess.run(
        [sys.executable, "-m", "blueprints.cli", "--help"],
        check=False,
        capture_output=True,
        text=True,
        cwd=PROJECT_ROOT,
    )

    assert result.returncode == 0
    assert "blueprints" in result.stdout.lower()
    assert "Blueprints - Development automation CLI" in result.stdout


@pytest.mark.parametrize(
    "command",
    [
        "install",
        "ci-install",
        "lint",
        "format",
        "typecheck",
        "test",
        "test-light",
        "check",
        "check-coverage",
        "coverage-report",
        "coverage-html",
        "build",
        "docs",
        "clean",
    ],
)
def test_cli_command_exists(command: str) -> None:
    """Test that all expected commands are available."""
    result = subprocess.run(
        [sys.executable, "-m", "blueprints.cli", command, "--help"],
        check=False,
        capture_output=True,
        text=True,
        cwd=PROJECT_ROOT,
    )

    # Should show help, not "No such command"
    assert result.returncode == 0
    assert "No such command" not in result.stderr
    assert "Error" not in result.stderr or "Usage:" in result.stdout


def test_cli_clean_command_execution() -> None:
    """Test that clean command can execute without errors.

    This is the only safe command to test end-to-end as it doesn't
    modify the environment in CI/CD.
    """
    result = subprocess.run(
        [sys.executable, "-m", "blueprints.cli", "clean"],
        check=False,
        capture_output=True,
        text=True,
        cwd=PROJECT_ROOT,
    )

    # Should succeed even if nothing to clean
    assert result.returncode == 0
    assert "Cleaning up" in result.stdout or "Cleaned up" in result.stdout


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
        # Check that uv venv was called first
        assert mock_run.call_count == 2


def test_install_command_venv_failure() -> None:
    """Test install command when venv creation fails."""
    mock_ctx = MagicMock()
    mock_ctx.args = []

    with patch("blueprints.cli.subprocess.run") as mock_run:
        mock_run.return_value = MagicMock(returncode=1, stderr="venv error")

        with pytest.raises(SystemExit) as exc_info:
            cli.install(mock_ctx)

        assert exc_info.value.code == 1


def test_ci_install_command() -> None:
    """Test ci-install command mocked execution."""
    mock_ctx = MagicMock()
    mock_ctx.args = []

    with patch("blueprints.cli.run_command") as mock_run:
        cli.ci_install(mock_ctx)
        mock_run.assert_called_once()


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
        cli.format(mock_ctx)
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
    """Test test-light command mocked execution."""
    mock_ctx = MagicMock()
    mock_ctx.args = []

    with patch("blueprints.cli.run_command") as mock_run:
        cli.test_light(mock_ctx)
        mock_run.assert_called_once()


def test_check_coverage_command() -> None:
    """Test check-coverage command mocked execution."""
    mock_ctx = MagicMock()
    mock_ctx.args = []

    with patch("blueprints.cli.run_command") as mock_run:
        cli.check_coverage(mock_ctx)
        mock_run.assert_called_once()


def test_coverage_report_command() -> None:
    """Test coverage-report command mocked execution."""
    mock_ctx = MagicMock()
    mock_ctx.args = []

    with patch("blueprints.cli.run_command") as mock_run:
        cli.coverage_report(mock_ctx)
        mock_run.assert_called_once()


def test_coverage_html_command() -> None:
    """Test coverage-html command mocked execution."""
    mock_ctx = MagicMock()
    mock_ctx.args = []

    with patch("blueprints.cli.subprocess.run") as mock_run:
        mock_run.return_value = MagicMock(returncode=0)

        with pytest.raises(SystemExit) as exc_info:
            cli.coverage_html(mock_ctx)

        assert exc_info.value.code == 0


def test_build_command() -> None:
    """Test build command mocked execution."""
    mock_ctx = MagicMock()
    mock_ctx.args = []

    with patch("blueprints.cli.subprocess.run") as mock_run:
        mock_run.return_value = MagicMock(returncode=0)

        with pytest.raises(SystemExit) as exc_info:
            cli.build(mock_ctx)

        assert exc_info.value.code == 0


def test_clean_command_with_artifacts() -> None:
    """Test clean command with artifacts to remove."""
    with patch("blueprints.cli.Path") as mock_path_class:
        mock_path_instance = MagicMock()
        mock_path_class.return_value = mock_path_instance
        mock_path_instance.exists.return_value = True
        mock_path_instance.is_dir.return_value = True

        with patch("blueprints.cli.shutil.rmtree") as mock_rmtree:
            cli.clean()
            mock_rmtree.assert_called()


def test_clean_command_with_removal_error() -> None:
    """Test clean command when artifact removal fails."""

    def path_side_effect(artifact: str) -> MagicMock:
        mock_path = MagicMock()
        if artifact == ".venv":
            # Make this one fail
            mock_path.exists.return_value = True
            mock_path.is_dir.return_value = True
            mock_path.unlink.side_effect = OSError("Permission denied")
        else:
            mock_path.exists.return_value = False
        return mock_path

    with patch("blueprints.cli.Path") as mock_path_class:
        mock_path_class.side_effect = path_side_effect
        with patch("blueprints.cli.shutil.rmtree") as mock_rmtree:
            mock_rmtree.side_effect = OSError("Permission denied")
            cli.clean()
            # Should complete even with error


def test_clean_command_no_artifacts() -> None:
    """Test clean command when there are no artifacts."""
    with patch("blueprints.cli.Path") as mock_path_class:
        mock_path_instance = MagicMock()
        mock_path_class.return_value = mock_path_instance
        mock_path_instance.exists.return_value = False

        cli.clean()
        # Should print "Nothing to clean"


def test_clean_command_with_file_artifacts() -> None:
    """Test clean command with file artifacts (not directories)."""
    call_count = 0

    def path_side_effect(artifact: str) -> MagicMock:
        mock_path = MagicMock()
        mock_path.exists.return_value = True
        # First artifact is a file, rest don't exist
        if artifact == ".coverage":
            mock_path.is_dir.return_value = False  # This is a file
        else:
            mock_path.exists.return_value = False
        return mock_path

    with patch("blueprints.cli.Path") as mock_path_class:
        mock_path_class.side_effect = path_side_effect

        cli.clean()
        # Should call unlink() for the .coverage file


def test_coverage_html_command_failure() -> None:
    """Test coverage-html command with failure."""
    mock_ctx = MagicMock()
    mock_ctx.args = []

    with patch("blueprints.cli.subprocess.run") as mock_run:
        mock_run.return_value = MagicMock(returncode=1)

        with pytest.raises(SystemExit) as exc_info:
            cli.coverage_html(mock_ctx)

        assert exc_info.value.code == 1


# Tests for CLI callback and new features


def test_version_flag() -> None:
    """Test --version flag displays version."""
    result = subprocess.run(
        [sys.executable, "-m", "blueprints.cli", "--version"],
        check=False,
        capture_output=True,
        text=True,
        cwd=PROJECT_ROOT,
    )
    assert result.returncode == 0
    assert "version" in result.stdout.lower()
    assert "0.5.2" in result.stdout


def test_version_short_flag() -> None:
    """Test -v shorthand flag displays version."""
    result = subprocess.run(
        [sys.executable, "-m", "blueprints.cli", "-v"],
        check=False,
        capture_output=True,
        text=True,
        cwd=PROJECT_ROOT,
    )
    assert result.returncode == 0
    assert "version" in result.stdout.lower()
    assert "0.5.2" in result.stdout


def test_callback_without_command_shows_help() -> None:
    """Test callback shows help when no command given."""
    result = subprocess.run(
        [sys.executable, "-m", "blueprints.cli"],
        check=False,
        capture_output=True,
        text=True,
        cwd=PROJECT_ROOT,
    )
    assert result.returncode == 0
    assert "Usage:" in result.stdout
    assert "Development automation CLI" in result.stdout
    assert "Blueprints CLI" in result.stdout


def test_callback_with_command_shows_banner() -> None:
    """Test callback shows banner before executing commands."""
    result = subprocess.run(
        [sys.executable, "-m", "blueprints.cli", "clean"],
        check=False,
        capture_output=True,
        text=True,
        cwd=PROJECT_ROOT,
    )
    # Should show banner then execute clean
    assert result.returncode == 0
    assert "Blueprints CLI" in result.stdout
    assert "Cleaning up" in result.stdout or "Nothing to clean" in result.stdout


def test_version_retrieval() -> None:
    """Test __version__ can be retrieved."""
    from blueprints.cli import __version__

    assert __version__ is not None
    assert isinstance(__version__, str)
    assert len(__version__) > 0


def test_banner_shows_current_version() -> None:
    """Test banner displays the correct version."""
    result = subprocess.run(
        [sys.executable, "-m", "blueprints.cli", "--version"],
        check=False,
        capture_output=True,
        text=True,
        cwd=PROJECT_ROOT,
    )

    assert result.returncode == 0
    # Check that version appears in banner
    assert "Blueprints CLI - v" in result.stdout


def test_callback_executes_with_valid_command() -> None:
    """Test callback executes before valid commands."""
    result = subprocess.run(
        [sys.executable, "-m", "blueprints.cli", "clean", "--help"],
        check=False,
        capture_output=True,
        text=True,
        cwd=PROJECT_ROOT,
    )

    assert result.returncode == 0
    # Banner should show
    assert "Blueprints CLI" in result.stdout
    # Help for command should show
    assert "Remove venv" in result.stdout or "Remove" in result.stdout


def test_main_callback_direct() -> None:
    """Test main callback function directly with mocking."""
    mock_ctx = MagicMock()
    mock_ctx.invoked_subcommand = "test"

    # Should not raise when a subcommand is being invoked
    cli.main(mock_ctx, version_flag=False)
    # If it gets here without raising, the test passes


def test_main_callback_version_flag() -> None:
    """Test main callback with version flag."""
    mock_ctx = MagicMock()

    # typer.Exit raises click.exceptions.Exit, not SystemExit
    with pytest.raises(Exception):  # Catches typer.Exit (which is click.exceptions.Exit)
        cli.main(mock_ctx, version_flag=True)


def test_main_callback_no_command() -> None:
    """Test main callback when no subcommand is invoked."""
    mock_ctx = MagicMock()
    mock_ctx.invoked_subcommand = None
    mock_ctx.get_help.return_value = "Help text"

    # typer.Exit raises click.exceptions.Exit, not SystemExit
    with pytest.raises(Exception):  # Catches typer.Exit (which is click.exceptions.Exit)
        cli.main(mock_ctx, version_flag=False)


def test_main_callback_missing_uv() -> None:
    """Test main callback warns when uv is missing."""
    mock_ctx = MagicMock()
    mock_ctx.invoked_subcommand = "test"

    with patch("blueprints.cli.shutil.which") as mock_which:
        mock_which.return_value = None

        # Should not raise, just show warning
        cli.main(mock_ctx, version_flag=False)


def test_main_callback_terminal_width_exception() -> None:
    """Test banner handles terminal width exceptions."""
    mock_ctx = MagicMock()
    mock_ctx.invoked_subcommand = "test"

    with patch("blueprints.cli.shutil.get_terminal_size") as mock_size:
        # Simulate exception when getting terminal size
        mock_size.side_effect = Exception("Terminal error")

        # Should default to 80 and not raise
        cli.main(mock_ctx, version_flag=False)


def test_main_callback_narrow_terminal() -> None:
    """Test banner handles narrow terminals gracefully."""
    mock_ctx = MagicMock()
    mock_ctx.invoked_subcommand = "test"

    with patch("blueprints.cli.shutil.get_terminal_size") as mock_size:
        # Mock a very narrow terminal
        mock_size.return_value = type("obj", (object,), {"columns": 30})()

        # Should still work with minimum width of 40
        cli.main(mock_ctx, version_flag=False)


def test_main_callback_very_wide_terminal() -> None:
    """Test banner handles very wide terminals."""
    mock_ctx = MagicMock()
    mock_ctx.invoked_subcommand = "test"

    with patch("blueprints.cli.shutil.get_terminal_size") as mock_size:
        # Mock a very wide terminal
        mock_size.return_value = type("obj", (object,), {"columns": 200})()

        # Should handle wide terminals correctly
        cli.main(mock_ctx, version_flag=False)


# Tests for Pass-Through Arguments


def test_install_with_pass_through_args() -> None:
    """Test install command passes extra arguments to uv."""
    mock_ctx = MagicMock()
    mock_ctx.args = ["--clear"]

    with patch("blueprints.cli.subprocess.run") as mock_run:
        mock_run.return_value = MagicMock(returncode=0)

        with pytest.raises(SystemExit) as exc_info:
            cli.install(mock_ctx)

        assert exc_info.value.code == 0
        # Check that --clear was passed to uv venv
        calls = mock_run.call_args_list
        first_call_args = calls[0][1]["args"]
        assert "--clear" in first_call_args


def test_install_with_python_version() -> None:
    """Test install command passes --python flag."""
    mock_ctx = MagicMock()
    mock_ctx.args = ["--python", "3.11"]

    with patch("blueprints.cli.subprocess.run") as mock_run:
        mock_run.return_value = MagicMock(returncode=0)

        with pytest.raises(SystemExit) as exc_info:
            cli.install(mock_ctx)

        assert exc_info.value.code == 0
        calls = mock_run.call_args_list
        first_call_args = calls[0][1]["args"]
        assert "--python" in first_call_args
        assert "3.11" in first_call_args


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
        cli.format(mock_ctx)
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
    """Test test-light command passes extra arguments."""
    mock_ctx = MagicMock()
    mock_ctx.args = ["--pdb"]

    with patch("blueprints.cli.run_command") as mock_run:
        cli.test_light(mock_ctx)
        call_args = mock_run.call_args[0][0]
        assert "--pdb" in call_args


def test_ci_install_with_pass_through_args() -> None:
    """Test ci-install command passes extra arguments."""
    mock_ctx = MagicMock()
    mock_ctx.args = ["--all-groups"]

    with patch("blueprints.cli.run_command") as mock_run:
        cli.ci_install(mock_ctx)
        call_args = mock_run.call_args[1]["cmd"]
        assert "--all-groups" in call_args


def test_check_coverage_with_pass_through_args() -> None:
    """Test check-coverage command passes extra arguments."""
    mock_ctx = MagicMock()
    mock_ctx.args = ["-k", "test_specific"]

    with patch("blueprints.cli.run_command") as mock_run:
        cli.check_coverage(mock_ctx)
        call_args = mock_run.call_args[0][0]
        assert "-k" in call_args
        assert "test_specific" in call_args


def test_coverage_report_with_pass_through_args() -> None:
    """Test coverage-report command passes extra arguments."""
    mock_ctx = MagicMock()
    mock_ctx.args = ["-x"]

    with patch("blueprints.cli.run_command") as mock_run:
        cli.coverage_report(mock_ctx)
        call_args = mock_run.call_args[0][0]
        assert "-x" in call_args


def test_coverage_html_with_pass_through_args() -> None:
    """Test coverage-html command passes extra arguments."""
    mock_ctx = MagicMock()
    mock_ctx.args = ["-k", "test_important"]

    with patch("blueprints.cli.subprocess.run") as mock_run:
        mock_run.return_value = MagicMock(returncode=0)

        with pytest.raises(SystemExit) as exc_info:
            cli.coverage_html(mock_ctx)

        assert exc_info.value.code == 0
        call_args = mock_run.call_args[0][0]
        assert "-k" in call_args
        assert "test_important" in call_args


def test_build_with_pass_through_args() -> None:
    """Test build command passes extra arguments."""
    mock_ctx = MagicMock()
    mock_ctx.args = ["--sdist"]

    with patch("blueprints.cli.subprocess.run") as mock_run:
        mock_run.return_value = MagicMock(returncode=0)

        with pytest.raises(SystemExit) as exc_info:
            cli.build(mock_ctx)

        assert exc_info.value.code == 0
        call_args = mock_run.call_args[0][0]
        assert "--sdist" in call_args


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
        for call in mock_run.call_args_list:
            call_args = call[0][0]
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
