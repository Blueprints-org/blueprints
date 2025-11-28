"""Blueprints CLI - Development and build automation commands.

This module provides a cross-platform command-line interface for common
development tasks, replacing the Makefile for better Windows compatibility.
"""

import shutil
import subprocess
import sys
from importlib.metadata import version
from pathlib import Path
from typing import Annotated, NoReturn, Optional

try:
    import typer
    from rich.console import Console
except ImportError:
    print("CLI dependencies not installed.")
    print("Install with: uv sync --group cli")
    print("Or: pip install blue-prints[cli]")
    sys.exit(1)


# Version retrieval from installed package
try:
    __version__ = version("blue-prints")
except Exception:  # pragma: no cover
    __version__ = "unknown"  # pragma: no cover


app = typer.Typer(
    name="blueprints",
    help="Blueprints - Development automation CLI",
    add_completion=False,
)
console = Console()


@app.callback(invoke_without_command=True)
def main(
    ctx: typer.Context,
    version_flag: Annotated[
        Optional[bool],
        typer.Option("--version", "-v", help="Show the CLI version."),
    ] = None,
) -> None:
    """Blueprints CLI main callback - runs before all commands.

    Displays a branded banner, checks for required dependencies (uv),
    and handles the --version flag. Shows help when no command is given.

    Parameters
    ----------
    ctx : typer.Context
        Typer context containing command information and invoked subcommand.
    version_flag : bool, optional
        If True, displays version information and exits. Activated by
        --version or -v flags. Default is None.

    Raises
    ------
    typer.Exit
        Exits after displaying version or help when no command is given.

    Notes
    -----
    The banner is terminal-width-aware and adjusts to the current terminal size.
    The uv dependency check is non-blocking - shows a warning if missing but
    continues execution.
    """
    # Check if uv is installed
    if not shutil.which("uv"):
        console.print(
            "[yellow]Warning: 'uv' is not installed.[/yellow]",
        )
        console.print(
            "[yellow]Install it with: pip install uv[/yellow]",
        )
        console.print(
            "[yellow]Or visit: https://github.com/astral-sh/uv[/yellow]",
        )

    # Show banner (terminal-width-aware)
    try:
        terminal_width = shutil.get_terminal_size().columns
    except Exception:
        terminal_width = 80

    # Ensure minimum width
    terminal_width = max(terminal_width, 40)

    console.print("=" * terminal_width, style="bold cyan")
    title = f"Blueprints CLI - v{__version__}"
    # Center the title
    padding = max(0, (terminal_width - len(title)) // 2)
    console.print(" " * padding + title, style="bold cyan")
    console.print("=" * terminal_width, style="bold cyan")

    # Handle --version flag
    if version_flag:
        console.print(f"Blueprints CLI version: {__version__}")
        raise typer.Exit()

    # Show help if no command given
    if ctx.invoked_subcommand is None:
        console.print(ctx.get_help())
        raise typer.Exit()


def run_command(cmd: list[str], success_msg: str = "") -> NoReturn:
    """Execute a command and exit with its return code.

    Runs a subprocess command and exits with the command's return code.
    Displays success message if provided and command succeeds.

    Parameters
    ----------
    cmd : list[str]
        Command and arguments as list.
    success_msg : str, optional
        Message to display on success. Default is empty string.

    Raises
    ------
    SystemExit
        Always exits with the command's return code or error code.
    """
    try:
        result = subprocess.run(cmd, text=True)

        if result.returncode == 0 and success_msg:
            console.print(f"[bold green]{success_msg}[/bold green]")

        sys.exit(result.returncode)

    except FileNotFoundError:
        console.print(f"[bold red]Error: Command not found: {cmd[0]}[/bold red]")
        console.print("[yellow]Make sure 'uv' is installed and in your PATH[/yellow]")
        sys.exit(1)

    except KeyboardInterrupt:
        console.print("\n[yellow]Interrupted by user[/yellow]")
        sys.exit(130)


# Environment Commands


@app.command()
def install() -> None:
    """Create venv and sync all dependencies.

    Creates a virtual environment and synchronizes all dependency groups.
    Equivalent to: make install
    """
    console.print("[bold blue]Creating virtual environment...[/bold blue]")

    result = subprocess.run(
        ["uv", "venv"],
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        console.print(f"[bold red]Error creating venv:[/bold red]\n{result.stderr}")
        sys.exit(1)

    console.print("[bold blue]Syncing all dependencies...[/bold blue]")
    run_command(
        ["uv", "sync", "--locked", "--all-groups"],
        "Environment setup complete!",
    )


@app.command()
def ci_install() -> None:
    """Sync dependencies for CI/CD tests.

    Synchronizes dependencies without dev dependencies for CI/CD environments.
    Equivalent to: make ci-install
    """
    console.print("[bold blue]Syncing CI dependencies...[/bold blue]")
    run_command(
        ["uv", "sync", "--locked", "--no-dev"],
        "CI dependencies synced!",
    )


# Code Quality Commands


@app.command()
def lint() -> None:
    """Lint with Ruff.

    Runs Ruff linter to check code style and quality issues.
    Equivalent to: make lint
    """
    console.print("[bold blue]Running Ruff linter...[/bold blue]")
    run_command(["uv", "run", "ruff", "check", "."])


@app.command()
def format() -> None:
    """Check the formatting with Ruff.

    Checks code formatting compliance using Ruff's formatter.
    Equivalent to: make format
    """
    console.print("[bold blue]Checking formatting with Ruff...[/bold blue]")
    run_command(["uv", "run", "ruff", "format", ".", "--check"])


@app.command()
def typecheck() -> None:
    """Run static type checks with mypy.

    Performs static type checking on the blueprints package using mypy.
    Equivalent to: make typecheck
    """
    console.print("[bold blue]Running mypy type checker...[/bold blue]")
    run_command(["uv", "run", "mypy", "-p", "blueprints"])


# Testing Commands


@app.command()
def test() -> None:
    """Run tests with pytest (parallel execution).

    Executes all tests in parallel using pytest with xdist plugin.
    Equivalent to: make test
    """
    console.print("[bold blue]Running tests...[/bold blue]")
    run_command(
        ["uv", "run", "--no-dev", "pytest", "tests/", "-n", "auto"],
    )


@app.command()
def test_verbose() -> None:
    """Run tests with pytest (verbose output).

    Executes all tests in parallel with verbose output for debugging.
    Equivalent to: make test-verbose
    """
    console.print("[bold blue]Running tests (verbose)...[/bold blue]")
    run_command(
        ["uv", "run", "--no-dev", "pytest", "tests/", "--verbose", "-n", "auto"],
    )


@app.command()
def test_light() -> None:
    """Run tests with pytest (lightweight, excludes slow tests).

    Runs fast tests only, skipping tests marked as slow for rapid iteration.
    Equivalent to: make test-light
    """
    console.print("[bold blue]Running lightweight tests...[/bold blue]")
    run_command(
        ["uv", "run", "--no-dev", "pytest", "tests/", "--verbose", "-m", "not slow"],
    )


@app.command()
def check_coverage() -> None:
    """Run tests and check 100% coverage.

    Executes tests with coverage reporting and enforces 100% coverage requirement.
    Equivalent to: make check-coverage
    """
    console.print("[bold blue]Checking code coverage...[/bold blue]")
    run_command(
        [
            "uv",
            "run",
            "--no-dev",
            "pytest",
            "--cov=./blueprints",
            "--cov-report",
            "term-missing:skip-covered",
            "--cov-fail-under=100",
        ],
    )


@app.command()
def coverage_report() -> None:
    """Run tests and generate coverage reports.

    Executes tests and generates XML coverage report for CI/CD integration.
    Equivalent to: make coverage-report
    """
    console.print("[bold blue]Generating coverage report...[/bold blue]")
    run_command(
        [
            "uv",
            "run",
            "--no-dev",
            "pytest",
            "--cov=./blueprints",
            "--cov-report=xml",
        ],
    )


@app.command()
def coverage_html() -> None:
    """Run tests and generate an html coverage report.

    Executes tests and generates interactive HTML coverage report in htmlcov/.
    Equivalent to: make coverage-html
    """
    console.print("[bold blue]Generating HTML coverage report...[/bold blue]")

    result = subprocess.run(
        [
            "uv",
            "run",
            "--no-dev",
            "pytest",
            "--cov=./blueprints",
            "--cov-report",
            "html",
        ],
        text=True,
    )

    if result.returncode == 0:
        console.print("[bold green]HTML report generated in htmlcov/[/bold green]")

    sys.exit(result.returncode)


# Build Commands


@app.command()
def build() -> None:
    """Build the project.

    Creates distribution packages (wheel and sdist) using uv build.
    Equivalent to: make build
    """
    console.print("[bold blue]Building project...[/bold blue]")

    result = subprocess.run(
        ["uv", "build"],
        text=True,
    )

    if result.returncode == 0:
        console.print("[bold green]Build complete![/bold green]")

    sys.exit(result.returncode)


@app.command()
def clean() -> None:
    """Remove venv and all build/test artifacts.

    Removes virtual environment, build artifacts, caches, and coverage data.
    Windows-compatible implementation using pathlib and shutil.
    Equivalent to: make clean
    """
    console.print("[bold yellow]Cleaning up...[/bold yellow]")

    artifacts = [
        ".venv",
        "htmlcov",
        ".pytest_cache",
        ".mypy_cache",
        ".ruff_cache",
        ".coverage",
        "dist",
        "build",
    ]

    removed = []
    for artifact in artifacts:
        path = Path(artifact)
        if path.exists():
            try:
                if path.is_dir():
                    shutil.rmtree(path)
                else:
                    path.unlink()
                removed.append(artifact)
            except OSError as e:
                console.print(
                    f"[yellow]Warning: Could not remove {artifact}: {e}[/yellow]"
                )

    if removed:
        console.print(
            f"[bold green]Removed: {', '.join(removed)}[/bold green]"
        )
    else:
        console.print("[bold green]Nothing to clean[/bold green]")


if __name__ == "__main__":  # pragma: no cover
    app()
