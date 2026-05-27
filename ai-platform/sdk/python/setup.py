"""
Setup script for simsekolah-ai package

This file provides backward compatibility for tools that expect setup.py.
"""

from setuptools import setup

# Read README for long description
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Read version from __init__.py
with open("simsekolah_ai/__init__.py", "r", encoding="utf-8") as fh:
    for line in fh:
        if line.startswith("__version__"):
            version = line.split("=")[1].strip().strip('"').strip("'")
            break
    else:
        version = "0.1.0"

setup(
    name="simsekolah-ai",
    version=version,
    author="SimSekolah Platform Team",
    author_email="platform@simsekolah.com",
    description="Python SDK for SimSekolah AI Platform services",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/simsekolah/ai-platform-sdk-python",
    project_urls={
        "Bug Tracker": "https://github.com/simsekolah/ai-platform-sdk-python/issues",
        "Documentation": "https://github.com/simsekolah/ai-platform-sdk-python#readme",
        "Source Code": "https://github.com/simsekolah/ai-platform-sdk-python",
    },
    packages=["simsekolah_ai"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    python_requires=">=3.8",
    install_requires=[
        "grpcio>=1.50.0",
        "grpcio-health-checking>=1.0.0",
        "protobuf>=4.0.0",
        "pydantic>=2.0.0",
        "tenacity>=8.0.0",
        "circuitbreaker>=2.0.0",
        "python-dotenv>=1.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-asyncio>=0.21.0",
            "pytest-cov>=4.1.0",
            "black>=23.0.0",
            "isort>=5.12.0",
            "mypy>=1.5.0",
            "ruff>=0.1.0",
            "pre-commit>=3.0.0",
        ],
        "docs": [
            "sphinx>=7.0.0",
            "sphinx-rtd-theme>=1.3.0",
            "myst-parser>=2.0.0",
        ],
    },
)