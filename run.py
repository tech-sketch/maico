import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), "./maico"))
import tornado.ioloop
from tornado.options import define, options
from maico.sensor.monitor.kinect_monitor import KinectMonitor
from maico.sensor.monitor.server.application import SensorMonitor
from maico.sensor.stream import WebSocketTerminal
from maico.sensor.streams.one_to_many_stream import OneToManyStream
from maico.model.first_action.model import FirstActionModel, FirstActionHandModel


TRAINING_FILE = os.path.join(os.path.dirname(__file__), "./tests/data/run_training.txt")


define("mode", default="S", help="mode: S is server, K is sensing (kinect monitor)")
define("server", default="ws://localhost:80/observation", help="websocket url to server")
define("trainer", default="ws://localhost:8080/receive", help="websocket url to training server")
define("training_file", default=TRAINING_FILE, help="training file path")


class SensingOneToMany():

    def __init__(self, server_url, trainer_url):
        self.server = WebSocketTerminal(server_url)
        self.trainer = WebSocketTerminal(trainer_url)
    
    def observe(self, stream):
        return OneToManyStream(stream).subscribe(self.server).subscribe(self.trainer)


if __name__ == "__main__":
    tornado.options.parse_command_line()
    
    if options.mode.upper() == "K":
        gui = KinectMonitor()
        logger = SensingOneToMany(options.server, options.trainer)
        gui.env.on_human_stream(logger.observe)
        gui.run()
    else:
        from maico.server.app import application
        application.listen(80)

        model = FirstActionHandModel()
        app = SensorMonitor(model, options.training_file)
        app.listen(8080)
        
        tornado.ioloop.IOLoop.current().start()
