#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Netease Music Player

Created on 2017-02-20
@author: Mellcap
'''

import os
import time
import threading

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
        self.playlist_list = None
        self.playlist_index = 0
        self.playlist_detail = None
        self.is_quit = False

    def init_playlist(self):
        '''
        playlist会发生闪退问题，暂时自己控制播放列表
        '''
        if os.path.exists(PLAYLIST_FILE):
            self.loadlist(PLAYLIST_FILE)

    def start_or_pause(self):
        self.pause = not self.pause

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
        # self.playlist_next()
        playlist_list = self.playlist_list
        if playlist_list:
            self.playlist_index += 1
            if self.playlist_index >= len(playlist_list):
                self.playlist_index = 0
            self.init_player()

    def prev_song(self):
        # self.playlist_prev()
        playlist_list = self.playlist_list
        if playlist_list:
            self.playlist_index -= 1
            if self.playlist_index < 0:
                self.playlist_index = len(self.playlist_list) - 1
            self.init_player()

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
            if self.category_playlist_index >= len(self.category_playlists):
                self.category_playlist_index = 0
            self.run_playlist()

    def prev_playlist(self):
        category_playlists = self.category_playlists
        if category_playlists:
            self.category_playlist_index -= 1
            if self.category_playlist_index < 0:
                self.category_playlist_index = len(self.category_playlists) - 1
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
        playlist_list, playlist_detail = NeteaseApi.parse_info(data=data, parse_type='playlist_detail')
        self.playlist_list = playlist_list
        self.playlist_detail = playlist_detail
        self.update_playlist_url()

    def update_playlist_url(self):
        song_ids = self.playlist_list
        data = NeteaseApi.song_detail_new(song_ids)
        song_details = NeteaseApi.parse_info(data=data, parse_type='song_detail_new')
        for song_id in self.playlist_detail:
            song_detail = song_details.get(song_id, None)
            if song_detail:
                song_info = {
                    'song_url': song_detail.get('song_url', None),
                    'song_br': song_detail.get('song_br', None)
                }
                self.playlist_detail[song_id].update(song_info)

    def get_play_info(self):
        play_info = ''
        if self.playlist_list and self.playlist_detail:
            play_detail = self.playlist_detail.get(self.playlist_list[self.playlist_index], None)
            if play_detail:
                song_name = play_detail.get('song_name', None)
                song_artists = play_detail.get('song_artists', None)
                if song_name and song_artists:
                    play_info = [song_name, song_artists]
        return play_info
            

    # def save_playlist(self):
    #     playlist = []
    #     m3u_title = '#EXTM3U\n'
    #     playlist.append(m3u_title)
    #     for song in self.playlist_detail:
    #         song_detail = '#EXTINF:,%s\n%s\n' % (song['song_id'], song['song_url'])
    #         playlist.append(song_detail)
    #     with open(PLAYLIST_FILE, 'w') as f:
    #         for line in playlist:
    #             f.write(line)

    #     return True

    def run_playlist(self):
        self.playlist_index = 0
        self.get_playlist()
        self.init_player()
            
    def init_player(self):
        if self.playlist_detail and self.playlist_list:
            song_info = self.playlist_detail.get(self.playlist_list[self.playlist_index], None)
            if song_info:
                song_url = song_info.get('song_url', None)
                if song_url:
                    self.play(song_url)


    # 音量控制
    def reduce_volume(self):
        volume = max(self.volume - 10, 0)
        self.volume = volume

    def increase_volume(self):
        volume = min(self.volume + 10, 100)
        self.volume = volume

    def mute_volume(self):
        self.mute = not self.mute
        
            
