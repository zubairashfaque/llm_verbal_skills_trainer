# Contributing to LLM Verbal Skills Trainer

Thank you for your interest in contributing! This document provides guidelines and instructions for setting up your development environment and contributing to the project.

## 📋 Table of Contents
- [Development Setup](#development-setup)
- [Code Quality Standards](#code-quality-standards)
- [Testing](#testing)
- [Pull Request Process](#pull-request-process)
- [Code of Conduct](#code-of-conduct)

## 🛠 Development Setup

### Prerequisites
- Python 3.11
- Poetry (for dependency management)
- Ollama (for local LLM inference)

### Initial Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/llm_verbal_skills_trainer.git
   cd llm_verbal_skills_trainer
   ```

2. **Install Poetry:**
   ```bash
   pip install poetry
   ```

3. **Install dependencies:**
   ```bash
   # Install main dependencies
   poetry install

   # Install development dependencies
   poetry install --with dev
   ```

4. **Set up environment variables:**
   ```bash
   # Copy the example environment file
   cp .env.example .env

   # Edit .env with your configuration
   nano .env
   ```

5. **Install Ollama and download models:**
   ```bash
   # Run the setup script
   poetry run python src/olla_setup.py
   ```

6. **Install pre-commit hooks:**
   ```bash
   poetry run pre-commit install
   ```

## 🎯 Code Quality Standards

We maintain high code quality standards using automated tools:

### Linting with Ruff
```bash
# Check for linting issues
poetry run ruff check .

# Auto-fix linting issues
poetry run ruff check --fix .

# Format code
poetry run ruff format .
```

### Type Checking with MyPy
```bash
poetry run mypy src/
```

### Pre-commit Hooks
Pre-commit hooks run automatically before each commit. To run them manually:
```bash
poetry run pre-commit run --all-files
```

### Code Style Guidelines
- **Line length:** Maximum 120 characters
- **Imports:** Sorted using isort (automatically handled by ruff)
- **Quotes:** Double quotes for strings
- **Type hints:** Add type hints to all function signatures
- **Docstrings:** Use Google-style docstrings for all public functions

Example:
```python
def process_audio(audio_path: str, model_name: str = "whisper") -> dict:
    """
    Process audio file and return transcription.

    Args:
        audio_path: Path to the audio file
        model_name: Name of the model to use for transcription

    Returns:
        Dictionary containing transcription results

    Raises:
        FileNotFoundError: If audio file doesn't exist
    """
    pass
```

## 🧪 Testing

### Running Tests
```bash
# Run all tests
poetry run pytest

# Run with coverage report
poetry run pytest --cov=src --cov-report=html

# Run specific test file
poetry run pytest tests/unit_tests.py

# Run specific test
poetry run pytest tests/unit_tests.py::TestModelManager::test_generate_response
```

### Writing Tests
- Place unit tests in `tests/unit_tests.py`
- Place integration tests in `tests/integration_tests.py`
- Aim for >80% code coverage
- Use mocks for external dependencies (LLM calls, file I/O)

Example test:
```python
import unittest
from unittest.mock import patch, MagicMock

class TestFeature(unittest.TestCase):
    @patch("src.module.external_call")
    def test_feature(self, mock_external):
        mock_external.return_value = "mocked_response"
        result = my_function()
        self.assertEqual(result, "expected_output")
```

## 📝 Pull Request Process

1. **Create a feature branch:**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes:**
   - Write clean, documented code
   - Add tests for new functionality
   - Update documentation as needed

3. **Run quality checks:**
   ```bash
   # Lint and format
   poetry run ruff check --fix .
   poetry run ruff format .

   # Type check
   poetry run mypy src/

   # Run tests
   poetry run pytest --cov=src
   ```

4. **Commit your changes:**
   ```bash
   git add .
   git commit -m "feat: add new feature description"
   ```

   Use conventional commit messages:
   - `feat:` - New feature
   - `fix:` - Bug fix
   - `docs:` - Documentation changes
   - `test:` - Test additions/changes
   - `refactor:` - Code refactoring
   - `chore:` - Maintenance tasks

5. **Push to your fork:**
   ```bash
   git push origin feature/your-feature-name
   ```

6. **Create a Pull Request:**
   - Provide a clear description of changes
   - Link any related issues
   - Ensure all CI checks pass

## 🔍 Project Structure

```
llm_verbal_skills_trainer/
├── config/              # Configuration files
│   ├── settings.py      # Application settings
│   └── task_tracking.json
├── src/                 # Source code
│   ├── conversation.py
│   ├── model_manager.py
│   ├── skill_training.py
│   ├── voice_interface.py
│   └── presentation_assessment.py
├── tests/               # Test files
│   ├── unit_tests.py
│   └── integration_tests.py
├── main.py              # Application entry point
├── pyproject.toml       # Project dependencies and config
└── .env.example         # Environment variables template
```

## 🐛 Reporting Issues

When reporting issues, please include:
- Python version
- Operating system
- Steps to reproduce
- Expected vs actual behavior
- Error messages/logs
- Screenshots (if applicable)

## 💡 Feature Requests

We welcome feature requests! Please:
- Check existing issues first
- Provide clear use case
- Explain expected behavior
- Consider implementation approach

## 📄 Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Focus on the code, not the person
- Help others learn and grow

## 🙏 Questions?

If you have questions:
- Check existing documentation
- Search closed issues
- Open a new issue with the "question" label

Thank you for contributing to LLM Verbal Skills Trainer! 🚀
