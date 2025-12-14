# Contributing to AI E-commerce Search

Thank you for your interest in contributing! This document provides guidelines for contributing to this project.

## 🤝 How to Contribute

### Reporting Bugs

If you find a bug, please create an issue with:
- Clear description of the problem
- Steps to reproduce
- Expected vs actual behavior
- Environment details (OS, Python version, etc.)
- Screenshots if applicable

### Suggesting Features

Feature requests are welcome! Please:
- Check if the feature already exists or is planned
- Provide a clear use case
- Explain why this would be valuable
- Consider implementation complexity

### Pull Requests

1. **Fork the repository**
   ```bash
   git clone https://github.com/yourusername/AI-FRONTEND.git
   cd AI-FRONTEND
   ```

2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make your changes**
   - Write clean, readable code
   - Follow existing code style
   - Add comments for complex logic
   - Update documentation if needed

4. **Test your changes**
   ```bash
   # Run the application locally
   python main.py
   
   # Test all endpoints
   curl http://localhost:5000/health
   ```

5. **Commit your changes**
   ```bash
   git add .
   git commit -m "feat: add amazing new feature"
   ```

6. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

7. **Create a Pull Request**
   - Provide a clear description
   - Reference any related issues
   - Include screenshots if UI changes

## 📝 Coding Standards

### Python Style
- Follow PEP 8 guidelines
- Use meaningful variable names
- Keep functions focused and small
- Add docstrings to functions and classes

### Example:
```python
def process_image(image_file):
    """
    Process uploaded image for CNN prediction.
    
    Args:
        image_file: Uploaded file object
        
    Returns:
        Preprocessed numpy array ready for model
    """
    # Implementation
    pass
```

### Commit Messages
Follow conventional commits:
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `style:` Code style changes
- `refactor:` Code refactoring
- `test:` Adding tests
- `chore:` Maintenance tasks

## 🧪 Testing

Before submitting:
- Test all API endpoints
- Verify Docker build works
- Check health endpoint responds
- Test with sample data

## 📚 Documentation

When adding features:
- Update README.md if needed
- Add API documentation
- Include code comments
- Update environment variables

## 🔍 Code Review

All submissions require review. We look for:
- Code quality and readability
- Proper error handling
- Security considerations
- Performance implications
- Documentation completeness

## 🎯 Priority Areas

We especially welcome contributions in:
- Performance optimization
- Additional search methods
- UI/UX improvements
- Test coverage
- Documentation
- Bug fixes

## ❓ Questions?

Feel free to:
- Open an issue for discussion
- Ask in pull request comments
- Reach out to maintainers

## 📜 License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for making this project better! 🙌
