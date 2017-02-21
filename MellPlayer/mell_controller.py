#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Netease Music MellController

Created on 2017-02-21
@author: Mellcap
'''

import getch
import ui

CONFIG = {
    # 主页
    'q': 'quit',
    'j': 'next_line',
    'k': 'prev_line',
    # 音乐
    ' ': 'play',
    'n': 'next_song',
    'p': 'prev_song',
    'f': 'next_playlist',
    'b': 'prev_playlist',
    # 歌词
    'l': 'lyric',
    # 帮组
    'h': 'help'
}


mell_ui = ui.UI()

def watch_key():
    while 1:
        key = getch.getch()
        action = CONFIG.get(key, None)
        if action == 'quit':
            break
        elif action:
            try:
                func = 'handler_%s' % action
                eval(func)()
            except Exception:
                pass

def handler_next_line():
    mell_ui.next_line()

def handler_prev_line():
    mell_ui.prev_line()

def handler_play():
    print('Start Playing...')

def handler_next_song():
    pass

def handler_prev_song():
    pass

def handler_next_playlist():
    pass

def handler_prev_playlist():
    pass

def handler_lyric():
    pass

def handler_help():
    pass

if __name__ == '__main__':
    mell_ui.display()
    watch_key()

