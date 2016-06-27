from datetime import datetime
from collections import namedtuple
from maico.sensor.target import SmartJSON


class SensingProtocol():

    class SensingProtocolHeader():

        def __init__(self, timestamp=None):
            self.timestamp = timestamp


    def __init__(self, target):
        self._id = target._id
        self.timestamp = datetime.utcnow()
        attributes = target._to_dict(target, ignore_private=True)
        c_type = target.__module__ + "." + target.__class__.__name__

        self.feature = {
            "__type__": c_type,
            "attributes": attributes
        }

    def serialize(self):
        return SmartJSON.dumps(self.__dict__)

    @classmethod
    def deserialize(cls, s):
        _s = s.strip()
        d = SmartJSON.loads(_s)

        h = SensingProtocol.SensingProtocolHeader(d["timestamp"])
        _type = d["feature"]["__type__"]
        names = _type.split(".")
        class_name = names[len(names) - 1]
        package_name = _type.replace("." + class_name, "")

        mod = __import__(package_name, fromlist=[class_name])
        obj = getattr(mod, class_name)(d["_id"])

        for f in d["feature"]["attributes"]:
            setattr(obj, f, d["feature"]["attributes"][f])
        
        return obj, h


class LearningProtocol(SensingProtocol):

    class LearningProtocolHeader(SensingProtocol.SensingProtocolHeader):

        def __init__(self, timestamp=None, prediction=(), feedback=()):
            super(LearningProtocolHeader, self).__init__(timestamp)
            self.prediction = prediction
            self.feedback = feedback


    def __init__(self, target, prediction, feedback=()):
        super().__init__(target)
        self.prediction = prediction
        self.feedback = feedback
        if len(self.feedback) == 0:
            self.feedback = dict.fromkeys(self.prediction.keys(), 0)

    @classmethod
    def deserialize(cls, s):
        _s = s.strip()
        obj, h  = super(LearningProtocol, cls).deserialize(_s)
        d = SmartJSON.loads(_s)

        return obj, LearningProtocolHeader(h.timestamp, d["prediction"], d["feedback"])
