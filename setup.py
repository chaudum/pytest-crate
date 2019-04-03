from setuptools import setup


def read(filename: str) -> str:
    with open(filename, "r") as fp:
        return fp.read()


setup(
    name="pytest-crate",
    version="0.1",
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
        "Development Status :: 3 - Alpha/Unstable",
        "Framework :: Pytest",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Software Development :: Testing",
    ],
)
