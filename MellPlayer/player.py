#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Netease Music Player

Created on 2017-02-20
@author: Mellcap
'''

import os

from mpv import MPV
from api import Netease
from directory import BASE_DIRECTORY

PLAYLIST_MAX = 50
PLAYLIST_FILE = os.path.join(BASE_DIRECTORY, 'playlist.m3u')
NeteaseApi = Netease()

class Player(MPV):

    def __init__(self, *extra_mpv_flags, log_handler=None, start_event_thread=True, **extra_mpv_opts):
        super(Player, self).__init__(*extra_mpv_flags, log_handler=log_handler, start_event_thread=start_event_thread, **extra_mpv_opts)
        self.category = None
        self.category_playlists = None
        self.playlist_detail = None

    def init_playlist(self):
        if os.path.exists(PLAYLIST_FILE):
            print('loadlist: %s' % PLAYLIST_FILE)
            self.loadlist(PLAYLIST_FILE)

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

    def get_category_playlists(self):
        category = self.category
        if category:
            # 初始化playlist_index
            self.playlist_index = 0
            # get data
            data = NeteaseApi.category_playlists(category=category)
            category_playlists = NeteaseApi.parse_info(data=data, parse_type='category_playlists')
            self.category_playlists = category_playlists
            return category_playlists
        return False

    def get_playlist(self, playlist_index=0):
        playlist_id = self.category_playlists[playlist_index]['playlist_id']
        data = NeteaseApi.playlist_detail(playlist_id)
        playlist_detail = NeteaseApi.parse_info(data=data, parse_type='playlist_detail')
        self.playlist_detail = playlist_detail
        return playlist_detail

    def save_playlist(self):
        playlist = []
        m3u_title = '#EXTM3U\n'
        playlist.append(m3u_title)
        for song in self.playlist_detail:
            song_detail = '#EXTINF:,%s\n%s\n' % (song['song_id'], song['song_url'])
            playlist.append(song_detail)
        with open(PLAYLIST_FILE, 'w') as f:
            for line in playlist:
                f.write(line)

        return True

    def next_playlist(self):
        pass
            
            
