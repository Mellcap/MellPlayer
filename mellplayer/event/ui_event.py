#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
MellPlayer UIEvent

Created on 2017-03-05
@author: Mellcap
'''

from mellplayer.ui import mell_ui, mell_lyric_ui

class UIEvent(object):

    # ===========================
    # Main UI
    # ===========================
    
    def handler_update_playInfo(self, play_info):
        mell_ui.update_play_info(play_info)

    def handler_update_title(self, items):
        mell_ui.update_title(items)

    # ===========================
    # Lyric UI
    # ===========================

    def handler_initial_lyric(self):
        mell_lyric_ui.initial_lyric()
        
    def handler_parse_lyric(self, origin_lyric):
        self.handler_initial_lyric()
        mell_lyric_ui.parse_lyric(origin_lyric=origin_lyric)

    def handler_roll_lyric(self, timestamp):
        mell_lyric_ui.roll(timestamp=timestamp)
    
