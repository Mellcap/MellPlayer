#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Netease Music API
'''
import requests

class Netease(object):

    def __init__(self):
        self.playlist_categories = []

    def playlist_categories(self):
        '''
        分类歌单
        http://music.163.com/discover/playlist/
        '''
        pass

    def playlist_category_detail(self):
        '''
        分类详情
        http://music.163.com/api/playlist/list?cat=学习&order=hot&offset=0&total=false&limit=50
        '''
        pass

    def playlist_detail(self):
        '''
        歌单详情
        http://music.163.com/api/playlist/detail?id=xxx>
        '''
        pass

    
    def song_detail(self):
        '''
        歌曲详情
        http://music.163.com/api/song/detail?ids=[xxx, xxx]
        '''
        pass

   
    def lyric_detail(self):
        '''
        歌词详情
        http://music.163.com/api/song/lyric?os=osx&id=xxx&lv=-1&kv=-1&tv=-1
        '''
        pass


    def parse_info(self, data, type):
        '''
        解析信息
        '''
        pass
