"""Blueprints CLI - Development and build automation commands.

This module provides a cross-platform command-line interface for common
development tasks when working with the Blueprints package.

Commands include environment setup, linting, formatting, type checking,
testing, coverage reporting, and documentation serving.

Start by running `blueprints --help` to see available commands and options.

Do you want to check if your changes are ready for a pull request?
Run `blueprints check` to run all quality checks in sequence.
"""

import shutil
import subprocess
import sys
from importlib.metadata import version
from typing import Annotated, NoReturn

try:
    import typer
    from rich.console import Console
except ImportError:
    print("CLI dependencies not installed.")  # noqa: T201
    print("Install with: uv sync --group cli")  # noqa: T201
    print("Or: pip install blue-prints[cli]")  # noqa: T201
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
        bool | None,
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
    terminal_width = shutil.get_terminal_size(fallback=(80, 24)).columns

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
        raise typer.Exit()  # noqa:RSE102

    # Show help if no command given
    if ctx.invoked_subcommand is None:
        console.print(ctx.get_help())
        raise typer.Exit()  # noqa:RSE102


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
        result = subprocess.run(cmd, check=False, text=True)

        if result.returncode == 0 and success_msg:
            console.print(f"[bold green]{success_msg}[/bold green]")

        sys.exit(result.returncode)

    except FileNotFoundError:
        console.print(f"[bold red]Error: Command not found: {cmd[0]}[/bold red]")
        console.print(f"[yellow]Make sure '{cmd[0]}' is installed and in your PATH[/yellow]")
        sys.exit(1)

    except KeyboardInterrupt:
        console.print("\n[yellow]Interrupted by user[/yellow]")
        sys.exit(130)


# Environment Commands


@app.command(context_settings={"allow_extra_args": True, "ignore_unknown_options": True})
def install(ctx: typer.Context) -> None:
    """Sync all dependencies and create venv if needed.

    Synchronizes all dependency groups. Creates a virtual environment
    automatically if it doesn't exist. Equivalent to: make install

    Parameters
    ----------
    ctx : typer.Context
        Typer context containing additional arguments to pass to uv sync.

    Notes
    -----
    Additional arguments are passed directly to uv sync. Common examples:
    - `--upgrade` : Upgrade all packages to latest versions
    - `--python 3.11` : Use specific Python version
    """
    console.print("[bold blue]Installing all dependencies...[/bold blue]")
    run_command(
        cmd=["uv", "sync", "--locked", "--all-groups", *ctx.args],
        success_msg="Environment setup complete!",
    )


# Code Quality Commands


@app.command(context_settings={"allow_extra_args": True, "ignore_unknown_options": True})
def lint(ctx: typer.Context) -> None:
    """Lint with Ruff.

    Runs Ruff linter to check code style and quality issues.
    Equivalent to: make lint

    Parameters
    ----------
    ctx : typer.Context
        Typer context containing additional arguments to pass to ruff check.

    Notes
    -----
    Additional arguments are passed directly to ruff check. Common examples:
    - `--fix` : Auto-fix detected issues
    - `--select E501` : Check specific rules
    - `--show-fixes` : Show suggested fixes
    """
    console.print("[bold blue]Running Ruff linter...[/bold blue]")
    run_command(["uv", "run", "ruff", "check", ".", *ctx.args])


@app.command(context_settings={"allow_extra_args": True, "ignore_unknown_options": True})
def formatting(ctx: typer.Context) -> None:
    """Format code using Ruff's formatter.

    Parameters
    ----------
    ctx : typer.Context
        Typer context containing additional arguments to pass to ruff format.

    Notes
    -----
    Additional arguments are passed directly to ruff format. Common examples:
    - Add `--check` to only check formatting without making changes; omit it to format files
    - `--line-length 100` : Use specific line length
    """
    console.print("[bold blue]Formatting code with Ruff...[/bold blue]")
    run_command(["uv", "run", "ruff", "format", ".", *ctx.args])


@app.command(context_settings={"allow_extra_args": True, "ignore_unknown_options": True})
def typecheck(ctx: typer.Context) -> None:
    """Run static type checks with mypy.

    Performs static type checking on the blueprints package using mypy.
    Equivalent to: make typecheck

    Parameters
    ----------
    ctx : typer.Context
        Typer context containing additional arguments to pass to mypy.

    Notes
    -----
    Additional arguments are passed directly to mypy. Common examples:
    - `--strict` : Enable strict mode
    - `--ignore-missing-imports` : Ignore missing imports
    - `--show-error-codes` : Show error codes
    """
    console.print("[bold blue]Running mypy type checker...[/bold blue]")
    run_command(["uv", "run", "mypy", "-p", "blueprints", *ctx.args])


