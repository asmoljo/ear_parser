#!/usr/bin/python


import os
import sys
import time
import shutil
import subprocess

from modules import textFileUtilities, jarFileUtilities


hfs_home = os.environ['HFS_HOME']
template_dir = hfs_home+'/bin/ear_parser/templates/'

def help():
    print '\nSkripta se mora pokrenuti u HFS_HOME folderu!'
    print 'Putanja do ear filea se zadaje relativnom putanjom!'
    print 'Drugi argument mora biti "cg|zaba|nesto"\n'
    print 'Primjer koristenja:'
    print '[$HFS_HOME]$bin/ear_parser/callParser.py ear/spray-ear-8.11.11.1.ear zaba\n'


def main():
    try:
        if sys.argv[2] == 'zaba':
            #textFileUtilities.test1()
            textFileUtilities.recreate_tmp_directory('tmp')
            textFileUtilities.change_working_directory('tmp')

            jarFileUtilities.extract_from_jar_file('../'+sys.argv[1], 'META-INF/application.xml')
            jarFileUtilities.extract_from_jar_file('../'+sys.argv[1], 'spray-web.war')
            jarFileUtilities.extract_from_jar_file('../' + sys.argv[1], 'spray-controller-ejb.jar')
            jarFileUtilities.extract_from_jar_file('spray-web.war','WEB-INF/web.xml')
            jarFileUtilities.extract_from_jar_file('spray-controller-ejb.jar','META-INF/ejb-jar.xml')

            textFileUtilities.search_and_replace_in_file('META-INF/application.xml', 'META-INF/application.xml', '>/dc<', '>cash<')

            if not textFileUtilities.search_in_file('WEB-INF/web.xml','security-role'):
                textFileUtilities.add_in_file_from_template('META-INF/application.xml',os.path.join(template_dir, 'template_security_role.txt'),'</application>','before')
                textFileUtilities.add_in_file_from_template('WEB-INF/web.xml',os.path.join(template_dir, 'template_security_role_and_constrain.txt'),'</web-app>', 'before')







        elif sys.argv[2] == 'cg':
            print 'CG parse'

        else:
            print 'Ne postoji aplikacija: %s' % sys.argv[2]

    except IndexError, e:
        print 'Index greska: %s' % e
        help()
        return False
    except Exception, e:
        print 'Greska: %s' % e
        help()
        return False



# __name__ je built in python varijabla koja u pozadini dobije vrijednost '__main__'
# ako se ova skripta direktno pokrece u pythonu npr. #python ./callParser.py .
#Ako se ova skripta ne pokrece direktno, nego se importa kao modul u neku drugu skriptu/klasu, onda nema vrijednost '__main__' i ne pokrece se funkcija main()
if __name__ == '__main__':
    main()
