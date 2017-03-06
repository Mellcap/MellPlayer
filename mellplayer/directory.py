#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
MellPlayer Directory

Created on 2017-02-23
@author: Mellcap
'''

import os

BASE_DIRECTORY = os.path.join(os.path.expanduser('~'), '.MellPlayer')

class Directory(object):

    def create_directory(self, directory=None):
        if not directory:
            directory = BASE_DIRECTORY
        if not os.path.exists(directory):
            os.makedirs(directory)

# ===========================
# Instance
# ===========================

mell_directory = Directory()
mell_directory.create_directory()
