#!/usr/bin/python

import subprocess
import sys
import os
import logging


class JarFileManager:

    def __init__(self, jar_bin):
        self.jar_bin = jar_bin
        self.logger = self.set_logger()

    def set_logger(self):
        logger = logging.getLogger(self.__class__.__name__)
        logger.setLevel(logging.DEBUG)
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger

    def extract_from_jar_file(self, jar_file, extract_file):
        try:
            extract = subprocess.check_call([self.jar_bin, '-xf', jar_file, extract_file])
            self.logger.info('extraktana datoteka: ' + extract_file)
        except Exception, e:
            self.logger.error(e)
            sys.exit(1)

    def add_to_jar_file(self, jar_file, add_file):
        try:
            add = subprocess.check_call([self.jar_bin, '-fu', jar_file, add_file])
            self.logger.info('zapakirana datoteka: ' + add_file)
        except Exception, e:
            self.logger.error(e)
            sys.exit(1)



