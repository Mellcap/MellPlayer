#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Netease Music UI

Created on 2017-02-21
@author: Mellcap
'''

import os


SONG_CATEGORIES = (
    '流行', '摇滚', '民谣', '说唱', '轻音乐', '爵士', '乡村', '古典', 'R&B/Soul', '电子', '舞曲', '另类/独立',\
    '学习', '工作', '午休', '清晨', '夜晚',\
    '华语', '欧美', '日语', '韩语', '粤语', '小语种',\
    '怀旧', '清新', '浪漫', '性感', '治愈', '放松', '兴奋', '快乐', '安静', '思念'
)

# 所有颜色 https://upload.wikimedia.org/wikipedia/commons/1/15/Xterm_256color_chart.svg
FORE_COLOR = {       # 前景色
    'default'      : 249,
    'white'        : 15,
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

    def __init__(self, ui_mode='home'):
        self.category_lines = SONG_CATEGORIES
        self.mark_index = 0
        self.play_index= 0
        self.play_info = ''
        self.top_index = 0
        self.screen_height = TERMINAL_SIZE.lines
        self.screen_width = TERMINAL_SIZE.columns
        self.title = self._get_title()
        self.ui_mode = ui_mode

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
        display_title = '\n%s%s\r' % (' '*5, self.title)
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

    def fill_blanks(self, display_lines, all_lines=ALL_LINES):
        delta_lines = self.screen_height - all_lines
        display_lines += [' ' for i in range(delta_lines)]
        return display_lines

    
# =====================
# HelpUI
# =====================
HELP_LINES = {
    'help_space_1': '',
    'control_move': '操作',
    'next_line':       '[j]     [Next Line]         ---> 下',
    'prev_line':       '[k]     [Prev Line]         ---> 上',
    'quit':            '[q]     [Quit]              ---> 退出',
    'help_space_2': '',
    'control_music': '音乐',
    'space':           '[space] [Start/Pause]       ---> 播放／暂停',
    'next_song':       '[n]     [Next Song]         ---> 下一曲',
    'prev_song':       '[p]     [Prev Song]         ---> 上一曲',
    'next_playlist':   '[f]     [Forward Playlist]  ---> 下个歌单',
    'prev_playlist':   '[b]     [Backward Playlist] ---> 上个歌单',
    'help_space_3': '',
    'control_volume': '音量',
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
        display_title = '\n%s%s\r' % (' '*5, self.title)
        display_lines.append(display_title)
        for key, help_line in HELP_LINES.items():
            display_lines.append('%s%s\r' % (' '*5, help_line))

        # fill blanks
        all_lines = len(HELP_LINES) + BLANK_CONSTANT
        if all_lines < self.screen_height:
            display_lines = self.fill_blanks(display_lines, all_lines=all_lines)
        print('\n'.join(display_lines) + '\r')

# =====================
# LyricUI
# =====================

class LyricUI(UI):
    def __init__(self):
        super(LyricUI, self).__init__(ui_mode='lyric')
        self.lyric_times = None
        self.lyric_lines = None
        self.lyric_display_lines = None

    def parse_lyric(self, origin_lyric):
        compiler = re.compile('\[(.+)\](.+?)\n')
        format_lyric = compiler.findall(origin_lyric)
        if format_lyric:
            self.lyric_times = [format_minute2second(l[0]) for l in format_lyric]
            self.lyric_lines = [l[1] for l in format_lyric]

    def display(self):
        display_lines = ['\r']
        display_title = '\n%s%s\r' % (' '*5, self.title)
        display_lines.append(display_title)
        if self.lyric_lines:
            for line in self.lyric_display_lines:
                display_lines.append('%s\r' % line)
        print('\n'.join(display_lines) + '\r')

    def roll(self, timestamp):
        lyric_times = self.lyric_times
        if lyric_times and timestamp in lyric_times:
            lyric_index = lyric_times.index(timestamp)
            self.lyric_display_lines = self.lyric_lines[:(lyric_index + 1)]
            self.display()

# Basic Method
def format_minute2second(timestamp):
    stamp_list = timestamp[:5].split(':')
    return int(stamp_list[0]) * 60 + int(stamp_list[1])
    
