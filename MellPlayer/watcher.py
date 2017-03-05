#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
MellPlayer Watcher

Created on 2017-03-05
@author: Mellcap
'''
import sys
import time
import queue
import threading

from controller import *
from utils import getch

KEY_QUEUE = queue.Queue()
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
    # 音量
    '-': 'reduce_volume',
    '=': 'increase_volume',
    'm': 'mute_volume',
    # 歌词
    'l': 'lyric',
    # 帮助
    'h': 'help'
}

# ===========================
# Key Watcher
# ===========================

def k_watcher():
    while 1:
        key = getch.getch()
        KEY_QUEUE.put(key)
        if key == 'q':
            mell_player.is_quit = True
            break

def k_executor():
    while 1:
        try:
            key = KEY_QUEUE.get_nowait()
            action = CONFIG.get(key, None)
            if action:
                try:
                    func = 'handler_%s' % action
                    eval(func)()
                    if action == 'quit':
                        break
                except Exception:
                    pass
        except Exception:
            pass


def key_watcher():
    k_watcher_thread = threading.Thread(target=k_watcher)
    k_executor_thread = threading.Thread(target=k_executor)

    k_watcher_thread.start()
    k_executor_thread.start()
    k_watcher_thread.join()
    k_executor_thread.join()


# ===========================
# Time Watcher
# ===========================

def t_watcher():
    while not mell_player.is_quit:
        if not mell_player.pause:
            time_remain = mell_player.time_remaining
            # if mell_ui.ui_mode == 'lyric':
            #     mell_lyric_ui.roll(mell_player.time_pos)
            if time_remain:
                if time_remain <= 2:
                    handler_next_song()
                m, s = divmod(time_remain, 60)
                time_remain = '%02d:%02d' % (m, s)
                show_footer(timestamp=time_remain)
        time.sleep(1)

def show_footer(timestamp):
    timestamp = mell_ui.gen_color(data=timestamp, color='blue')
    footer = '%s%s%s' % (' '*(mell_ui.screen_width - 8), timestamp,'\r')
    sys.stdout.write(footer)
    sys.stdout.flush()
            

def time_watcher():
    t_watcher_thread = threading.Thread(target=t_watcher)
    t_watcher_thread.start()

