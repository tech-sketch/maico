import json
from datetime import datetime


class SmartJSON:
    DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S.%f"

    @classmethod
    def dumps(cls, obj):
        return json.dumps(obj, cls=SmartJSON.SmartJSONEncoder)

    @classmethod
    def loads(cls, string):
        return json.loads(string, cls=SmartJSON.SmartJSONDecoder)

    class SmartJSONEncoder(json.JSONEncoder):

        def default(self, obj):
            if isinstance(obj, datetime):
                return obj.strftime(SmartJSON.DATETIME_FORMAT)
            return json.JSONEncoder.default(self, obj)


    class SmartJSONDecoder(json.JSONDecoder):

        def __init__(self, *args, **kargs):
            super(SmartJSON.SmartJSONDecoder, self).__init__(object_hook=self.dict_to_object, *args, **kargs)
        
        def dict_to_object(self, d):
            return self._convert(d)
             
        def decode(self, obj):
            decoded = super(SmartJSON.SmartJSONDecoder, self).decode(obj)
            return self._convert(decoded)

        def _convert(self, dic):
            for k in dic:
                v = dic[k]
                if isinstance(v, str) and len(v) == 26 and v[:4].isdigit():
                    # 26 -> formatted datetime string length
                    try:
                        dic[k] = datetime.strptime(v, SmartJSON.DATETIME_FORMAT)
                    except ValueError as vex:
                        pass
            return dic


class Target():

    def __init__(self, _id=""):
        """
        Target class has to have argument-less constructor for deserialization.
        So if you need some arguments, please set default value to these.
        """
        self._id = _id  # unique id to identify the target
    
    def serialize(self, ignores=(), ignore_private=True):
        d = self._to_dict(self, ignores, ignore_private)
        return SmartJSON.dumps(d)

    @classmethod
    def deserialize(cls, string):
        instance = cls()
        j = SmartJSON.loads(string)

        attrs = instance.__dict__
        for a in attrs:
            if a in j:
                setattr(instance, a, j[a])

        return instance

    @classmethod
    def _to_dict(cls, instance, ignores=(), ignore_private=True):
        attrs = instance.__dict__
        result = {}
        for a in attrs:
            if ignore_private and a.startswith("_"):
                continue
            if a in ignores:
                continue

            result[a] = attrs[a]

        return result
