import os
import json
import tornado.escape
import tornado.web
import tornado.websocket
from tornado.ioloop import PeriodicCallback
from maico.protocol.sensing_protocol import SensingProtocol, LearningProtocol


class SensorMonitor(tornado.web.Application):

    def __init__(self, model, training_file="", is_append=False, file_source=None, interval=1000):
        self.watcher = None
        TrainingHandler.model = model
        TrainingHandler.set_training_file(training_file, is_append)

        if file_source:
            SensingHandler.set_watch_file(file_source.destination, interval)

        handlers = [
            (r"/", IndexHandler),
            (r"/monitor", TrainingHandler),
            (r"/receive", SensingHandler),
        ]

        settings = dict(
            cookie_secret="__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__",
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            xsrf_cookies=True,
            debug=True
        )
        super(SensorMonitor, self).__init__(handlers, **settings)


class IndexHandler(tornado.web.RequestHandler):

    def get(self):
        self.render("index.html", protocols=TrainingHandler.cache)


class TrainingHandler(tornado.websocket.WebSocketHandler):
    model = None
    training_file = ""
    write_mode = "w"
    waiters = set()
    cache = []
    cache_size = 100
    feedbacks = {}

    @classmethod
    def set_training_file(cls, file_path, is_append=False):
        if not os.path.exists(os.path.dirname(file_path)):
            raise Exception("The directory does not exist")
        cls.training_file = file_path
        if is_append:
            cls.write_mode = "a"

    def open(self):
        if len(TrainingHandler.waiters) == 0 and SensingHandler.watch_scheduler is not None:
            if not SensingHandler.watch_scheduler.is_running():
                SensingHandler.watch_scheduler.start()

        TrainingHandler.waiters.add(self)

    def on_close(self):
        TrainingHandler.waiters.remove(self)

    @classmethod
    def update_cache(cls, log):
        cls.cache.append(log)
        if len(cls.cache) > cls.cache_size:
            cls.cache = cls.cache[-cls.cache_size:]

    @classmethod
    def predict(cls, target_or_targets):
        ts = target_or_targets if isinstance(target_or_targets, (list, tuple)) else [target_or_targets]

        def p(t):
            predicted = {} if cls.model is None else cls.model.predict(t).to_dict()
            feedback = {}

            if t._id in cls.feedbacks:
                feedback = cls.feedbacks[t._id]

            lp = LearningProtocol(t, predicted, feedback)
            return lp.serialize()
        
        lps = [p(t) for t in ts]
                
        # send to client
        for waiter in cls.waiters:
            for lp in lps:
                try:
                    waiter.write_message(lp)
                except:
                    gen_log.error("Error is occurred when sending message: {0}".format(str(ex)))

        # write to file
        cls.write_trainings(lps)

    def on_message(self, message):
        msg = json.loads(message)
        target_id = msg["_id"]
        feedback = msg["feedback"]        

        if target_id not in self.feedbacks:
            self.feedbacks[target_id] = {}
        
        self.feedbacks[target_id] = feedback
        return True

    @classmethod
    def write_trainings(cls, learning_protocols):
        if not cls.training_file:
            return False

        """
        if initial and os.path.isfile(cls.training_file):
            os.remove(training_file)
        """

        with open(cls.training_file, cls.write_mode, encoding="utf-8") as f:
            f.write("\n".join(learning_protocols))

        cls.write_mode = "a"


class SensingHandler(tornado.websocket.WebSocketHandler):
    watch_file = ""
    watch_position = 0
    watch_scheduler = None

    @classmethod
    def set_watch_file(cls, file_path, interval):
        if not os.path.isfile(file_path):
            raise Exception("The file to watch does not exist")
        cls.watch_file = file_path
        cls.watch_position = 0
        cls.watch_scheduler = PeriodicCallback(cls.file_read, interval)

    def on_message(self, message):
        obj = SensingProtocol.deserialize(message)
        cls.send([obj])
    
    @classmethod
    def file_read(cls):
        sensed = []
        initial = True if cls.watch_position == 0 else False
        with open(cls.watch_file, "r", encoding="utf-8") as f:
            f.seek(cls.watch_position)
            for ln in f:
                obj = SensingProtocol.deserialize(ln)
                sensed.append(obj)
            
            cls.watch_position = f.tell()

        cls.send(sensed)
    
    @classmethod
    def send(self, sensed):
        TrainingHandler.predict(sensed)
