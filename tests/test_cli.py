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
        "test-verbose",
        "test-light",
        "check-coverage",
        "coverage-report",
        "coverage-html",
        "build",
        "clean",
    ],
)
def test_cli_command_exists(command: str) -> None:
    """Test that all expected commands are available."""
    result = subprocess.run(
        [sys.executable, "-m", "blueprints.cli", command, "--help"],
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
        mock_run.assert_called_once_with(["test_cmd"], text=True)


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
    with patch("blueprints.cli.subprocess.run") as mock_run:
        mock_run.return_value = MagicMock(returncode=0)

        with pytest.raises(SystemExit) as exc_info:
            cli.install()

        assert exc_info.value.code == 0
        # Check that uv venv was called first
        assert mock_run.call_count == 2


def test_install_command_venv_failure() -> None:
    """Test install command when venv creation fails."""
    with patch("blueprints.cli.subprocess.run") as mock_run:
        mock_run.return_value = MagicMock(returncode=1, stderr="venv error")

        with pytest.raises(SystemExit) as exc_info:
            cli.install()

        assert exc_info.value.code == 1


def test_ci_install_command() -> None:
    """Test ci-install command mocked execution."""
    with patch("blueprints.cli.run_command") as mock_run:
        cli.ci_install()
        mock_run.assert_called_once()


def test_lint_command() -> None:
    """Test lint command mocked execution."""
    with patch("blueprints.cli.run_command") as mock_run:
        cli.lint()
        mock_run.assert_called_once()


def test_format_command() -> None:
    """Test format command mocked execution."""
    with patch("blueprints.cli.run_command") as mock_run:
        cli.format()
        mock_run.assert_called_once()


def test_typecheck_command() -> None:
    """Test typecheck command mocked execution."""
    with patch("blueprints.cli.run_command") as mock_run:
        cli.typecheck()
        mock_run.assert_called_once()


def test_test_command() -> None:
    """Test test command mocked execution."""
    with patch("blueprints.cli.run_command") as mock_run:
        cli.test()
        mock_run.assert_called_once()


def test_test_verbose_command() -> None:
    """Test test-verbose command mocked execution."""
    with patch("blueprints.cli.run_command") as mock_run:
        cli.test_verbose()
        mock_run.assert_called_once()


def test_test_light_command() -> None:
    """Test test-light command mocked execution."""
    with patch("blueprints.cli.run_command") as mock_run:
        cli.test_light()
        mock_run.assert_called_once()


def test_check_coverage_command() -> None:
    """Test check-coverage command mocked execution."""
    with patch("blueprints.cli.run_command") as mock_run:
        cli.check_coverage()
        mock_run.assert_called_once()


def test_coverage_report_command() -> None:
    """Test coverage-report command mocked execution."""
    with patch("blueprints.cli.run_command") as mock_run:
        cli.coverage_report()
        mock_run.assert_called_once()


def test_coverage_html_command() -> None:
    """Test coverage-html command mocked execution."""
    with patch("blueprints.cli.subprocess.run") as mock_run:
        mock_run.return_value = MagicMock(returncode=0)

        with pytest.raises(SystemExit) as exc_info:
            cli.coverage_html()

        assert exc_info.value.code == 0


def test_build_command() -> None:
    """Test build command mocked execution."""
    with patch("blueprints.cli.subprocess.run") as mock_run:
        mock_run.return_value = MagicMock(returncode=0)

        with pytest.raises(SystemExit) as exc_info:
            cli.build()

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
    with patch("blueprints.cli.subprocess.run") as mock_run:
        mock_run.return_value = MagicMock(returncode=1)

        with pytest.raises(SystemExit) as exc_info:
            cli.coverage_html()

        assert exc_info.value.code == 1


# Tests for CLI callback and new features


def test_version_flag() -> None:
    """Test --version flag displays version."""
    result = subprocess.run(
        [sys.executable, "-m", "blueprints.cli", "--version"],
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
        mock_size.return_value = type('obj', (object,), {'columns': 30})()

        # Should still work with minimum width of 40
        cli.main(mock_ctx, version_flag=False)


def test_main_callback_very_wide_terminal() -> None:
    """Test banner handles very wide terminals."""
    mock_ctx = MagicMock()
    mock_ctx.invoked_subcommand = "test"

    with patch("blueprints.cli.shutil.get_terminal_size") as mock_size:
        # Mock a very wide terminal
        mock_size.return_value = type('obj', (object,), {'columns': 200})()

        # Should handle wide terminals correctly
        cli.main(mock_ctx, version_flag=False)
