# -*- coding: utf-8 -*-
"""
Created on Fri Jul 19 2019
"""
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

__author__ = "yuhao"

from os import path

from matplotlib.colors import LinearSegmentedColormap, Normalize

DEFAULT_FILE_PATH = path.join(path.dirname(__file__), 'ColTabs')

class OpendtectColormaps(object):
    def __init__(self, filename=DEFAULT_FILE_PATH):
        self.od_cm_file = filename
        self.color_dicts = None
        self.normalizer = Normalize(vmin=0, vmax=255)
        self._convert_to_cm()

    @property
    def cmaps(self):
        return list(self.color_dicts.keys())

    def __call__(self, cm):
        return LinearSegmentedColormap.from_list(
            cm,
            colors=self.color_dicts[cm],
            N=256,
            gamma=1.0)

    def _convert_to_cm(self):
        with open(self.od_cm_file, 'r') as fl:
            text = fl.readlines()

        text_select = []
        num=-1
        for line in text:
            if line.split('.')[0].isdigit():
                num_color = int(line.split('.')[0])-1
                if num_color != num:
                    num = num_color
                    text_select.append([])
                text_select[num].append(line.split(':'))

        text_select = [dict(a) for a in text_select]

        color_dicts = {}
        for dic in text_select:
            color_dicts[self.get_name(dic)] = self.get_cdict(dic)

        self.color_dicts = color_dicts

    def get_name(self, abc):
        for k in abc.keys():
            if "Name" in k:
                return abc[k].rstrip('\n').lstrip(' ').\
                    replace('-', '_').replace(' ', '_')

    def get_cdict(self, abc):
        cdict=[]
        for k in abc.keys():
            if "Value-Color" in k:
                str_list = abc[k].rstrip("\n").split('`')
                str_list = str_list[:-1] if len(str_list) == 5 else str_list
                v = float(str_list[0])
                list_int = [self.normalizer(int(i)) for i in str_list[1:]]
                cdict.append(tuple((v, tuple(list_int))))
        return cdict
