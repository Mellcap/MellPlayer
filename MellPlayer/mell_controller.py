#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Netease Music MellController

Created on 2017-02-21
@author: Mellcap
'''

import threading
import time
import queue

import getch
import ui
import player
from directory import create_directory

CONFIG = {
    # 主页
    'q': 'quit',
    'j': 'next_line',
    'k': 'prev_line',
    # 音乐
    ' ': 'space',
    'n': 'next_song',
    'p': 'prev_song',
    'f': 'next_playlist',
    'b': 'prev_playlist',
    # 歌词
    'l': 'lyric',
    # 帮助
    'h': 'help'
}
SONG_CATEGORIES = ui.SONG_CATEGORIES

def my_log(loglevel, component, message):
    # if loglevel == 'error':
    #     handler_next_song()
    # print('[{}] {}: {}\r'.format(loglevel, component, message))
    pass

mell_ui = ui.UI()
mell_player = player.Player(log_handler=my_log, ytdl=True)
q = queue.Queue()

def watcher():
    while 1:
        key = getch.getch()
        q.put(key)
        if key == 'q':
            break

def executor():
    while 1:
        try:
            key = q.get_nowait()
            action = CONFIG.get(key, None)
            if action == 'quit':
                break
            elif action:
                try:
                    func = 'handler_%s' % action
                    eval(func)()
                except Exception:
                    pass
        except Exception:
            pass


def key_watcher():
    t1 = threading.Thread(target=watcher)
    t2 = threading.Thread(target=executor)

    t1.start()
    t2.start()
    t1.join()
    t2.join()

def handler_space():
    current_category = SONG_CATEGORIES[mell_ui.mark_index]
    if mell_player.category == current_category:
        handler_play()
    else:
        # change UI play_index
        mell_ui.update_play_index()
        # change playlist category
        mell_player.category = current_category
        mell_player.get_category_playlists()
        mell_player.run_playlist()

def handler_next_line():
    mell_ui.next_line()

def handler_prev_line():
    mell_ui.prev_line()

def handler_play():
    mell_player.start_or_pause()

def handler_next_song():
    mell_player.next_song()
    handler_update_playInfo()

def handler_prev_song():
    mell_player.prev_song()
    handler_update_playInfo()

def handler_next_playlist():
    mell_player.next_playlist()

def handler_prev_playlist():
    mell_player.prev_playlist()

def handler_lyric():
    pass

def handler_help():
    pass

def handler_update_playInfo():
    play_info = mell_player.get_play_info()
    mell_ui.update_play_info(play_info)

def initial_player():
    current_category = SONG_CATEGORIES[mell_ui.mark_index]
    mell_player.category = current_category
    mell_player.get_category_playlists()
    mell_player.run_playlist()
    handler_update_playInfo()

def run_player():
    t = threading.Thread(target=initial_player)
    t.start()

if __name__ == '__main__':
    mell_ui.display()
    run_player()
    key_watcher()


    

