# 🤝 Contributing to Animal Classification

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Making Changes](#making-changes)
- [Testing](#testing)
- [Submitting Changes](#submitting-changes)
- [Style Guidelines](#style-guidelines)

## 🌟 Code of Conduct

- Be respectful and inclusive
- Welcome newcomers and help them learn
- Focus on constructive feedback
- Respect differing viewpoints and experiences

## 🚀 Getting Started

### Prerequisites

- Python 3.9+
- Git
- Basic understanding of PyTorch and FastAPI

### Finding Issues

- Check the [Issues](https://github.com/yourusername/animal-classification/issues) page
- Look for issues labeled `good first issue` or `help wanted`
- Comment on an issue before starting work to avoid duplication

## 💻 Development Setup

1. **Fork and clone the repository:**
   ```bash
   git clone https://github.com/yourusername/animal-classification.git
   cd animal-classification
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run tests to verify setup:**
   ```bash
   pytest
   ```

## 🔨 Making Changes

### Branch Naming Convention

- Feature: `feature/description`
- Bug fix: `fix/description`
- Documentation: `docs/description`
- Performance: `perf/description`

Example:
```bash
git checkout -b feature/add-bird-classification
```

### Commit Messages

Follow the [Conventional Commits](https://www.conventionalcommits.org/) specification:

- `feat: add new animal class`
- `fix: correct prediction confidence calculation`
- `docs: update README with new features`
- `test: add unit tests for model`
- `refactor: improve code structure`
- `perf: optimize image processing`

## 🧪 Testing

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=. --cov-report=html

# Run specific test file
pytest tests/test_model.py

# Run specific test
pytest tests/test_api.py::TestPredictEndpoint::test_predict_with_valid_image
```

### Writing Tests

- Place tests in the `tests/` directory
- Name test files with `test_` prefix
- Use descriptive test names
- Aim for >80% code coverage
- Include both unit and integration tests

Example test:
```python
def test_model_prediction():
    """Test that model makes predictions correctly"""
    model = AnimalCNN(num_classes=10)
    input_tensor = torch.randn(1, 3, 224, 224)
    output = model(input_tensor)
    assert output.shape == (1, 10)
```

## 📝 Submitting Changes

### Pull Request Process

1. **Update your fork:**
   ```bash
   git fetch upstream
   git rebase upstream/main
   ```

2. **Push your changes:**
   ```bash
   git push origin feature/your-feature-name
   ```

3. **Create a Pull Request:**
   - Go to your fork on GitHub
   - Click "New Pull Request"
   - Provide a clear title and description
   - Reference any related issues

### Pull Request Checklist

- [ ] Code follows style guidelines
- [ ] Tests pass locally
- [ ] New tests added for new features
- [ ] Documentation updated
- [ ] No merge conflicts
- [ ] Commit messages are clear
- [ ] Screenshots included (if UI changes)

## 🎨 Style Guidelines

### Python Style

Follow [PEP 8](https://pep8.org/) guidelines:

- Use 4 spaces for indentation
- Maximum line length: 127 characters
- Use meaningful variable names
- Add docstrings to functions and classes
- Type hints for function parameters

Example:
```python
def predict_animal(image: Image, model: nn.Module) -> Dict[str, float]:
    """
    Predict animal species from image.
    
    Args:
        image: PIL Image object
        model: PyTorch model
    
    Returns:
        Dictionary with predictions and confidence scores
    """
    # Implementation here
    pass
```

### Code Formatting

Use automated tools:

```bash
# Format code with black
black .

# Sort imports with isort
isort .

# Lint with flake8
flake8 .
```

### Documentation

- Use clear, concise language
- Include code examples
- Add emojis for better readability 🎉
- Keep README up to date
- Document API endpoints

## 🏗️ Project Structure

```
animal-classification/
├── model.py              # Model architecture
├── train.py              # Training logic
├── main_api.py           # FastAPI server
├── analytics.py          # Metrics tracking
├── gradcam.py            # Visualization
├── security.py           # Security middleware
├── tests/                # Test suite
│   ├── test_model.py
│   ├── test_api.py
│   └── test_integration.py
├── frontend/             # Web interface
├── dataset/              # Training data
└── docs/                 # Documentation
```

## 🐛 Reporting Bugs

### Before Reporting

- Search existing issues
- Try latest version
- Reproduce the bug

### Bug Report Template

```markdown
**Describe the bug**
A clear description of what the bug is.

**To Reproduce**
Steps to reproduce the behavior:
1. Go to '...'
2. Click on '...'
3. See error

**Expected behavior**
What you expected to happen.

**Screenshots**
If applicable, add screenshots.

**Environment:**
- OS: [e.g., Windows 10]
- Python version: [e.g., 3.10]
- Browser: [e.g., Chrome 120]
```

## 💡 Feature Requests

We welcome feature requests! Please:

1. Check if feature already requested
2. Provide clear use case
3. Explain expected behavior
4. Consider implementation complexity

## 📚 Resources

- [PyTorch Documentation](https://pytorch.org/docs/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [ResNet Paper](https://arxiv.org/abs/1512.03385)
- [Grad-CAM Paper](https://arxiv.org/abs/1610.02391)

## 🏅 Recognition

Contributors will be recognized in:
- README contributors section
- Release notes
- Project documentation

## 📫 Contact

- GitHub Issues: [Project Issues](https://github.com/yourusername/animal-classification/issues)
- Email: your.email@example.com

Thank you for contributing! 🎉
