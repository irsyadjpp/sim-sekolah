# Python SDK Publishing Guide

This guide explains how to publish the SimSekolah AI Platform Python SDK to PyPI or internal registry.

## Prerequisites

### Required Tools

```bash
# Install build tools
pip install --upgrade build twine hatchling

# Install development tools (optional)
pip install --upgrade pip setuptools wheel
```

### PyPI Credentials

For publishing to PyPI, you need:
- PyPI account: https://pypi.org/account/register/
- API token: https://pypi.org/manage/account/token/
- Configure twine: `twine configure`

For internal registry, you'll need the registry URL and credentials.

## Publishing Process

### 1. Version Management

```bash
# Bump version (patch, minor, or major)
python publish.py --bump patch

# Or manually edit version in:
# - simsekolah_ai/__init__.py
# - pyproject.toml
```

### 2. Clean Build Artifacts

```bash
# Clean previous builds
python publish.py --clean

# Or manually
rm -rf dist/ build/ *.egg-info/
```

### 3. Build Package

```bash
# Build wheel and source distribution
python publish.py

# Or manually
python -m build
```

This creates:
- `dist/simsekolah-ai-0.1.0.tar.gz` (source distribution)
- `dist/simsekolah_ai-0.1.0-py3-none-any.whl` (wheel)

### 4. Publish to PyPI

```bash
# Publish to PyPI
python publish.py --target pypi

# Or manually
twine upload dist/*
```

### 5. Publish to TestPyPI

```bash
# Publish to TestPyPI for testing
python publish.py --target testpypi

# Or manually
twine upload --repository testpypi dist/*
```

### 6. Publish to Internal Registry

```bash
# Publish to internal registry
python publish.py --target internal --repository-url https://pypi.simsekolah.com/simple

# Or manually
twine upload --repository-url https://pypi.simsekolah.com/simple dist/*
```

## Environment Configuration

### PyPI Configuration

Create `~/.pypirc`:

```ini
[distutils]
index-servers =
    pypi
    testpypi
    internal

[pypi]
username = __token__
password = <your-pypi-token>

[testpypi]
repository = https://test.pypi.org/legacy/
username = __token__
password = <your-testpypi-token>

[internal]
repository = https://pypi.simsekolah.com/simple/
username = <username>
password = <password>
```

### Internal Registry Setup

For internal registry, you may need to:

1. Set up a PyPI server (e.g., devpi, pypiserver)
2. Configure SSL certificates
3. Set up authentication
4. Configure CI/CD pipelines

## CI/CD Integration

### GitHub Actions Example

```yaml
name: Publish Python SDK

on:
  push:
    tags:
      - 'v*'

jobs:
  publish:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Install build dependencies
      run: |
        python -m pip install --upgrade build twine hatchling
    
    - name: Build package
      working-directory: ./sdk/python
      run: |
        python -m build
    
    - name: Publish to PyPI
      working-directory: ./sdk/python
      env:
        TWINE_USERNAME: __token__
        TWINE_PASSWORD: ${{ secrets.PYPI_API_TOKEN }}
      run: |
        twine upload dist/*
```

### GitLab CI Example

```yaml
publish:
  stage: deploy
  only:
    - tags
  script:
    - cd sdk/python
    - pip install build twine
    - python -m build
    - twine upload --repository-url ${CI_API_V4_URL}/project/${CI_PROJECT_ID}/packages/pypi dist/*
```

## Versioning Strategy

Follow Semantic Versioning (SemVer):

- **MAJOR**: Breaking changes, incompatible API updates
- **MINOR**: New features, backwards-compatible changes
- **PATCH**: Bug fixes, backwards-compatible changes

Example:
- `0.1.0` → `0.1.1` (patch release)
- `0.1.0` → `0.2.0` (minor release)  
- `0.1.0` → `1.0.0` (major release)

## Pre-Publishing Checklist

