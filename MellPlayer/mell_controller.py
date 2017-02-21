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
    'q': 'quit',
    'j': 'next_line',
    'k': 'prev_line',
    ' ': 'play',
    
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

if __name__ == '__main__':
    mell_ui.display()
    watch_key()

