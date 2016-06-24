from maico.sensor.target import SmartJSON


class SensingProtocol():

    def __init__(self, target):
        self._id = target._id
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

        _type = d["feature"]["__type__"]
        names = _type.split(".")
        class_name = names[len(names) - 1]
        package_name = _type.replace("." + class_name, "")

        mod = __import__(package_name, fromlist=[class_name])
        obj = getattr(mod, class_name)(d["_id"])

        for f in d["feature"]["attributes"]:
            setattr(obj, f, d["feature"]["attributes"][f])
        
        return obj


class LearningProtocol(SensingProtocol):

    def __init__(self, target, prediction, feedback=()):
        super().__init__(target)
        self.prediction = prediction
        self.feedback = feedback
        if len(self.feedback) == 0:
            self.feedback = dict.fromkeys(self.prediction.keys(), None)

    @classmethod
    def deserialize(cls, s):
        _s = s.strip()
        obj = super(LearningProtocol, cls).deserialize(_s)
        d = SmartJSON.loads(_s)

        return obj, d["prediction"], d["feedback"]
