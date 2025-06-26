from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

import archspec  # pyright: ignore[reportMissingImports]
import archspec.cpu  # pyright: ignore[reportMissingImports]

if TYPE_CHECKING:
    from collections.abc import Generator


@dataclass(frozen=True)
class VariantFeatureConfig:
    name: str

    # Acceptable values in priority order
    values: list[str]


@dataclass(frozen=True)
class VariantProperty:
    namespace: str
    feature: str
    value: str


class AArch64Plugin:
    namespace = "aarch64"
    dynamic = False

    max_known_version = "armv9.0a"
    """Max version supported at the time"""

    all_features = [
        # neoverse_n2/v2 (armv9.0) features
        "sve2",
        "flagm2",
        "frint",
        "sb",
        # m2 (armv8.5) features
        "btiecv",
        # m1 (armv8.4) features
        "paca",
        "pacg",
        "ssbs",
        # neoverse_v1 (armv8.4) features
        "asimdfhm",
        "bf16",
        "dcpodp",
        "dgh",
        "dit",
        "flagm",
        "i8mm",
        "ilrcpc",
        "jscvt",
        "rng",
        "sha3",
        "sha512",
        "svebf16",
        "svei8mm",
        "uscat",
        # neoverse_n1 (armv8.2) features
        "asimddp",
        "lrcpc",
        # a64fx (armv8.2) features
        "asimdhp",
        "dcpop",
        "fcma",
        "fphp",
        "sve",
        # thunerx2 (armv8.1) features
        "asimdrdmatomics",
        # cortex_a72 (armv8.0) features
        "aes",
        "asimd",
        "cpuid",
        "crc32",
        "evtstrm",
        "fp",
        "pmull",
        "sha1",
        "sha2",
    ]
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

    def validate_property(self, variant_property: VariantProperty) -> bool:
        assert variant_property.namespace == self.namespace
        if variant_property.feature == "version":
            return variant_property.value in self._version_range(
                archspec.cpu.TARGETS[self.max_known_version]
            )
        return (
            variant_property.feature in self.all_features
            and variant_property.value == "on"
        )

    def get_supported_configs(
        self, known_properties: frozenset[VariantProperty] | None
    ) -> list[VariantFeatureConfig]:
        microarch = archspec.cpu.host()
        if "aarch64" in (microarch.generic, *microarch.ancestors):
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
        self, properties: list[VariantProperty]
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


if __name__ == "__main__":
    plugin = AArch64Plugin()
    print(plugin.get_supported_configs(None))  # noqa: T201
    # print(plugin.get_all_configs())
