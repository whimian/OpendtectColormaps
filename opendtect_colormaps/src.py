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
        n_levels = self.color_dicts[cm]['N']
        n_levels = 256 if (n_levels is None or n_levels == 0) else n_levels
        cmap = LinearSegmentedColormap.from_list(
            cm,
            colors=self.color_dicts[cm]['cdict'],
            N=n_levels,
            gamma=1.0)
        undef_color = self.color_dicts[cm]['undef']
        if undef_color is not None:
            cmap.set_bad(undef_color)
        return cmap

    def _convert_to_cm(self):
        with open(self.od_cm_file, 'r') as fl:
            text = fl.readlines()

        text_select = []
        num = -1
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
            color_dicts[self.get_name(dic)] = {
                "cdict": self.get_cdict(dic),
                "undef": self.get_undef_color(dic),
                "N": self.get_nr_segments(dic)
            }
        self.color_dicts = color_dicts

    @staticmethod
    def get_name(abc):
        colormap_name = None
        for k in abc.keys():
            if "Name" in k:
                colormap_name = abc[k].rstrip('\n').lstrip(' ').\
                    replace('-', '_').replace(' ', '_')
                break
        return colormap_name

    def get_cdict(self, abc):
        cdict = []
        for k in abc.keys():
            if "Value-Color" in k:
                str_list = abc[k].rstrip("\n").split('`')
                str_list = str_list[:-1] if len(str_list) == 5 else str_list
                v = float(str_list[0])
                list_int = [self.normalizer(int(i)) for i in str_list[1:]]
                cdict.append(tuple((v, tuple(list_int))))
        return cdict

    def get_undef_color(self, abc):
        undef_color = None
        for k in abc.keys():
            if "Undef color" in k:
                str_list = abc[k].rstrip("\n").split('`')
                str_list = str_list[:-1] if len(str_list) == 4 else str_list
                list_int = [self.normalizer(int(i)) for i in str_list]
                undef_color = tuple(list_int)
                break
        return undef_color

    @staticmethod
    def get_nr_segments(abc):
        nr_segments = None
        for k in abc.keys():
            if "Nr segments" in k:
                nr_segments = int(abc[k].rstrip("\n"))
                break
        return nr_segments
