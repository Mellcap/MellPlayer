#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Netease Music API

Created on 2017-02-19
@author: Mellcap
'''
import requests
import json

from mellplayer.utils.encrypt_utils import encrypted_request
from mellplayer.mell_logger import mell_logger


class Netease(object):

    def __init__(self):
        self.playlist_categories = []

    def _request(self, url, method='GET', is_raw=True, data=None):
        '''
        对requests简单封装
        '''
        headers = {'appver': '2.0.2', 'Referer': 'http://music.163.com'}
        if method == 'GET':
            result = requests.get(url=url, headers=headers)
        elif method == 'POST' and data:
            result = requests.post(url=url, data=data, headers=headers)
        # if request failed, return False
        if not result.ok:
            return False
        result.encoding = 'UTF-8'
        if is_raw:
            return json.loads(result.text)
        return result.text

    def playlist_categories(self):
        '''
        分类歌单
        http://music.163.com/discover/playlist/
        '''
        url = 'http://music.163.com/discover/playlist/'
        result = self._request(url)
        return result

    def category_playlists(self, category='流行', offset=0, limit=50, order='hot', total='false'):
        '''
        分类详情
        http://music.163.com/api/playlist/list?cat=流行&order=hot&offset=0&total=false&limit=50
        '''
        url = 'http://music.163.com/api/playlist/list?cat=%s&order=%s&offset=%s&total=%s&limit=%s' % (category, order, offset, total, limit)
        result = self._request(url)
        return result

    def playlist_detail(self, playlist_id):
        '''
        歌单详情
        http://music.163.com/api/playlist/detail?id=xxx
        '''
        url = 'http://music.163.com/api/playlist/detail?id=%s' % playlist_id
        result = self._request(url)
        return result

    
    def song_detail(self, song_ids):
        '''
        歌曲详情
        http://music.163.com/api/song/detail?ids=[xxx, xxx]
        '''
        url = 'http://music.163.com/api/song/detail?ids=%s' % song_ids
        result = self._request(url)
        return result

    def song_detail_new(self, song_ids):
        url = 'http://music.163.com/weapi/song/enhance/player/url?csrf_token='
        data = {'ids': song_ids, 'br': 320000, 'csrf_token': ''}
        data = encrypted_request(data)
        result = self._request(url, method="POST", data=data)
        return result

   
    def lyric_detail(self, song_id):
        '''
        歌词详情
        http://music.163.com/api/song/lyric?os=osx&id=xxx&lv=-1&kv=-1&tv=-1
        '''
        url = 'http://music.163.com/api/song/lyric?os=osx&id=%s&lv=-1&kv=-1&tv=-1' % song_id
        result = self._request(url)
        return result


    def parse_info(self, data, parse_type):
        '''
        解析信息
        '''
        res = None
        if parse_type == 'category_playlists':
            res = [d['id'] for d in data['playlists']]
        elif parse_type == 'playlist_detail':
            tracks = data['result']['tracks']
            playlist_ids = [t['id'] for t in tracks]
            playlist_detail = {t['id']: {
                'song_id': t['id'],
                'song_name': t['name'],
                'song_url': t['mp3Url'],
                'song_artists': ' & '.join(map(lambda a: a['name'], t['artists']))
            } for t in tracks}
            res = (playlist_ids, playlist_detail)
        elif parse_type == 'lyric_detail':
            if 'lrc' in data:
                res = {
                    'lyric': data['lrc']['lyric']
                }
            else:
                res = {
                    'lyric': 'no_lyric'
                }
        elif parse_type == 'song_detail_new':
            res = {d['id']: {
                'song_url': d['url'],
                'song_br': d['br']
            } for d in data['data']}
        return res
                
            
