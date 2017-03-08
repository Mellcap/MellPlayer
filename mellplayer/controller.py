#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
MellPlayer Controller

Created on 2017-03-05
@author: Mellcap
'''
import threading

from mellplayer.player import mell_player
from mellplayer.ui import mell_ui, mell_help_ui, mell_lyric_ui, SONG_CATEGORIES
from mellplayer.mell_logger import mell_logger


# ===========================
# Controller Handler
# ===========================

def handler_space():
    current_category = SONG_CATEGORIES[mell_ui.mark_index]
    if mell_player.category == current_category:
        handler_play()
    else:
        # change UI play_index 
        mell_ui.update_play_index()
        # change playlist category
        mell_player.switch_category(new_category=current_category)


def handler_next_line():
    mell_ui.next_line()

def handler_prev_line():
    mell_ui.prev_line()

def handler_play():
    mell_player.start_or_pause()

def handler_next_song():
    mell_player.next_song()

def handler_prev_song():
    mell_player.prev_song()

def handler_next_playlist():
    mell_player.next_playlist()

def handler_prev_playlist():
    mell_player.prev_playlist()

def handler_reduce_volume():
    mell_player.reduce_volume()

def handler_increase_volume():
    mell_player.increase_volume()

def handler_mute_volume():
    mell_player.mute_volume()

def handler_lyric():
    if mell_ui.ui_mode == 'home' and mell_player.time_remaining:
        mell_ui.ui_mode = 'lyric'
        handler_lyric_display()
    elif mell_ui.ui_mode == 'lyric':
        mell_ui.display()
        mell_ui.ui_mode = 'home'

def handler_lyric_display():
    song_id = mell_player.playlist_ids[mell_player.playlist_index]
    if mell_player.lyric_id != song_id:
        mell_lyric_ui.initial_lyric()
        mell_player.get_lyric_detail()
    mell_lyric_ui.display()

def handler_help():
    if mell_ui.ui_mode == 'home':
        mell_help_ui.display()
        mell_ui.ui_mode = 'help'
    elif mell_ui.ui_mode == 'help':
        mell_ui.display()
        mell_ui.ui_mode = 'home'

def handler_quit():
    mell_player.terminate()


# ===========================
# Initial Player
# ===========================

def i_player():
    current_category = SONG_CATEGORIES[mell_ui.mark_index]
    mell_player.switch_category(new_category=current_category)
    # handler_update_playInfo()

def initial_player():
    initPlayer_thread = threading.Thread(target=i_player)
    initPlayer_thread.start()

