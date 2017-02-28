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
    ' ': 'play',
    'n': 'next_song',
    'p': 'prev_song',
    'f': 'next_playlist',
    'b': 'prev_playlist',
    # 歌词
    'l': 'lyric',
    # 帮助
    'h': 'help'
}

def my_log(loglevel, component, message):
    if loglevel == 'error':
        print('>>>>> I got an error')
    print('[{}] {}: {}'.format(loglevel, component, message))

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

# def run():
#     p = '/Users/zhaoye/.MellPlayer/playlist.m3u'
#     mell_player.loadlist(p)
#     mell_player.wait_for_playback()
#     print('wait 5 seconds')
#     time.sleep(5)
#     mell_player.pause = True
#     print('wait another 5 seconds')
#     time.sleep(5)
#     mell_player.pause = False
#     print('wait another 5 seconds')
#     time.sleep(5)
#     mell_player.play('http://m2.music.126.net/LJOP6drGL9Vo2cmkjbFazQ==/3393092919088491.mp3')


if __name__ == '__main__':
    mell_ui.display()
    key_watcher()
    # create_directory()
    # mell_player.category = '流行'
    # mell_player.get_category_playlists()
    # mell_player.run_playlist()
    # t = threading.Thread(target=run)
    # t.start()

    

