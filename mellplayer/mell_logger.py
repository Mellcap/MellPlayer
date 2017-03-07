#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
MellPlayer logger

Created on 2017-03-06
@author: Mellcap
'''

import os
import logging

from mellplayer.directory import BASE_DIRECTORY

LOG_FILE = os.path.join(BASE_DIRECTORY, 'mell_logger.log')

 
# create logger
mell_logger = logging.getLogger('mell_logger')  
mell_logger.setLevel(logging.DEBUG)
 
# define handler write in file
fh = logging.FileHandler(LOG_FILE)
fh.setLevel(logging.DEBUG)
 
# define formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s \n- %(message)s')
fh.setFormatter(formatter)
 
# add handler
mell_logger.addHandler(fh)
 

