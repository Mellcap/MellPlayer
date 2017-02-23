#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Netease Music Player

Created on 2017-02-23
@author: Mellcap
'''

import os

BASE_DIRECTORY = os.path.join(os.path.expanduser('~'), '.MellPlayer')

def create_directory(directory=None):
    if not directory:
        directory = BASE_DIRECTORY
    if not os.path.exists(directory):
        os.makedirs(directory)
