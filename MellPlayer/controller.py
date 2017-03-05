#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Netease Music MellController

Created on 2017-03-05
@author: Mellcap
'''
import threading

import player
import ui

SONG_CATEGORIES = ui.SONG_CATEGORIES

mell_ui = ui.UI()
mell_help_ui = ui.HelpUI()

def mell_logger(loglevel, component, message):
    if loglevel == 'error':
        # print('[{}] {}: {}\r'.format(loglevel, component, message))
        handler_next_song()
        
mell_player = player.Player(log_handler=mell_logger, ytdl=True)


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
        handler_update_playInfo()

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
    handler_update_playInfo()

def handler_prev_playlist():
    mell_player.prev_playlist()
    handler_update_playInfo()

def handler_reduce_volume():
    mell_player.reduce_volume()

def handler_increase_volume():
    mell_player.increase_volume()

def handler_mute_volume():
    mell_player.mute_volume()

def handler_lyric():
    pass

def handler_help():
    if mell_ui.ui_mode == 'home':
        mell_help_ui.display()
        mell_ui.ui_mode = 'help'
    elif mell_ui.ui_mode == 'help':
        mell_ui.display()
        mell_ui.ui_mode = 'home'

def handler_quit():
    mell_player.terminate()

def handler_update_playInfo():
    play_info = mell_player.get_play_info()
    mell_ui.update_play_info(play_info)


# ===========================
# Initial Player
# ===========================

def i_player():
    current_category = SONG_CATEGORIES[mell_ui.mark_index]
    mell_player.category = current_category
    mell_player.get_category_playlists()
    mell_player.run_playlist()
    handler_update_playInfo()

def initial_player():
    initPlayer_thread = threading.Thread(target=i_player)
    initPlayer_thread.start()

