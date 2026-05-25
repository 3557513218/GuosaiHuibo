import socket
import time
from threading import Thread, RLock

def str2list(data):
    res = data.split(",")
    tem = []
    for i in res:
        tem.append(float(i))
    return tem

class FrRobot():
    def __init__(self, ip, port):
        self.running = True
        self.__move_flag = -1
        self.__robot_ip = ip
        self.__robot_port = port
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__lock = RLock()

    def __communication(self):
        while self.running:
            time.sleep(2)
            self.__socket.settimeout(3)
            try:
                self.__socket.connect((self.__robot_ip, self.__robot_port))
            except:
                print("robot connect error...")
                continue
            last_time = time.time()
            while self.running:
                _type = 377
                cmd = "GetRobotMotionStatus()"
                msg = f"/f/bIII{52}III{_type}III{len(cmd)}III{cmd}III/b/f"
                flag, recv_data = self.sendAndRecvMsg(self.__socket, msg)
                current_time = time.time()
                if flag:
                    recv_data = recv_data.split("III")
                    move_state = recv_data[4]
                    move_state = move_state.split(",")
                    self.__move_flag = int(move_state[1])
                    last_time = current_time

                if ((current_time - last_time) > 2):
                    break
                time.sleep(0.05)

    def startProcess(self):
        Thread(target=self.__communication, daemon=True).start()
        time.sleep(1)

    def stopProcess(self):
        self.running = False

    @property
    def moveFlag(self):
        return self.__move_flag

    def sendAndRecvMsg(self, socket, msg):
        flag = False
        result = None
        with self.__lock:
            try:
                socket.sendall(msg.encode("utf-8"))
                recv_data = socket.recv(2048).decode("utf-8")
                flag = True
                result = recv_data
            except:
                print("send or recv msg error")
            if (result is None) or (result == b''):
                flag = False
            return flag, result

    def inverseKin(self, x, y, z, rx, ry, rz):
        flag = False
        result = None
        _type = 201
        cmd = f"GetInverseKin(0,{x},{y},{z},{rx},{ry},{rz},-1)"
        msg = f"/f/bIII{52}III{_type}III{len(cmd)}III{cmd}III/b/f"
        recv_flag, recv_data = self.sendAndRecvMsg(self.__socket, msg)
        if not recv_flag:
            return flag, result
        recv_data = recv_data.split("III")
        if recv_data[2] == "500":
            return flag, result

        flag = True
        result = str2list(recv_data[4])
        return flag, result

    def getActualTCPPose(self):
        flag = False
        result = None
        _type = 377
        cmd = "GetActualTCPPose()"
        msg = f"/f/bIII{52}III{_type}III{len(cmd)}III{cmd}III/b/f"
        recv_flag, recv_result = self.sendAndRecvMsg(self.__socket, msg)
        if recv_flag:
            flag = True
            recv_result = recv_result.split("III")
            result = str2list(recv_result[4])
        return flag, result

    def _moveJ(self, x, y, z, rx, ry, rz, tool=0, speed=50, acc=50, ovl=50):
        flag = False
        result = None
        self.__move_flag = -1
        ret_flag, angle = self.inverseKin(x, y, z, rx, ry, rz)
        if not ret_flag:
            return flag, result

        _type = 201
        cmd = f"MoveJ({angle[0]},{angle[1]},{angle[2]},{angle[3]},{angle[4]},{angle[5]},{x},{y},{z},{rx},{ry},{rz},{tool},0,{speed},{acc},{ovl},0,0,0,0,0,0,0,0,0,0,0,0)"
        msg = f"/f/bIII{52}III{_type}III{len(cmd)}III{cmd}III/b/f"
        recv_flag, recv_data = self.sendAndRecvMsg(self.__socket, msg)

        if not recv_flag:
            return flag, result
        recv_data = recv_data.split("III")
        if recv_data[2] == "500":
            return flag, result
        flag = True
        result = recv_data[2]
        return flag, result

    def moveJ(self, x, y, z, rx, ry, rz, tool=0, speed=50, acc=50, ovl=50):
        flag, result = self._moveJ(x, y, z, rx, ry, rz, tool, speed, acc, ovl)
        if not flag:
            self.resetAllError()
        return flag, result

    def _moveL(self, x, y, z, rx, ry, rz, tool=0, speed=50, acc=50, ovl=50):
        flag = False
        result = None
        self.__move_flag = -1
        ret_flag, angle = self.inverseKin(x, y, z, rx, ry, rz)
        if not ret_flag:
            return flag, result
        _type = 203
        cmd = f"MoveL({angle[0]},{angle[1]},{angle[2]},{angle[3]},{angle[4]},{angle[5]},{x},{y},{z},{rx},{ry},{rz},{tool},0,{speed},{acc},{ovl},-1,0,0,0,0,0,0,0,0,0,0,0,0)"
        msg = f"/f/bIII{52}III{_type}III{len(cmd)}III{cmd}III/b/f"
        recv_flag, recv_data = self.sendAndRecvMsg(self.__socket, msg)

        if not recv_flag:
            return flag, result
        recv_data = recv_data.split("III")
        if recv_data[2] == "500":
            return flag, result
        flag = True
        result = recv_data[2]
        return flag, result

    def moveL(self, x, y, z, rx, ry, rz, tool=0, speed=50, acc=50, ovl=50):
        flag, result = self._moveL(x, y, z, rx, ry, rz, tool, speed, acc, ovl)
        if not flag:
            self.resetAllError()
        return flag, result

    def setDO(self, io, state):
        flag = False
        result = None
        _type = 204
        cmd = f"SetDO({io},{state},0)"
        msg = f"/f/bIII{52}III{_type}III{len(cmd)}III{cmd}III/b/f"
        recv_flag, recv_data = self.sendAndRecvMsg(self.__socket, msg)
        if recv_flag:
            recv_data = recv_data.split("III")
            flag = True
            result = recv_data[4]
        return flag, result

    def resetAllError(self):
        flag = False
        result = None
        _type = 107
        cmd = "RESETALLERROR"
        msg = f"/f/bIII{52}III{_type}III{len(cmd)}III{cmd}III/b/f"
        recv_flag, recv_data = self.sendAndRecvMsg(self.__socket, msg)
        if not recv_flag:
            return flag, result
        recv_data = recv_data.split("III")
        if recv_data[3] == "1":
            flag = True
            result = recv_data[3]
        return flag, result

    def stop(self):
        flag = False
        result = None
        _type = 102
        cmd = "STOP"
        msg = f"/f/bIII{52}III{_type}III{len(cmd)}III{cmd}III/b/f"
        recv_flag, recv_data = self.sendAndRecvMsg(self.__socket, msg)
        if not recv_flag:
            return flag, result
        recv_data = recv_data.split("III")
        if recv_data[3] == "1":
            flag = True
            result = recv_data[3]
        return flag, result

if __name__ == '__main__':
    pose=[386.949,-34,350,164.586,2.122,-111.948]
    arm=FrRobot("192.168.8.100",8080)
    arm.startProcess()
    time.sleep(2)
    # arm.moveL(*pose)
    arm.setDO(1,1)
    arm.stopProcess()