from setuptools import setup

setup(
    name="tars-cli",
    version="2.0.0",
    py_modules=["tars"],
    install_requires=[
        "typer",
        "rich",
        "kubernetes",
        "google-genai",
    ],
    entry_points={
        "console_scripts": [
            "tars=tars:app",
        ],
    },
)
