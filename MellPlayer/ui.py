#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Netease Music UI

Created on 2017-02-21
@author: Mellcap
'''

import os


SONG_CATEGORIES = (
    '流行', '摇滚', '民谣', '说唱', '轻音乐', '乡村', '古典', 'R&B/Soul', '电子', '另类/独立',\
    '学习', '工作', '午休',\
    '华语', '欧美', '日语', '韩语', '粤语', '小语种',\
    '怀旧', '清新', '浪漫', '性感', '治愈', '放松', '兴奋', '快乐', '安静', '思念'
)

class UI(object):

    def __init__(self):
        self.category_lines = SONG_CATEGORIES
        self.mark_line = 0
        self.play_line = 0

    def display(self):
        display_lines = []
        terminal_size = os.get_terminal_size()
        self.screen_height, self.screen_width = terminal_size.lines, terminal_size.columns
        top_index = self.top_index
        bottom_index = self.screen_height + top_index - 3

        for index, category in enumerate(self.category_lines):
            # mark_line
            mark_line = True if self.mark_line else False
            category = self.gen_category(index=index, category=category, mark_line=mark_line)
            # play_line
            play_line = self.gen_playline(index=index)

            complete_line = '%s %s' % (category, play_line)
            display_lines.append(complete_line)

        print('\n'.join(display_lines))

    def gen_category(self, index, category, mark_line=False):
        pass

    def gen_playline(self, index):
        pass

    def gen_color(self):
        pass
        
