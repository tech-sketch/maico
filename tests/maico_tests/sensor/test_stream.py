import unittest
from maico.sensor.stream import Stream, Observer
from maico.sensor.stream import Confluence


class SampleConfluence(Confluence):

    def __init__(self, *streams):
        super(SampleConfluence, self).__init__(streams)
    
    def is_full(self):
        print(self._pool)
        if len(self.get(int)) >= 2 and len(self.get(float)) >= 3:
            return True
        else:
            return False

    def _merge(self):
        result = 0
        for i in self.get(int):
            result += i / 2

        for f in self.get(float):
            result += f * 2

        return result


class TestStream(unittest.TestCase):

    def test_stream(self):
        st = Stream()
        st.subscribe(print)
        st.inflow(range(10))

    def test_confluence(self):
        s1 = Stream()
        s2 = Stream()
        answers = []

        conf = SampleConfluence(s1, s2)
        conf.out_stream.subscribe(lambda t: answers.append(t))
        
        for i in range(6):
            s1.push(i)
            s2.push(i/10)
        
        self.assertEqual(len(answers), 2)


if __name__ == '__main__':
    unittest.main()
