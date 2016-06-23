from datetime import datetime
from maico.sensor.stream import Confluence
from maico.sensor.targets.human import Human
from maico.sensor.targets.human_feature import MoveStatistics
from maico.sensor.targets.first_action_feature import FirstActionFeature
import maico.sensor.streams.human_stream as hs


class OneToManyStream(Confluence):
    KINECT_FPS = 30
    FRAMES_FOR_MOVE = 15
    MOVES_FOR_STAT = 4

    def __init__(self, human_stream):

        self._observation_begin = datetime.utcnow()

        # hyper parameters (it will be arguments in future)
        self.move_threshold = 0.1  # above this speed, human act to move (not searching items)

        self.move_stream = hs.MoveStream(human_stream, self.FRAMES_FOR_MOVE, self.KINECT_FPS, self.move_threshold)
        self.move_stat_stream = hs.MoveStatisticsStream(self.move_stream, self.MOVES_FOR_STAT)
        super(OneToManyStream, self).__init__(human_stream, self.move_stat_stream)
    
    def notify(self, target):
        key = target.__class__
        
        if key is Human:
            self._pool[key] = [target]  # store only 1 (latest) human 
        else:
            if key not in self._pool:
                self._pool[key] = []
            self._pool[key].append(target)
        
        if self.is_activated():
            t = self.merge()
            self.out_stream.push(t)
            self.reset()

    def is_activated(self):
        hs = self.get(Human)
        stats = self.get(MoveStatistics)

        if len(hs) == 1 and len(stats) == 1:
            return True
        else:
            return False

    def merge(self):
        h = self.get(Human)[0]
        stat = self.get(MoveStatistics)[0]

        staying_time = h.get_elapsed_seconds()
        feature = FirstActionFeature(
            _id=h._id,
            staying_time=staying_time,
            mean_moving_rate=stat.moving_time.sum_ / stat.seconds.sum_,
            max_moving_rate=stat.moving_time.max_ / stat.seconds.mean_,
            min_moving_rate=stat.moving_time.min_ / stat.seconds.mean_,
            mean_moving_speed=stat.moving_speed.mean_
            )
        return feature
