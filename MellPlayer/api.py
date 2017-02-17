#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Netease Music API
'''
import requests

class Netease(object):

    def __init__(self):
        self.playlist_categories = []

    # 分类歌单
    # http://music.163.com/discover/playlist/
    def playlist_categories(self):
        pass

    # 分类详情
    # http://music.163.com/api/playlist/list?cat=学习&order=hot&offset=0&total=false&limit=50
    def playlist_category_detail(self):
        pass

    # 歌单详情
    # http://music.163.com/api/playlist/detail?id=xxx
    def playlist_detail(self):
        pass

    # 歌曲详情
    # http://music.163.com/api/song/detail?ids=[xxx, xxx]
    def song_detail(self):
        pass

    # 歌词详情
    # http://music.163.com/api/song/lyric?os=osx&id=xxx&lv=-1&kv=-1&tv=-1
    def lyric_detail(self):
        pass
