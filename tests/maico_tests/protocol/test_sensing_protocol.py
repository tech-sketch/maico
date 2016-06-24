import unittest
from datetime import datetime
from maico.protocol.sensing_protocol import SensingProtocol
from maico.sensor.target import Target


class SampleTarget(Target):

    def __init__(self, _id = "", title="", number=0, date=None):
        super().__init__(_id)
        self.title = title
        self.number = number
        self.date = date


class TestSensingProtocol(unittest.TestCase):

    def test_serialize_deserialize(self):
        t = SampleTarget("111", "test_sensing_protocol", 1, datetime.now())
        p = SensingProtocol(t)
        s = p.serialize()
        # maybe send to server...
        r = SensingProtocol.deserialize(s)

        self.assertEqual(t._id, r._id)
        self.assertEqual(t.title, r.title)
        self.assertEqual(t.number, r.number)
        self.assertEqual(t.date, r.date)


if __name__ == '__main__':
    unittest.main()
