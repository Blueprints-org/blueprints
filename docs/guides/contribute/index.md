# Contributing to Blueprints

Firstly, thank you for considering contributing to Blueprints! Your help is very valuable, and it's what makes the open-source community such a
fantastic place to learn, inspire, and create. By contributing to this project, you are helping to advance the field of civil engineering. Engineers
around the world will be thankful for your contribution.

## Can I Contribute?

Yes! We have oportunities for contributors of all skill levels. Whether you're a seasoned developer, a civil engineer with coding skills.

**Whether you're new to open source or an experienced contributor, there's a place for you here.**

When you are new to open source, it can be daunting to know where to start. We are here to help!
We have some [advice for first-time contributors](first-time-contributors.md) to help you get past any initial doubts and fears you may have.

## What can I do?

There are many ways to contribute to Blueprints. Here are some common ways you can help out:

<div class="grid cards" markdown>

- **Fix an issue**

    ---
    
    The most direct way to contribute is to write code to fix an existing issue.
    
    [➡ Browse issues](https://github.com/Blueprints-org/blueprints/issues)

- **Implement a new Feature**

    ---
    
    Would like that Blueprints does something new, and you have the skills to implement it? Go for it!
    

- **Report a Bug**

    ---
    
    Found something that doesn't work? Help us fix it.
    
    [➡ Report an issue](https://github.com/Blueprints-org/blueprints/issues/new?template=bug_report.yml)

- **Request a Feature**

    ---
    
    Have an idea for a new formula or feature?
    
    [➡ Submit a request](https://github.com/Blueprints-org/blueprints/issues/new?template=feature_request.yml)

- **Improve Documentation**

    ---
    
    Fix typos, clarify explanations, add examples.
    
    [➡ Find documentation issues](https://github.com/Blueprints-org/blueprints/issues?q=is%3Aopen+label%3Adocumentation)

</div>

Once you've chosen what to work on, you are ready to set up your development environment.

## How to set up your development environment

If you plan to contribute to Blueprints, you should begin by cloning the repository:

```terminal
git clone https://github.com/Blueprints-org/blueprints.git
cd blueprints
```

Blueprints uses `uv` for python project management. 

It can be installed via pip:

```terminal
pip install uv
```
For other methods check [this](https://docs.astral.sh/uv/getting-started/installation/).

`uv` can then be used to install the latest compatible version of python:

```terminal
uv python install 3.13
```

Blueprints and its development dependencies can be installed with:

```terminal
uv sync --all-groups
```

Refer to the `uv` [documentation](https://docs.astral.sh/uv/) for more information relating to using `uv` for project management.

## How to test the project

### Running Tests

Blueprints has a comprehensive test suite, and all PR's must introduce and pass appropriate tests. 
Coverage of 100% is also enforced. To run the tests, use our own [Blueprints CLI tool](cli.md):

```terminal
bp coverage
```

### Pre-commit

Blueprints uses pre-commit hooks to manage code quality, including formatting, linting, and type-safety. 
All PRs must pass the pre-commit hooks, which are run as part of the CI process. 
To install the pre-commit hooks, run:

```terminal
uv run pre-commit install
```
This will run `pre-commit` against all changed files when attempting to `git commit`. 
You will need to fix the offending files prior to being able to commit a change unless you run `git commit --no-verify`.

Alternatively, you can run the pre-commit hooks manually against all files:

```terminal
pre-commit run --all-files
```

## Building Documentation

Blueprints uses MkDocs with Material theme for documentation. The documentation is automatically built and deployed to [blueprints.readthedocs.io](https://blueprints.readthedocs.io), but you can build it locally for development and testing using:

```terminal
bp docs
```

This will start a local server, typically at `http://localhost:8000`, where you can view the documentation. The server will automatically reload when you make changes to the documentation files.
The first time you run this command, it will take a few minutes to build the documentation, but subsequent runs will be faster.

## Checklist for Code Submission

- Python >= 3.12
- All code must be in English
- Max ~400 lines per PR
- Use Typehints and Docstrings (numpy style)
- Add unit tests. (100% coverage is enforced)
- Update the user documentation on the site, if applicable
- Include examples for new features

## Code of Conduct

We enforce a code of conduct for all maintainers and contributors. For more details, check out [Code of Conduct](https://github.com/Blueprints-org/blueprints/blob/main/.github/CODE_OF_CONDUCT.md).

## Contact

For questions, feel free to contact Enrique at [@egarciamendez](https://github.com/egarciamendez) or any other of our maintainers.
