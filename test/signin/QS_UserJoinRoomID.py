#========================================================
#+++++++++++++++++  测试用例信息   ++++++++++++++++
# 用例  ID: QS_userJoinRoomID_001_001
# 用例标题: 用户加入房间
# 预置条件: userA已创建房间
# 测试步骤:
# 1.A用户创建房间；
# 2.B用户加入房间。 

# 预期结果:
#   1.B用户成功加入房间。
# 脚本作者: bxf
# 写作日期: 20180428
#=========================================================
import requests
import json
import time
import sys
import yaml
import os
import unittest
import socket
import asyncio
import re
import threading
import datetime

sys.path.append("../../lib/runFast")
sys.path.append("../../lib/common")
sys.path.append("../../conf/runFast")
import QS_pack,QS_runFast,QS_net_tcp,QSCommon
confData = QSCommon.runFastData()
time_stamp = datetime.datetime.now()
userData = QSCommon.runFastData()

class openAndClosePosition(unittest.TestCase):
    def setUp(self):
        pass

    def test_runFast_1(self):
        #登录加载

        #实例客户端1的连接
        self.transfer1 = QS_runFast.connCallBackEvent.callBackEvent(self)
        self.transfer1.Connect(userData['IP'], userData['Port'])
        #实例客户端2的连接
        self.transfer2 = QS_runFast.connCallBackEvent.callBackEvent(self)
        self.transfer2.Connect(userData['IP'], userData['Port'])

        def client1_operater():
            flag_connect1 = False
            flag_connect2 = False
            flag_1000 = False
            flag_1996 = False

            while True:
                if QS_runFast.varList.connectState == True:
                    # print(QS_runFast.varList.responseCode)
                    if flag_connect1 == False:
                        #client 1 连接服务
                        connect_srv1 = QS_runFast.connect_srv_1000(midID=userData['userAmid'],sesskey= userData['userAsesskey'])
                        self.transfer1.SendPack(connect_srv1.writeOver())
                        flag_connect1 = True
                        #收到1000登陆后创建房间
                        if 0 == QS_runFast.varList.connected_1000 and flag_1996 == False:
                            print("client1 收到1000登陆后创建房间")
                            # flag_1000 = True
                            self.transfer1.SendPack(QS_runFast.create_room_1996().writeOver())
                            flag_1996 = True
          

        def client2_operater():
            flag_connect2 = False
            flag_1000 = False
            flag_1001 = False
            flag_1996 = False
           
            # global client2_seatNum
            while True:
                if QS_runFast.varList.connectState == True:
                    #收到1000登陆后创建房间
                    if flag_connect2 == False:
                        print("client2 收到1000登陆后连接")
                        #client 2 连接服务
                        connect_srv2 = QS_runFast.connect_srv_1000(midID=userData['userBmid'],sesskey= userData['userBsesskey'])
                        self.transfer2.SendPack(connect_srv2.writeOver())
                        flag_connect2 = True
                        #收到1000登陆后加入房间
                        if 0 == QS_runFast.varList.connected_1000 and flag_1996 == False:
                            print("client2 收到1996登陆后join房间: ",QS_runFast.varList.roomID_1996)
                            self.transfer2.SendPack(QS_runFast.join_room_1001(roomID=QS_runFast.varList.roomID_1996).writeOver())
                            flag_1996 = True


        condition = threading.Condition()
        p1 = threading.Thread(name='p1',target=client1_operater)
        # P1线程必须通之后才走P2
        p2 = threading.Thread(name='p2',target=client2_operater)

        p1.start()
        time.sleep(5)
        p2.start()

    def tearDown(self):
        #客户端1申请离开房间
        if QS_runFast.varList.roomID_1996 != 0 or QS_runFast.varList.roomID_1999 != 0:
            print("start dissolev_room_6001: ", QS_runFast.varList.roomID_1999)
            time.sleep(5)
            self.transfer1.SendPack(QS_runFast.dissolev_room_6001().writeOver())
            print("end dissolev_room_6001: ", QS_runFast.varList.roomID_1999)
            #客户端2响应离开房间，1同意，2拒绝。
            time.sleep(5)
            # dissolevRoom6002 = QS_runFast.dissolev_room_6002(1)
            self.transfer2.SendPack(QS_runFast.dissolev_room_6002().writeOver())
            print("end dissolev_room_6001: ", QS_runFast.varList.roomID_1999)
 

if __name__ == '__main__':
    unittest.main()
