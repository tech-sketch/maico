from maico.sensor.target import Target


class FirstActionFeature(Target):

    def __init__(self, 
                 _id="",
                 staying_time=0,
                 mean_moving_rate=0,
                 max_moving_rate=0,
                 min_moving_rate=0,
                 mean_moving_speed=0
                 ):
        super().__init__(_id)
        self.staying_time = staying_time
        self.elapse_time = staying_time
        self.mean_moving_rate = mean_moving_rate
        self.max_moving_rate = max_moving_rate
        self.min_moving_rate = min_moving_rate
        self.mean_stopping_rate = 1 - mean_moving_rate
        self.mean_moving_speed = mean_moving_speed


class FirstActionPrediction(Target):

    def __init__(self, 
                 _id="",
                 probability=0,
                 execution=0,
                 ):
        super().__init__(_id)
        self.probability = probability
        self.execution = execution
