from collections import deque
from maico.model.interface import MaicoModel
from maico.sensor.targets.first_action import FirstActionPrediction


class FirstActionModel(MaicoModel):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def predict(self, feature):
        """
        implements machine learning model
        """

        return FirstActionPrediction(feature._id, probability=0.5)


class FirstActionHandModel(MaicoModel):

    def __init__(self, **kwargs):
        self.nerve = 1
        self.nervous_threshold = 0.2  # if moving_speed over this threshold, then nerve become min nerve
        self.recovery_rate = 1.2  # self.nerve recover and recover by this rate
        self.confidence_rate = 0.6  # the rate from long term reliability feature
        self.confidence_seconds = 60  # if staying time over this seconds, confidence raises
        self.moving_stability_threshold = 0.2 # if max - min of moving rate is below than this threshold, judge as stable
        self.stopping_rate = 0.6 
        self.action_threshold = 0.8
        self.rates = deque(maxlen=3)

    def predict(self, feature):
        is_stable = lambda f: (f.max_moving_rate - f.min_moving_rate) < self.moving_stability_threshold

        confidence = min(feature.staying_time / self.confidence_seconds, 1) * self.confidence_rate
        timing = 0.4
        if is_stable(feature) and feature.mean_stopping_rate >= self.stopping_rate:
            timing = min(feature.mean_stopping_rate * 0.5, timing)
        else:
            timing = min(feature.mean_stopping_rate * 0.25, 0.1)

        if feature.mean_moving_speed > self.nervous_threshold:
            self.nerve = 0.1
        else:
            self.nerve = min(self.nerve * self.recovery_rate, 1)

        rate = min((confidence + timing) * self.nerve, 1)

        self.rates.append(rate)
        execute = 0
        if min(self.rates) > self.action_threshold and sum(self.rates) / len(self.rates) > self.action_threshold:
            execute = 1
            self.nerve = 0.1

        return FirstActionPrediction(feature._id, probability=rate, execution= execute)
