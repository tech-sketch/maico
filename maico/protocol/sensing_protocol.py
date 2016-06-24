from maico.sensor.target import SmartJSON


class SensingProtocol():

    def __init__(self, target):
        self.target_id = target._id
        features = target._to_dict(target, ignore_private=True)
        c_type = target.__module__ + "." + target.__class__.__name__

        self.body = {
            "__type__": c_type,
            "features": features
        }

    def serialize(self):
        return SmartJSON.dumps(self.__dict__)

    @classmethod
    def deserialize(cls, s):
        _s = s.strip()
        d = SmartJSON.loads(_s)

        _type = d["body"]["__type__"]
        names = _type.split(".")
        class_name = names[len(names) - 1]
        package_name = _type.replace("." + class_name, "")

        mod = __import__(package_name, fromlist=[class_name])
        obj = getattr(mod, class_name)(d["target_id"])

        for f in d["body"]["features"]:
            setattr(obj, f, d["body"]["features"][f])
        
        return obj


class LearningProtocol(SensingProtocol):

    def __init__(self, target, prediction, feedback=()):
        super().__init__(target)
        self.prediction = prediction
        self.feedback = feedback
        if len(self.feedback) == 0:
            self.feedback = dict.fromkeys(self.prediction.keys(), -1)

    @classmethod
    def deserialize(cls, s):
        _s = s.strip()
        obj = super(LearningProtocol, cls).deserialize(_s)
        d = SmartJSON.loads(_s)

        return obj, d["prediction"], d["feedback"]
