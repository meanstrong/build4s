#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os
import subprocess
import zipfile
import logging

import yaml

class Build(object):
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter("[%(asctime)s] [%(name)s] [%(levelname)s] : %(message)s")
        sh = logging.StreamHandler()
        sh.setFormatter(formatter)
        sh.setLevel(logging.DEBUG)
        self.logger.addHandler(sh)

        self._spec_file = None
        self._variables = None
        self._parameters = None
        self._target_file = None

    def set_spec_file(self, spec_file):
        self._spec_file = spec_file
        return self

    def set_target_file(self, target_file):
        if not target_file.endswith(".zip"):
            target_file += ".zip"
        self._target_file = target_file
        return self

    def build(self):
        with open(self._spec_file, "r") as f:
            buildspec = yaml.load(f.read())

        env = buildspec.get("env")
        if env is not None:
            self._variables = env.get("variables")
            self._parameters = env.get("parameter-store")

        phases = buildspec.get("phases")

        if phases is not None:
            self.logger.info("phase install ...")
            install = phases.get("install")
            if install is not None:
                self._run_commands(install.get("commands"))

            self.logger.info("phase pre_build ...")
            pre_build = phases.get("pre_build")
            if pre_build is not None:
                self._run_commands(pre_build.get("commands"))

            self.logger.info("phase build ...")
            build = phases.get("build")
            if build is not None:
                self._run_commands(build.get("commands"))

            self.logger.info("phase post_build ...")
            post_build = phases.get("post_build")
            if post_build is not None:
                self._run_commands(post_build.get("commands"))

        self.logger.info("artifacts > %s ..." % self._target_file)
        self.artifacts(buildspec.get("artifacts"))

        self.logger.info("build OK.")

    def _run_commands(self, commands):
        if commands is None:
            return
        try:
            for cmd in commands:
                self._run_cmd(cmd)
        except Exception as err:
            raise Exception("error: " + repr(err))

    def _run_cmd(self, cmd):
        env = os.environ.copy()
        if self._variables is not None:
            env.update(self._variables)
        if self._parameters is not None:
            env.update(self._parameters)
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, env=env)
        while p.poll() is None:
            line = p.stdout.readline()
            self.logger.info(line.strip())
        rc = p.returncode
        if rc != 0:
            self.logger.warn("rc: " + str(rc))
            self.logger.warn("stderr: " + p.stderr.read())
            raise Exception("run cmd error.")
        return rc

    def artifacts(self, artifacts):
        if artifacts is None:
            return
        if artifacts.get("base-directory") is not None:
            root_path = artifacts.get("base-directory")
        else:
            root_path = "."
        discard_paths = artifacts.get("discard-paths")

        zf = zipfile.ZipFile(self._target_file, "w")
        for entry in artifacts.get("files"):
            if entry.endswith("**/*"):
                for root, dirs, files in os.walk(os.path.join(root_path, entry[:-4])):
                    for f in files:
                        self.compress(zf, root_path, os.path.join(root, f), discard_paths)
            elif entry.endswith("/*"):
                subdir = entry[:-2]
                for f in os.listdir(os.path.join(root_path, subdir)):
                    f = os.path.join(root_path, subdir, f)
                    if os.path.isfile(f):
                        self.compress(zf, root_path, f, discard_paths)
            else:
                self.compress(zf, root_path, os.path.join(root_path, entry), discard_paths)
        zf.close()

    @staticmethod
    def compress(zf, root_path, filename, discard_path=False):
        if discard_path:
            arcname = os.path.basename(filename)
        else:
            arcname = os.path.relpath(filename, root_path)
        zf.write(filename, arcname)
