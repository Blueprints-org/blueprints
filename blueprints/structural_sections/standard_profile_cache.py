"""Loader helper for cached section properties for standard profiles.

Functions:
 - `get_cached_section(profile_name: str, data_dir: str = 'data/profile_sections')` -> dict
   Searches the `data_dir` for a matching JSON file named `<PROFILE_NAME>.json` and returns
   the loaded dict. If not found, returns None.
 - `get_or_compute(profile, data_dir=...)` -> dict
   Attempts to load from cache; if missing computes `profile.section_properties(...)` and returns a dict.
"""

from __future__ import annotations

import contextlib
import importlib
import json
import os
from typing import Any

DEFAULT_DATA_DIR = os.path.join("blueprints", "structural_sections", "steel", "standard_profiles", "_section_properties")


def _search_file_for_profile(profile_name: str, data_dir: str) -> str | None:
    """Recursively search `data_dir` for a file named `<profile_name>.json`.

    Returns the path if found, else None.
    """
    for root, _, files in os.walk(data_dir):
        target = f"{profile_name}.json"
        if target in files:
            return os.path.join(root, target)
    return None


def get_cached_section(profile_name: str, data_dir: str = DEFAULT_DATA_DIR) -> dict | None:
    """Return cached section dict for `profile_name` or None if not found."""
    path = _search_file_for_profile(profile_name, data_dir)
    if path is None:
        return None
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def get_or_compute(profile: object, data_dir: str = DEFAULT_DATA_DIR) -> dict:
    """Return cached section dict if available, otherwise compute and return live values.

    Note: this does not write the cache — use the build script to generate files.
    """
    name = getattr(profile, "name", None) or getattr(profile, "profile_name", None)
    if name:
        cached = get_cached_section(name, data_dir=data_dir)
        if cached is not None:
            return cached

    # compute live
    section_props = profile.section_properties(geometric=True, plastic=True, warping=False)
    # simple serializer for a minimal set
    result: dict[str, Any] = {
        "name": name or "",
        "area": float(profile.area),
        "centroid": {"x": float(profile.centroid.x), "y": float(profile.centroid.y)},
        "profile_width": float(profile.profile_width),
        "profile_height": float(profile.profile_height),
    }
    # try some common attributes
    for attr in ("ixx_c", "iyy_c", "ixx", "iyy", "j"):
        if hasattr(section_props, attr):
            with contextlib.suppress(Exception):
                result[attr] = float(getattr(section_props, attr))

    return result


class CachedSectionProperties:
    """A lightweight SectionProperties-like object constructed from cached JSON.

    It exposes numeric attributes as found in the cache (e.g. `ixx`, `ixx_c`, `area`, `centroid`, `j`, ...)
    so callers that only read attributes will work transparently.
    """

    def __init__(self, data: dict) -> None:
        """Initialize the cached proxy with raw JSON `data`.

        Numeric attributes are exposed directly and `centroid` is converted to an
        object with `x`/`y` attributes for compatibility.
        """
        self._data = data
        # populate attributes for easy access
        for k, v in data.items():
            # create numeric attributes directly, nested centroid as x/y
            if k == "centroid" and isinstance(v, dict):
                self.centroid = type("C", (), {"x": v.get("x"), "y": v.get("y")})()
            else:
                setattr(self, k, v)

    def as_dict(self) -> dict:
        """Return a shallow copy of the underlying cached dict."""
        return dict(self._data)

    # No-op calculation methods so callers that expect a SectionProperties
    # instance can safely call these without error when using the cached proxy.
    def calculate_geometric_properties(self) -> None:
        """Compatibility no-op for geometric calculation API."""
        return

    def calculate_plastic_properties(self) -> None:
        """Compatibility no-op for plastic calculation API."""
        return

    def calculate_warping_properties(self) -> None:
        """Compatibility no-op for warping calculation API."""
        return


def get_section_properties_for(
    profile_or_name: object, geometric: bool = True, plastic: bool = True, warping: bool = False, data_dir: str = DEFAULT_DATA_DIR
) -> CachedSectionProperties | None:
    """Return a CachedSectionProperties object for the given profile instance or profile name.

    Conditions for returning a cached object:
    - a matching JSON file for the profile `name` is present under `data_dir` (recursively), and
    - the caller requested properties that are present in the JSON. If the JSON contains more than
      requested (e.g. warping data exists) the full cache will still be loaded and returned.

    If no cache file is found, returns `None`.
    """
    # accept either a profile instance or a string name
    name = profile_or_name if isinstance(profile_or_name, str) else getattr(profile_or_name, "name", None)
    # mark unused params used to satisfy linters
    _ = (geometric, plastic)
    if not name:
        return None

    path = _search_file_for_profile(name, data_dir)
    if path is None:
        return None

    try:
        with open(path, encoding="utf-8") as fh:
            data = json.load(fh)
    except Exception:
        return None

    # Respect computed metadata if present: if warping was requested but not computed in the cache,
    # we must return None so callers will compute live properties.
    computed = data.get("computed") if isinstance(data, dict) else None
    if warping:
        if isinstance(computed, dict):
            if not computed.get("warping", False):
                return None
        else:
            # no metadata -> conservative: assume no warping
            return None

    # If only geometric/plastic requested and cache exists, return full cache regardless of requested subset.
    return CachedSectionProperties(data)


def _to_number(value: object) -> object:
    """Attempt to coerce `value` to a JSON-serializable numeric form.

    Falls back to calling `tolist()` for array-like objects, or returns the
    original object if coercion fails.
    """
    try:
        return float(value)
    except Exception:
        pass
    try:
        return int(value)
    except Exception:
        pass
    try:
        return value.tolist()  # type: ignore[attr-defined]
    except Exception:
        return value


def extract_section_props_from_live(profile: object) -> dict[str, Any]:
    """Compute and return a serializable dict of section properties from `profile`."""
    section_props = profile.section_properties(geometric=True, plastic=True, warping=False)
    out: dict[str, Any] = {
        "name": getattr(profile, "name", ""),
        "area": _to_number(profile.area),
        "centroid": {"x": _to_number(profile.centroid.x), "y": _to_number(profile.centroid.y)},
        "profile_width": _to_number(profile.profile_width),
        "profile_height": _to_number(profile.profile_height),
    }
    # common numeric attrs
    for attr in ("ixx_c", "iyy_c", "ixx", "iyy", "j", "wplx", "wplz"):
        if hasattr(section_props, attr):
            with contextlib.suppress(Exception):
                out[attr] = _to_number(getattr(section_props, attr))
    return out


def _find_profile_by_key(profile_key: str) -> tuple[object | None, str | None]:
    """Search standard profile classes to find and instantiate a profile by its key.

    Returns (profile_instance, class_name) or (None, None) if not found.
    """
    pkg = importlib.import_module("blueprints.structural_sections.steel.standard_profiles")
    for class_name in getattr(pkg, "__all__", []):
        cls = getattr(pkg, class_name, None)
        if cls is None:
            continue
        if not hasattr(cls, "_database") or not hasattr(cls, "_factory"):
            continue
        if profile_key in cls._database:
            params = cls._database[profile_key]
            profile = cls._factory(**params._asdict())
            return profile, class_name
    return None, None
