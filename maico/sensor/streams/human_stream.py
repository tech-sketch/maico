from collections import deque
import numpy as np
from maico.sensor.stream import Accumulator
from maico.sensor.targets.human_feature import MoveFeature, MoveStatistics


class MoveStream(Accumulator):

    def __init__(self, human_stream, frame_count, sec_per_frame, move_threshold=0.1, shift=0):
        super(MoveStream, self).__init__(human_stream, frame_count, shift)
        self._sec_per_frame = sec_per_frame
        self._move_threshold = move_threshold

    def accumulate(self):
        locations = [h.location() for h in self.queue]
        locations = [lc for lc in locations if sum(lc) != 0]

        mean = np.mean(locations, axis=0)

        # see detail about kinect coordinate
        # https://msdn.microsoft.com/ja-jp/library/dn785530.aspx
        distance = mean[-1]  # distance from kinect
        seconds = self.size / self._sec_per_frame
        movement = np.linalg.norm(np.array(locations[-1]) - np.array(locations[0]))
        speed = movement / seconds  # meter / second 

        # set property
        feature = MoveFeature(
            seconds=seconds,
            distance=distance,
            moving_speed=speed,
            moving_time=seconds if speed > self._move_threshold else 0,
            location=list(mean)
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

