#!/usr/bin/env python3
"""
Setup script for QuantQuill package.
"""

from setuptools import setup, find_packages

setup(
    name="quantquill",
    version="0.1.0",
    description="A comprehensive quantitative trading framework with strategy backtesting and execution capabilities",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="jaskirat1208",
    author_email="jaskirat@example.com",
    url="https://github.com/jaskirat1208/quantquill",
    license="MIT",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        "quantquill": ["*.json", "*.yaml", "*.yml", "*.txt"],
    },
    install_requires=[
        "smartapi-python>=1.5.5",
        "plotly>=6.6.0", 
        "pandas>=2.3.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=22.0.0",
            "flake8>=5.0.0",
            "mypy>=1.0.0",
        ],
        "docs": [
            "sphinx>=5.0.0",
            "sphinx-rtd-theme>=1.0.0",
        ],
    },
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Financial and Insurance Industry",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Office/Business :: Financial :: Investment",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords=["trading", "quantitative", "backtesting", "strategies", "finance"],
    entry_points={
        "console_scripts": [
            "quantquill=quantquill.cli:main",
        ],
    },
)
