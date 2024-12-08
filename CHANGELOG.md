# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.9] - 2024-12-08

### Changed

- Expose function `visit_string_values` of module `variable_parser`.
- Added function `visit_variables` to module `variable_parser`.

## [0.1.8] - 2024-12-06

### Changed

- Bump PyYAML version to `6.0.2`

## [0.1.7] - 2024-12-06

### Added

- Ignore case, underscore `_` and dash `-` in variable names when replacing.

## [0.1.6] - 2024-06-22

### Changed

- `YamlLoader` to return default if specified or fail fast.

## [0.1.5] - 2024-06-09

### Added

- Secrets masking for log records.

## [0.1.4] - 2024-06-01

### Added

- Lock down dependency versions.
- Add scripts for running tests, installing.

### Changed

- `variable_parser` method names prefix from `parse_` to `replace_`
- `yaml_loader` to expose methods `load_from_path`and `get_path`

## [0.1.3] - 2024-05-29

### Fixed

- App version in `setup.py`

## [0.1.2] - 2024-05-29

### Added

Sub packages of `pyu` to automatic package discovery.

## [0.1.1] - 2024-05-24

### Added

- CHANGELOG file.
- Author, licence and project urls in `setup.py`.

## [0.1.0] - 2024-05-24

### Added

- README file.
- First commit.