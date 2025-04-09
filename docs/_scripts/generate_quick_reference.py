"""Generate the quick reference page using the README.md file and fixing the cross links."""

import re
from pathlib import Path

import mkdocs_gen_files

root = Path(__file__).parents[2]
readme_file = root / "README.md"


def replace_links(readme_content: str) -> str:
    """Replace the relative links to the overview page by removing the .md extension."""
    readme_content = readme_content.replace("docs/objects_overview/", "")
    # replace the relative links to the overview page by removing the .md extension
    readme_content = re.sub(r"/\w+\.md", lambda match: match.group(0)[:-3], readme_content)
    # replace blueprints/code references by links to the API reference
    readme_content = readme_content.replace('"blueprints/codes', '"../API reference/codes')
    # add 'https://github.com/Blueprints-org/blueprints' prefix to file in [link](file) if file is not a URL
    return re.sub(r"\[([^\]]+)\]\((?!http)([^)]+)\)", r"[\1](https://github.com/Blueprints-org/blueprints/blob/main/\2)", readme_content)


with open(readme_file, encoding="utf-8") as fd:
    ## extract the  ## Quick Reference to Blueprint's Objects section
    readme_content = fd.read()
    pattern = re.compile(r"## Quick Reference to Blueprint's Objects.*?(?=## )", re.DOTALL)

    match = pattern.search(readme_content)

    if match:
        quick_reference_content = match.group(0).replace("##", "#")
        quick_reference_content = replace_links(quick_reference_content)
    else:
        raise ValueError("No match found for reference table")

with mkdocs_gen_files.open("objects_overview/index.md", "w") as fd:
    # hide navigation in the index page
    fd.write(quick_reference_content)
