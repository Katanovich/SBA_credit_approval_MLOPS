#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pathlib import Path
from setuptools import find_packages, setup

# Package meta-data.
NAME = 'classification_model'
DESCRIPTION = "Example of classification model"
URL = "https://github.com/Katanovich/SBA_credit_approval_MLOPS" # Твой репозиторий
EMAIL = "vera-vla.edu@gmail.com"
AUTHOR = "Khegay, Kim, Kim"
REQUIRES_PYTHON = ">=3.7.0"

long_description = DESCRIPTION


ROOT_DIR = Path(__file__).resolve().parent


PACKAGE_DIR = ROOT_DIR


REQUIREMENTS_DIR = ROOT_DIR / 'requirements'


about = {}

with open(ROOT_DIR / "VERSION") as f:
    _version = f.read().strip()
    about["__version__"] = _version

# Функция для чтения требований
def list_reqs(fname="requirements.txt"):
    # Проверяем, есть ли папка requirements, если нет - ищем в корне папки
    path = REQUIREMENTS_DIR / fname if REQUIREMENTS_DIR.exists() else ROOT_DIR / fname
    with open(path) as fd:
        return fd.read().splitlines()

setup(
    name=NAME,
    version=about["__version__"],
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    packages=find_packages(exclude=("tests",)),
    package_data={"classification_model": ["VERSION"]},
    install_requires=list_reqs(),
    include_package_data=True,
    license="BSD-3",
    classifiers=[
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: Implementation :: CPython",
    ],
)
