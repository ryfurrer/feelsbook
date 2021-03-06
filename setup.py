#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""feelsbook setup.py"""

import codecs
import os
import re
import sys

from setuptools import setup, find_packages
from setuptools.command.test import test


def find_version(*file_paths):
    with codecs.open(os.path.join(os.path.abspath(os.path.dirname(__file__)), *file_paths), "r") as fp:
        version_file = fp.read()
    m = re.search(r"^__version__ = \((\d+), ?(\d+), ?(\d+)\)", version_file, re.M)
    if m:
        return "{}.{}.{}".format(*m.groups())
    raise RuntimeError("Unable to find a valid version")


VERSION = find_version("feelsbook", "__init__.py")


class Pylint(test):
    user_options = [('pylint-args=', 'a', "Arguments to pass to pylint")]

    def initialize_options(self):
        test.initialize_options(self)
        self.pylint_args = "feelsbook --persistent=y --rcfile=.pylintrc --output-format=colorized"

    def run_tests(self):
        import shlex
        # import here, cause outside the eggs aren't loaded
        from pylint.lint import Run
        Run(shlex.split(self.pylint_args))


class PyTest(test):
    user_options = [("pytest-args=", "a", "Arguments to pass to pytest")]

    def initialize_options(self):
        test.initialize_options(self)
        self.pytest_args = "-v --cov={}".format("feelsbook")

    def run_tests(self):
        import shlex
        # import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(shlex.split(self.pytest_args))
        sys.exit(errno)


def readme():
    with open("README.rst", encoding="utf-8") as f:
        return f.read()


setup(
    name="FeelsBook",
    version=VERSION,
    description="Project for HakED 2019",
    long_description=readme(),
    author="Ryan Furrer",
    author_email="rfurrer@ualberta.ca",
    url="https://github.com/ryfurrer/feelsbook",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
    ],
    packages=find_packages(exclude=["test"]),
    include_package_data=True,
    package_data={
        "": ["README.rst"],
    },
    install_requires=[
    ],
    tests_require=[
        "pytest",
        "pytest-cov",
        "pylint",
    ],
    entry_points={
        "console_scripts": [
        ],
    },
    cmdclass={"test": PyTest, "lint": Pylint},
)
