#!/usr/bin/env python
#-*- coding:utf-8 -*-

from setuptools import setup, find_packages

import build4s


with open("README.md", encoding="utf-8") as f:
    readme = f.read()

setup(
    name="build4s",
    version=build4s.__version__,
    packages=find_packages(exclude=["test*"]),
    install_requires=["PyYAML"],
    zip_safe=False,

    url="https://github.com/meanstrong/build4s",
    description="A build tools for CodeBuild",
    long_description=readme,
    long_description_content_type="text/markdown",
    author="pengmingqiang",
    author_email="rockypengchina@outlook.com",
    maintainer="pengmingqiang",
    maintainer_email="rockypengchina@outlook.com",
    platforms=['any'],
    license="GPLv3",
    entry_points={
        'console_scripts': [
            'buildcli = build4s.cli:main',
        ]
    },
)
