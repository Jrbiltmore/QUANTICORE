from setuptools import setup, find_packages

setup(
    name="quanticore",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "numpy",
        "scipy",
        "pandas",
        "sklearn",
        "matplotlib",
    ],
    entry_points={
        "console_scripts": [
            "quanticore=src.core:main",
        ],
    },
)
