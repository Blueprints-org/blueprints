from __future__ import annotations

import ast
import importlib.util
import inspect
from enum import Enum
from pathlib import Path

##################################################################################
# Stub file generation functions for StandardProfileMeta classes                #
##################################################################################


def _extract_class_and_database_info(file_path: Path) -> dict[str, tuple[str, str, str]] | None:  # noqa: C901, PLR0912
    """Extract class name, factory type, and database variable from a Python file.

    Analyzes a Python file using AST to find classes that use StandardProfileMeta
    and extracts their _factory and _database information.

    Parameters
    ----------
    file_path : Path
        Path to the Python file to analyze.

    Returns
    -------
    dict[str, tuple[str, str, str]] | None
        Dictionary mapping class names to tuples of (factory_class_name, database_var_name, factory_module).
        Returns None if no StandardProfileMeta classes are found or if the file cannot be parsed.

    Examples
    --------
    >>> result = _extract_class_and_database_info(Path("chs.py"))
    >>> result
    {'CHS': ('CHSProfile', 'CHS_PROFILES', 'blueprints.structural_sections.steel.profile_definitions.chs_profile')}

    """
    try:
        with file_path.open() as f:
            tree = ast.parse(f.read(), filename=str(file_path))
    except Exception:
        return None

    result = {}
    imports = {}

    # First pass: collect imports
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom):
            module = node.module or ""
            for alias in node.names:
                imports[alias.asname or alias.name] = f"{module}.{alias.name}" if module else alias.name

    # Second pass: find classes with StandardProfileMeta
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            # Check if class uses StandardProfileMeta
            for keyword in node.keywords:
                if keyword.arg == "metaclass" and isinstance(keyword.value, ast.Name) and keyword.value.id == "StandardProfileMeta":
                    # Extract _factory and _database
                    factory = None
                    database = None
                    factory_full_path = None

                    for item in node.body:
                        if isinstance(item, ast.Assign):
                            for target in item.targets:
                                if isinstance(target, ast.Name):
                                    if target.id == "_factory" and isinstance(item.value, ast.Name):
                                        factory = item.value.id
                                        factory_full_path = imports.get(factory, factory)
                                    elif target.id == "_database" and isinstance(item.value, ast.Name):
                                        database = item.value.id

                    if factory and database and factory_full_path:
                        result[node.name] = (factory, database, factory_full_path)

    return result if result else None


def _load_module_from_file(file_path: Path) -> object | None:
    """Dynamically load a Python module from a file path.

    Parameters
    ----------
    file_path : Path
        Path to the Python file to load.

    Returns
    -------
    object | None
        The loaded module object, or None if loading fails.

    """
    try:
        spec = importlib.util.spec_from_file_location(file_path.stem, file_path)
        if spec is None or spec.loader is None:
            return None
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
    except Exception:
        return None
    else:
        return module


def _get_factory_return_type(factory_full_path: str) -> str:
    """Get the return type annotation for a factory class.

    Parameters
    ----------
    factory_full_path : str
        Full import path to the factory class (e.g., 'module.submodule.ClassName').

    Returns
    -------
    str
        The return type as a string suitable for use in stub files.
        Returns the factory class name if it cannot be determined.

    """
    parts = factory_full_path.rsplit(".", 1)
    if len(parts) == 2:
        return parts[1]
    return factory_full_path


