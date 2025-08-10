"""Generate downloadable Python code files from Jupyter notebooks."""

import json
from pathlib import Path

import mkdocs_gen_files


def extract_code_from_notebook(notebook_path: Path) -> str:
    """Extract all Python code cells from a Jupyter notebook.

    Parameters
    ----------
    notebook_path : Path
        Path to the notebook file.

    Returns
    -------
    str
        Combined Python code from all code cells.
    """
    with open(notebook_path, encoding="utf-8") as f:
        notebook = json.load(f)

    code_lines = []

    # Add a header comment
    code_lines.append(f"# Code automatically extracted from {notebook_path.name}.\n")

    for cell in notebook.get("cells", []):
        if cell.get("cell_type") == "code":
            source = cell.get("source", [])
            if source:
                # Join source lines if it's a list, otherwise use as is
                cell_code = "".join(source) if isinstance(source, list) else source

                # Skip empty cells or cells with only whitespace
                if cell_code.strip():
                    code_lines.append(cell_code)
                    # Add spacing between cells
                    if not cell_code.endswith("\n"):
                        code_lines.append("\n")
                    code_lines.append("\n")

    # removes trailing whitespace and ensures a single newline at the end
    return "".join(code_lines).rstrip() + "\n"


def main() -> None:
    """Generate Python code files from all Jupyter notebooks in docs."""
    root = Path(__file__).parents[2]
    docs_dir = root / "docs"

    # Find all notebook files recursively in docs
    notebook_files = list(docs_dir.rglob("*.ipynb"))

    for notebook_path in notebook_files:
        # Extract code from notebook
        code_content = extract_code_from_notebook(notebook_path)

        # Calculate relative path from docs directory
        relative_path = notebook_path.relative_to(docs_dir)

        # Generate corresponding .py file path preserving directory structure
        py_filename = notebook_path.stem + ".py"
        output_path = relative_path.parent / notebook_path.stem / py_filename

        # Write the extracted code to a .py file
        with mkdocs_gen_files.open(output_path, "w") as f:
            f.write(code_content)

        print(f"Generated {output_path} from {relative_path}")


main()
