import roslibpy
import time
import math
from roslib.utils import try_except


class RosBase:
    def __init__(self, host, port):
        self.unsubscribe_flag = 0
        self.pub_flag = False
        self.ros_data = {}
        self.distance = -0.15
        self.ros = roslibpy.Ros(host=host, port=port)

    @try_except
    def rosConnect(self):
        self.ros.run(timeout=5)

    def rosReConnect(self):
        self.ros.connect()

    def rosUnConnect(self):
        self.ros.close()

    def rosClose(self):
        self.ros.terminate()

    def topicPub(self, topic_name, topic_type, topic_data, pub_num=0, pub_frequency=10):
        talker = roslibpy.Topic(self.ros, topic_name, topic_type)
        if pub_num == 0:
            while self.ros.is_connected:
                talker.publish(roslibpy.Message(topic_data))
                time.sleep(1 / pub_frequency)
                if self.pub_flag:
                    break
        elif pub_num != 0:
            i = 1
            while i <= pub_num and self.ros.is_connected:
                talker.publish(roslibpy.Message(topic_data))
                time.sleep(1 / pub_frequency)
                i = i + 1

    def topicSub(self, topic_name, topic_type, topic_callback=None):
        listener = roslibpy.Topic(self.ros, topic_name, topic_type)
        listener.subscribe(topic_callback)
        while self.ros.is_connected:
            if self.unsubscribe_flag == 1:
                self.unsubscribe_flag = 0
                listener.unsubscribe()
                break

    def subCallback(self, data, name, cmd, key=None, value=None):
        if cmd == 0:
            self.ros_data[name] = data
            print(data)
        elif cmd == 1:
            if data[key] == value:
                self.ros_data[name] = data
                self.unsubscribe_flag = 1
        elif cmd == 2:
            if data:
                # print(data)
                self.ros_data[name] = data
                self.unsubscribe_flag = 1

    def serverClient(self, server_name, server_type, server_data):
        if self.ros.is_connected:
            service = roslibpy.Service(self.ros, server_name, server_type)
            request = roslibpy.ServiceRequest(server_data)
            result = service.call(request)
            return result

    def modelChange(self, model):
        server_name = "/chassis_control_mode_service"
        server_type = "kilox_nav_msgs/ChassisControlModeService"
        server_data = {
            "cmd_attribute": "Set",
            "manual_enable": model
        }
        return self.serverClient(server_name, server_type, server_data)

    def chassisManualCmdVel(self, m_x, m_raw):
        topic_name = '/chassis_twist'
        topic_type = 'geometry_msgs/Twist'
        topic_data = {
            "linear": {
                "x": m_x,
                "y": 0,
                "z": 0
            },
            "angular": {
                "x": 0,
                "y": 0,
                "z": m_raw
            }
        }
        self.topicPub(topic_name, topic_type, topic_data, pub_num=1)

    def moveToPose(self, pose, cmd="new"):
        server_name = '/move_to_pose_service'
        server_type = 'kilox_robot_manager/MoveToPoseService'
        server_data = {
            "task_uid": "1",
            "cmd": cmd,
            "pose_target": {"x": pose[0], "y": pose[1], "z": 0.0, "roll": 0.0, "pitch": 0.0, "yaw": pose[2]}
        }
        self.modelChange(False)
        time.sleep(0.5)
        result = self.serverClient(server_name, server_type, server_data)
        print(result)
        if result["message_res"] == 'SKIP':
            self.chassisManualCmdVel(0, -0.1)
            time.sleep(5)
            self.chassisManualCmdVel(0, 0)
            self.modelChange(False)
            time.sleep(0.5)
            if self.serverClient(server_name, server_type, server_data)["message_res"] == '':
                self.navigationState()
        elif result["message_res"] == '':
            self.navigationState()
        else:
            return -1

    def moveToPoseC(self, pose, param):
        if self.moveToPose((pose[0] + param[0], pose[1] + param[1], pose[2])) != -1:
            self.modelChange(True)
            time.sleep(0.5)
            while True:
                self.chassisStatePose()
                time.sleep(1)
                result = self.ros_data["pose_data"]
                vec = (pose[0] - result["x"], pose[1] - result["y"])
                dis = (vec[0] ** 2 + vec[1] ** 2) ** 0.5
                if (vec[0] > 0 and vec[1] > 0) or (vec[0] < 0 and vec[1] > 0):
                    angle = math.acos(vec[0] / dis)
                else:
                    angle = -math.acos(vec[0] / dis)
                self.angleC(angle)
                self.odomC(dis)
                self.angleC(pose[2])
                self.chassisStatePose()
                time.sleep(1)
                res = self.ros_data["pose_data"]
                if abs(res["x"] - pose[0]) > param[2] or abs(res["y"] - pose[1]) > param[3]:
                    self.odomC(self.distance)
                else:
                    if param[4] != 0:
                        self.odomC(param[4])
                    print("到达目标点位")
                    return True
        else:
            return False

    def navigationState(self):
        topic_name = '/navigation_state'
        topic_type = 'std_msgs/String'
        self.unsubscribe_flag = 0
        self.topicSub(topic_name, topic_type,
                      topic_callback=lambda data: self.subCallback(data, 'nav_state', 1, "data", "success"))

    def io606Out(self, port, cmd):
        server_name = "/io606_out"
        server_type = "kilox_robot_manager/io606_out"
        server_data = {
            "port": port,
            "cmd": cmd
        }
        return self.serverClient(server_name, server_type, server_data)

    def chassisStatePose(self):
        topic_name = '/chassis_state_pose'
        topic_type = 'kilox_nav_msgs/Pose3D'
        self.topicSub(topic_name, topic_type, topic_callback=lambda data: self.subCallback(data, 'pose_data', 2))

    def angleC(self, yaw):
        server_name = "/angle_c"
        server_type = "srai/Float32"
        server_data = {
            "data": yaw,
        }
        return self.serverClient(server_name, server_type, server_data)

    def odomC(self, dis):
        server_name = "/odom_c"
        server_type = "srai/Float32"
        server_data = {
            "data": dis,
        }
        return self.serverClient(server_name, server_type, server_data)

    def realsense(self, data):
        server_name = "/realsense_photograph"
        server_type = "srai/Camera"
        server_data = {
            "picture_name": data
        }
        return self.serverClient(server_name, server_type, server_data)

    def asrResult(self):
        topic_name = '/asr_result'
        topic_type = 'std_msgs/String'
        self.unsubscribe_flag = 0
        self.topicSub(topic_name, topic_type,
                      topic_callback=lambda data: self.subCallback(data, 'asr_data', 2, "data", "success"))

    def voiceTTS(self, str):
        topic_name = "/tts_text"
        topic_type = "std_msgs/String"
        topic_data = {
            "data": str
        }
        self.topicPub(topic_name, topic_type, topic_data, pub_num=1, pub_frequency=1)

    def personInfo(self, cmd, name=None):
        topic_name = '/person_info'
        topic_type = 'srai/Person'
        self.topicSub(topic_name, topic_type,
                      topic_callback=lambda data: self.subCallback(data, 'person_data', cmd, 'name', name))

    def envInfo(self):
        topic_name = '/env_status'
        topic_type = 'kilox_robot_manager/env_status'
        self.topicSub(topic_name, topic_type,
                      topic_callback=lambda data: self.subCallback(data, 'env_data', 2))

    def clamp(self,cmd):
        server_name = "/clamp"
        server_type = "std_srvs/SetBool"
        server_data = {
            "data": cmd
        }
        return self.serverClient(server_name, server_type, server_data)

    # def hkCamera(self, cmd, yaw=0,pitch=0,path=""):
    #     server_name = "/hk_camera"
    #     server_type = "kilox_pantilt/pantilt_cmd"
    #     server_data = {
    #         "cmd": {"command_id":'',
    #                 "type": {"data":cmd},
    #                 "z":{"data":0},
    #                 "yaw":{"data":yaw},
    #                 "pitch":{"data":pitch},
    #                 "zoom":{"data":0},
    #                 "focus_visual":{"data":0},
    #                 "focus_thermal":{"data":0},
    #                 "iris":{"data":0},
    #                 "speed":{"data":0},
    #                 "path":{"data":path},
    #                 "duration":{"data":0},
    #                 "path_t":{"data":''}
    #                 }
    #     }
    #     return self.serverClient(server_name, server_type, server_data)

    @try_except
    def setSafety(self, cmd, target, status):
        server_name = "/set_safety"
        server_type = "kilox_robot_manager/set_safety"
        server_data = {
            "cmd": cmd,
            "target": target,
            "status": status
        }
        res=self.serverClient(server_name, server_type, server_data)
        if res['status']=="":
            return -1
        return res

    # def __del__(self):
    #     self.rosUnConnect()

if __name__ == '__main__':
    agv=RosBase("192.168.8.11",51848)
    agv.rosConnect()
    print(agv.modelChange(False))