#!/usr/bin/python


import re
import os
import sys
import shutil
import platform
import fileinput
import subprocess


def test1():
    print 'Radiiiiiiiiiiiiiiiiiiii'


def search_in_file(fileToSearch, searchStrBlock):

    try:
        f = open(fileToSearch, 'r').read()
        if searchStrBlock in f:
            return True

    except Exception, e:
        print 'Greska: %s' % e
        return False

