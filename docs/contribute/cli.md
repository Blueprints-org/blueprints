# Developer CLI Guide

Blueprints includes a command-line interface for development automation, trying to simplify developing and contributing to the project.

## Installation

Install the CLI with its dependencies:

```bash
# Using uv
uv sync --group cli

# Or using pip with extras
pip install blue-prints[cli]

```

## Available Commands

### Environment Setup

**`blueprints install`**

- Sync all dependencies (creates venv automatically if needed)
- Supports pass-through args: `--upgrade`, `--python 3.13`, etc.
- Example: `blueprints install --upgrade`

### Quality Assurance

**`blueprints check`** (Recommended before PR)

- Run all quality checks in sequence: lint, format, typecheck, coverage
- Provides detailed summary of which checks passed/failed
- Exits with code 0 on success, 1 on any failure (CI-friendly)
- Continues all checks even if one fails (full visibility)
- Supports pass-through args: `-x` (stop on first test failure), `-k pattern` (filter tests)
- Example: `blueprints check`


### Code Quality

**`blueprints lint`**

- Run Ruff linter for code style and quality checks
- Supports pass-through args: `--fix`, `--select E501`, `--show-fixes`
- Example: `blueprints lint --fix`

**`blueprints format`**

- Check code formatting compliance with Ruff
- Note: Uses `--check` by default (only validates, doesn't modify)
- Supports pass-through args: `--line-length 100`
- Example: `blueprints format --line-length 100`

**`blueprints typecheck`**

- Run mypy static type checker on blueprints package
- Supports pass-through args: `--strict`, `--ignore-missing-imports`, `--show-error-codes`
- Example: `blueprints typecheck --strict`

### Testing

**`blueprints test`**

- Run all tests in parallel using pytest with xdist
- Use `--light` flag to skip slow tests for rapid iteration
- Supports pass-through args: `-k pattern`, `--verbose`, `-x`, `--pdb`, `--light`
- Example: `blueprints test -k test_cli --verbose`
- Example: `blueprints test --light` (fast tests only)

**`blueprints coverage`**

- Run tests with coverage reporting and enforce 100% coverage by default
- Generate terminal report with missing coverage details
- Use `--xml` to also generate XML coverage report for CI/CD integration
- Use `--html` to also generate interactive HTML coverage report in `htmlcov/`
- Use `--no-check` to generate reports without enforcing 100% coverage
- Supports pass-through args
- Examples:
  - `blueprints coverage` - Terminal report with 100% enforcement
  - `blueprints coverage --xml` - Terminal + XML reports with enforcement
  - `blueprints coverage --html` - Terminal + HTML reports with enforcement
  - `blueprints coverage --xml --html` - All three formats with enforcement
  - `blueprints coverage --no-check` - Reports without 100% enforcement

### Documentation

**`blueprints docs`**

- Serve documentation locally with live reload
- Opens documentation server at http://localhost:8000
- Browser automatically refreshes when docs are updated
- Perfect for working on documentation
- Press Ctrl+C to stop the server
- Example: `blueprints docs`

## Pre-PR Workflow

Before submitting a pull request, run:

```bash
blueprints check
```

This single command validates all aspects of your changes:

1. **Linting** - Code style and quality checks with Ruff
2. **Formatting** - Code formatting compliance with Ruff
3. **Type Checking** - Static type validation with mypy
4. **Coverage** - Code coverage validation and HTML report generation

### Success Output

```
============================================================
Running comprehensive quality checks...
============================================================

1. Linting with Ruff...
Lint: PASSED

2. Checking formatting with Ruff...
Format: PASSED

3. Running type checks with mypy...
Type Check: PASSED

4. Checking code coverage...
Coverage: PASSED
HTML report generated in htmlcov/

============================================================
Quality Check Summary
============================================================
Passed (4): Lint, Format, Type Check, Coverage
All checks passed! Ready for PR.
```

### Failure Output

If any check fails, the command will show which ones failed and exit with code 1:

```
============================================================
Quality Check Summary
============================================================
Passed (3): Lint, Format, Type Check
Failed (1): Coverage
```

## Pass-Through Arguments

All CLI commands support passing additional arguments to the underlying tools. This allows you to access tool-specific options without waiting for CLI updates.

### Install with Flags

```bash
blueprints install --upgrade            # Upgrade all packages to latest versions
blueprints install --python 3.13        # Use specific Python version
```

### Test with pytest Flags

```bash
blueprints test -k test_specific        # Run tests matching pattern
blueprints test --verbose --pdb         # Verbose output with debugger
blueprints test -x                      # Stop on first failure
blueprints test --light -k test_fast    # Fast tests with pattern filter
blueprints test --light                 # Skip slow tests for rapid iteration
```

### Lint with Ruff Flags

```bash
blueprints lint --fix                   # Auto-fix detected issues
blueprints lint --select E501           # Check specific rules
blueprints lint --show-fixes            # Show suggested fixes
```

### Format with Ruff Flags

```bash
blueprints format --line-length 100     # Use specific line length
```

### Type Checking with mypy Flags

```bash
blueprints typecheck --strict           # Enable strict mode
blueprints typecheck --show-error-codes # Show error codes
blueprints typecheck --ignore-missing-imports  # Ignore missing imports
```

### Build with Flags

```bash
blueprints build --sdist                # Build only source distribution
blueprints build --wheel                # Build only wheel
blueprints build --out-dir dist         # Specify output directory
```

### Coverage with Options and pytest Flags

```bash
blueprints coverage                     # Terminal report with 100% enforcement
blueprints coverage --xml               # Also generate XML report
blueprints coverage --html              # Also generate HTML report
blueprints coverage --xml --html        # Generate all three formats
blueprints coverage --no-check          # Skip 100% coverage enforcement
blueprints coverage -k test_pattern     # Filter tests by pattern
```

### Check with pytest Flags

```bash
blueprints check -x                     # Stop on first test failure
blueprints check -k test_pattern        # Filter tests by pattern
```

## Version Information

Check the CLI version:

```bash
blueprints --version
# or
blueprints -v
```

## Help

For more information:

```bash
blueprints --help              # Show general help
blueprints <command> --help    # Show command-specific help
```

## Requirements

The CLI requires `uv` to be installed. If not present, you'll see a warning message with installation instructions.

Install `uv`:
```bash
pip install uv
# or visit https://github.com/astral-sh/uv
```

## Make vs CLI

Both tools are available and equivalent:

- **Make**: Stable interface for CI/CD pipelines
- **CLI**: Cross-platform developer tool (works on Windows without Make)

```bash
# These are equivalent:
make test
blueprints test

```

## Features

- **Cross-platform**: Works on Windows, macOS, and Linux
- **Pass-through arguments**: Access all underlying tool features
- **Flexible**: Supports all uv, pytest, ruff, and mypy options
- **Future-proof**: New tool features automatically available
- **Windows-compatible**: No shell dependencies, pure Python implementation
- **Rich output**: Colored terminal output for better readability
- **CI-friendly**: Proper exit codes for automation

## Troubleshooting

### "Error: 'uv' not found"

Install `uv`:
```bash
pip install uv
```

### CLI dependencies not found

Install with CLI group:
```bash
# With pip
pip install blue-prints[cli]

# With uv
uv sync --group cli
```

### Tests fail with "No module named pytest"

The `test` group is not installed. Reinstall:
```bash
uv sync --group test
```
