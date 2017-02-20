#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Netease Music Player

Created on 2017-02-20
@author: Mellcap
'''

from .mpv import MPV

class Player(object):

    def __init__(self):
        pass

    def start(self):
        pass

    def pause(self):
        pass

    def start_or_pause(self):
        pass

    def switch_song(self, action='next'):
        '''
        action: next/prev
        '''
        pass

    def switch_playlist(self, action='next'):
        '''
        action: next/prev
        '''
        pass
