from maico.model.interface import MaicoModel
from maico.sensor.targets.first_action import FirstActionPrediction


class FirstActionModel(MaicoModel):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def predict(self, target):
        return FirstActionPrediction(target._id, probability=0.5)
