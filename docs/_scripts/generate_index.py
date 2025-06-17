"""Generate the index page using the README.md file and fixing the cross links."""

import re
from pathlib import Path

import mkdocs_gen_files

root = Path(__file__).parents[2]
readme_file = root / "README.md"


def replace_links(readme_content: str) -> str:
    """Replace the relative links to the overview page by removing the .md extension."""
    readme_content = readme_content.replace("docs/", "")
    # replace the relative links to the overview page by removing the .md extension
    readme_content = re.sub(r"/\w+\.md", lambda match: match.group(0)[:-3], readme_content)
    # replace blueprints/code references by links to the API reference
    readme_content = readme_content.replace('"blueprints/codes', '"API reference/codes')
    # add 'https://github.com/Blueprints-org/blueprints' prefix to file in [link](file) if file is not a URL
    return re.sub(r"\[([^\]]+)\]\((?!http)([^)]+)\)", r"[\1](https://github.com/Blueprints-org/blueprints/blob/main/\2)", readme_content)


with open(readme_file, encoding="utf-8") as fd:
    readme_content = fd.read()
    readme_content = replace_links(readme_content)
    # remove the read the docs chapter, we're already in the docs
    readme_content = re.sub(r"## Read the docs!\n\n.*\n## Quick", "## Quick", readme_content, flags=re.DOTALL)

with mkdocs_gen_files.open("index.md", "w") as fd:
    # hide navigation in the index page
    fd.writelines(["---\n", "hide:\n", "  - navigation\n", "---\n"])
    fd.write(readme_content)
