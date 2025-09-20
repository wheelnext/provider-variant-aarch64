"""A wheel variant provider with properties specific to AArch64 CPUs"""

from __future__ import annotations

from .plugin import AArch64Plugin

__version__ = "0.0.3"

namespace = AArch64Plugin.namespace
get_supported_configs = AArch64Plugin.get_supported_configs
get_all_configs = AArch64Plugin.get_all_configs
get_compiler_flags = AArch64Plugin.get_compiler_flags
