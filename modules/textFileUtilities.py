#!/usr/bin/python


import re
import os
import sys
import shutil
import platform
import fileinput
import subprocess


java_home = os.environ['JAVA_HOME']
jar_bin = java_home+'bin/jar'


def test1():

    print java_home
    print jar_bin


def changeWorkDir(dir):
    print dir
    try:
      os.chdir(os.path.dirname(dir))
      print '== Radni direktorij je %s' % os.getcwd()
    except:
        print '!! Ne postoji direktorij: %s%s. Prekidam izvrsavanje.\n' % (os.getcwd(),dir)
        sys.exit(1)



def search_in_file(fileToSearch, searchStrBlock):

    try:
        f = open(fileToSearch, 'r').read()
        if searchStrBlock in f:
            return True

    except Exception, e:
        print 'Greska: %s' % e
        return False

