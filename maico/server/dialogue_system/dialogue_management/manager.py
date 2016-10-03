# -*- coding: utf-8 -*-
from ..dialogue_management.state import DialogueState
from ..knowledge.reader import read_dialogues
from ..language_understanding.utils.utils import match_rate


class DialogueManager(object):
    def __init__(self):
        self.__rules = read_dialogues()
        self.dialogue_state = DialogueState()

    def update_dialogue_state(self, dialogue_act):
        self.dialogue_state.update(dialogue_act)

    def select_action(self, dialogue_act, sent):
        act_type = dialogue_act['user_act_type']
        rule = self.match_text(act_type, sent)
        return rule.goto

    def match_text(self, act_type, sent):
        for rule in self.__rules:
            if rule.type != 'input':
                continue
            if rule.act_type == act_type:
                return rule
            if rule.acc and match_rate(sent, rule.text) >= int(rule.acc):
                return rule

    def welcome(self):
        for rule in self.__rules:
            if rule.type != 'output start':
                continue
            return rule.goto