- [ ] Version number updated in `__init__.py` and `pyproject.toml`
- [ ] CHANGELOG.md updated with release notes
- [ ] All tests passing (`pytest`)
- [ ] Code formatted (`black`, `isort`)
- [ ] Type checking passed (`mypy`)
- [ ] Documentation updated
- [ ] README.md examples tested
- [ ] Dependencies are up-to-date
- [ ] No sensitive information in package

## Post-Publishing Tasks

1. **Verify Installation**
   ```bash
   pip install simsekolah-ai
   python -c "import simsekolah_ai; print(simsekolah_ai.__version__)"
   ```

2. **Test in Clean Environment**
   ```bash
   python -m venv test_env
   source test_env/bin/activate
   pip install simsekolah-ai
   python -c "from simsekolah_ai import AIClient; print('OK')"
   ```

3. **Update Documentation**
   - Update version in documentation
   - Publish release notes
   - Tag repository with version

4. **Monitor Downloads**
   - Check PyPI stats
   - Monitor for installation issues
   - Respond to user feedback

## Troubleshooting

### Build Errors

**Issue**: Build fails with import errors
```bash
# Solution: Install package in development mode first
pip install -e .
python -m build
```

**Issue**: Missing dependencies
```bash
# Solution: Update pyproject.toml dependencies
# Then clean and rebuild
python publish.py --clean
python -m build
```

### Publishing Errors

**Issue**: 403 Forbidden from PyPI
```bash
# Solution: Check API token
twine check
# Regenerate token if needed
```

**Issue**: File already exists
```bash
# Solution: Delete from PyPI and republish, or bump version
python publish.py --bump patch
```

**Issue**: Invalid package name
```bash
# Solution: Ensure package name is valid (lowercase, hyphens only)
# Check in pyproject.toml and setup.py
```

### Internal Registry Issues

**Issue**: SSL certificate errors
```bash
# Solution: For development, add trusted hosts
pip install --trusted-host pypi.simsekolah.com simsekolah-ai
```

**Issue**: Authentication failures
```bash
# Solution: Verify credentials and repository URL
twine check --repository-url https://pypi.simsekolah.com/simple
```

## Rollback Procedure

If a published version has issues:

1. **Yank the version** (PyPI only):
   ```bash
   # This requires PyPI admin privileges
   # Contact PyPI support or use web interface
   ```

2. **Publish a fix**:
   ```bash
   python publish.py --bump patch
   # Fix the issue
   python -m build
   twine upload dist/*
   ```

3. **Communicate**:
   - Update documentation
   - Notify users of the issue
   - Provide migration guide if needed

## Best Practices

1. **Always test** before publishing
2. **Use semantic versioning** consistently
3. **Document changes** in CHANGELOG
4. **Tag releases** in Git
5. **Monitor** for issues after publishing
6. **Keep dependencies** updated and secure
7. **Use environment markers** for platform-specific dependencies
8. **Include license** and proper metadata
9. **Write clear descriptions** and usage examples
10. **Maintain backward compatibility** when possible

## Automated Publishing

### Using GitHub Actions

Create `.github/workflows/publish.yml`:

```yaml
name: Publish SDK

on:
  push:
    tags:
      - 'v*'

jobs:
  publish:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          pip install build twine
      
      - name: Build
        working-directory: ./sdk/python
        run: python -m build
      
      - name: Publish to PyPI
        working-directory: ./sdk/python
        env:
          TWINE_USERNAME: __token__
          TWINE_PASSWORD: ${{ secrets.PYPI_API_TOKEN }}
        run: twine upload dist/*
```

## Security Considerations

1. **Never commit** API tokens or credentials
2. **Use environment variables** for sensitive data
3. **Sign packages** if using internal registry
4. **Verify checksums** after download
5. **Monitor** for supply chain attacks
6. **Review dependencies** regularly for vulnerabilities
7. **Use Dependabot** for dependency updates

## Support

For publishing issues:
- Documentation: https://packaging.python.org/
- Twine docs: https://twine.readthedocs.io/
- PyPI help: https://pypi.org/help/
- Platform team: platform@simsekolah.com