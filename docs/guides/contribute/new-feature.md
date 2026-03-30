# Introducing New Features

We welcome contributions that improve the library, but new features must follow a clear review and approval process.

??? question "What constitutes a new feature?"
    A new feature is any addition or change without prior discussion or precedent, including:

    * New functionality
    * New public interfaces
    * Breaking and non-breaking changes to existing functionality or APIs
    * Changes to the library's architecture or design

    #### What does not constitute a new feature:
    * Adding a new formula, a new type of steel profile or a new concrete grade is not considered a new feature, as long as it follows the existing interfaces and design.


## Proposal and Approval Process

### 1. Propose Before You Build

All new features must be discussed with the core team *before* any implementation work begins. This ensures alignment with the project’s goals, design principles, and roadmap.

???+ note "Open a Proposal issue containing:"

    * The problem your feature solves
    * Proposed interface or API design
    * High-level implementation approach
    * Possible alternatives considered

??? info "Example of a proposal issue"

    **Introduce a universal `CheckProtocol` for structural checks**

    **Problem Statement**

    There are currently no standardized interfaces for checks in the library. This leads to inconsistencies and makes the integration and maintenance of checks very difficult, especially when they are implemented as duck-typed classes without inheriting from a common base class.

    **Proposed design**

    A `CheckProtocol` (structural subtyping via `typing.Protocol`) defining the minimal interface any check must implement.

    **Implementation Approach**

    - Define `CheckProtocol` as a `@runtime_checkable` Protocol in `blueprints/checks/`.

    ```python
    class CheckProtocol(Protocol):
        name: str

        @staticmethod
        def source_docs() -> list[str]: ...
        def subchecks(self) -> dict[str, CheckProtocol]: ...
        def result(self) -> CheckResult: ...
        def report(self, n: int) -> Report: ...
    ```

    **Alternatives Considered**

    - Using the ABC-only approach, which would require all checks to inherit from a common base class, was considered less favorable due to the flexibility and simplicity of structural subtyping with Protocols.


??? tip "Proposal content"

    When writing your proposal, you may include any content that you think would help the core team understand your proposal and make an informed decision. For example:

    - [Mermaid diagrams](https://mermaid.js.org/)
    - Pseudocode
    - Examples of usage
    - Links to related work or research
    - Link to a prototype implementation (if you have one)

### 2. Get Core Team Consensus

The core team will discuss and review the proposal in bi-weekly meetings, providing feedback and requesting clarifications as needed.

???+ note "Before implementation, the core team must reach consensus on:"

    * Whether the feature aligns with the project’s vision and roadmap
    * The feature scope
    * The public interface
    * The implementation strategy
    * Potential reviewers for the eventual PR

??? question "What does consensus mean?"
    The approval process is based on consensus, which means that all core team members must agree on the proposal before it can be implemented. If there is a disagreement, the core team will discuss the proposal further until a consensus is reached.


??? info "Core Team"
    The core team is responsible for reviewing and approving new feature proposals. The current core team members are:

    - Gerjan Dorgelo ([@GerjanDorgelo](https://github.com/GerjanDorgelo))
    - Wichard Bron ([@bro-wi](https://github.com/bro-wi))
    - Enrique García Méndez ([@egarciamendez](https://github.com/egarciamendez))
    - Sina Zel taat ([@SZeltaat](https://github.com/SZeltaat))


### 3. Implement the Approved Design and Submit a PR

Once approved, your implementation should adhere to the agreed interface and design.

* For complex features:
    - the implementation steps must be discussed with the potential reviewers.
    - The implementation should be broken down into smaller, manageable PRs that can be reviewed and merged incrementally. See this [example](https://github.com/Blueprints-org/blueprints/issues/734)
* Significant deviations require additional discussion.
* When submitting your PR, please reference the original proposal issue.

??? question "When is a feature considered complex?"
    A complex feature is one that involves significant changes to the library’s architecture, design, or public API. Examples include:

    * Introducing a new core component or module
    * Significant refactoring of existing code
    * Changes that affect multiple parts of the library
    * Changes that require updates to documentation, examples, and tests across the library
    * Changes that surpass the 400 lines of code threshold (added + removed) in a single PR


## Automated Code and AI

You are encouraged to use all the tools you want to do your work and contribute as efficiently as possible, this includes AI (LLM) tools, etc. Nevertheless, contributions should have meaningful human intervention, judgement, context, etc.

If your contribution contains code generated by AI you must make sure that you yourself have reviewed all changes in your pull request, and believe that they are relevant and correct.

*"If the human effort put in a PR, e.g. writing LLM prompts, is less than the effort we would need to put to review it, please don't submit the PR. Think of it this way: we can already write LLM prompts or run automated tools ourselves, and that would be faster than reviewing external PRs."*  [Source: FastAPI contributing guidelines](https://fastapi.tiangolo.com/contributing/#automated-code-and-ai).


## Implementation strategy
The core team must agree on an implementation strategy. Any implementation strategy should meet the following requirements:

???+ note "Integrability and Backward Compatibility"
    The new feature should integrate cleanly with the existing architecture and design. While backward compatibility is desirable, it must not come at the cost of a coherent and maintainable design.

???+ note "Maintainability"
    The code should be maintainable in the long term.

???+ note "Dependencies"
    The implementation should minimize external dependencies and ensure that any new dependencies are well-maintained and compatible with the project's goals.

???+ note "Technical considerations"
    The following technical considerations should be taken into account when designing the implementation:

    - Design Patterns (e.g. Factory, Builder, Strategy, Singleton, etc.)
    - ABC vs. Protocols
    - Inheritance vs. Composition
    - Mutability (e.g. immutable data structures, frozen dataclasses, etc.)
    - Naming conventions (e.g. class names, method names, variable names, etc.)
    - Module organization (e.g. where to place new code, how to structure the modules, etc.)
    - Performance implications (e.g. time complexity, space complexity, etc.)
    - ...
