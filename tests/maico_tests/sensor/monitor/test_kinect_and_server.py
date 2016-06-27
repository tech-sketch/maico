import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), "../../../../"))
import tornado.ioloop
from tornado.options import define, options
from maico.sensor.monitor.kinect_monitor import KinectMonitor
from maico.sensor.monitor.server.application import SensorMonitor
from maico.sensor.stream import WebSocketTerminal
from maico.sensor.streams.one_to_many_stream import OneToManyStream
from maico.model.first_action.model import FirstActionModel, FirstActionHandModel


LEARNING_FILE = os.path.join(os.path.dirname(__file__), "../../../data/test_learning_ws.txt")


define("port", default=8080, help="Server Port")
define("mode", default="L", help="mode: L is learning (server), S is sensing (kinect monitor)")
define("url", default="ws://localhost:8080/receive", help="websocket url")
define("l_path", default=LEARNING_FILE, help="learning file to write")


class LogOneToMany():

    def __init__(self, path):
        self.terminal = WebSocketTerminal(path)
    
    def print_console(self, feature):
        print("Human {0}: {1}".format(feature._id, feature.serialize()))

    def observe(self, stream):
        return OneToManyStream(stream).subscribe(self.terminal).subscribe(self.print_console)


if __name__ == "__main__":
    tornado.options.parse_command_line()
    
    if options.mode.upper() == "L":
        model = FirstActionHandModel()
        app = SensorMonitor(model, options.l_path)
        app.listen(options.port)
        tornado.ioloop.IOLoop.current().start()

    else:
        gui = KinectMonitor()
        logger = LogOneToMany(options.url)
        gui.env.on_human_stream(logger.observe)
        gui.run()
