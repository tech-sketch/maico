import os
import sys
import argparse
sys.path.append(os.path.join(os.path.dirname(__file__), "../../../../"))
import tornado.ioloop
from tornado.options import define, options
from maico.sensor.monitor.kinect_monitor import KinectMonitor
from maico.sensor.monitor.server.application import SensorMonitor
from maico.sensor.stream import FileTerminal
from maico.sensor.streams.one_to_many_stream import OneToManyStream
from maico.model.first_action.model import FirstActionModel


SENSING_FILE = os.path.join(os.path.dirname(__file__), "../../../data/test_sensing.txt")
LEARNING_FILE = os.path.join(os.path.dirname(__file__), "../../../data/test_learning.txt")


define("port", default=8080, help="Server Port")
define("mode", default="L", help="mode: L is learning (server), S is sensing (kinect monitor)")
define("s_file", default=SENSING_FILE, help="sensing file to write")
define("l_file", default=LEARNING_FILE, help="learning file to write")


class LogOneToMany():

    def __init__(self, file_path):
        self.terminal = FileTerminal(file_path)
    
    def print_console(self, feature):
        print("Human {0}: {1}".format(feature._id, feature.serialize()))

    def observe(self, stream):
        return OneToManyStream(stream).subscribe(self.terminal).subscribe(self.print_console)


if __name__ == "__main__":
    tornado.options.parse_command_line()
    
    if options.mode.upper() == "L":
        # run monitoring server
        source = FileTerminal(options.s_file)
        app = SensorMonitor(FirstActionModel(), options.l_file, file_source=source, emulate=True)
        app.listen(options.port)
        tornado.ioloop.IOLoop.current().start()

    else:
        gui = KinectMonitor()
        logger = LogOneToMany(options.s_file)
        gui.env.on_human_stream(logger.observe)
        gui.run()
