import os
from pathlib import Path

from pkg_resources.extern.packaging.version import Version
from setuptools import setup

# a version must be PEP 440 compliant
__version__ = Version("0.2.0")


def cwd() -> Path:
    return Path(os.path.dirname(__file__))


def read(path: str) -> str:
    filepath: Path = cwd() / path
    with open(filepath.absolute(), "r", encoding="utf-8") as f:
        return f.read()


setup(
    name="pytest-crate",
    version=str(__version__),
    description="Manages CrateDB instances during your integration tests",
    long_description=read("README.rst"),
    author="Christian Haudum",
    author_email="developer@christianhaudum.at",
    url="https://github.com/chaudum/pytest-crate",
    packages=["pytest_crate"],
    install_requires=[
        "cr8",
        "pytest>=4.0",
    ],
    extras_require={
        "develop": [
            "pytest-flake8",
            "pytest-mypy",
            "pytest-isort",
        ],
    },
    entry_points={
        "pytest11": [
            "crate=pytest_crate.plugin:crate",
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Framework :: Pytest",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: Unix",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Software Development :: Testing",
        "Topic :: Database",
    ],
)
