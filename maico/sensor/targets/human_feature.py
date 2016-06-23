from collections import namedtuple
import numpy as np
from maico.sensor.target import Target


class MoveFeature(Target):

    def __init__(self,
                 seconds=0,
                 distance=0,
                 moving_speed=0,
                 moving_time=0,
                 location=()):
        super(MoveFeature, self).__init__()
        self.seconds = seconds
        self.distance = distance
        self.moving_speed = moving_speed
        self.moving_time = moving_time
        self.location = [] if len(location) == 0 else location


class MoveStatistics(Target):
    StatisticsFeature = namedtuple("StatisticsFeature", ["sum_", "min_", "max_", "mean_"])

    def __init__(self, 
                 seconds=None,
                 distance=None,
                 moving_speed=None,
                 moving_time=None,
                 location=None):
        super(MoveStatistics, self).__init__()
        self.seconds = seconds
        self.distance = distance
        self.moving_speed = moving_speed
        self.moving_time = moving_time
        self.location = location
