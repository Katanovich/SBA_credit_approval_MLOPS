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


# Чтение версии
about = {}
VERSION_PATH = ROOT_DIR / "VERSION"
if not VERSION_PATH.exists():
    VERSION_PATH = ROOT_DIR / "classification_model" / "VERSION"

with open(VERSION_PATH) as f:
    about["__version__"] = f.read().strip()


def list_reqs(fname="requirements.txt"):
    # Проверяем 3 места, где может лежать файл:
    # 1. Прямо в папке с setup.py
    # 2. В папке requirements/ рядом с setup.py
    # 3. Во вложенной папке classification_model/

    possible_paths = [
        ROOT_DIR / fname,
        ROOT_DIR / "requirements" / fname,
        ROOT_DIR / "classification_model" / fname
    ]

    for path in possible_paths:
        if path.exists():
            with open(path) as fd:
                return fd.read().splitlines()

    # Если файл вообще не найден, возвращаем пустой список, чтобы не падать
    print(f"WARNING: {fname} not found!")
    return []


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
