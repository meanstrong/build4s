#!/usr/bin/env python
#-*- coding:utf-8 -*-

from setuptools import setup, find_packages


with open("README.md", encoding="utf-8") as f:
    readme = f.read()

with open("LICENSE", encoding="utf-8") as f:
    license = f.read()

setup(
    name="build4s",
    version="1.0.2",
    packages=find_packages(exclude=["test*"]),
    install_requires=["PyYAML"],
    zip_safe=False,

    url="https://github.com/meanstrong/build4s",
    # license=license,
    description="A build tools for CodeBuild",
    long_description=readme,
    long_description_content_type="text/markdown",
    author="pengmingqiang",
    author_email="rockypengchina@outlook.com",
    maintainer="pengmingqiang",
    maintainer_email="rockypengchina@outlook.com",
    platforms=['any'],

    entry_points={
        'console_scripts': [
            'buildcli = build4s.cli:main',
        ]
    },
)
