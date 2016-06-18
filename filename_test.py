# -*- coding: utf-8 -*-
"""
Created on Wed Jun 15 15:18:49 2016

@author: ctaylor
"""

import os

input_dir = '.' + os.sep + 'input'
output_dir = '.' + os.sep + 'output'

#if os.path.isfile(input_dir + os.sep + '*.*'):
#    print('Files exist.')
#else:
#    print('Empty directory.')

for path, subdirs, files in os.walk(input_dir):
#    print(path)
#    print(subdirs)
#    print(files)
    for file in files:
        if path == input_dir:
            print(path + '\\' + file)
#        print(input_dir + os.sep + file)
#        print(output_dir + os.sep + file[:-4] + '_out.conll10')
#        print(output_dir + os.sep + file)
#        print(os.linesep)