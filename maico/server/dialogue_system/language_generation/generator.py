# -*- coding: utf-8 -*-
from ..knowledge.reader import read_dialogues
from ..knowledge.reader import read_spots


class LanguageGenerator(object):
    def __init__(self):
        self.__rules = read_dialogues()

    def generate_sentence(self, goto, state=None):
        rule = self.match_goto(goto)
        if goto == 'suggest':
            spot = Suggester().select_spot(state)
            text = rule.text.format(spot.place)
            text += spot.text
            return text
        else:
            return rule.text

    def match_goto(self, goto):
        for rule in self.__rules:
            if rule.type != 'output' and rule.type != 'output start':
                continue
            if rule.label == goto:
                return rule

        return None


class Suggester(object):
    def __init__(self):
        self.__spots = read_spots()

    def select_spot(self, state):
        spots = []
        if state.has('small_area'):
            spots = self.filter_by_small_area(state)
        elif state.has('middle_area'):
            spots = self.filter_by_middle_area(state)
        elif state.has('large_area'):
            spots = self.filter_by_large_area(state)
        else:
            pass
        spot = self.filter_by_rate(spots)
        return spot

    def filter_by_small_area(self, state):
        spots = [spot for spot in self.__spots if spot.place == state.get_small_area()]
        return spots

    def filter_by_middle_area(self, state):
        spots = [spot for spot in self.__spots if spot.pref == state.get_middle_area()]
        return spots

    def filter_by_large_area(self, state):
        spots = [spot for spot in self.__spots if
                 spot.area == state.get_large_area() and state.get_sea_or_mt() in spot.type]
        return spots

    def filter_by_rate(self, spots):
        return sorted(spots, key=lambda s: s.rate)[0]
