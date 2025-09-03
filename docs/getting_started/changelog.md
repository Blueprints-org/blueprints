# Changelog and versioning
## Versioning

Blueprints follows a pragmatic pre-1.0.0 versioning scheme:

- Minor version (X.Y.Z → X.(Y+1).0): increased for breaking changes.
- Patch version (X.Y.Z → X.Y.(Z+1)): increased for bug fixes, enhancements, and other non-breaking changes.

Once Blueprints reaches v1.0.0, we intend to follow Semantic Versioning. See https://semver.org/ for details.

> Note
> Until v1.0.0, we may group breaking changes into clearly marked minor releases to keep iteration fast and predictable.

## Changelog

All release notes are maintained on GitHub:

- Blueprints changelog (GitHub Releases): https://github.com/Blueprints-org/blueprints/releases

Each release includes a summary of changes, with highlights for any breaking changes.

## Minimum supported Python version


The minimum supported Python version is defined in `pyproject.toml` under `requires-python`.

- Current requirement: `>=3.12`
- This minimum may change in a minor or patch release when required by the project.

### Using lower Python versions

You may attempt to use Blueprints with a lower Python version, but this is not supported or guaranteed to work. If you choose to do so, you must build the package from source. We cannot provide support or fixes for issues encountered on unsupported Python versions.