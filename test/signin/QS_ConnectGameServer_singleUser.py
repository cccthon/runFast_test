#========================================================
#+++++++++++++++++  测试用例信息   ++++++++++++++++
# 用例  ID: QS_ConnectGameServer_001_001
# 用例标题: 连接游戏服务器
# 预置条件: 
# 测试步骤:
#   1.获取用户的mid，sesskey
#   2.发送数据请求服务器
#   3.监听socket响应，检查回调
# 预期结果:
#   1.建立请求服务器成功，返回数据完整无报错。
# 脚本作者: bxf
# 写作日期: 20180412
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
# import QS_client0

sys.path.append("../../lib/runFast")
sys.path.append("../../lib/common")
import QS_pack,QS_runFast,QS_net_tcp,QSCommon
confData = QSCommon.runFastData()
time_stamp = datetime.datetime.now()
userData = QSCommon.runFastData()

class openAndClosePosition(unittest.TestCase):
    def setUp(self):
        '''连接游戏服务器'''

    def test_runFast_1(self):
        serverIP= confData['IP']
        serverPort= confData['Port']
        midID = confData['userAmid']
        sesskey = confData['userAsesskey']
        
        #连接游戏服务器
        self.transfer1 = QS_runFast.connCallBackEvent.callBackEvent(self)
        # print("transfer: ",transfer1)
        self.transfer1.Connect(serverIP, serverPort)

        flag_connect = False
        flag_connect_1996 = False
        con1 = False
        # while True:
        # print(QS_runFast.varList.connectState)
        if QS_runFast.varList.connectState == True:
            if con1 == False:
                print("client1 连接服务")
                connect_srv1 = QS_runFast.connect_srv_1000(midID=midID,sesskey= sesskey)
                self.transfer1.SendPack(connect_srv1.writeOver())
                con1 = True
                #断言连接服务器1000指令返回码（0，成功）
                self.assertEqual(QS_runFast.varList.connected_1000,1)
              
    def tearDown(self):
        #清空测试环境，还原测试数据
        # if QS_runFast.varList.roomID_1996 != 0 or QS_runFast.varList.roomID_1999 != 0:
        #     print("start dissolev_room_6001: ", QS_runFast.varList.roomID_1999)
        #     time.sleep(1)
        #     self.transfer1.SendPack(QS_runFast.dissolev_room_6001().writeOver())
        #     print("end dissolev_room_6001: ", QS_runFast.varList.roomID_1999)
            #客户端2响应离开房间，1同意，2拒绝。
            # time.sleep(5)
            # # dissolevRoom6002 = QS_runFast.dissolev_room_6002(1)
            # self.transfer2.SendPack(QS_runFast.dissolev_room_6002().writeOver())
            # print("end dissolev_room_6001: ", QS_runFast.varList.roomID_1999)
        pass

if __name__ == '__main__':
    unittest.main()


