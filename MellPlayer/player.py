#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Netease Music Player

Created on 2017-02-20
@author: Mellcap
'''

from .mpv import MPV

class Player(MPV):

    def init_playlist(self):
        self.loadlist('/Users/zhaoye/test_dir/test001.m3u')

    def start_or_pause(self):
        if self.pause:
            self._set_property('pause', False)
        else:
            self._set_property('pause', True)

    def switch_song(self, action='next'):
        '''
        action: next/prev
        '''
        if action == 'next':
            self.playlist_next()
        elif action == 'prev':
            self.playlist_prev()

    def switch_playlist(self):
        # find playlists
        # choose playlist != this
        # return
        pass
