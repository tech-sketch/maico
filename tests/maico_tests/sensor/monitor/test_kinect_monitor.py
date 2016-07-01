import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), "../../../../"))
from maico.sensor.monitor.kinect_monitor import KinectMonitor


def handle_stream(stream):

    def show_human(human):
        if human.tracked:
            print("Tracking Human {0}.".format(human._id))
        else:
            print("Human {0} disappered.".format(human._id))

    stream.subscribe(show_human).subscribe(wt)


def main():
    gui = KinectMonitor()
    gui.env.on_human_stream(handle_stream)
    gui.run()


if __name__ == "__main__":
    main()
