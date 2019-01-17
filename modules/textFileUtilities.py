#!/usr/bin/python


import re
import os
import sys
import shutil
import platform
import fileinput
import subprocess

java_home = os.environ['JAVA_HOME']
jar_bin = java_home + 'bin/jar'


def test1():
    print java_home
    print jar_bin


def change_working_directory(dir):
    try:
        os.chdir(dir)
        print '== Radni direktorij je %s' % os.getcwd()
    except:
        print '!! Ne postoji direktorij: %s%s. Prekidam izvrsavanje.\n' % (os.getcwd(), dir)
        sys.exit(1)


def recreate_tmp_directory(directory):
    try:
        shutil.rmtree(directory, ignore_errors=True)  # True da ne baca gresku ako ne postoji direktorij
        print '== Obrisan je direktorij %s' % directory
        os.mkdir(directory, 0755)
        print '== Kreiran je direktorij %s' % directory
    except Exception, e:
        print 'Greska: %s' % e


def search_in_file(file_to_search, search_string):
    try:
        f = open(file_to_search, 'r').read()
        if search_string in f:
            return True

    except Exception, e:
        print 'Greska: %s' % e
        return False


def search_and_replace_in_file(file_to_modify, file_to_save, search_string, replace_string):
    try:
        f = open(file_to_modify, 'r').read()
        search = search_string
        replace = replace_string
        w = open(file_to_save, 'w')
        w.write(f.replace(search, replace))
        w.close()
        print '== Promijene spremljene u datoteku %s.' % file_to_save
        return True

    except IOError, e:
        print '!! I/O greska: %s' % e
        return False

    except OSError, e:
        print '!! OS greska: %s' % e
        return False


def add_in_file_from_template(file_to_add,template_file,starting_line,position):
    try:
        f = open(template_file,'r').read()
        for line in fileinput.input(file_to_add, inplace=1):
            if line.startswith(starting_line):
                if position == 'after':
                    print line,
                    print f.rstrip()
                elif position == 'before':
                    print f.rstrip()
                    print line,
                else:
                    print 'Pozicija teksta koji se dodaje u file nije ispravno zadana. Moze biti "after" ili "before"!'
                    return False

        print line,
        print 'Text dodan u datoteku %s.' % file_to_add
        return True

    except Exception, e:
        print e
        return False

