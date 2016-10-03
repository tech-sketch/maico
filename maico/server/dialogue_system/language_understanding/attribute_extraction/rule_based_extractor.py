# -*- coding: utf-8 -*-
import re

from maico.server.dialogue_system.knowledge.reader import read_small_areas, read_middle_areas, read_large_areas
from ..utils.utils import kansuji2arabic, match_rate


class RuleBasedAttributeExtractor(object):
    def __init__(self):
        self.__small_areas = read_small_areas()
        self.__middle_areas = read_middle_areas()
        self.__large_areas = read_large_areas()

    def extract(self, text):
        attribute = {'small_area': self.__extract_small_area(text),
                     'middle_area': self.__extract_middle_area(text),
                     'large_area': self.__extract_large_area(text),
                     'date': self.__extract_date(text),
                     'seamt': self.__extract_sea_or_mt(text)}

        return attribute

    def __extract_area(self, text, areas):
        # locations = [loc for loc in areas if loc in text]
        locations = [loc for loc in areas if match_rate(text, loc) >= 60]
        locations.sort(key=len, reverse=True)
        location = locations[0] if len(locations) > 0 else ''

        return location

    def __extract_small_area(self, text):
        small_area = self.__extract_area(text, self.__small_areas)

        return small_area

    def __extract_middle_area(self, text):
        middle_area = self.__extract_area(text, self.__middle_areas)

        return middle_area

    def __extract_large_area(self, text):
        large_area = self.__extract_area(text, self.__large_areas)

        return large_area

    def __extract_sea_or_mt(self, text):
        sea_or_mt = [p for p in ['海', '山'] if p in text]
        sea_or_mt = sea_or_mt[-1] if len(sea_or_mt) > 0 else ''

        return sea_or_mt

    def __extract_date(self, text):
        pattern = r'\d月|[一二三四五六七八九十]+月'
        match_obj = re.findall(pattern, text)
        month_str = match_obj[0][:-1] if len(match_obj) > 0 else ''
        month_int = kansuji2arabic(month_str)

        return month_int
