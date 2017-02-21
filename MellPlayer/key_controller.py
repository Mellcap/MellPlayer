#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Netease Music KeyController

Created on 2017-02-21
@author: Mellcap
'''

import getch


class KeyController(object):

    def __init__(self):
        pass

    def watch_key(self):
        while 1:
            key = getch.getch()
            self.hander(key)

    def handler(self, key):
        pass