def generate_stub_for_file(
    source_file: Path,
    stub_file: Path | None = None,
) -> bool:
    """Generate a .pyi stub file for a standard profile module.

    Analyzes a Python module that uses StandardProfileMeta and generates
    a corresponding stub file with proper type hints for all profile attributes.

    Parameters
    ----------
    source_file : Path
        Path to the source .py file to generate stubs for.
    stub_file : Path | None, optional
        Path where the stub file should be saved. If None, will create a .pyi
        file with the same name as source_file in the same directory.

    Returns
    -------
    bool
        True if stub generation was successful, False otherwise.

    Examples
    --------
    >>> generate_stub_for_file(Path("chs.py"))
    True
    # Creates chs.pyi with all CHS profile attributes properly typed

    """
    if stub_file is None:
        stub_file = source_file.with_suffix(".pyi")

    # Extract class and database information from AST
    class_info = _extract_class_and_database_info(source_file)
    if not class_info:
        return False

    # Load the module to get the actual database
    module = _load_module_from_file(source_file)
    if module is None:
        return False

    stub_lines = []

    # Generate imports for each factory class
    factory_imports = {}
    for class_name, (factory, database, factory_full_path) in class_info.items():
        parts = factory_full_path.rsplit(".", 1)
        if len(parts) == 2:
            module_path, class_name_only = parts
            if module_path not in factory_imports:
                factory_imports[module_path] = []
            if class_name_only not in factory_imports[module_path]:
                factory_imports[module_path].append(class_name_only)

    # Write imports
    for module_path, classes in sorted(factory_imports.items()):
        classes_str = ", ".join(sorted(classes))
        stub_lines.append(f"from {module_path} import {classes_str}")

    stub_lines.append("")

    # Generate class stubs
    for class_name, (factory, database, factory_full_path) in class_info.items():
        return_type = _get_factory_return_type(factory_full_path)

        # Get the database dictionary from the module
        database_dict = getattr(module, database, {})

        stub_lines.append(f"class {class_name}:")

        # Generate class attributes for each profile in the database
        for profile_name in database_dict:
            stub_lines.append(f"    {profile_name}: {return_type}")  # noqa: PERF401

        stub_lines.append("")

    # Write stub file
    stub_file.write_text("\n".join(stub_lines))
    return True


def generate_all_stubs(
    profiles_dir: Path | str | None = None,
    force_regenerate: bool = False,
) -> dict[str, bool]:
    """Generate stub files for all standard profile modules in a directory.

    Scans a directory for Python files that use StandardProfileMeta and generates
    corresponding .pyi stub files for each one.

    Parameters
    ----------
    profiles_dir : Path | str | None, optional
        Directory containing the standard profile modules. If None, uses the
        directory of this script (default: None).
    force_regenerate : bool, optional
        If True, regenerate stub files even if they already exist.
        If False, only generate missing stub files (default: False).

    Returns
    -------
    dict[str, bool]
        Dictionary mapping file names to success status (True/False).

    Examples
    --------
    >>> results = generate_all_stubs()
    >>> results
    {'chs.py': True, 'rhs.py': True, 'ipe.py': True}

    >>> # Regenerate all stubs even if they exist
    >>> results = generate_all_stubs(force_regenerate=True)

    """
    profiles_dir = Path(__file__).parent if profiles_dir is None else Path(profiles_dir)

    results = {}

    # Iterate through all Python files in the directory
    for py_file in profiles_dir.glob("*.py"):
        # Skip private files and this script itself
        if py_file.name.startswith("_") or py_file.name == Path(__file__).name:
            continue

        stub_file = py_file.with_suffix(".pyi")

        # Skip if stub exists and we're not forcing regeneration
        if stub_file.exists() and not force_regenerate:
            continue

        # Generate stub
        success = generate_stub_for_file(py_file, stub_file)
        results[py_file.name] = success

    return results


#####################################################################################
### The following temporary functions are used to generate standard profile dicts ###
### from Enum classes. They can be removed once the profile definition files      ###
### have been generated and saved.                                                ###
#####################################################################################


