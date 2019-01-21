#!/usr/bin/python

import os
import sys
import shutil
import platform
import fileinput
import subprocess
import logging


class TextFileManager():

    def __init__(self, properties_build_file, properties_common_file, template_dir):
        self.properties_build = properties_build_file
        self.properties_common = properties_common_file
        self.template_dir = template_dir
        self.logger = self.set_logger()

    def set_logger(self):
        logger = logging.getLogger(self.__class__.__name__)
        logger.setLevel(logging.DEBUG)
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger


    def change_working_directory(self, dir):
        try:
            os.chdir(dir)
            self.logger.info('Radni direktorij je %s' % os.getcwd())
        except Exception, e:
            self.logger.error(e)
            sys.exit(1)


    def recreate_tmp_directory(self, directory):
        try:
            shutil.rmtree(directory, ignore_errors=True)  # True da ne baca gresku ako ne postoji direktorij
            self.logger.info('Obrisan je direktorij %s' % directory)
            os.mkdir(directory, 0755)
            self.logger.info('Kreiran je direktorij %s' % directory)
        except Exception, e:
            self.logger.error(e)
            sys.exit(1)


    def search_in_file(self, file_to_search, search_string):
        try:
            f = open(file_to_search, 'r').read()
            if search_string in f:
                return True
            else:
                return False
        except Exception, e:
            self.logger.error(e)
            sys.exit(1)


    def search_and_replace_in_file(self, file_to_modify, file_to_save, search_string, replace_string):
        try:
            f = open(file_to_modify, 'r').read()
            search = search_string
            replace = replace_string
            w = open(file_to_save, 'w')
            w.write(f.replace(search, replace))
            w.close()
            self.logger.info('Izmjena texta napravljena u datoteci %s.' % file_to_save)
            return True

        except Exception, e:
            self.logger.error(e)
            return False


    def add_text_block_to_file_from_template(self, file_to_add, template_file_name, starting_line, position):
        try:
            f_template = open(self.template_dir+template_file_name, 'r').read()
            text_block = f_template.rstrip()
            for line in fileinput.input(file_to_add, inplace=1):
                if starting_line in line:
                    if position == 'after':
                        print line,
                        print text_block
                    elif position == 'before':
                        print text_block
                        print line,
                    else:
                        print text_block  # Ako nije ispravno zadan 'position', onda se text_block dodaje iznad zadane linije 'starting_line', tj 'before'
                        print line,

                else:
                    print line,  # zarez znaci da se ne ispisuje nova prazna linija poslije komande 'print'(sto python inace radi)

            self.logger.info('Text iz templatea "%s" dodan u datoteku "%s".' % (template_file_name, file_to_add))
            return True

        except Exception, e:
            self.logger.error(e)
            return False

    def add_text_block_to_file_from_template_with_parameters(self, file_to_add, template_file_name, parameter_names_list, starting_line, position):
        parameters_dict = self.read_properties_file_parameters(parameter_names_list)
        text_block = self.get_text_block_from_template_with_parameters(parameters_dict, template_file_name)
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

            self.logger.info('Text iz templatea "%s" dodan u datoteku "%s".' % (template_file_name, file_to_add))
            return True
        except Exception, e:
            self.logger.error(e)
            return False


    def get_text_block_from_template_with_parameters(self, parameters_dict,template_file_name):
        template_block_list = []
        text_block = ''
        try:
            f_template = open(self.template_dir+template_file_name, 'r').readlines()
            for line in f_template:
                for key in parameters_dict.iterkeys():
                    template_block_list.append(line.replace(key, parameters_dict[key]))

            text_block = text_block.join(template_block_list)
            return text_block

        except Exception, e:
            self.logger.error(e)
            return False


    #Metoda koja skenira obje propertie datoteke properties.build i properties.common i trazi parametre koji su predani u listi i ako nadje parametre stavlja ih u Dictionary i vraca
    def read_properties_file_parameters(self, parameter_names_list):
        parameters_dict = {}
        try:
            if len(parameter_names_list) > 0:

                prop_build = open(self.properties_build, 'r').readlines()
                for parameter in parameter_names_list:
                    for line in prop_build:
                        if parameter in line and line[0] != '#' and line[0:6] != 'export':
                            value = line.split('=',1)[1].strip()#drugi argument '1' u split() funkciji znaci da radi split samo na prvom znanku '='.to treba jer vrijednosti nekih parametara imaju takoder u sebi znak '=', npr. SCOPE_CONT
                            parameters_dict[parameter] = value

                prop_common = open(self.properties_common, 'r').readlines()
                for parameter in parameter_names_list:
                    for line in prop_common:
                        if parameter in line and line[0] != '#' and line[0:6] != 'export':
                            value = line.split('=',1)[1].strip()#drugi argument '1' u split() funkciji znaci da radi split samo na prvom znanku '='.to treba jer vrijednosti nekih parametara imaju takoder u sebi znak '=', npr. SCOPE_CONT
                            parameters_dict[parameter] = value

            return parameters_dict

        except Exception, e:
            self.logger.error(e)
            return False




