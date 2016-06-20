class OperationProtocol():

    def __init__(self, 
                 sensor_id="",
                 operation=None):
        
        self.sendor_id = sensor_id
        self.operation = operation


class Operation():

    def __init__(self, 
                 utterance="",
                 gesture="",
                 picture="",
                 move=""):
        self.utterance = utterance
        self.gesture = gesture
        self.picture = picture
        self.move = move
