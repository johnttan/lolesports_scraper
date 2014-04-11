from subprocess import call
import glob
import os
import shutil


for file in glob.glob("*.py"):
    print('Doccoing {}'.format(file))
    os.system('pycco ' + file)


srcfile = 'pycco.css'
dest = './docs'
shutil.copy(srcfile, dest)

os.system('docco-central ' + '*.py')