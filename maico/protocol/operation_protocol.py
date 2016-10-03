from enum import Enum
from maico.sensor.target import SmartJSON


class ActionType(Enum):
    welcome="W"
    one_to_many="OTM"
    call="C"
    one_to_one="OTO"
    human="H"
    terminate="T"
    shutdown="X"


class OperationProtocol():

    def __init__(self, 
                 sensor_id="",
                 action_type="",
                 operation=None):
        
        self.sendor_id = sensor_id
        self.action_type = action_type if isinstance(ActionType, str) else action_type.value 
        self.operation = operation

    def serialize(self):
        return SmartJSON.dumps(self.__dict__)



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
