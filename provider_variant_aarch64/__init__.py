"""A wheel variant provider with properties specific to AArch64 CPUs"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

__version__ = "0.0.1.post2"


def _load_vendored_archspec() -> None:
    """
    Load a vendored `archspec` library.

    Returns:
        module (ModuleType): The loaded module.
    """
    name = "archspec"

    spec = importlib.util.spec_from_file_location(
        name=name,
        location=Path(__file__).parent / "vendor/archspec/archspec/__init__.py",
    )
    if spec is None or spec.loader is None:
        raise ImportError("The submodule `archspec` is missing.")

    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)


_load_vendored_archspec()
