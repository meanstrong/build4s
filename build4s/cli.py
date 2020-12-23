#!/usr/bin/env python
#-*- coding:utf-8 -*-

import sys
import traceback

from .build import Build


def main():
    spec_file = "buildspec.yml"
    target_file = "target.zip"
    for arg in sys.argv:
        if arg.startswith("--spec-file="):
            spec_file = arg.split("=", 1)[1]
        elif arg.startswith("--target-file="):
            target_file = arg.split("=", 1)[1]
        elif arg == "-h" or arg == "--help":
            print_help()
            return

    if spec_file is None or target_file is None:
        print_help()
        return

    Build().set_spec_file(spec_file).set_target_file(target_file).build()

def print_help():
    msg = '''
    Usage: buildcli --spec-file=buildspec_debug.yml
    Options:
        --spec-file     The build spec file path, default is buildspec.yml.
        --target-file   The ZIP result filename.
    '''
    print(msg)


if __name__ == "__main__":
    main()
