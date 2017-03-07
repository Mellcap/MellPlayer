#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
MellPlayer UIEvent

Created on 2017-03-05
@author: Mellcap
'''

from mellplayer.ui import mell_ui

class UIEvent(object):

    def handler_update_playInfo(self, play_info):
        mell_ui.update_play_info(play_info)

    def handler_update_title(self, items):
        mell_ui.update_title(items)
