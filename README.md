# OBS recording autosort scaffold

A development starting point for an OBS Studio recording-sorting plugin, derived
from the OBS Project plugin template.

**Status: scaffold only.** The current module logs when OBS loads or unloads it.
It does not observe recording events, choose destination folders, move or rename
recordings, or expose sorting settings. The repository name describes the intended
project; there is no working autosort feature or published release here.

## Current contents

- A minimal C plugin with module identity and a description of its scaffold status.
- CMake configuration using the machine name `obs-recordingautosort`.
- Historical OBS 28.0.1 dependency pins and cross-platform packaging helpers.
- A small automated source/build check, plus the preserved original template
  documentation and workflow for provenance.

The template version `1.0.0` remains in the build metadata to avoid changing the
historical dependency/package setup. It is not a claim of a completed 1.0 release.

## Build with an installed OBS development environment

The module requires CMake, C/C++ compilers and an OBS development installation that
exports the `OBS::libobs` CMake target. This cleanup does not install OBS or change
its recording configuration.

```sh
cmake -S . -B build -DCMAKE_PREFIX_PATH=/path/to/obs-development-prefix
cmake --build build
```

Use the architecture and compiler supported by your OBS development installation.
Generated plugin headers stay in the build directory. The source tree is not an
output directory for those headers.

`buildspec.json` retains the original OBS 28.0.1 and 2022 dependency references.
Compatibility with current OBS releases, Windows/macOS packaging, signing and
notarization has not been established. The inherited helper scripts are retained
for development reference; they are not a supported one-command release process.

For packaging, supply your own `PLUGIN_AUTHOR` and `LINUX_MAINTAINER_EMAIL` CMake
cache values. Both default to empty rather than template names or invented contact
details. `MACOS_BUNDLEID` is configurable and uses the current repository owner's
namespace. Review these values when preparing a real distribution.

## Validation scope

The active GitHub workflow checks the scaffold without downloading or building
OBS. Its offline CMake/compiler smoke check uses a minimal substitute for the
libobs development interface. That verifies local build wiring and the module's
small load/unload behavior; it is **not** an OBS ABI, plugin installation or
recording-sorting integration test.

Run the same Linux-only check locally with Python 3, CMake and C/C++ compilers installed:

```sh
python3 tests/check_scaffold.py
```

The check uses a temporary source copy and does not change an OBS installation.

A real libobs development package was unavailable in the cleanup environment.
The real OBS build and loading the plugin inside OBS therefore remain unverified.
No recording files were inspected, moved or renamed.

The previous multi-platform workflow is preserved, inactive, at
[`docs/upstream/main-2022.yml`](docs/upstream/main-2022.yml). Its old build/release
assumptions require a separate update before use. The active workflow does not
publish releases, upload installers, or use signing credentials.

## Work still needed for autosort

A functional implementation would need recording lifecycle integration, an
explicit sorting rule and destination setting, handling for files still being
written, collision-safe moves and useful failure reporting. Those features are
not implemented by this cleanup. This scaffold should not be presented as a
completed plugin or evidence of a tested recording workflow.

## Attribution and license

The initial commit imported the OBS plugin template. The module's starting source
is upstream template code; its commit attribution does not establish original
authorship of that template. See [provenance](PROVENANCE.md) and the preserved
[original template README](docs/upstream-template-README.md).

The existing [GPL version 2 license text](LICENSE) and source notices permitting
GPL version 2 or later are retained. No new blanket licensing terms are added.
