#!/usr/bin/env python
#-*- coding:utf-8 -*-

from setuptools import setup, find_packages
import build4s
import time

setup(
    name="Build4s",
    version="0.0.1",
    packages=find_packages(exclude=["test*"]),
    # py_modules=["test"],
    # data_files=[(".", ["pip_requirements.txt"])],
    install_requires=["PyYAML"],
    zip_safe=False,

    description="A build tools",
    author="pengmingqiang",
    author_email="pmq2008@gmail.com",

    license="GPL",
    platforms="Independant",
    url="",
    entry_points={
        'console_scripts': [
            'buildcli = build4s.cli:main',
        ]
    },
)
