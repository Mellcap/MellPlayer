#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Netease Music Player

Created on 2017-02-23
@author: Mellcap
'''

import os

DIRECTORY = '~/.MellPlayer'

def create_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
