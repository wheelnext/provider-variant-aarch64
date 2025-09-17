# provider-variant-aarch64

This is a plugin for the proposed [wheel variants implementation](
https://github.com/wheelnext/pep_xxx_wheel_variants) that provides
properties specific to AArch64 CPUs.

## Usage

Namespace: `aarch64`

Plugin API: `provider_variant_aarch64.plugin:AArch64Plugin`

Example use in `pyproject.toml`:

```toml
[variant.providers.aarch64]
requires = ["provider-variant-aarch64 >=0.0.1,<1"]
plugin-api = "provider_variant_aarch64.plugin:AArch64Plugin"
```

## Provided properties

To obtain the full list of properties supported by a given plugin
version, install it, then use:

```sh
variantlib plugins get-configs -a -n aarch64
```

To obtain the full list of properties compatible with your system, use:

```sh
variantlib plugins get-configs -s -n aarch64
```

### aarch64 :: version

Values: `8.1a`, `8.2a`...

Specifies the targeted [microarchitecture version](
https://en.wikipedia.org/wiki/AArch64#ARM-A_(application_architecture)).
The plugin automatically adds appropriate `-march=` value to `CFLAGS`.
The resulting wheel will be incompatible with CPUs below the specified
microarchitecture version.

Please note that many extensions (such as SVE) are technically optional
for multiple microarchitecture versions, so this optional may have
limited usefulness.

### aarch64 :: &lt;extension&gt;

Feature names: `asimdhp`, `sha3`, `sve`...

Values: `on`

Specifies that the built wheel uses the specific CPU extension.
The plugin does not emit any compiler flags at the moment.
The resulting wheel will be incompatible with CPUs that do not implement
the specific extension.

These properties should only be used when the relevant intrinsics are
used unconditionally. If the code using them uses runtime detection,
they should not be specified, as they will prevent installing the wheel
on systems where the extension is not available (yet the code would work
fine, disabling the code in question).
