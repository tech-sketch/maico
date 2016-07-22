from datetime import datetime
from pykinect2 import PyKinectV2
from pykinect2.PyKinectV2 import JointType_Count, TrackingState_Tracked, TrackingState_Inferred
from maico.sensor.target import Target


class Human(Target):

    def __init__(self,
                 _id="",
                 k_joints=None,
                 k_joint_points=None,
                 face=None,
                 tracked=True):
        super(Human, self).__init__(_id)        

        self.joints = []
        if k_joints is not None and k_joint_points is not None :
            self.joints = Joint.map_from_kinect_joints(k_joints, k_joint_points)

        self.face = face
        self.tracked = tracked
        
    def location(self):
        if Joint.joints_are_tracked(self.joints, PyKinectV2.JointType_HipRight, PyKinectV2.JointType_HipLeft):
            # take point between hip right & left use camera space to calculate distance
            rl = [self.joints[j] for j in [PyKinectV2.JointType_HipRight, PyKinectV2.JointType_HipLeft]]
            x = (rl[0].x + rl[1].x) / 2
            y = (rl[0].y + rl[1].y) / 2
            z = (rl[0].z + rl[1].z) / 2
            return x, y, z
        else:
            return 0, 0, 0


class Joint(Target):

    def __init__(self):
        self.joint_type = -1  # it depends on Kinect https://github.com/Kinect/PyKinect2/blob/master/pykinect2/PyKinectV2.py#L997
        self.is_tracked = False
        self.is_accurate = False
        self.x = -1
        self.y = -1
        self.z = -1
        self.x_2d = -1  # depth space position
        self.y_2d = -1
    
    @classmethod
    def map_from_kinect_joints(self, joints, joint_points):
        m_joints = {}
        for i in range(JointType_Count):
            mj = Joint()
            j = joints[i]
            jp = joint_points[i]

            mj.joint_type = i

            if j.TrackingState == TrackingState_Tracked:
                mj.is_tracked = True
                mj.is_accurate = True
            elif j.TrackingState == TrackingState_Inferred:
                mj.is_tracked = True

            # caution! x,y,z is meter, but x_2d, y_2d is pixel
            # https://msdn.microsoft.com/ja-jp/library/hh973078.aspx
            mj.x = j.Position.x
            mj.y = j.Position.y
            mj.z = j.Position.z
            mj.x_2d = joint_points[i].x
            mj.y_2d = joint_points[i].y
            
            m_joints[i] = mj

        return m_joints
    
    @classmethod
    def joints_are_tracked(self, joints, *joint_parts):
        tracked = True
        low_confidence = 0
        for jp in joint_parts:
            if jp not in joints:
                tracked = False
                break
            else:
                j = joints[jp]
                if not j.is_tracked:
                    tracked = False
                    break
                elif not j.is_accurate:
                    low_confidence += 1
        
        if len(joint_parts) == low_confidence:
            tracked = False
        
        return tracked
