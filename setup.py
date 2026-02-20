from setuptools import setup, find_packages

setup(
    name="stars-cli",
    version="4.3.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "typer>=0.9.0",
        "rich>=13.0.0",
        "kubernetes>=28.0.0",
        "google-genai>=0.2.0",
        "prometheus-api-client>=0.5.0",
        "pyyaml>=6.0",
        "pydantic>=2.0.0",
        "pydantic-settings>=2.0.0",
        "keyring>=24.0.0",
    ],
    entry_points={
        "console_scripts": [
            "stars=stars.cli:main",
        ],
    },
    python_requires=">=3.9",
)