# Testing Commands


@app.command(context_settings={"allow_extra_args": True, "ignore_unknown_options": True})
def test(
    ctx: typer.Context,
    light: Annotated[
        bool,
        typer.Option(
            help="Run lightweight tests only, excluding slow tests for rapid iteration.",
        ),
    ] = False,  # noqa: PT028
) -> None:
    """Run tests with pytest.

    Executes tests in parallel using pytest with xdist plugin. Use --light flag
    to skip tests marked as slow for faster iteration during development.
    Equivalent to: make test (or make test-light with --light flag)

    Parameters
    ----------
    ctx : typer.Context
        Typer context containing additional arguments to pass to pytest.
    light : bool
        If True, exclude tests marked as slow for rapid iteration.
        Default is False (run all tests).

    Notes
    -----
    Additional arguments are passed directly to pytest. Common examples:
    - `-k pattern` : Run tests matching pattern
    - `--verbose` : Verbose output
    - `-x` : Stop on first failure
    - `--pdb` : Drop into debugger on failure
    """
    if light:
        console.print("[bold blue]Running lightweight tests...[/bold blue]")
        run_command(
            ["uv", "run", "pytest", "tests/", "-n", "auto", "-m", "not slow", *ctx.args],
        )
    else:
        console.print("[bold blue]Running tests...[/bold blue]")
        run_command(
            ["uv", "run", "pytest", "tests/", "-n", "auto", *ctx.args],
        )


def _run_coverage(ctx_args: list[str], xml: bool = False, html: bool = False, enforce: bool = True) -> int:
    """Helper function to run coverage tests and return exit code.

    Parameters
    ----------
    ctx_args : list[str]
        Pass-through arguments for pytest.
    xml : bool
        If True, also generate XML coverage report for CI/CD integration.
    html : bool
        If True, also generate interactive HTML coverage report in htmlcov/.
    enforce : bool
        If True, enforce 100% coverage requirement.

    Returns
    -------
    int
        Exit code from pytest (0 = success, 1 = failure).
    """
    # Build coverage report formats
    reports = ["term-missing:skip-covered"]
    if xml:
        reports.append("xml")
    if html:
        reports.append("html")

    # Build pytest command
    cmd = ["uv", "run", "pytest", "--cov=./blueprints", "-n", "auto"]

    # Add coverage report formats
    for report_format in reports:
        cmd.extend(["--cov-report", report_format])

    # Add coverage enforcement if requested
    if enforce:
        cmd.append("--cov-fail-under=100")

    # Add pass-through arguments
    cmd.extend(ctx_args)

    result = subprocess.run(cmd, check=False)
    return result.returncode


@app.command(context_settings={"allow_extra_args": True, "ignore_unknown_options": True})
def coverage(
    ctx: typer.Context,
    xml: Annotated[
        bool,
        typer.Option(
            "--xml",
            help="Also generate XML coverage report for CI/CD integration.",
        ),
    ] = False,
    html: Annotated[
        bool,
        typer.Option(
            "--html",
            help="Also generate interactive HTML coverage report in htmlcov/.",
        ),
    ] = False,
    enforce: Annotated[
        bool,
        typer.Option(help="Enforce 100% coverage requirement (enabled by default, use --no-enforce to disable)."),
    ] = True,
) -> None:
    """Run tests and generate coverage reports.

    Executes tests with coverage reporting. By default, enforces 100% coverage
    and displays terminal report. Use --xml and/or --html to generate additional
    report formats. Use --no-enforce to generate reports without 100% coverage enforcement.

    Parameters
    ----------
    ctx : typer.Context
        Typer context containing additional arguments to pass to pytest.
    xml : bool
        If True, also generate XML coverage report for CI/CD integration.
    html : bool
        If True, also generate interactive HTML coverage report in htmlcov/.
    enforce : bool
        If False, generate coverage reports without enforcing 100% coverage requirement.

    Notes
    -----
    Additional arguments are passed directly to pytest.
    """
    console.print("[bold blue]Running tests with coverage...[/bold blue]")

    exit_code = _run_coverage(ctx.args, xml=xml, html=html, enforce=enforce)

    # Print completion messages
    if html:
        console.print("[bold green]HTML report generated in htmlcov/[/bold green]")
    if enforce and exit_code == 0:
        console.print("[bold green]Coverage check passed![/bold green]")

    sys.exit(exit_code)


