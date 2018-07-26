#========================================================
#+++++++++++++++++  测试用例信息   ++++++++++++++++
# 用例  ID: QS_ConnectGameServer_001_001
# 用例标题: 两人打牌
# 预置条件: 
# 测试步骤:
# 1.发送数据请求服务器  

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

        # client1_seatNum = 0
        def client1_operater():
            flag_connect = False
            flag_1000 = False
            flag_1001 = False
            flag_1999 = False
            flag_1071 = False
            # flag_6001 = False
            # global client1_seatNum
        

            while True:
                if QS_runFast.varList.connectState == True:
                    # print(QS_runFast.varList.responseCode)
                    if flag_connect == False:
                        #client 1 连接服务
                        connect_srv1 = QS_runFast.connect_srv_1000(midID=userData['userAmid'],sesskey= userData['userAsesskey'])
                        self.transfer1.SendPack(connect_srv1.writeOver())

                        #收到1000登陆后创建房间
                        if 0 == QS_runFast.varList.connected_1000:
                            print("client1 收到1000登陆后创建房间")
                            # flag_1000 = True
                            self.transfer1.SendPack(QS_runFast.create_room_1996().writeOver())
                        # flag_connect = True
                     
                    # if 1001 == QS_runFast.varList.responseCode and flag_1001 == False:
                            print("client1 接收到1001进入房间后准备")
                            self.transfer1.SendPack(QS_runFast.perpare_1006().writeOver())
                        flag_connect = True
                        # flag_1001 = True
                    #获取座位号相关信息
                    if 1071 == QS_runFast.varList.responseCode and flag_1071 == False:
                        # print("client1_1071 获取座位号相关信息")
                        for seat in QS_runFast.varList.seatList_1006:
                            if seat["midID_1006"] == userData['userAmid'] and seat["seatNum_1006"] == QS_runFast.varList.currPlayer_1071:
                                    #开始出牌逻辑
                                    for user in QS_runFast.varList.allCardsList_1035:
                                        # if  seat["seatNum_1006"] == key["seatNum_1035"]:
                                        if user['seatNum'] == QS_runFast.varList.currPlayer_1071:
                                            print("client1_seatNum 的扑克信息: ", user)
                                            print("client1_seatNum 上一个出牌的信息: ", QS_runFast.varList.cardList_1071)
                                            # client1_firstCard = True
                                            print("client1_seatNum: wo yao chupai  le la .................")
                                            #如果1073上一张出牌信息为空，证明当前牌为第一张牌，出最小的即可。QS_runFast.varList.cardList_1071
                                            if QS_runFast.varList.lastPlayCard['cards'] == []:
                                                self.transfer1.SendPack(QS_runFast.play_cards_1072(card=user["pokers"][0]['poker']).writeOver())
                                                print("client1_seatNum: chupai  wancheng . : ", [user["pokers"][0]['poker']])
                                            elif QS_runFast.varList.lastPlayCard['cards'] != []:
                                                lastCardsIndex = QS_runFast.mapping(pokers=QS_runFast.varList.lastPlayCard['cards'],seatNum=QS_runFast.varList.currPlayer_1071)
                                                for poker in user["pokers"]:
                                                    if poker['index'] > lastCardsIndex['pokers'][0]['index']:
                                                        self.transfer1.SendPack(QS_runFast.play_cards_1072(card=poker['poker']).writeOver())
                                                        print("client1_seatNum: chupai  wancheng . : ", [poker['poker']])


        # client2_seatNum = 0
        def client2_operater():
            flag_connect = False
            flag_1000 = False
            flag_1001 = False
            flag_1071 = False
           
            # global client2_seatNum
            while True:
                if QS_runFast.varList.connectState == True:
                    #收到1000登陆后创建房间
                    if flag_connect == False:
                        #client 2 连接服务
                        connect_srv2 = QS_runFast.connect_srv_1000(midID=userData['userBmid'],sesskey= userData['userBsesskey'])
                        self.transfer2.SendPack(connect_srv2.writeOver())
                        #收到1000登陆后加入房间
                        if 0 == QS_runFast.varList.connected_1000:
                            print("client2 收到1996登陆后join房间: ",QS_runFast.varList.roomID_1996)
                            # flag_1000 = True
                            self.transfer2.SendPack(QS_runFast.join_room_1001(roomID=QS_runFast.varList.roomID_1996).writeOver())
                        # flag_connect = True
                    # if 1001 == QS_runFast.varList.responseCode and flag_1001 == False:
                            print("client2 接收到1001进入房间后准备")
                            self.transfer2.SendPack(QS_runFast.perpare_1006().writeOver())
                        flag_connect = True
                        # flag_1001 = True
                        

                    #获取座位号相关信息
                    if 1071 == QS_runFast.varList.responseCode and flag_1071 == False:
                        # print("client2_1071 获取座位号相关信息")
                        for seat in QS_runFast.varList.seatList_1006:
                            if seat["midID_1006"] == userData['userBmid'] and seat["seatNum_1006"] == QS_runFast.varList.currPlayer_1071:
                                    #开始出牌逻辑
                                    for user in QS_runFast.varList.allCardsList_1035:
                                        if user['seatNum'] == QS_runFast.varList.currPlayer_1071:
                                            print("client2_seatNum 监听是否是当前用户先出牌: ", user)
                                            print("client2_seatNum 上一个出牌的信息: ", QS_runFast.varList.cardList_1071)
                                            # client1_firstCard = True
                                            print("client2_seatNum: wo yao chupai  le la .................")
                                            #如果1073上一张出牌信息为空，证明当前牌为第一张牌，出最小的即可。
                                            if QS_runFast.varList.lastPlayCard['cards'] == []:
                                                self.transfer2.SendPack(QS_runFast.play_cards_1072(card=user["pokers"][0]['poker']).writeOver())
                                                print("client2_seatNum: chupai  wancheng . : ", [user["pokers"][0]['poker']])
                                            elif QS_runFast.varList.lastPlayCard['cards'] != []:
                                                lastCardsIndex = QS_runFast.mapping(pokers=QS_runFast.varList.lastPlayCard['cards'],seatNum=QS_runFast.varList.currPlayer_1071)
                                                for poker in user["pokers"]:
                                                    if poker['index'] > lastCardsIndex['pokers'][0]['index']:
                                                        self.transfer2.SendPack(QS_runFast.play_cards_1072(card=poker['poker']).writeOver())
                                                        print("client2_seatNum: chupai  wancheng . : ", [poker['poker']])


        condition = threading.Condition()
        p1 = threading.Thread(name='p1',target=client1_operater)
        # P1线程必须通之后才走P2
        p2 = threading.Thread(name='p2',target=client2_operater)

        p1.start()
        time.sleep(3)
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


# #解散房间
# def dissolev_room_6001():
#     dissolveRoom = QS_pack.pack(6001)

# def client1_operater():
#     connect_srv1 = connect_srv_1000(midID=userData['userAmid'],sesskey= userData['userAsesskey'])
#     self.transfer1.SendPack(connect_srv1.writeOver())
#     status_1000 = False
#     status_1001 = False
#     status_1071 = False
#     status_1069 = False
#     status_1999 = False
#     client1_firstCard = False
#     while True:
#         if connectState == True:
#             #收到1000登陆后创建房间
#             if 1000 == statusCode and status_1000 == False:
#                 print("client1_seatNum 收到1000登陆后创建房间")
#                 status_1000 = True
#                 self.transfer1.SendPack(create_room_1996().writeOver())
#             #接收到1001进入房间后准备
#             if statusCode == 1001:
#                 print("client1_seatNum 接收到1001进入房间后准备: ",statusCode, status_1001)
     
#     condition = threading.Condition()
# p1 = threading.Thread(name='p1',target=client1_operater)


# p1.start()

