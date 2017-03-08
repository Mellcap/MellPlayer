#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
MellPlayer Player Deco

Created on 2017-03-08
@author: Mellcap
'''

# ===========================
# Deco
# ===========================

def show_changing_text(func):
    '''
    加载歌曲显示
    '''
    def wrapper(*args, **kw):
        # args[0] == player
        p = args[0]
        p.show_song_changing()
        return func(*args, **kw)
    return wrapper

def show_song_info_text(func):
    '''
    歌曲详情显示
    '''
    def wrapper(*args, **kw):
        func(*args, **kw)
        p = args[0]
        while 1:
            if p.time_pos:
                p.show_song_info()
                break
            time.sleep(1)
    return wrapper

def update_title_text(func):
    '''
    更新title
    '''
    def wrapper(*args, **kw):
        # args[0] == player
        func(*args, **kw)
        p = args[0]
        p.update_title()
    return wrapper
