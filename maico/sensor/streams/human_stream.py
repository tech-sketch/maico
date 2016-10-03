from collections import deque
import numpy as np
from maico.sensor.stream import Accumulator
from maico.sensor.targets.human_feature import MoveFeature, MoveStatistics


class MoveStream(Accumulator):

    def __init__(self, human_stream, frame_count, frame_per_sec, move_threshold=0.1, shift=0):
        super(MoveStream, self).__init__(human_stream, frame_count, shift)
        self._frame_per_sec = frame_per_sec
        self._move_threshold = move_threshold

    def accumulate(self):
        locations = list(filter(lambda lc: sum(lc) != 0, [h.location() for h in self.queue]))
        
        # move parameters
        seconds = self.size / self._frame_per_sec
        distance = 0.0
        movement = 0.0
        speed = 0.0
        location = []

        if len(locations) > 0:
            # see detail about kinect coordinate
            # https://msdn.microsoft.com/ja-jp/library/dn785530.aspx
            mean = np.mean(locations, axis=0)
            distance = mean[-1]  # z axis, distance from kinect
            location = list(mean)

            if len(locations) >= 2:  # two locations must be needed to calculate movement
                movement = np.linalg.norm(np.array(locations[-1]) - np.array(locations[0]))
                speed = movement / seconds  # meter / second

        # set property
        feature = MoveFeature(
            seconds=seconds,
            distance=distance,
            moving_speed=speed,
            moving_time=seconds if speed > self._move_threshold else 0,
            location=location
            )
        return feature


class MoveStatisticsStream(Accumulator):

    def __init__(self, move_stream, size, shift=0):
        super(MoveStatisticsStream, self).__init__(move_stream, size, shift)

    def accumulate(self):
        move_features = self.queue
        seconds = self.__calc_statistics([f.seconds for f in move_features])
        distance = self.__calc_statistics([f.distance for f in move_features])
        moving_speed = self.__calc_statistics([f.moving_speed for f in move_features])
        moving_time = self.__calc_statistics([f.moving_time for f in move_features])
        location = self.__calc_statistics([f.location for f in move_features])

        ms = MoveStatistics(seconds, distance, moving_speed, moving_time, location)
        return ms
 
    @classmethod
    def __calc_statistics(cls, sequence):
        sum_ = 0
        min_ = 0
        max_ = 0
        mean_ = 0

        if len(sequence) > 0:
            if isinstance(sequence[0], (list, tuple)):
                norms = [np.linalg.norm(x) for x in sequence]
                min_ = sequence[np.argmin(norms)]
                max_ = sequence[np.argmax(norms)]
                mean_ = list(np.mean(sequence, axis=0))
                sum_ = list(np.sum(sequence, axis=0))
            else:
                sum_ = sum(sequence)
                min_ = min(sequence)
                max_ = max(sequence)
                mean_ = np.mean(sequence)

        return MoveStatistics.StatisticsFeature(sum_, min_, max_, mean_)

