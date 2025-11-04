# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Environment-based configuration using python-dotenv
- `.env.example` template file for configuration
- Development dependencies (pytest, pytest-cov, mypy, ruff, black, pre-commit)
- Pre-commit hooks configuration (`.pre-commit-config.yaml`)
- Comprehensive `CONTRIBUTING.md` with development guidelines
- `Makefile` with common development commands
- Ruff linting configuration in `pyproject.toml`
- MyPy type checking configuration in `pyproject.toml`
- Pytest and coverage configuration in `pyproject.toml`
- Type hints to `voice_interface.py` functions
- Development setup section in README
- Project structure documentation in README

### Changed
- Migrated all hardcoded configuration values to environment variables in `config/settings.py`
- Updated `src/model_manager.py` to use configuration from settings
- Updated `src/skill_training.py` to import TRACKING_FILE from settings
- Updated `main.py` to import TRACKING_FILE from settings
- Improved `.gitignore` with comprehensive exclusions
- Enhanced README with development and contributing sections

### Fixed
- Removed duplicate `skill_training_voice()` function in `main.py` (lines 127-150)
- Fixed poetry.lock gitignore conflict (removed from .gitignore)
- Fixed missing imports in `voice_interface.py` (time, threading, List)
- Removed duplicate import statements in `voice_interface.py`

### Removed
- Hardcoded configuration values replaced with environment variables
- poetry.lock from .gitignore (should be committed for reproducible builds)

## [0.1.0] - 2025-11-04

### Initial Release
- LLM-powered verbal skills training system
- Support for Impromptu Speaking, Storytelling, and Conflict Resolution
- Voice interface with Whisper integration
- Gradio-based web UI
- Model benchmarking capabilities
- Progress tracking system
