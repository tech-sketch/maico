# -*- coding: utf-8 -*-
import unittest
from maico.manipulator import Manipulator
from maico.protocol.operation_protocol import ActionType, OperationProtocol, Operation


class TestPepper(unittest.TestCase):

    def test_invoke_one_to_many(self):
        self._invoke_app(ActionType.one_to_many)

    def test_invoke_one_to_one(self):
        self._invoke_app(ActionType.one_to_one)
    
    def test_switch_one_to_one(self):
        self._invoke_app(ActionType.one_to_one)
        self._invoke_app(ActionType.human)

    def test_human_operation(self):
        opr = Operation(
            utterance="‚±‚ê‚Í‚Ä‚·‚Æ‚¾‚æ",
            gesture="",
            picture="",
            move="")

        self._invoke_app(ActionType.human, opr)

    def test_terminate_dialog(self):
        self._invoke_app(ActionType.one_to_one)
        self._invoke_app(ActionType.terminate)
        # confirm that one to one end and one to many begin 

    def test_terminate_dialog(self):
        self._invoke_app(ActionType.human)
        self._invoke_app(ActionType.terminate)
        # confirm that vr connection end and one to many begin 

    def test_one_to_many_terminate_is_ignored(self):
        self._invoke_app(ActionType.one_to_many)
        self._invoke_app(ActionType.terminate)
        # confirm one to many still works

    def test_shutdown(self):
        self._invoke_app(ActionType.one_to_many)
        self._invoke_app(ActionType.shutdown)
        # confirm application stops

    def _invoke_app(self, action_type, operation=None):
        host, pepper_id = self._read_setting()
        manipulator = Manipulator(host)
        opr = OperationProtocol(pepper_id, action_type, operation)
        manipulator.send(opr)

    def _read_setting(self):
        return "server", "pepper_id"
