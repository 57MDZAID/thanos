# Changelog

All notable changes to this project will be documented in this file.

## [0.1.1] – 2025-11-XX

### Added

- **`--seed` / `-s` option** for deterministic, reproducible file selection
    - Running `--dry-run --seed <N>` and then `--seed <N>` deletes the exact same files
    - Useful for debugging, auditing, testing, and scripting

### Fixed

- Random selection now remains consistent when a seed is provided

---

## [0.1.0] – 2025-XX-XX

### Added

- Initial release
- Random file elimination (exactly 50% of files)
- Dry run mode
- Recursive directory support
- Interactive confirmation
- CLI powered by Typer
- Basic project documentation

---

[0.1.1]: https://github.com/soldatov-ss/thanos/releases/tag/v0.1.1

[0.1.0]: https://github.com/soldatov-ss/thanos/releases/tag/v0.1.0
