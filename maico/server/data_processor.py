import os

from maico.model.first_action.model import FirstActionHandModel
from maico.protocol.sensing_protocol import SensingProtocol, LearningProtocol


class TrainingHandler(object):
    model = None
    feedbacks = {}

    @classmethod
    def predict(cls, target_or_targets):
        body_header = SensingProtocol.deserialize(target_or_targets)
        body, header = body_header

        def p(t):
            predicted = {} if cls.model is None else cls.model.predict(t).to_dict()
            feedback = {}

            if t._id in cls.feedbacks:
                feedback = cls.feedbacks[t._id]

            lp = LearningProtocol(t, predicted, feedback)
            return lp.serialize()

        return p(body)


class SensingHandler(object):
    watch_file = ""
    watch_position = 0

    @classmethod
    def reset(cls):
        cls.watch_position = 0

    @classmethod
    def set_watch_file(cls, file_path):
        if not os.path.isfile(file_path):
            raise Exception("The file to watch does not exist")
        cls.watch_file = file_path
        cls.watch_position = 0

    @classmethod
    def file_read(cls):
        with open(cls.watch_file, "r", encoding="utf-8") as f:
            f.seek(cls.watch_position)
            ln = f.readline()
            cls.watch_position = f.tell()

        return ln


if __name__ == '__main__':
    SENSING_FILE = os.path.join(os.path.dirname(__file__), "../../tests/samples/sensing_protocol_samples.txt")
    LEARNING_FILE = os.path.join(os.path.dirname(__file__), "../../tests/samples/learning_protocol_samples.txt")
    model = FirstActionHandModel()
    TrainingHandler.model = model
    SensingHandler.set_watch_file(SENSING_FILE)
    ln = SensingHandler.file_read()
    TrainingHandler.predict(ln)
