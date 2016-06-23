from collections import deque
from maico.sensor.target import Target


class Stream():

    def __init__(self):
        self.observers = []
    
    def subscribe(self, observer):
        self.observers.append(observer)

    def push(self, target):
        for o in self.observers:
            if isinstance(o, Observer):
                o.notify(target)
            elif hasattr(o, "__call__"):
                o(target)

    def inflow(self, sequence):
        for s in sequence:
            self.push(s)


class Observer():

    def notify(self, target):
        raise Exception("Observer have to implements notify method")


class Accumulator(Observer):

    def __init__(self, in_stream, size, shift=0):
        super(Accumulator, self).__init__()
        self.size = size
        self.shift = shift
        self.queue = deque(maxlen=size)
        self.out_stream = Stream()
        in_stream.subscribe(self)
    
    def subscribe(self, observer):
        self.out_stream.subscribe(observer)

    def notify(self, target):
        self.queue.append(target)

        if self.is_full():
            a = self.accumulate()
            self.out_stream.push(a)
            self.reset()

    def reset(self):
        if self.shift == 0:
            self.queue.clear()
        else:
            for i in range(selfself.shift):
                self.queue.popleft()

    def is_full(self):
        return True if len(self.queue) == self.size else False

    def accumulate(self):
        raise Exception("You have to implements accumulate process")


class Confluence(Observer):
    
    def __init__(self, *streams):
        super(Confluence, self).__init__()
        self._pool = {}
        self.out_stream = Stream()

        for s in streams:
            s.subscribe(self)
    
    def subscribe(self, observer):
        self.out_stream.subscribe(observer)

    def notify(self, target):
        key = target.__class__

        if key not in self._pool:
            self._pool[key] = []

        self._pool[key].append(target)
        
        if self.is_activate():
            t = self.merge()
            self.out_stream.push(t)
            self.reset()

    def reset(self):
        for c in self._pool:
            self._pool[c].clear()

    def get(self, key):
        return [] if key not in self._pool else self._pool[key]
    
    def is_activated(self):
        raise Exception("You have to implements is_activated to judge the pool is full")

    def merge(self):
        raise Exception("You have to implements merge to make instance from pooled targets")