def enum_to_nested_dict(
    enum_class: type[Enum],
    value_keys: list[str] | None = None,
) -> dict[str, dict[str, str | float | int]]:
    """Convert an Enum to a nested dictionary.

    Parameters
    ----------
    enum_class : type[Enum]
        The Enum class to convert.
    value_keys : list[str] | None, optional
        The keys to use for each value in the enum member's value tuple.
        If None (default), the keys will be inferred from the parameter names
        of the enum's __init__ method (excluding 'self').

    Returns
    -------
    dict[str, dict[str, str | float | int]]
        A nested dictionary where each key is the enum member name,
        and the value is a dictionary mapping value_keys to the corresponding
        values from the enum member's value tuple.

    Examples
    --------
    >>> class CHSEnum(Enum):
    ...     CHS21_3x2_3 = ("CHS 21.3x2.3", 21.3, 2.3)
    ...     CHS21_3x2_6 = ("CHS 21.3x2.6", 21.3, 2.6)
    ...
    ...     def __init__(self, alias: str, diameter: float, thickness: float) -> None:
    ...         self.alias = alias
    ...         self.diameter = diameter
    ...         self.thickness = thickness
    >>> # Keys inferred from __init__ parameters
    >>> result = enum_to_nested_dict(CHSEnum)
    >>> result["CHS21_3x2_3"]
    {'alias': 'CHS 21.3x2.3', 'diameter': 21.3, 'thickness': 2.3}
    >>>
    >>> # Or explicitly provide keys
    >>> result = enum_to_nested_dict(CHSEnum, ["name", "d", "t"])
    >>> result["CHS21_3x2_3"]
    {'name': 'CHS 21.3x2.3', 'd': 21.3, 't': 2.3}

    """
    # Infer value_keys from __init__ method if not provided
    if value_keys is None:
        init_method = enum_class.__init__
        sig = inspect.signature(init_method)
        # Get parameter names excluding 'self'
        value_keys = [param for param in sig.parameters if param != "self"]

    result = {}
    for member in enum_class:
        member_dict = dict(zip(value_keys, member.value, strict=True))
        result[member.name] = member_dict
    return result


def save_dict_to_profile_file(
    data: dict[str, dict[str, str | float | int]],
    variable_name: str,
    file_path: Path | str = "profile_dicts.py",
) -> None:
    """Save a dictionary to a Python file as a variable.

    Appends the dictionary to the end of the specified file with proper
    formatting as a Python variable assignment.

    Parameters
    ----------
    data : dict[str, dict[str, str | float | int]]
        The nested dictionary to save to the file.
    variable_name : str
        The name of the variable to assign the dictionary to in the file.
    file_path : Path | str, optional
        The path to the file where the dictionary will be saved.
        Defaults to "profile_dicts.py".

    Examples
    --------
    >>> chs_data = {
    ...     "CHS21_3x2_3": {"alias": "CHS 21.3x2.3", "diameter": 21.3, "thickness": 2.3},
    ...     "CHS21_3x2_6": {"alias": "CHS 21.3x2.6", "diameter": 21.3, "thickness": 2.6},
    ... }
    >>> save_dict_to_profile_file(chs_data, "chs_enum")
    # Creates or appends to profile_dicts.py with:
    # chs_enum = {
    #     "CHS21_3x2_3": {
    #         "alias": "CHS 21.3x2.3",
    #         "diameter": 21.3,
    #         "thickness": 2.3,
    #     },
    #     ...
    # }

    """
    file_path = Path(file_path)

    # Format the dictionary with proper indentation
    lines = [f"{variable_name} = {{"]

    for outer_key, inner_dict in data.items():
        lines.append(f'    "{outer_key}": {{')
        for i, (inner_key, value) in enumerate(inner_dict.items()):
            # Format value based on type
            formatted_value = f'"{value}"' if isinstance(value, str) else str(value)

            # Add comma to all items
            lines.append(f'        "{inner_key}": {formatted_value},')

        lines.append("    },")

    lines.append("}\n")

    # Read existing content if file exists
    if file_path.exists():
        existing_content = file_path.read_text()
        # Add newlines before appending if file doesn't end with newline
        if existing_content and not existing_content.endswith("\n"):
            prefix = "\n\n"
        elif existing_content:
            prefix = "\n"
        else:
            prefix = ""
    else:
        prefix = ""

    # Append to file
    with file_path.open("a") as f:
        f.write(prefix + "\n".join(lines))


if __name__ == "__main__":
    # Generate stubs for all files in the standard_profiles directory
    results = generate_all_stubs(force_regenerate=True)

    print("Stub generation results:")  # noqa: T201
    for filename, success in results.items():
        status = "✅" if success else "❌"
        print(f"  {status} {filename}")  # noqa: T201
