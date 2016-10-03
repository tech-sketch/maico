# -*- coding: utf-8 -*-


class DialogueState(object):
    def __init__(self):
        self.__state = {'small_area': None,
                        'middle_area': None,
                        'large_area': None,
                        'date': None,
                        'seamt': None}

    def update(self, dialogue_act):
        self.__state['small_area'] = dialogue_act.get('small_area', self.__state['small_area'])
        self.__state['middle_area'] = dialogue_act.get('middle_area', self.__state['middle_area'])
        self.__state['large_area'] = dialogue_act.get('large_area', self.__state['large_area'])
        self.__state['date'] = dialogue_act.get('date', self.__state['date'])
        self.__state['seamt'] = dialogue_act.get('seamt', self.__state['seamt'])

    def has(self, name):
        return self.__state.get(name, None) != None

    def get_small_area(self):
        return self.__state['small_area']

    def get_middle_area(self):
        return self.__state['middle_area']

    def get_large_area(self):
        return self.__state['large_area']

    def get_date(self):
        return self.__state['date']

    def get_sea_or_mt(self):
        return self.__state['seamt']

    def clear(self):
        self.__init__()

    def __str__(self):
        import pprint
        return pprint.pformat(self.__state)
