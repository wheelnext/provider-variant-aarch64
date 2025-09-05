from __future__ import annotations

from argparse import Namespace

import pytest

from provider_variant_aarch64.plugin import AArch64Plugin
from provider_variant_aarch64.plugin import VariantFeatureConfig
from provider_variant_aarch64.plugin import archspec_cpu
from variantlib.models.variant import VariantProperty


@pytest.fixture
def plugin() -> AArch64Plugin:
    return AArch64Plugin()


def test_cortex_a72_configs(mocker, plugin):
    mocker.patch(
        "provider_variant_aarch64.plugin.archspec_cpu.host"
    ).return_value = archspec_cpu.TARGETS["cortex_a72"]
    assert plugin.get_supported_configs() == [
        VariantFeatureConfig("version", ["8a"]),
        VariantFeatureConfig("aes", ["on"]),
        VariantFeatureConfig("asimd", ["on"]),
        VariantFeatureConfig("cpuid", ["on"]),
        VariantFeatureConfig("crc32", ["on"]),
        VariantFeatureConfig("evtstrm", ["on"]),
        VariantFeatureConfig("fp", ["on"]),
        VariantFeatureConfig("pmull", ["on"]),
        VariantFeatureConfig("sha1", ["on"]),
        VariantFeatureConfig("sha2", ["on"]),
    ]


def test_a64fx_configs(mocker, plugin):
    mocker.patch(
        "provider_variant_aarch64.plugin.archspec_cpu.host"
    ).return_value = archspec_cpu.TARGETS["a64fx"]
    assert plugin.get_supported_configs() == [
        VariantFeatureConfig("version", ["8.2a", "8.1a", "8a"]),
        VariantFeatureConfig("asimdhp", ["on"]),
        VariantFeatureConfig("dcpop", ["on"]),
        VariantFeatureConfig("fcma", ["on"]),
        VariantFeatureConfig("fphp", ["on"]),
        VariantFeatureConfig("sve", ["on"]),
        VariantFeatureConfig("asimd", ["on"]),
        VariantFeatureConfig("cpuid", ["on"]),
        VariantFeatureConfig("crc32", ["on"]),
        VariantFeatureConfig("evtstrm", ["on"]),
        VariantFeatureConfig("fp", ["on"]),
        VariantFeatureConfig("sha1", ["on"]),
        VariantFeatureConfig("sha2", ["on"]),
    ]


def test_arm84a_configs(mocker, plugin):
    mocker.patch(
        "provider_variant_aarch64.plugin.archspec_cpu.host"
    ).return_value = archspec_cpu.TARGETS["armv8.4a"]
    assert plugin.get_supported_configs() == [
        VariantFeatureConfig("version", ["8.4a", "8.3a", "8.2a", "8.1a", "8a"]),
    ]


def test_aarch64_configs(mocker, plugin):
    mocker.patch(
        "provider_variant_aarch64.plugin.archspec_cpu.host"
    ).return_value = archspec_cpu.TARGETS["aarch64"]
    assert plugin.get_supported_configs() == [
        VariantFeatureConfig("version", ["8a"]),
    ]


def test_non_arm_configs(mocker, plugin):
    mocker.patch(
        "provider_variant_aarch64.plugin.archspec_cpu.host"
    ).return_value = archspec_cpu.TARGETS["nehalem"]
    assert plugin.get_supported_configs() == []


def test_get_compiler_flags(plugin):
    assert plugin.get_compiler_flags(
        "c",
        "gcc",
        "14.3.0",
        [
            VariantProperty("aarch64", "version", "8.4a"),
            VariantProperty("aarch64", "sve", "on"),
        ],
    ) == ["-march=armv8.4-a"]


def test_get_compiler_flags_no_level(plugin):
    assert (
        plugin.get_compiler_flags(
            "c++",
            "clang",
            "20.1.8",
            [
                VariantProperty("aarch64", "sve", "on"),
            ],
        )
        == []
    )


def test_get_compiler_flags_no_properties(plugin):
    assert plugin.get_compiler_flags("c", "clang", "19.1.7", []) == []


def test_level_cap(mocker, plugin):
    """Test that we do not return level higher than declared supported"""

    compatible_versions = ["9.0a", "8.5a", "8.4a", "8.3a", "8.2a", "8.1a", "8a"]
    compatible_microarchitectures = [
        f"armv{ver}" if ver != "8a" else "aarch64" for ver in compatible_versions
    ]
    mocker.patch(
        "provider_variant_aarch64.plugin.archspec_cpu.host"
    ).return_value = Namespace(
        name="frobnicator",
        ancestors={"armv9.1a", *compatible_microarchitectures},
        generic=Namespace(name="armv9.1a", ancestors={*compatible_microarchitectures}),
    )
    assert plugin.get_supported_configs() == [
        VariantFeatureConfig("version", compatible_versions),
    ]
