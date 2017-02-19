#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Netease Music API

Created on 2017-02-19
@author: Mellcap
'''
import requests
import json

class Netease(object):

    def __init__(self):
        self.playlist_categories = []

    def _request(self, url, method='GET', is_raw=False):
        '''
        对requests简单封装
        '''
        headers = {'appver': '2.0.2', 'Referer': 'http://music.163.com'}
        if method == 'GET':
            result = requests.get(url, headers=headers)
        elif method == 'POST':
            result = requests.post(url, headers=headers)
        # 如果请求不成功，直接返回False
        if not result.ok:
            return False
        result.encoding = 'UTF-8'
        # 如果请求原网址，则用json load一下
        if is_raw:
            return json.loads(result.text)
        return result.text

    # def playlist_categories(self):
    #     '''
    #     分类歌单
    #     http://music.163.com/discover/playlist/
    #     '''
    #     url = 'http://music.163.com/discover/playlist/'
    #     result = self._request(url, is_raw=True)
    #     return result

    def playlist_category_detail(self, category='全部', offset=0, limit=50, order='hot', total='false'):
        '''
        分类详情
        http://music.163.com/api/playlist/list?cat=全部&order=hot&offset=0&total=false&limit=50
        '''
        url = 'http://music.163.com/api/playlist/list?cat=%s&order=%s&offset=%s&total=%s&limit=%s' % (category, order, offset, total, limit)
        result = self._request(url, is_raw=True)
        return result

    def playlist_detail(self, playlist_id):
        '''
        歌单详情
        http://music.163.com/api/playlist/detail?id=xxx
        '''
        url = 'http://music.163.com/api/playlist/detail?id=%s' % playlist_id
        result = self._request(url, is_raw=True)
        return result

    
    def song_detail(self, song_ids):
        '''
        歌曲详情
        http://music.163.com/api/song/detail?ids=[xxx, xxx]
        '''
        url = 'http://music.163.com/api/song/detail?ids=%s' % song_ids
        result = self._request(url, is_raw=True)
        return result

   
    def lyric_detail(self, song_id):
        '''
        歌词详情
        http://music.163.com/api/song/lyric?os=osx&id=xxx&lv=-1&kv=-1&tv=-1
        '''
        url = 'http://music.163.com/api/song/lyric?os=osx&id=%s&lv=-1&kv=-1&tv=-1' % song_id
        result = self._request(url, is_raw=True)
        return result


    def parse_info(self, data, parse_type):
        '''
        解析信息
        '''
        if parse_type == 'playlist_category_detail':
            pass
        elif parse_type == 'playlist_detail':
            pass
        elif parse_type == 'song_detail':
            pass
        elif parse_type == 'lyric_detail':
            pass
            
