# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.3.0] - 2025-11-04

### Added - Phase C: Modern Features & Production Readiness
- CI/CD Pipeline
  - GitHub Actions workflow with 6 automated jobs
  - Lint job: Ruff code quality checks
  - Type-check job: MyPy static analysis
  - Test job: Pytest with coverage upload to Codecov
  - Security job: Safety vulnerability scanning
  - Build job: Package building with artifacts
  - Docker job: Container image building
- Dependabot configuration for automated updates
  - Weekly Python dependency updates
  - GitHub Actions version updates
  - Docker base image updates
- Docker support
  - Multi-stage Dockerfile (builder + runtime)
  - Production docker-compose.yml
  - Development docker-compose.dev.yml with hot reload
  - Non-root user for security
  - Health checks for monitoring
  - Model downloader service
- Performance monitoring (`src/utils/performance.py`)
  - PerformanceMetrics dataclass
  - PerformanceMonitor class
  - @monitor_performance decorator
  - MetricsCollector for aggregation
  - System metrics collection (CPU, memory, disk)
  - JSONL-based metrics storage
- Deployment documentation (`DEPLOYMENT.md`)
  - Docker deployment guide (400+ lines)
  - Production considerations
  - Security checklist
  - Monitoring & maintenance
  - Troubleshooting guide
- Dependencies: psutil (5.9.0)
- Makefile Docker commands (9 new commands)

### Changed - Phase C
- README updated with Docker deployment option
- Makefile enhanced with Docker operations

## [0.2.0] - 2025-11-04

### Added - Phase B: Testing & Quality Infrastructure
- Comprehensive unit tests (60+ test cases across 6 test files)
  - `tests/test_model_manager.py` - LLM operations testing
  - `tests/test_skill_training.py` - Training modules testing
  - `tests/test_conversation.py` - Chat feedback testing
  - `tests/test_presentation_assessment.py` - Assessment testing
  - `tests/test_voice_interface.py` - Audio processing testing
- Integration tests in `tests/test_integration.py`
  - End-to-end workflow tests
  - Error handling tests
  - Concurrent operations tests
  - Data persistence tests
- Test fixtures in `tests/conftest.py`
- Structured logging framework
  - `config/logging_config.yaml` - Logging configuration
  - `src/utils/logging_utils.py` - Logging utilities
  - Rotating file handlers (10MB max, 5 backups)
  - Module-specific logging levels
- Custom exception hierarchy in `src/utils/exceptions.py`
  - `VerbalsSkillsTrainerError` base exception
  - Specific exceptions for model, audio, tracking, and validation errors
  - Centralized error messages
- Dependencies: pyyaml (6.0.1), python-json-logger (2.0.7)

### Added - Phase A: Critical Infrastructure
- Environment-based configuration using python-dotenv
- `.env.example` template file for configuration
- Development dependencies (pytest, pytest-cov, mypy, ruff, black, pre-commit)
- Pre-commit hooks configuration (`.pre-commit-config.yaml`)
- Comprehensive `CONTRIBUTING.md` with development guidelines
- `Makefile` with common development commands (15+ commands)
- Ruff linting configuration in `pyproject.toml`
- MyPy type checking configuration in `pyproject.toml`
- Pytest and coverage configuration in `pyproject.toml`
- Type hints to `voice_interface.py` functions
- Development setup section in README
- Project structure documentation in README
- `CHANGELOG.md` for version tracking
- `PHASE_A_SUMMARY.md` for Phase A details
- `MODERNIZATION_SUMMARY.md` for complete overview

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
