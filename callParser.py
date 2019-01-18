#!/usr/bin/python


import os
import sys
import time
import shutil
import subprocess

from modules import jarFileModule, textFileModule


#Definiranje varijabli i objekata(objekti su malim slovima)
HFS_HOME = os.getcwd()
TEMPLATE_DIR = HFS_HOME + '/bin/ear_parser/templates/'
PROPERTIES_BUILD_FILE_PATH = HFS_HOME + '/config/properties.build'
PROPERTIES_COMMON_FILE_PATH = HFS_HOME + '/config/properties.common'
tfmgr = textFileModule.TextFileManager(PROPERTIES_BUILD_FILE_PATH, PROPERTIES_COMMON_FILE_PATH, TEMPLATE_DIR)
JAVA_HOME = tfmgr.read_properties_file_parameters(['JAVA_HOME'])['JAVA_HOME']
jfmgr = jarFileModule.JarFileManager(JAVA_HOME + 'bin/jar')



def help():
    print '\nSkripta se mora pokrenuti u HFS_HOME folderu!'
    print 'Putanja do ear filea se zadaje relativnom putanjom!'
    print 'Drugi argument mora biti "cg|zaba|nesto"\n'
    print 'Primjer koristenja:'
    print '[$HFS_HOME]$bin/ear_parser/callParser.py ear/spray-ear-8.11.11.1.ear zaba\n'


def main():
    print 'project: ' + sys.argv[2]
    try:
        if sys.argv[2] == 'zaba':
            zaba()
        elif sys.argv[2] == 'ccms':
            ccms()
        elif sys.argv[2] == 'test':
            test()
        else:
            print 'Ne postoji aplikacija: %s' % sys.argv[2]
    except IndexError, e:
        print '\nIndex greska: %s' % e
        help()
        return False
    except Exception, e:
        print '\nGreska: %s' % e
        help()
        return False


def zaba():

    #textFileModule.recreate_tmp_directory('tmp')
    #textFileModule.change_working_directory('tmp')

    tfmgr.recreate_tmp_directory('tmp')
    tfmgr.change_working_directory('tmp')

    jfmgr.extract_from_jar_file('../' + sys.argv[1], 'META-INF/application.xml')
    jfmgr.extract_from_jar_file('../' + sys.argv[1], 'spray-web.war')
    jfmgr.extract_from_jar_file('../' + sys.argv[1], 'spray-controller-ejb.jar')
    jfmgr.extract_from_jar_file('spray-web.war', 'WEB-INF/web.xml')
    jfmgr.extract_from_jar_file('spray-controller-ejb.jar', 'META-INF/ejb-jar.xml')

    #textFileModule.search_and_replace_in_file('META-INF/application.xml', 'META-INF/application.xml', '>/dc<', '>cash<')
    tfmgr.search_and_replace_in_file('META-INF/application.xml', 'META-INF/application.xml', '>/dc<', '>cash<')

    #if not textFileModule.search_in_file('WEB-INF/web.xml', 'security-role'):
    #    textFileModule.add_text_block_to_file_from_template('META-INF/application.xml', os.path.join(TEMPLATE_DIR, 'template_security_role.txt'), '</application>', 'before')
    #    textFileModule.add_text_block_to_file_from_template('WEB-INF/web.xml', os.path.join(TEMPLATE_DIR, 'template_security_role_and_constrain.txt'), '</web-app>', 'before')

    if not tfmgr.search_in_file('WEB-INF/web.xml', 'security-role'):
        tfmgr.add_text_block_to_file_from_template('META-INF/application.xml', 'template_security_role.txt', '</application>', 'before')
        tfmgr.add_text_block_to_file_from_template('WEB-INF/web.xml', 'template_security_role_and_constrain.txt', '</web-app>', 'before')

    #textFileModule.add_text_block_to_file_from_template_with_parameters('META-INF/ejb-jar.xml', os.path.join(TEMPLATE_DIR, 'template_resource_ref_ejb3.txt'), PROPERTIES_BUILD_FILE_PATH, ['RES_REF_NAME_CONTROLLER_DATASOURCE'], '<display-name>spray-controller-ejb</display-name>', 'after')
    tfmgr.add_text_block_to_file_from_template_with_parameters('META-INF/ejb-jar.xml', 'template_resource_ref_ejb3.txt', ['RES_REF_NAME_CONTROLLER_DATASOURCE'], '<display-name>spray-controller-ejb</display-name>', 'after')


def ccms():
    print 'CCMS parse'


def test():
    jfmgr.extract_from_jar_file('../fs' + sys.argv[1], 'META-INF/application.xml')





# __name__ je built in python varijabla koja u pozadini dobije vrijednost '__main__'
# ako se ova skripta direktno pokrece u pythonu npr. #python ./callParser.py .
#Ako se ova skripta ne pokrece direktno, nego se importa kao modul u neku drugu skriptu/klasu, onda nema vrijednost '__main__' i ne pokrece se funkcija main()
if __name__ == '__main__':
    main()
