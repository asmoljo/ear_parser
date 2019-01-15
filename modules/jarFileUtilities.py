#!/usr/bin/python

import subprocess
import sys
import os

java_home = os.environ['JAVA_HOME']
jar_bin = java_home+'bin/jar'


def extractFromJarFile(jarFile, extractFile):
    try:
        extract = subprocess.check_call([jar_bin, '-xf', jarFile, extractFile])
        if not os.path.exists(extractFile):
            print "!! Ne postoji datoteka '" + extractFile + "' u arhivi '" + jarFile + "'. Prekidam izvrsavanje.\n"
            sys.exit(1)
    except IOError, e:
        print '!! %s' % e + '. Prekidam izvrsavanje.\n'
        sys.exit(1)

