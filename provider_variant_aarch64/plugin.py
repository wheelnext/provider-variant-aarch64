from __future__ import annotations

from typing import TYPE_CHECKING

import archspec.cpu

from variantlib.models.provider import VariantFeatureConfig
from variantlib.protocols import PluginType
from variantlib.protocols import VariantFeatureConfigType
from variantlib.protocols import VariantPropertyType

if TYPE_CHECKING:
    from collections.abc import Generator


class AArch64Plugin(PluginType):
    namespace = "aarch64"

    max_known_version = "armv9.0a"
    """Max version supported at the time"""

    all_features = []
    """All features supported by archspec at the time, sorted in preference order"""

    @staticmethod
    def _archspec_to_plugin(archspec_name: str) -> str:
        if archspec_name == "aarch64":
            return "8a"
        if archspec_name.startswith("armv") and archspec_name[-1] == "a":
            return f"{archspec_name[4:-1]}a"
        raise NotImplementedError(f"Unexpected archspec name: {archspec_name}")

    @classmethod
    def _version_range(cls, microarch) -> Generator[str]:
        yield cls._archspec_to_plugin(microarch.name)
        for ancestor in microarch.ancestors:
            yield cls._archspec_to_plugin(ancestor.name)

    def get_all_configs(self) -> list[VariantFeatureConfigType]:
        return [
            VariantFeatureConfig(
                "version",
                list(self._version_range(archspec.cpu.TARGETS[self.max_known_version])),
            ),
        ] + [VariantFeatureConfig(feature, ["on"]) for feature in self.all_features]

    def get_supported_configs(self) -> list[VariantFeatureConfigType]:
        microarch = archspec.cpu.host()
        if "aarch64" in microarch.ancestors:
            generic = microarch.generic
            # ceil to max supported version
            if self.max_known_version in generic.ancestors:
                generic = archspec.cpu.TARGETS[self.max_known_version]
            return [
                VariantFeatureConfig("version", list(self._version_range(generic))),
            ] + [
                VariantFeatureConfig(feature, ["on"])
                for feature in self.all_features
                if feature in microarch
            ]

        return []

    def get_build_setup(
        self, properties: list[VariantPropertyType]
    ) -> dict[str, list[str]]:
        for prop in properties:
            assert prop.namespace == self.namespace
            if prop.feature == "version":
                flag = f"-march=armv{prop.value.replace('a', '-a')}"
                return {
                    "cflags": [flag],
                    "cxxflags": [flag],
                }
        return {}
