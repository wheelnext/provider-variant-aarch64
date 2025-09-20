from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

import provider_variant_aarch64.vendor.archspec.archspec.cpu as archspec_cpu

if TYPE_CHECKING:
    from collections.abc import Generator


@dataclass(frozen=True)
class VariantFeatureConfig:
    name: str
    # Acceptable values in priority order
    values: list[str]
    multi_value: bool = False


@dataclass(frozen=True)
class VariantProperty:
    namespace: str
    feature: str
    value: str


class AArch64Plugin:
    namespace = "aarch64"

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

    @classmethod
    def get_all_configs(cls) -> list[VariantFeatureConfig]:
        return [
            VariantFeatureConfig(
                "version",
                list(cls._version_range(archspec_cpu.TARGETS[cls.max_known_version])),
            ),
        ] + [VariantFeatureConfig(feature, ["on"]) for feature in cls.all_features]

    @classmethod
    def get_supported_configs(cls) -> list[VariantFeatureConfig]:
        microarch = archspec_cpu.host()
        if "aarch64" in (microarch.generic, *microarch.ancestors):
            generic = microarch.generic
            # ceil to max supported version
            if cls.max_known_version in generic.ancestors:
                generic = archspec_cpu.TARGETS[cls.max_known_version]
            return [
                VariantFeatureConfig("version", list(cls._version_range(generic))),
            ] + [
                VariantFeatureConfig(feature, ["on"])
                for feature in cls.all_features
                if feature in microarch
            ]

        return []

    @classmethod
    def get_compiler_flags(
        cls,
        language: str,
        compiler_name: str,
        compiler_version: str,
        properties: list[VariantProperty],
    ) -> list[str]:
        # TODO: use archspec to get flags

        if language not in ("c", "c++", "fortran") or compiler_name not in (
            "gcc",
            "clang",
        ):
            raise NotImplementedError(
                f"Flags for language {language} compiler {compiler_name} "
                "not implemented"
            )

        for prop in properties:
            assert prop.namespace == cls.namespace
            if prop.feature == "version":
                return [f"-march=armv{prop.value.replace('a', '-a')}"]
        return []


if __name__ == "__main__":
    print(f"{AArch64Plugin.namespace=}")  # noqa: T201
    print(f"{AArch64Plugin.get_supported_configs()=}")  # noqa: T201
    print(f"{AArch64Plugin.get_all_configs()=}")  # noqa: T201
