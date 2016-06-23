import unittest
import json
from datetime import datetime
from maico.sensor.target import Target


class SampleTarget(Target):

    def __init__(self):
        super(SampleTarget, self).__init__()
        self.title = ""
        self.array = []
        self.dictionary = {}
        self.date = datetime.now()


class TestTarget(unittest.TestCase):

    def test_serialize(self):
        t = SampleTarget()
        t.title = "title"
        t.array = [1, 2, 3]
        t.dictionary = {"a": 1, "b": 2}
        
        s = t.serialize()
        r = SampleTarget.deserialize(s)

        self.assertEqual(t.title, r.title)
        self.assertEqual(t.array, r.array)
        self.assertEqual(t.dictionary, r.dictionary)
        self.assertEqual(t.date, r.date)


if __name__ == '__main__':
    unittest.main()
