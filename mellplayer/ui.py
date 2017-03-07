#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
MellPlayer UI

Created on 2017-02-21
@author: Mellcap
'''

import os
import re

from mellplayer.mell_logger import mell_logger


SONG_CATEGORIES = (
    '流行', '摇滚', '民谣', '说唱', '轻音乐', '爵士', '乡村', '古典', '电子', '舞曲', '另类/独立',\
    '学习', '工作', '午休', '清晨', '夜晚',\
    '华语', '欧美', '日语', '韩语', '粤语', '小语种',\
    '怀旧', '清新', '浪漫', '性感', '治愈', '放松', '兴奋', '快乐', '安静', '思念'
)

# 所有颜色 https://upload.wikimedia.org/wikipedia/commons/1/15/Xterm_256color_chart.svg
FOREGROUND_COLOR = {       # 前景色
    'default'      : 246,
    'white'        : 15,
    'blue'         : 39,    
    'green'        : 118,
    'gray'         : 239,
    'red'          : 196,
    'pink'         : 201,
    'yellow'       : 220,
}

BLANK_CONSTANT = 3
TERMINAL_SIZE = os.get_terminal_size()
BOLD_STR = '\033[1m'
MAX_LINES = len(SONG_CATEGORIES)
ALL_LINES = MAX_LINES + BLANK_CONSTANT

class UI(object):

    def __init__(self, ui_mode='home'):
        self.category_lines = SONG_CATEGORIES
        self.mark_index = 0
        self.play_index= 0
        self.play_info = ''
        
        self.top_index = 0
        self.screen_height = TERMINAL_SIZE.lines
        self.screen_width = TERMINAL_SIZE.columns
        self.base_title = self._get_base_title()
        self.title = self.base_title
        self.ui_mode = ui_mode

    # =====================
    # UI Displayer
    # =====================
    
    def _get_base_title(self):
        player_name = '%s%s' % (BOLD_STR, self.gen_color('MellPlayer', 'blue'))
        netease = self.gen_color('网易云音乐', 'red')
        divider = self.gen_color(data=r'\\')
        display_items = [player_name, netease]
        return (' %s ' % divider).join(display_items)

    def update_title(self, items=None):
        if not items:
            self.title = self.base_title
        else:
            divider = self.gen_color(data=r'\\')
            divider_play = self.gen_color(data=r'>>')
            items = [self.gen_color(data=i, color='green') for i in items]
            extend_title = (' %s ' % divider).join(items)
            extend_title = ' %s %s' % (divider_play, extend_title)
            self.title = self.base_title + extend_title
        self.display()

    def display(self):
        '''
        UI 输出
        说明：多线程终端输出有问题，在每行结尾加\r
        '''
        display_lines = ['\r']
        display_title = '\n%s%s' % (' '*5, self.title)
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

            complete_line = '%s%s%s' % (category, ' '*10, play_info)
            display_lines.append(complete_line)

        if ALL_LINES < self.screen_height:
            # fill_blanks
            display_lines = self.fill_blanks(display_lines)
        # add tail
        display_lines = self.add_tail(source_list=display_lines, tail='\r')
        print('\n'.join(display_lines))
        
    def gen_category(self, category, is_markline=False):
        if is_markline:
            category = self.gen_mark(category)
            category = self.gen_color(data=category, color='yellow')
        else:
            category = '%s%s' % (' '*5, category)
            category = self.gen_color(data=category, color='')
        return category

    def gen_mark(self, category):
        return '  ➣  %s' % category

    def gen_playline(self):
        complete_info = [self.gen_color(data=p, color='yellow') for p in self.play_info]
        divider = self.gen_color(data='|', color='')
        return ('  %s  ' % divider).join(complete_info)

    # =====================
    # UI Controller
    # =====================
    
    def next_line(self):
        '''
        下一行
        '''
        if self.mark_index < (MAX_LINES - 1):
            self.mark_index += 1
            bottom_index = (self.screen_height - BLANK_CONSTANT) + self.top_index
            if self.mark_index > (bottom_index - 1):
                self.top_index += 1
        self.display()

    def prev_line(self):
        '''
        上一行
        '''
        if self.mark_index > 0:
            self.mark_index -= 1
            if self.mark_index < self.top_index:
                self.top_index -= 1
        self.display()

    def update_play_index(self):
        '''
        更新歌曲信息展示在光标选定行
        '''
        self.play_index = self.mark_index

    def update_play_info(self, play_info):
        '''
        更新歌曲信息
        '''
        if type(play_info) is str:
            play_info = [play_info]
        self.play_info = play_info
        self.display()

    # =====================
    # Utils
    # =====================
    
    def gen_color(self, data, color='default'):
        '''
        参考地址:http://blog.csdn.net/gatieme/article/details/45439671
        但是目前用不到这么多类型，目前只用前景色
        '''
        color_code = FOREGROUND_COLOR.get(color, 246)
        data = "\001\033[38;5;%sm\002%s\001\033[0m\002" % (color_code, data)
        return data

    def add_tail(self, source_list, tail):
        return map(lambda x: '%s%s' % (str(x), tail), source_list)

    def fill_blanks(self, display_lines, all_lines=ALL_LINES):
        '''
        补全空白行
        '''
        delta_lines = self.screen_height - all_lines
        display_lines += [' ' for i in range(delta_lines)]
        return display_lines

    
# =====================
# HelpUI
# =====================

HELP_LINES = {
    'help_space_1':    '',
    'control_move':    '操作',
    'next_line':       '[j]     [Next Line]         ---> 下',
    'prev_line':       '[k]     [Prev Line]         ---> 上',
    'quit':            '[q]     [Quit]              ---> 退出',
    'help_space_2':    '',
    'control_music':   '音乐',
    'space':           '[space] [Start/Pause]       ---> 播放／暂停',
    'next_song':       '[n]     [Next Song]         ---> 下一曲',
    'prev_song':       '[p]     [Prev Song]         ---> 上一曲',
    'next_playlist':   '[f]     [Forward Playlist]  ---> 下个歌单',
    'prev_playlist':   '[b]     [Backward Playlist] ---> 上个歌单',
    'help_space_3':    '',
    'control_volume':  '音量',
    'reduce_volume':   '[-]     [Reduce Volume]     ---> 减小音量',
    'increase_volume': '[=]     [Increase Volume    ---> 增加音量',
    'mute':            '[m]     [Mute]              ---> 静音',
    # 'help_space_4': '',
    # 'control_lyric': '歌词',
    # 'lyric': '[l] [Show/Hide Lyric] ---> 显示／关闭歌词',
    'help_space_5': '',
    'control_help': '帮助',
    'help':            '[h]     [Show/Hide Help]    ---> 显示／关闭帮助'
}

class HelpUI(UI):
    
    def __init__(self):
        super(HelpUI, self).__init__(ui_mode='help')

    def display(self):
        display_lines = ['\r']
        display_title = '\n%s%s' % (' '*5, self.title)
        display_lines.append(display_title)
        for key, help_line in HELP_LINES.items():
            colored_help_line = self.color_line(key=key, line=help_line)
            display_lines.append('%s%s' % (' '*5, colored_help_line))

        # fill blanks
        all_lines = len(HELP_LINES) + BLANK_CONSTANT
        if all_lines < self.screen_height:
            display_lines = self.fill_blanks(display_lines, all_lines=all_lines)
        # add tail
        display_lines = self.add_tail(source_list=display_lines, tail='\r')
        print('\n'.join(display_lines))

    def color_line(self, key, line):
        if key.startswith('control'):
            return self.gen_color(data='%s%s' % (BOLD_STR, line), color='yellow')
        else:
            return self.gen_color(data=line)

# =====================
# LyricUI
# =====================

class LyricUI(UI):
    
    def __init__(self):
        
        super(LyricUI, self).__init__(ui_mode='lyric')
        self.has_lyric = True
        self.lyric_times = None
        self.lyric_lines = ''
        self.lyric_display_lines = ''

    def parse_lyric(self, origin_lyric):
        if origin_lyric == 'no_lyric':
            self.has_lyric = False
        else:
            compiler = re.compile('\[(.+)\](.+?)\n')
            format_lyric = compiler.findall(origin_lyric)
            # mell_logger.debug('format_lyric: %s' % format_lyric)
            if format_lyric:
                self.lyric_times = [format_minute2second(l[0]) for l in format_lyric]
                self.lyric_lines = [l[1] for l in format_lyric]

    def display(self):
        display_lines = ['\r']
        display_title = '\n%s%s' % (' '*5, self.title)
        display_lines.append(display_title)
        if not self.has_lyric:
            self.display_center(text='没有找到歌词')
        elif not self.lyric_display_lines:
            self.display_center(text='歌词加载中')
        elif self.lyric_lines:
            for line in self.lyric_display_lines:
                display_lines.append('%s' % line)
            # fill blanks
            all_lines = len(self.lyric_display_lines) + BLANK_CONSTANT
            if all_lines < self.screen_height:
                display_lines = self.fill_blanks(display_lines, all_lines=all_lines)
            # add tail
            display_lines = self.add_tail(source_list=display_lines, tail='\r')
            print('\n'.join(display_lines) + '\r')

    def display_center(self, text):
        print(text)

    def roll(self, timestamp):
        lyric_times = self.lyric_times
        if lyric_times:
            if timestamp in lyric_times:
                lyric_index = lyric_times.index(timestamp) + 1
            else:
                lyric_times_copy = lyric_times[:]
                lyric_times_copy.append(timestamp)
                lyric_times_copy.sort()
                lyric_index = lyric_times_copy.index(timestamp)
            self.lyric_display_lines = self.lyric_lines[:lyric_index]
            mell_logger.debug('display_lines: %s' % self.lyric_display_lines)
            self.display()

    def initial_lyric(self):
        self.has_lyric = True
        self.lyric_times = None
        self.lyric_lines = ''
        self.lyric_display_lines = ''

# Basic Method
def format_minute2second(timestamp):
    stamp_list = timestamp[:5].split(':')
    return int(stamp_list[0]) * 60 + int(stamp_list[1])
    


# =====================
# Instance
# =====================

mell_ui = UI()
mell_help_ui = HelpUI()
mell_lyric_ui = LyricUI()
