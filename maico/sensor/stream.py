from collections import deque
import os
from maico.sensor.target import Target
from maico.protocol.sensing_protocol import SensingProtocol


class Stream():

    def __init__(self):
        self.observers = []
    
    def subscribe(self, observer):
        self.observers.append(observer)
        return self

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


class Terminal(Observer):

    def __init__(self, destination):
        super(Terminal, self).__init__()
        self.destination = destination

    def notify(self, target):
        payload = SensingProtocol(target)
        self.send(payload)
    
    def send(self, protocol):
        raise Exception("Terminal have to implements send method")


class FileTerminal(Terminal):

    def __init__(self, destination, initialize_file=True):
        super().__init__(destination)
        self._mode = "a"
        dir = os.path.dirname(destination)
        if not os.path.exists(dir):
            raise Exception("{0} does not exist.".format(dir))
        if initialize_file:
            self._mode = "w"           

    def send(self, protocol):
        line = protocol.serialize()
        with open(self.destination, self._mode, encoding="utf-8") as f:
            f.write(line + "\n")
        self._mode = "a"


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
        return self

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
        return self

    def notify(self, target):
        key = target.__class__

        if key not in self._pool:
            self._pool[key] = []

        self._pool[key].append(target)
        
        if self.is_activated():
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
