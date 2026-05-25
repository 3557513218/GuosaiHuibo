#!/usr/bin/env python3
import os
import rospy
from std_msgs.msg import String
from kilox_nav_msgs.srv import ChassisControlModeService, ChassisControlModeServiceRequest
from geometry_msgs.msg import Twist
from kilox_robot_manager.srv import MoveToPoseService, MoveToPoseServiceRequest
from realsensehb.srv import RealsenseSrv, RealsenseSrvRequest

from flask import Flask, request, jsonify
from flask_cors import CORS
from gevent import pywsgi
from threading import RLock
import json

app = Flask(__name__)
CORS(app)


class RosNode():
    def __init__(self):
        self.__navigation_state = "free"
        self.__speed_pub = rospy.Publisher("/chassis_twist", Twist, queue_size=1)
        self.__navigation_state_sub = rospy.Subscriber("/navigation_state", String, self.__navigation_state_callback,
                                                       queue_size=1)
        self.__mode_change_client = rospy.ServiceProxy("/chassis_control_mode_service", ChassisControlModeService)
        self.__move_to_pose_client = rospy.ServiceProxy("/move_to_pose_service", MoveToPoseService)
        self.__realsense_client = rospy.ServiceProxy("/realsenseHb", RealsenseSrv)

    def moveToPose(self, x, y, yaw, cmd="new"):
        errorCode = 0
        req = MoveToPoseServiceRequest()
        req.task_uid = 1
        req.cmd = cmd
        req.pose_target.x = x
        req.pose_target.y = y
        req.pose_target.yaw = yaw
        try:
            resp = self.__move_to_pose_client.call(req)
            if resp.message_res == 'SKIP':
                errorCode = 2
        except Exception as e:
            rospy.logerr(str(e))
            errorCode = 1
        return errorCode

    def modelChange(self, model):
        errorCode = 0
        req = ChassisControlModeServiceRequest()
        req.cmd_attribute = "Set"
        req.manual_enable = model
        try:
            self.__mode_change_client.call(req)
        except Exception as e:
            rospy.logerr(str(e))
            errorCode = 1
        return errorCode

    def __navigation_state_callback(self, msg):
        self.__navigation_state = msg.data

    @property
    def navigationState(self):
        return self.__navigation_state

    def manualMove(self, speed_x, speed_yaw):
        speed = Twist()
        speed.linear.x = speed_x
        speed.angular.z = speed_yaw
        self.__speed_pub.publish(speed)

    def realsense(self, cmd):
        errorCode = 0
        result = None
        req = RealsenseSrvRequest()
        req.type = cmd
        try:
            result = self.__realsense_client.call(req)
        except Exception as e:
            print(e)
            rospy.logerr(str(e))
            errorCode = 1
        return errorCode, result


@app.route("/realsense", methods=["GET"])
def realsense():
    ret = {"error_code": 0, "result": None, "reason": ""}
    cmd = request.values.get("cmd")
    if cmd is None:
        ret["error_code"] = 1
        ret["reason"] = "param is None"
        return jsonify(ret)
    errorCode, result = node.realsense(int(cmd))
    if errorCode == 0:
        result = json.loads(result.ret)
        ret["result"] = result["imgPath"]
    else:
        ret["error_code"] = 2
        ret["reason"] = "The calling interface is incorrect"
    return jsonify(ret)


@app.route("/moveToPose", methods=["GET"])
def moveToPose():
    cmd = request.values.get("cmd")
    x = request.values.get("x")
    y = request.values.get("y")
    yaw = request.values.get("yaw")
    ret = {"error_code": 0, "result": None, "reason": ""}
    if (cmd is None) or (x is None) or (y is None) or (yaw is None):
        ret["error_code"] = 1
        ret["reason"] = "param is None"
        return jsonify(ret)
    errorCode = node.moveToPose(float(x), float(y), float(yaw), cmd)
    if errorCode == 0:
        ret["result"] = "success"
    else:
        ret["error_code"] = 2
        ret["reason"] = "The calling interface is incorrect"
    return jsonify(ret)


@app.route("/modelChange", methods=["GET"])
def modelChange():
    ret = {"error_code": 0, "result": None, "reason": ""}
    model = request.values.get("model")
    if model is None:
        ret["error_code"] = 1
        ret["reason"] = "param is None"
        return jsonify(ret)
    errorCode = node.modelChange(model)
    if errorCode == 0:
        ret["result"] = "success"
    else:
        ret["error_code"] = 2
        ret["reason"] = "The calling interface is incorrect"
    return jsonify(ret)


@app.route("/getNavigationState", methods=["GET"])
def getNavigationState():
    ret = {"error_code": 0, "result": None, "reason": ""}
    ret["result"] = node.navigationState
    return jsonify(ret)


@app.route("/manualMove", methods=["GET"])
def manualMove():
    ret = {"error_code": 0, "result": None, "reason": ""}
    speed_x = request.args.get("x")
    speed_yaw = request.args.get("yaw")
    if (speed_x is None) or (speed_yaw is None):
        ret["error_code"] = 1
        ret["reason"] = "param error"
    else:
        node.manualMove(float(speed_x), float(speed_yaw))
    return ret


if __name__ == "__main__":
    rospy.init_node("my_flask")
    node = RosNode()
    # app.run(host="0.0.0.0",port=5000)
    server = pywsgi.WSGIServer(("0.0.0.0", 5001), app)
    server.serve_forever()