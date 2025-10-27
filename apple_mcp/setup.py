#!/usr/bin/env python3
"""
Setup configuration for Tonnage MCP Server
"""

from setuptools import setup, find_packages
import os

# Read the long description from README
def read_file(filename):
    filepath = os.path.join(os.path.dirname(__file__), filename)
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    return ""

setup(
    name="tonnage-mcp-server",
    version="1.0.0",
    description="MCP Server for Apple Tonnage Prediction",
    long_description=read_file("README.md"),
    long_description_content_type="text/markdown",
    author="Your Name",
    author_email="your.email@example.com",
    url="https://github.com/yourusername/apple_mcp",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.8",
    install_requires=[
        "pandas>=1.3.0",
        "numpy>=1.21.0",
        "scikit-learn>=1.0.0",
        "flask>=2.0.0",
        "flask-cors>=3.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-asyncio>=0.21.0",
            "pytest-cov>=4.0.0",
            "pytest-mock>=3.10.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
        ]
    },
    entry_points={
        "console_scripts": [
            "tonnage-mcp-server=tonnage_mcp.server:main",
            "tonnage-http-server=tonnage_mcp.http_wrapper:main",
        ]
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    keywords="mcp server tonnage prediction machine-learning",
    project_urls={
        "Documentation": "https://github.com/yourusername/apple_mcp/blob/main/docs/",
        "Source": "https://github.com/yourusername/apple_mcp",
        "Bug Reports": "https://github.com/yourusername/apple_mcp/issues",
    },
)
