from pykinect2 import PyKinectV2
from pykinect2.PyKinectV2 import *
from pykinect2 import PyKinectRuntime
import ctypes
import _ctypes
import numpy as np
import _thread as thread
from datetime import datetime
from maico.sensor.environment import Environment
from maico.sensor.stream import Stream
from maico.sensor.targets.human import Human


class KinectEnvironment(Environment):

    def __init__(self):
        super(KinectEnvironment, self).__init__()
                     
        self._kinect = None
        self._bodies = None        
        self.tracking = []

        self._streams[Human] = {}

        self._continue = False
        self.observation_width = 0
        self.observation_height = 0

        self._on_infrared_frame = None
        self._on_body_joints = None
    
    def on_infrared_frame(self, handler):
        self._on_infrared_frame = handler

    def on_body_joints(self, handler):
        self._on_body_joints = handler

    def on_human_stream(self, handler):
        self._on_human_stream = handler

    def open(self):
        self._kinect = PyKinectRuntime.PyKinectRuntime(PyKinectV2.FrameSourceTypes_Infrared | PyKinectV2.FrameSourceTypes_Body)
        self._continue = True
        self.observation_width = self._kinect.infrared_frame_desc.Width
        self.observation_height = self._kinect.infrared_frame_desc.Height
    
    def stop(self):
        self._continue = False
            
    def close(self):
        self._continue = False
        self._kinect.close()

    def observe(self):

        if not self._continue:
            self.open()

        while self._continue:
            if self._kinect.has_new_infrared_frame():
                frame = self._kinect.get_last_infrared_frame()
                if self._on_infrared_frame:
                    self._on_infrared_frame(frame)

            if self._kinect.has_new_body_frame(): 
                self._bodies = self._kinect.get_last_body_frame()
            
            if self._bodies is not None:
                detected = []
                for i in range(0, self._kinect.max_body_count):
                    body = self._bodies.bodies[i]
                    if not body.is_tracked:
                        continue 
                    else:
                        _id = str(body.tracking_id)
                        detected.append(_id)
                        if _id not in self.tracking:
                            self.tracking.append(_id)
                            self.get_stream(Human)[_id] = Stream()
                            if self._on_human_stream:
                                self._on_human_stream(self.get_stream(Human)[_id])

                        joints = body.joints
                        joint_points = self._kinect.body_joints_to_depth_space(joints)
                        st = self.get_stream(Human)[_id]
                        h = Human(_id, joints, joint_points)
                        st.push(h)
                        if self._on_body_joints:
                            self._on_body_joints(i, joints, joint_points)


                # confirm exist or not
                disappeared = [k for k in self.tracking if k not in detected]
                for d in disappeared:
                    self.tracking.remove(d)
                    self.get_stream(Human)[d].push(Human(d, tracked=False))
                    del self.get_stream(Human)[d]

            frame = None

            yield True

        self.close()
        return False
