# Contributing to Blueprints

Firstly, thank you for considering contributing to Blueprints! Your help is very valuable and it's what makes the open-source community such a
fantastic place to learn, inspire, and create. By contributing to this project, you are helping to advance the field of civil engineering. Engineers
around the world will be thankful for your contribution.

## How to Contribute

### Reporting Bugs

1. **Check existing issues:** Before creating a new issue, please check the existing open and closed issues to see if someone else has had the same
   issue.
2. **File a new issue:** If you're sure your issue is new, open a new issue, providing as much detail as you
   can. [Submit an issue here](https://github.com/Blueprints-org/blueprints/issues).

### Feature Requests

1. **Check existing feature requests:** Before submitting a new feature request, check to see if it has already been discussed.
2. **File a new feature request:** If your idea is new, submit it as a new issue.

### Pull Requests

1. **Fork the Repository:** Fork the project repository and clone your fork to your machine.
2. **Create a new branch:** Create a new branch with a meaningful name.
3. **Make Changes:** Make your code changes, ensuring you adhere to the coding standards and guidelines below.
4. **Run Tests:** Please run tests to make sure your changes don't break existing functionality.
5. **Submit a Pull Request:** Submit your changes as a pull request, providing detailed information in the PR description.

## How to set up your development environment
If you plan to contribute to `blueprints`, you should begin by cloning the repository:

```shell
git clone https://github.com/Blueprints-org/blueprints.git
cd blueprints
```

`blueprints` uses `uv` for python project management. `uv` can be installed with pip:

```shell
pip install uv
```
For other methods check [this](https://docs.astral.sh/uv/getting-started/installation/).

`uv` can then be used to install the latest compatible version of python:

```shell
uv python install 3.13
```

`blueprints` and its development dependencies can be installed with:

```shell
uv sync
```

or if you want to install all optional dependency groups, you can run:
```shell
uv sync --all-groups
```
Refer to the `uv` [documentation](https://docs.astral.sh/uv/) for more information relating to using `uv` for project management.

## How to test the project

### Running Tests
`blueprints` has a comprehensive test suite, and all PR's must introduce and pass appropriate tests. 
Coverage of 100% is also enforced. To run the tests, use pytest:

```shell
uv run pytest
```

### Pre-commit
`blueprints` uses pre-commit hooks to manage code quality, including formatting, linting, and type-safety. 
All PRs must pass the pre-commit hooks, which are run as part of the CI process. 
To install the pre-commit hooks, run:

```shell
uv run pre-commit install
```
This will run `pre-commit` against all changed files when attempting to `git commit`. 
You will need to fix the offending files prior to being able to commit a change unless you run `git commit --no-verify`.

Alternatively, you can run the pre-commit hooks manually against all files:

```shell
pre-commit run --all-files
```

## Building Documentation

`blueprints` uses MkDocs with Material theme for documentation. The documentation is automatically built and deployed to [blueprints.readthedocs.io](https://blueprints.readthedocs.io/en/latest/), but you can build it locally for development and testing.

### Install Documentation Dependencies

To install the documentation dependencies:

```shell
uv sync --group docs
```

### Serve Documentation Locally

To serve the documentation locally with live reload (recommended for development):

```shell
uv run mkdocs serve
```

This will start a local server, typically at `http://127.0.0.1:8000`, where you can view the documentation. The server will automatically reload when you make changes to the documentation files.
The first time you run this command, it will take a few minutes to build the documentation, but subsequent runs will be faster.

### Build Static Documentation

To build the static documentation files:

```shell
uv run mkdocs build
```

This creates a `site/` directory with the built HTML files.

### Documentation Structure

- Documentation source files are located in the `docs/` directory
- Configuration is in `mkdocs.yml`
- The documentation includes auto-generated API reference pages
- Examples are provided as Jupyter notebooks in `docs/examples/`

## Branching Strategy

We use Git flow for our branching strategy. Only create branches from issues/feature requests.

## Checklist for Code Submission

- Python >= 3.12
- All code must be in English
- Max ~400 lines per PR
- Use Typehints and Docstrings (numpy style)
- Add unit tests. (100% coverage is enforced)
- Update the user documentation on the site, if applicable
- Include examples for new features

## Issues

Any contributor can create an issue. No contribution is too small. If you think something is missing or could be improved, please don't hesitate to
submit an issue or a pull request. This is intended to be a central open library for civil engineering, and your input is invaluable.

## Code of Conduct

We enforce a code of conduct for all maintainers and contributors. For more details, check out [Code of Conduct](.github/CODE_OF_CONDUCT.md).

## Contact

For questions, feel free to contact Enrique at [@egarciamendez](https://github.com/egarciamendez) or any other of our maintainers.
