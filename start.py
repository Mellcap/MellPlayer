#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
MellPlayer Starter

Created on 2017-03-05
@author: Mellcap
'''

from mellplayer.controller import mell_ui, initial_player
from mellplayer.watcher import time_watcher, key_watcher

def main():
    mell_ui.display()
    initial_player()
    time_watcher()
    key_watcher()

if __name__ == '__main__':
    main()
