import time

import snap7
from threading import Thread,RLock
from snap7.util import *

class Carry():
    def __init__(self,ip):
        self.ip=ip
        self.s7 = snap7.client.Client()
        self.is_connected = False
        self.__dbData_100=None
        self.__send_data = [0, 0.0, 0.0, 0.0, 0, 0, 0, 0]
        self.__magnetic_state=0
        self.__lock=RLock()

    def snap7Connect(self):
        self.s7.connect(self.ip, 0, 1)
        self.is_connected = True

    def snap7UnConnect(self):
        self.s7.disconnect()
        self.is_connected = False

    def writeData(self,db,start,data):
        with self.__lock:
            self.s7.db_write(db, start, data)

    def setBool(self,db,start,bool_index,value):
        boolData = bytearray([0b00000000])
        set_bool(boolData, 0,bool_index,value)
        self.writeData(db,start,boolData)

    def setByte(self,db,start,value):
        byteData=bytearray([0b00000000])
        set_byte(byteData,0,value)

    def setInt(self,db,start,value):
        intData = bytearray(2)
        set_int(intData,0,value)
        self.writeData(db,start,intData)

    def setReal(self,db,start,value):
        realData=bytearray(4)
        set_real(realData,0,value)
        self.writeData(db, start, realData)

    def setString(self,db,start,value):
        stringData=bytearray(len(value)+2)
        set_string(stringData,0,value)
        self.writeData(db, start, stringData)

    def readData(self,db,start,size):
        with self.__lock:
            return self.s7.db_read(db, start, size)

    def readBool(self,db, start,bool_index):
        data=self.readData(db, start,1)
        return get_bool(data,0,bool_index)

    def readInt(self,db,start):
        data = self.readData(db, start, 2)
        return get_int(data,0)

    def readReal(self,db,start):
        data = self.readData(db, start,4)
        return get_real(data, 0)

    def readString(self,db,start):
        data = self.readData(db, start,256)
        return get_string(data, 0)

    def getDbData(self, db, start, size, format='>hhfff'):
        '''
        获取PLC数据
        :param db: DB块编号
        :param start: 起始地址
        :param size: 数据大小(字节）
        :param format: 数据转换
        :return:
        '''
        data = self.readData(db, start, size)
        return struct.unpack(format, data[:])

    def setDbData(self, db, start, data, format=">hfffhhhh"):
        '''
        发送PLC数据
        :param db: DB块编号
        :param start: 起始地址
        :param data: 数据
        :param format: 数据转换
        :return:
        '''
        data_ = struct.pack(format, *data)
        self.writeData(db,start,bytearray(data_))

    def process(self):
        self.runing = True
        if not self.is_connected:
            try:
                self.snap7Connect()
            except:
                print("plc连接错误")
                return
        while self.runing:
            try:
                self.__dbData_100=self.getDbData(100, 0, 16)
            except:
                self.__dbData_100=None
            time.sleep(0.05)

    def getMoveState(self):
        '''
        获取桥吊运动状态
        :return: 0:运动完成;1:运行中
        '''
        return self.__dbData_100[1]

    def getCurrentPose(self):
        '''
        获取桥吊当前坐标
        :return: 桥吊当前坐标
        '''
        return self.__dbData_100[2:]

    def absMove(self,pose:list):
        '''
        桥吊绝对运动
        :param pose: 坐标值
        :return: True:运动成功;False:运动失败
        '''
        self.__send_data=[1,pose[0],pose[1],pose[2],0,0,0,self.__magnetic_state]
        self.setDbData(101,0,self.__send_data,">hfffhhhh")

    def relativeMove(self,pose):
        '''
        桥吊相对运动
        :param pose: 坐标值
        :return: 运动成功;False:运动失败
        '''
        self.__send_data = [2,pose[0],pose[1],pose[2],0,0,0, self.__magnetic_state]
        self.setDbData(101,0,self.__send_data,">hfffhhhh")

    def moveX(self,cmd:int):
        '''
        桥吊X方向运动
        :param cmd:0:停止； 1:前进；2:后退
        :return:True:运动成功;False:运动失败
        '''
        self.setInt(101,14,cmd)


    def moveY(self,cmd:int):
        '''
        桥吊Y方向运动
        :param cmd: 0:停止；1:前进；2:后退
        :return:运动成功;False:运动失败
        '''
        self.setInt(101, 16, cmd)

    def moveZ(self,cmd:int):
        '''
        桥吊z方向运动
        :param cmd: 0:停止；1:前进；2:后退
        :return:运动成功;False:运动失败
        '''
        self.setInt(101, 18, cmd)

    def magnetic(self,cmd:int):
        '''
        电磁铁操作
        :param cmd: 0:停止；1:吸合
        :return:成功;False:失败
        '''
        self.setInt(101, 20, cmd)
        self.__magnetic_state = cmd

    def clearWarn(self):
        '''
        清除报警
        :return:
        '''
        self.setByte(200, 0, 0b1000)
        self.setByte(200, 1, 0b10000)
        self.setByte(200, 1, 0b00000)

    def reset(self):
        '''
        复位
        :return:
        '''
        self.setByte(200, 0, 0b1100)
        self.setByte(200, 1, 0b1001)
        self.setByte(200, 1, 0b0000)

    def moveDone(self):
        '''
        桥吊运动完成(阻塞)
        :return:
        '''
        time.sleep(0.01)
        while self.runing:
            if self.getMoveState() == 0:
                break
            time.sleep(0.1)

    def startProcess(self):
        Thread(target=self.process,daemon=True).start()
        time.sleep(1)

    def stopProcess(self):
        self.runing=False
        if self.is_connected:
            self.snap7UnConnect()

    def __del__(self):
        self.stopProcess()




if __name__ == '__main__':
    carry=Carry("192.168.8.50")
    carry.startProcess()
    time.sleep(1)
    carry.absMove([100,0,0])
    # print(carry.reset())
    # carry.moveX(0)
    # time.sleep(3)
    # carry.moveX(0)



