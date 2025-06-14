from __future__ import annotations

from argparse import Namespace

import archspec.cpu
import pytest

from provider_variant_aarch64.plugin import AArch64Plugin
from variantlib.models.provider import VariantFeatureConfig
from variantlib.models.variant import VariantProperty


@pytest.fixture
def plugin() -> AArch64Plugin:
    return AArch64Plugin()


def test_cortex_a72_configs(mocker, plugin):
    mocker.patch("archspec.cpu.host").return_value = archspec.cpu.TARGETS["cortex_a72"]
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
    mocker.patch("archspec.cpu.host").return_value = archspec.cpu.TARGETS["a64fx"]
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
    mocker.patch("archspec.cpu.host").return_value = archspec.cpu.TARGETS["armv8.4a"]
    assert plugin.get_supported_configs() == [
        VariantFeatureConfig("version", ["8.4a", "8.3a", "8.2a", "8.1a", "8a"]),
    ]


def test_aarch64_configs(mocker, plugin):
    mocker.patch("archspec.cpu.host").return_value = archspec.cpu.TARGETS["aarch64"]
    assert plugin.get_supported_configs() == [
        VariantFeatureConfig("version", ["8a"]),
    ]


def test_non_arm_configs(mocker, plugin):
    mocker.patch("archspec.cpu.host").return_value = archspec.cpu.TARGETS["nehalem"]
    assert plugin.get_supported_configs() == []


def test_get_build_setup(plugin):
    assert plugin.get_build_setup(
        [
            VariantProperty("aarch64", "version", "8.4a"),
            VariantProperty("aarch64", "sve", "on"),
        ]
    ) == {
        "cflags": ["-march=armv8.4-a"],
        "cxxflags": ["-march=armv8.4-a"],
    }


def test_get_build_setup_no_level(plugin):
    assert (
        plugin.get_build_setup(
            [
                VariantProperty("aarch64", "sve", "on"),
            ]
        )
        == {}
    )


def test_get_build_setup_no_properties(plugin):
    assert plugin.get_build_setup([]) == {}


def test_level_cap(mocker, plugin):
    """Test that we do not return level higher than declared supported"""

    compatible_versions = ["9.0a", "8.5a", "8.4a", "8.3a", "8.2a", "8.1a", "8a"]
    compatible_microarchitectures = [
        f"armv{ver}" if ver != "8a" else "aarch64" for ver in compatible_versions
    ]
    mocker.patch("archspec.cpu.host").return_value = Namespace(
        name="frobnicator",
        ancestors={"armv9.1a", *compatible_microarchitectures},
        generic=Namespace(name="armv9.1a", ancestors={*compatible_microarchitectures}),
    )
    assert plugin.get_supported_configs() == [
        VariantFeatureConfig("version", compatible_versions),
    ]
