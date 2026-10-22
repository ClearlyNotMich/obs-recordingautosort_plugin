# Provenance and licensing

## Original template

All 63 tracked paths in the repository's initial commit
`904134207150a083d8e27258e8f5bf4b3ebd9d67` match the file modes and Git blob IDs
of the official [OBS plugin template snapshot
`5db14e5850617a0632800416ca0d283024cd5b8d`](https://github.com/obsproject/obs-plugintemplate/commit/5db14e5850617a0632800416ca0d283024cd5b8d).
The initial commit imported that template without a recording-sorting feature.

Credit belongs to the OBS Project template contributors for the inherited source,
build helpers and packaging scaffold. The local commit's attribution to
ObviouslyNotMich identifies the import; it does not establish original authorship
of those files.

The [original README](docs/upstream-template-README.md) and
[original workflow](docs/upstream/main-2022.yml) are preserved byte-for-byte.
The latter is outside `.github/workflows/` and does not run as GitHub Actions.
Existing build helper scripts and symlinks remain unchanged.

## Cleanup changes

The portfolio cleanup gives the scaffold a consistent module identity, states
that sorting is unimplemented, generates headers in the build directory, replaces
invented template contact details with configurable values, and adds a limited
offline build check. It does not implement recording sorting or produce a tested
OBS distribution.

The former automated workflow targeted retired infrastructure, including
[`macos-12`](https://github.blog/changelog/2024-08-19-notice-of-upcoming-deprecations-and-breaking-changes-in-github-actions-runners/)
and [artifact actions v3](https://github.blog/changelog/2024-04-16-deprecation-notice-v3-of-the-artifact-actions/).
It is retained for provenance. The replacement workflow checks only the scaffold
and does not build OBS, sign installers, or publish releases. The OBS 28.0.1 and
2022 dependency pins in `buildspec.json` remain unchanged.

## License and owner confirmation

The original [LICENSE](LICENSE) contains the GNU General Public License version
2. The plugin source notices allow version 2 or, at the recipient's option, any
later version. Those terms remain in place; this cleanup adds no blanket license
and removes no actual upstream copyright attribution.

The owner identified this as their personal project on 22 October 2026 when asked
about authority to publish/transfer and any employer, client, sponsor or course
restrictions. No additional restrictions were identified. That confirmation
concerns the repository and the owner's additions; inherited template code
continues to carry its upstream terms and credit.

The original commit and author metadata are retained. This repository contains no
recording files, model weights or bundled user datasets in its original snapshot.
