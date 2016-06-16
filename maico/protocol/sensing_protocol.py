class SensingProtcol():

    def __init__(self, 
                 sensor_id="",
                 sensed=()):
        self.sendor_id = sensor_id
        self.sensed = sensed if len(sensed) > 0 else []


class Sensed():

    def __init__(self, 
                 target_id="",
                 behaviors=()):
        self.target_id = target_id
        self.behaviors = behaviors if len(behaviors) > 0 else {}
