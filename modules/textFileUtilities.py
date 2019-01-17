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


def add_text_block_to_file_from_template(file_to_add, template_file_path, starting_line, position):
    try:
        f_template = open(template_file_path, 'r').read()
        text_block = f_template.rstrip()
        for line in fileinput.input(file_to_add, inplace=1):
            if starting_line in line:
                if position == 'after':
                    print text_block
                elif position == 'before':
                    print text_block
                else:
                    print 'Pozicija teksta koji se dodaje u file nije ispravno zadana. Moze biti "after" ili "before"!'
                    return False
            print line, #zarez znaci da se ne ispisuje nova prazna linija poslije komande 'print'(sto python inace radi)

        print 'Text dodan u datoteku %s.' % file_to_add
        return True

    except Exception, e:
        print e
        return False


def add_text_block_to_file_from_template_with_parameters(file_to_add, template_file_path, properties_file_path, parameter_names_list, starting_line, position):
    parameters_dict = read_properties_file_parameters(parameter_names_list, properties_file_path)
    text_block = get_text_block_from_template_with_parameters(parameters_dict, template_file_path)
    try:
        for line in fileinput.input(file_to_add, inplace=1):
            if starting_line in line:
                if position == 'after':
                    print line,
                    print text_block
                elif position == 'before':
                    print text_block
                    print line,
                else:
                    print text_block #Ako nije ispravno zadan 'position', onda se text_block dodaje iznad zadane linije 'starting_line', tj 'before'
                    print line,

            else:
                print line,  # zarez znaci da se ne ispisuje nova prazna linija poslije komande 'print'(sto python inace radi)

        print 'Text dodan u datoteku %s.' % file_to_add
        return True
    except Exception, e:
        print e
        return False




def get_text_block_from_template_with_parameters(parameters_dict,template_file_path):
    template_block_list = []
    text_block = ''
    try:
        f_template = open(template_file_path, 'r').readlines()
        for line in f_template:
            for key in parameters_dict.iterkeys():
                template_block_list.append(line.replace(key, parameters_dict[key]))

        text_block = text_block.join(template_block_list)
        return text_block

    except Exception, e:
        print e
        return False


def read_properties_file_parameters(parameter_names_list,properties_file_path):
    parameters_dict = {}
    try:
        if len(parameter_names_list) > 0:
            prop_f = open(properties_file_path, 'r').readlines()
            for parameter in parameter_names_list:
                for line in prop_f:
                    if parameter in line and line[0] != '#':
                        value = line.split('=',1)[1].strip()#drugi argument '1' u split() funkciji znaci da radi split samo na prvom znanku '='.to treba jer vrijednosti nekih parametara imaju takoder u sebi znak '=', npr. SCOPE_CONT
                        parameters_dict[parameter] = value
        return parameters_dict

    except Exception, e:
        print e
        return False




