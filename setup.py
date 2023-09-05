import os

from setuptools import setup


def read(file_name):
    return open(os.path.join(os.path.dirname(__file__), file_name)).read()


setup(
    name="travelist_recruiting_task",
    version="0.1",
    author="Maciej Zięba",
    author_email="maciekz82@gmail.com",
    description="Travelist Recruiting Task",
    url="https://github.com/maciekz/travelist_recruiting_task",
    long_description=read("README.md"),
    entry_points={},
    install_requires=[
        "Django == 2.2.18",
        "factory-boy == 3.3.0",
        "pytest-django == 4.5.2",
    ],
    extras_require={
        "dev": [
            "black",
            "flake8",
            "flake8-isort",
            "isort",
            "mypy",
            "pydocstyle",
            "pylama",
            "prospector",
            "remote_pdb",
        ]
    },
)