# Quality Assurance Commands


@app.command()
def check() -> None:  # noqa: PLR0915
    """Run all quality checks before making a PR.

    Runs lint, format check, type checking, and coverage validation in sequence.
    This is the recommended command to run before creating a pull request.

    Notes
    -----
    Runs the following checks in order:
    1. Lint with Ruff
    2. Format check with Ruff
    3. Type checking with mypy
    4. Coverage validation with pytest

    Raises
    ------
    SystemExit
        Exits with non-zero code if any check fails.
    """
    console.print("[bold cyan]" + "=" * 60 + "[/bold cyan]")
    console.print("[bold cyan]Running comprehensive quality checks...[/bold cyan]")
    console.print("[bold cyan]" + "=" * 60 + "[/bold cyan]")

    checks_passed = []
    checks_failed = []

    # 1. Lint
    console.print("\n[bold blue]1. Linting with Ruff...[/bold blue]")
    try:
        result = subprocess.run(
            args=["uv", "run", "ruff", "check", "."],
            capture_output=False,
            text=True,
            check=False,
        )
        if result.returncode == 0:
            checks_passed.append("Lint")
            console.print("[bold green]Lint: PASSED[/bold green]")
        else:
            checks_failed.append("Lint")
            console.print("[bold red]Lint: FAILED[/bold red]")
    except FileNotFoundError:
        console.print("[bold red]Error: 'uv' not found[/bold red]")
        sys.exit(1)

    # 2. Format check
    console.print("\n[bold blue]2. Checking formatting with Ruff...[/bold blue]")
    result = subprocess.run(
        args=["uv", "run", "ruff", "format", ".", "--check"],
        capture_output=False,
        text=True,
        check=False,
    )
    if result.returncode == 0:
        checks_passed.append("Format")
        console.print("[bold green]Format: PASSED[/bold green]")
    else:
        checks_failed.append("Format")
        console.print("[bold red]Format: FAILED (Use `blueprints formatting` to auto-format files)[/bold red]")

    # 3. Type check
    console.print("\n[bold blue]3. Running type checks with mypy...[/bold blue]")
    result = subprocess.run(
        args=["uv", "run", "mypy", "-p", "blueprints"],
        capture_output=False,
        text=True,
        check=False,
    )
    if result.returncode == 0:
        checks_passed.append("Type Check")
        console.print("[bold green]Type Check: PASSED[/bold green]")
    else:
        checks_failed.append("Type Check")
        console.print("[bold red]Type Check: FAILED[/bold red]")

    # 4. Coverage
    console.print("\n[bold blue]4. Checking code coverage...[/bold blue]")
    exit_code = _run_coverage(ctx_args=[], xml=False, html=True, enforce=True)
    if exit_code == 0:
        checks_passed.append("Coverage")
        console.print("[bold green]Coverage: PASSED[/bold green]")
        console.print("[bold green]HTML report generated in htmlcov/[/bold green]")
    else:
        checks_failed.append("Coverage")
        console.print("[bold red]Coverage: FAILED[/bold red]")

    # Summary
    console.print("\n[bold cyan]" + "=" * 60 + "[/bold cyan]")
    console.print("[bold cyan]Quality Check Summary[/bold cyan]")
    console.print("[bold cyan]" + "=" * 60 + "[/bold cyan]")

    if checks_passed:
        console.print(f"[bold green]Passed ({len(checks_passed)}): {', '.join(checks_passed)}[/bold green]")

    if checks_failed:
        console.print(f"[bold red]Failed ({len(checks_failed)}): {', '.join(checks_failed)}[/bold red]")
        sys.exit(1)
    else:
        console.print("[bold green]All checks passed! Ready for PR.[/bold green]")
        sys.exit(0)


@app.command()
def docs() -> None:
    """Serve documentation locally with live reload.

    Starts MkDocs development server with live reload enabled.
    Documentation will be available at http://localhost:8000

    Notes
    -----
    Press Ctrl+C to stop the server.
    The browser will automatically refresh when docs are updated.

    Raises
    ------
    SystemExit
        Exits with code returned by mkdocs serve command.
    """
    console.print("[bold blue]Starting documentation server...[/bold blue]")
    console.print("[bold green]Documentation available at http://localhost:8000[/bold green]")
    console.print("[bold yellow]Press Ctrl+C to stop the server[/bold yellow]")
    run_command(["uv", "run", "mkdocs", "serve", "--livereload"])


if __name__ == "__main__":  # pragma: no cover
    app()
