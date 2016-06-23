import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), "../../../../"))
from maico.sensor.monitor.kinect_monitor import KinectMonitor
from maico.sensor.streams.one_to_many_stream import OneToManyStream


def handle_stream(stream):

    def show_human(feature):
        print("Human {0}: {1}".format(feature._id, feature.serialize()))

    return OneToManyStream(stream).subscribe(show_human)


def main():
    gui = KinectMonitor()
    gui.env.on_human_stream(handle_stream)
    gui.run()


if __name__ == "__main__":
    main()
