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

from mellplayer.controller import *
from mellplayer.utils import getch

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
        key = KEY_QUEUE.get()
        action = CONFIG.get(key, None)
        if action:
            func = 'handler_%s' % action
            eval(func)()
            if action == 'quit':
                break

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
            time_pos = mell_player.time_pos
            time_remain = mell_player.time_remaining
            if time_pos and time_remain:
                if mell_ui.ui_mode == 'lyric':
                    mell_lyric_ui.roll(int(time_pos))
                if time_remain <= 2:
                    handler_next_song()
                timestamp = format_timestamp(time_pos, time_remain)
                show_footer(timestamp=timestamp)
        time.sleep(1)

def format_timestamp(time_pos, time_remain):
    total_time = time_pos + time_remain
    format_time_pos = '%02d:%02d' % divmod(time_pos, 60)
    format_time_total = '%02d:%02d' % divmod(total_time, 60)
    return ' / '.join((format_time_pos, format_time_total))

def show_footer(timestamp):
    timestamp = mell_ui.gen_color(data=timestamp, color='blue')
    footer = timestamp.rjust(mell_ui.screen_width + 13) + '\r'
    sys.stdout.write(footer)
    sys.stdout.flush()
            

def time_watcher():
    t_watcher_thread = threading.Thread(target=t_watcher)
    t_watcher_thread.start()

