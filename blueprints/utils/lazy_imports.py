"""Functions related to lazy importing."""

import importlib
import re
from types import ModuleType
from typing import List


def lazy_import_get_attr(_package: str, _name: str, _chapters: List[str]) -> ModuleType:
    """Function overrides the getattr for using modules, to allow for lazy importing.

    This is used as (for example):
    Normally:
    > from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_3_materials.formula_3_1 import (
    >   Form3Dot1EstimationConcreteCompressiveStrength
    > )

    With lazy importing this is also possible:
    > import blueprints.codes.en_1992_1_1_2004 as en
    > formula = en.Form3Dot7NonLinearCreepCoefficient(10, 5)

    Then en.Form will not be an import, but a getattr call, which is overridden in en_1992_1_1_2004/__init__.py.

    This function will parse the Form3Dot7... in regex, to retrieve 3 and 7, which are used to get the chapter module
    and the formula submodule, and then load in the function from there.

    Args:
        _package (str): The __package__ name, used for the import.
        _name (str): The __name__ coming from e.g. en_1992_1_1_2004.
        _chapters (list[str]): A list of submodules names, often coming from __all__.
    """
    # Parse the given Form name, to get the path to it
    match = re.match(r"(Form|SubForm|Table)(\d+|[a-zA-Z])Dot(\w+)", _name)
    if match:
        formula_type, chapter, rest = match.groups()
        num_match = re.match(r"((?:\d+And)*\d+)([a-z]*)([A-Z]\w*)", rest)
        if not num_match:
            raise AttributeError(f"module {_package} has no attribute {_name}")
        number_part, prefix, suffix = num_match.groups()
        formula_numbers = "_".join(number_part.split("And"))

        # get the right sub_module, based on the pattern. Pattern is always chapter_3_... or annex_a...
        if chapter.isdigit():
            pattern = re.compile(rf"chapter_{chapter}(_|$)")
            result = next((c for c in _chapters if pattern.search(c)), None)
        else:
            pattern = re.compile(rf"annex_{chapter.lower()}(_|$)")
            result = next((c for c in _chapters if pattern.search(c)), None)

        if formula_type == "Table":
            module_name = f"{result}.table_{chapter.lower()}_{formula_numbers}"
        else:
            module_name = f"{result}.formula_{chapter.lower()}_{formula_numbers}"

            # If name of the formula starts with an capital N and next character is upper (name check); add n
            if prefix:
                module_name += f"{prefix}"

        try:
            module = importlib.import_module(f".{module_name}", _package)
            return getattr(module, _name)
        except (ImportError, AttributeError):
            raise AttributeError(f"module {_package} has no attribute {_name}")
    raise AttributeError(f"module {_package} has no attribute {_name}")
