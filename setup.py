#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Setup configuration for sentinel-x package
"""

from setuptools import setup, find_packages

# Read the contents of README file
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="sentinel-x",
    version="0.1.0",
    author="Shivam Gawade",
    author_email="shivamgawade@example.com",
    description="A powerful security monitoring and threat detection system",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/shivamgawade-droid/sentinel-x",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Topic :: Security",
        "Topic :: System :: Monitoring",
    ],
    python_requires=">=3.8",
    install_requires=[
        # Add your project dependencies here
        # Examples:
        # "requests>=2.25.0",
        # "numpy>=1.19.0",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=2.10",
            "black>=21.0",
            "flake8>=3.9",
            "isort>=5.0",
        ],
    },
    entry_points={
        "console_scripts": [
            # Add console script entry points here if needed
            # Example: "sentinel-x=sentinel_x.cli:main",
        ],
    },
    project_urls={
        "Bug Reports": "https://github.com/shivamgawade-droid/sentinel-x/issues",
        "Source": "https://github.com/shivamgawade-droid/sentinel-x",
        "Documentation": "https://github.com/shivamgawade-droid/sentinel-x#readme",
    },
    include_package_data=True,
    zip_safe=False,
)
