# -*- coding: utf-8 -*-
from .dialogue_management.manager import DialogueManager
from .language_generation.generator import LanguageGenerator
from .language_understanding.language_understanding import RuleBasedLanguageUnderstanding


class Bot(object):
    def __init__(self):
        self.generator = LanguageGenerator()
        self.language_understanding = RuleBasedLanguageUnderstanding()
        self.manager = DialogueManager()

    def reply(self, sent):
        dialogue_act = self.language_understanding.execute(sent)

        self.manager.update_dialogue_state(dialogue_act)
        sys_act_type = self.manager.select_action(dialogue_act, sent)

        state = self.manager.dialogue_state
        sent = self.generator.generate_sentence(sys_act_type, state)
        sent = {'utt': sent}
        return sent
