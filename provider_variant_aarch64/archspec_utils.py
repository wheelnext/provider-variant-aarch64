import importlib.util
import sys
from pathlib import Path
from types import ModuleType


def load_archspec() -> ModuleType:
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
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def load_archspec_cpu() -> ModuleType:
    """
    Get the archspec.cpu module.

    Returns:
        archspec.cpu (ModuleType): The archspec.cpu module.
    """
    # Load `archspec` from a specific path
    archspec = load_archspec()
    assert archspec.__version__ is not None

    module = importlib.import_module("archspec.cpu")

    assert module.TARGETS is not None

    return module
