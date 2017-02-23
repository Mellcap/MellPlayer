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
        self.category_playlist_index = 0
        self.playlist_detail = None

    def init_playlist(self):
        if os.path.exists(PLAYLIST_FILE):
            # print('playlist: %s' % PLAYLIST_FILE)
            self.loadlist(PLAYLIST_FILE)

    def start_or_pause(self):
        if self.pause:
            self._set_property('pause', False)
        else:
            self._set_property('pause', True)

    def loop_playlist(self):
        self._set_property('loop', True)

    def switch_song(self, action='next'):
        '''
        action: next/prev
        '''
        if action == 'next':
            self.playlist_next()
        elif action == 'prev':
            self.playlist_prev()

    def next_song(self):
        self.playlist_next()

    def prev_song(self):
        self.playlist_prev()

    def switch_playlist(self):
        '''
        action: next/prev
        '''
        if action == 'next':
            self.next_playlist()
        elif action == 'prev':
            self.prev_playlist()

    def switch_category(self, new_category):
        if new_category == self.category:
            self.start_or_pause()
        else:
            self.category = new_category
            self.get_category_playlists()
            self.run_playlist()
    
    def next_playlist(self):
        category_playlists = self.category_playlists
        if category_playlists:
            self.category_playlist_index += 1
            if self.category_playlist_index >= self.playlist_count:
                self.category_playlist_index = 0
            self.run_playlist()

    def prev_playlist(self):
        category_playlists = self.category_playlists
        if category_playlists:
            self.category_playlist_index -= 1
            if self.category_playlist_index < 0:
                self.category_playlist_index = self.playlist_count - 1
            self.run_playlist()

    def get_category_playlists(self):
        category = self.category
        if category:
            # 初始化category_playlist_index
            self.category_playlist_index = 0
            # get data
            data = NeteaseApi.category_playlists(category=category)
            category_playlists = NeteaseApi.parse_info(data=data, parse_type='category_playlists')
            self.category_playlists = tuple(category_playlists)

    def get_playlist(self):
        playlist_id = self.category_playlists[self.category_playlist_index]
        data = NeteaseApi.playlist_detail(playlist_id)
        playlist_detail = NeteaseApi.parse_info(data=data, parse_type='playlist_detail')
        self.playlist_detail = playlist_detail

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

    def run_playlist(self):
        self.get_playlist()
        self.save_playlist()
        self.init_playlist()
            
            
