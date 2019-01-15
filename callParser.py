#!/usr/bin/python


import os
import sys
import time
import shutil
import subprocess

from modules import textFileUtilities, jarFileUtilities


hfs_home = os.environ['HFS_HOME']

print hfs_home

def main():
    #textFileUtilities.test1()


    textFileUtilities.changeWorkDir(hfs_home+'/ear')
    print '== Radni direktorij je %s' % os.getcwd()
    jarFileUtilities.extractFromJarFile(sys.argv[1], 'META-INF/application.xml')


# __name__ je built in python varijabla koja u pozadini dobije vrijednost '__main__'
# ako se ova skripta direktno pokrece u pythonu npr. #python ./callParser.py .
#Ako se ova skripta ne pokrece direktno, nego se importa kao modul u neku drugu skriptu/klasu, onda nema vrijednost '__main__' i ne pokrece se funkcija main()
if __name__ == '__main__':
    main()
