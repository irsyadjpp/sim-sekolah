#!/usr/bin/env python3
"""
Publish script for simsekolah-ai Python SDK

This script handles building and publishing the SDK to PyPI or internal registry.
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path


def run_command(cmd, check=True):
    """Run a shell command."""
    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, check=check)
    return result


def clean_build():
    """Clean build artifacts."""
    print("Cleaning build artifacts...")
    dirs_to_remove = ["dist", "build", "*.egg-info", "simsekolah_ai.egg-info"]
    
    for dir_name in dirs_to_remove:
        for path in Path(".").glob(dir_name):
            if path.is_dir():
                run_command(["rm", "-rf", str(path)])
                print(f"Removed {path}")


def build_package():
    """Build the package."""
    print("Building package...")
    run_command([sys.executable, "-m", "build"])


def publish_to_pypi(repository_url=None):
    """Publish to PyPI."""
    print("Publishing to PyPI...")
    
    cmd = [sys.executable, "-m", "twine", "upload", "dist/*"]
    
    if repository_url:
        cmd.extend(["--repository-url", repository_url])
    
    run_command(cmd)


def publish_to_test_pypi():
    """Publish to TestPyPI."""
    print("Publishing to TestPyPI...")
    run_command([
        sys.executable, "-m", "twine", "upload",
        "--repository", "testpypi",
        "dist/*"
    ])


def check_version():
    """Check if version is properly set."""
    try:
        import simsekolah_ai
        version = simsekolah_ai.__version__
        print(f"Current version: {version}")
        return version
    except ImportError:
        print("Warning: Could not import simsekolah_ai to check version")
        return None


def bump_version(version_type="patch"):
    """Bump the version number."""
    import re
    
    # Read current version
    with open("simsekolah_ai/__init__.py", "r") as f:
        content = f.read()
    
    # Extract current version
    version_match = re.search(r'__version__ = ["\']([^"\']+)["\']', content)
    if not version_match:
        raise ValueError("Could not find version in __init__.py")
    
    current_version = version_match.group(1)
    major, minor, patch = map(int, current_version.split("."))
    
    # Bump version
    if version_type == "major":
        major += 1
        minor = 0
        patch = 0
    elif version_type == "minor":
        minor += 1
        patch = 0
    else:  # patch
        patch += 1
    
    new_version = f"{major}.{minor}.{patch}"
    
    # Update version
    new_content = re.sub(
        r'__version__ = ["\'][^"\']+["\']',
        f'__version__ = "{new_version}"',
        content
    )
    
    with open("simsekolah_ai/__init__.py", "w") as f:
        f.write(new_content)
    
    # Update pyproject.toml
    with open("pyproject.toml", "r") as f:
        pyproject_content = f.read()
    
    pyproject_content = re.sub(
        r'version = "\d+\.\d+\.\d+"',
        f'version = "{new_version}"',
        pyproject_content
    )
    
    with open("pyproject.toml", "w") as f:
        f.write(pyproject_content)
    
    print(f"Version bumped from {current_version} to {new_version}")
    return new_version


def main():
    parser = argparse.ArgumentParser(description="Publish simsekolah-ai SDK")
    parser.add_argument(
        "--target",
        choices=["pypi", "testpypi", "internal"],
        default="pypi",
        help="Target registry"
    )
    parser.add_argument(
        "--repository-url",
        help="Custom repository URL for internal registry"
    )
    parser.add_argument(
        "--clean",
        action="store_true",
        help="Clean build artifacts before building"
    )
    parser.add_argument(
        "--skip-build",
        action="store_true",
        help="Skip building (use existing dist/)"
    )
    parser.add_argument(
        "--bump",
        choices=["major", "minor", "patch"],
        help="Bump version before publishing"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Do everything except actually publishing"
    )
    
    args = parser.parse_args()
    
    # Change to script directory
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    # Bump version if requested
    if args.bump:
        bump_version(args.bump)
    
    # Check version
    check_version()
    
    # Clean if requested
    if args.clean:
        clean_build()
    
    # Build package
    if not args.skip_build:
        build_package()
    else:
        print("Skipping build, using existing dist/")
    
    # Publish
    if not args.dry_run:
        if args.target == "pypi":
            publish_to_pypi(args.repository_url)
        elif args.target == "testpypi":
            publish_to_test_pypi()
        elif args.target == "internal":
            if not args.repository_url:
                parser.error("--repository-url is required for internal registry")
            publish_to_pypi(args.repository_url)
    else:
        print("Dry run - skipping actual publishing")
        print("Would publish to:", args.target)
        if args.repository_url:
            print("Repository URL:", args.repository_url)


if __name__ == "__main__":
    main()