class Environment():

    def __init__(self):
        self._streams = {}

    def get_stream(self, klass):
        return None if klass not in self._streams else self._streams[klass]

    def open(self):
        raise Exception("Environment has to implements open method to initialize environment")

    def close(self):
        raise Exception("Environment has to implements close method to destroy environment safely")
