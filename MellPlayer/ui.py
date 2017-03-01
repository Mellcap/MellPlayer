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

# 所有颜色 https://upload.wikimedia.org/wikipedia/commons/1/15/Xterm_256color_chart.svg
FORE_COLOR = {              # 前景色
    'default'      : 249,   #  默认
    'blue'         : 39,    
    'green'        : 34,
    'gray'         : 239,
    'red'          : 196,
    'pink'         : 201

}

BLANK_CONSTANT = 3
MAX_LINES = len(SONG_CATEGORIES)
ALL_LINES = MAX_LINES + BLANK_CONSTANT
TERMINAL_SIZE = os.get_terminal_size()

class UI(object):

    def __init__(self):
        self.category_lines = SONG_CATEGORIES
        self.mark_index = 0
        self.play_index= 0
        self.play_info = ''
        self.top_index = 0
        self.screen_height = TERMINAL_SIZE.lines
        self.screen_width = TERMINAL_SIZE.columns

    def _get_title(self):
        player_name = '\033[1m%s' % self.gen_color('MellPlayer', 'blue')
        netease = self.gen_color('网易云音乐', 'red')
        divider = self.gen_color(data=r'\\', color='')
        display_items = [player_name, netease]
        return (' %s ' % divider).join(display_items)

    def display(self):
        '''
        说明：多线程终端输出有问题，在每行结尾加\r
        '''
        display_lines = ['\r']
        display_title = '\n%s%s\r' % (' '*5, self._get_title())
        display_lines.append(display_title)
        top_index = self.top_index
        bottom_index = (self.screen_height - BLANK_CONSTANT) + top_index

        for index, category in enumerate(self.category_lines[top_index: bottom_index]):
            # mark_index            
            is_markline = True if (index + self.top_index) == self.mark_index else False
            category = self.gen_category(category, is_markline)
            # play_index
            play_info = ''
            is_playline = True if (index + self.top_index) == self.play_index else False
            if is_playline:
                play_info = self.gen_playline()

            complete_line = '%s%s%s\r' % (category, ' '*10, play_info)
            display_lines.append(complete_line)

        if ALL_LINES < self.screen_height:
            # fill_blanks
            display_lines = self.fill_blanks(display_lines)
        print('\n'.join(display_lines) + '\r')

    def next_line(self):
        if self.mark_index < (MAX_LINES - 1):
            self.mark_index += 1
            bottom_index = (self.screen_height - BLANK_CONSTANT) + self.top_index
            if self.mark_index > (bottom_index - 1):
                self.top_index += 1
        self.display()

    def prev_line(self):
        if self.mark_index > 0:
            self.mark_index -= 1
            if self.mark_index < self.top_index:
                self.top_index -= 1
        self.display()

    def update_play_index(self):
        self.play_index = self.mark_index
        self.display()

    def update_play_info(self, play_info):
        self.play_info = play_info
        self.display()
        
    def gen_category(self, category, is_markline=False):
        if is_markline:
            category = self.gen_mark(category)
            category = self.gen_color(data=category, color='pink')
        else:
            # fill 3 blanks
            category = '%s%s' % (' '*5, category)
            category = self.gen_color(data=category, color='')
        return category

    def gen_mark(self, category):
        return '  ➣  %s' % category

    def gen_playline(self):
        complete_info = [self.gen_color(data=p, color='pink') for p in self.play_info]
        divider = self.gen_color(data='|', color='')
        return ('  %s  ' % divider).join(complete_info)

    def gen_color(self, data, color):
        '''
        参考地址:http://blog.csdn.net/gatieme/article/details/45439671
        但是目前用不到这么多类型，目前只用前景色
        '''
        color_code = FORE_COLOR.get(color, 246)
        # data = "\033[;%s;m%s\033[0m" % (color_code, data)
        data = "\001\033[38;5;%sm\002%s\001\033[0m\002" % (color_code, data)
        return data

    def fill_blanks(self, display_lines):
        delta_lines = self.screen_height - ALL_LINES
        display_lines += [' ' for i in range(delta_lines)]
        return display_lines

        
