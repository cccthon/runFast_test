#========================================================
#+++++++++++++++++  测试用例信息   ++++++++++++++++
# 用例  ID: FM_TradeOnLine_open_001_001
# 用例标题: 请求服务器
# 预置条件: 
# 测试步骤:
#   1.建立PHP链接，获取json参数
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
import copy
# import QS_client0

sys.path.append("../../lib/runFast")
sys.path.append("../../lib/common")
sys.path.append("../../conf/runFast")
import QS_pack,QS_runFast,QS_net_tcp,QSCommon
confData = QSCommon.runFastData()
time_stamp = datetime.datetime.now()

#######################################################################
#################### PHP 相关方法封装 ################################
#登陆
def signin(url, headers="", interfaceName="", printLogs=0):
    res = Http.get(url, headers=headers, interfaceName=interfaceName, logs=printLogs)
    return res
    
#加载
def signinLoad(url, headers="", interfaceName="", printLogs=0):
    res = Http.get(url, headers=headers, interfaceName=interfaceName, logs=printLogs),
    return res

########################################################################
######################## 对牌进行规整为字典 ############################
#映射值
def mapping(pokers=[],seatNum=0):
  dicting3 = []
  mapping = {'seatNum': seatNum,'indexList':[],'bomList':[],'pokers':{}}
  dicting = {}
  indexs = []
  bomList = []
  bomIndex = []
  bom = {}
  #映射表
  zdpai = dict([('3', 0),('4', 1),('5', 2),('6', 3),('7', 4),('8', 5),('9', 6),('T', 7),('J', 8),('Q', 9),('K', 10),('A', 11),('2', 12)])
  for poker in pokers:
      for k,v in zdpai.items():
        if poker[0] in k:
          dicting2 = copy.deepcopy(dicting)
          dicting2["poker"],dicting2["index"]=poker,v
          dicting3.append(dicting2)
          #排序
          sortMap = sorted(dicting3, key=lambda e: e.__getitem__('index'))
          mapping["pokers"]=sortMap
  #检查是否有炸弹,获取炸弹的索引
  for i in mapping["pokers"]:
    indexs.append(i['index'])
    # index 的长度等于4即为炸弹
    if indexs.count(i['index']) == 4:
      bomIndex.append(i['index'])
  #将炸弹数据规整加入dict
  for index in bomIndex:
    bomPokers = []
    for j in mapping["pokers"]:
      if j["index"] == index:
        bomPokers.append(j['poker'])
        bom2 = copy.deepcopy(bom)
    bom2["index"],bom2["boms"]=index,bomPokers
    bomList.append(bom2)
  mapping["bomList"],mapping['indexList']=bomList,indexs
  return mapping
########################################################################
# #以下数据调试用
# #客户端1的牌
# client1 = ['Qh', '6c', '6s', '3s', '9c', 'As', '6s', 'Td', '9d', '9s', 'Ad', '6d', '3c', '3h', 'Tc', '3d']
# #客户端2的牌
# client2 = ['Jh', '7c', '3s', '9s', '5c', '4s', 'Ks', '8d', '7d', '5s', 'Ac', '2d', '7s', 'Th', 'Tc', 'Ad']
# #映射后的列表
# c1 = mapping(pokers=client1)
# c2 = mapping(pokers=client2)
# print("c1: ", c1)
# print("c2: ", c2)



##########################################################################
####################### Run Fast 相关方法封装 ############################
##########################################################################

####################### Run Fast 指令发送相关方法########################
#发送登陆，1000是指令固定。(需要断言int32 错误码等于0登陆成功。)
def connect_srv_1000(midID='',sesskey=''):
    connect = QS_pack.pack(1000)
    connect.writeINT32(int(midID))#服务器给的mid
    connect.writeString(sesskey)#sesskey
    connect.writeINT32(101)#可以固定
    connect.writeINT32(1300)#游戏类型固定
    return connect


# #开房，1996是指令固定。
# #刚开始创建房间参数 （）
def create_room_1996():
    createRoom = QS_pack.pack(1996)
    createRoom.writeString("1")#固定值
    createRoom.writeString('A1')#房间类型
    createRoom.writeINT32(0)#没有值，但不能为空
    createRoom.writeINT32(0)#1:房间选项（1:显示牌数 2:首局黑桃3出牌 4:红桃十抓鸟 8:快速 16:可以四带二 32:可以四带三 64:炸弹不可拆 128:3A是炸弹。。。。。。
    createRoom.writeINT32(2)#玩家人数（2-3）
    createRoom.writeINT32(0)#是否是代理商支付房卡（1:代理商支付房卡）
    createRoom.writeINT32(0)#俱乐部ID
    createRoom.writeString("")#俱乐部名称
    createRoom.writeINT32(0)#没有值，但不能为空
    createRoom.writeINT32(1)#是否立即加入房间。（1:加入房间）
    createRoom.writeString("")#VIP
    return createRoom


#申请解散房间
def dissolev_room_6001():
    dissolveRoom6001 = QS_pack.pack(6001)
    return dissolveRoom6001
    # dissolveRoom6001.data.getReadData()

#解散房间投票（1:同意 2:拒绝）
def dissolev_room_6002():
    dissolveRoom6002 = QS_pack.pack(6002)
    dissolveRoom6002.writeINT32(1)
    return dissolveRoom6002

# userA加入QS_client0房间
def join_room_1001(roomID=''):
    user = QS_pack.pack(1001)
    user.writeINT32(roomID)
    user.writeString('A1')
    user.writeINT32(0)
    return user

#各玩家加入房间后点击准备
def perpare_1006():
    perpare = QS_pack.pack(1006)
    return perpare

#客户端发送出牌给服务器
def play_cards_1072(card=[]):
    play_cards = QS_pack.pack(1072)
    play_cards.writeINT32(len([card]))
    play_cards.writeString(card)
    return play_cards

##后面的在这加


###############################################################################
######################### Run Fast 回调方法封装 ##############################
class varList():
    roomID_1996 = 0
    roomID_1999 = 0
    responseCode = 0
    currPlayer_1071 = 0
    cardList_1071 = []
    seatList_1006 = []
    cardList_1035 = []
    cardDict_1035 = {}
    allCardsList_1035 = []
    midID_1006 = 0
    seatNum_1006 = 0
    seatNum_1035 = 0
    cards_1035 = []
    transfer = ''
    connectState = False
    connected_1000 = 0
    client1_seatNum = 0
    client2_seatNum = 0
    cards_1083 = []
    lastPlayCard = {"seatNum":0,"cards":[]}

#封装callBack事件
class connCallBackEvent():
    def callBackEvent(self):
        #接收回调
        def recvCallBack(data):
            # print("返回的数据类型: ",type(d ata))
            # print("data getReadData: ", data.getReadData())
            varList.responseCode =  data.getCmd()
            print( "服务端响应命令:", varList.responseCode )

            if varList.responseCode == 1000:
                connected_1000 = data.readINT32()
                print(varList.responseCode,": 连接服务器接收错误码为:", connected_1000)#错误码为0表示成功
                print("")
                #开房，1996是指令固定。
                #刚开始创建房间参数 （）
                # print("数据:",data.readBuffer)

            elif varList.responseCode == 1996:

                print(varList.responseCode,": 创建房间接收错误码为:", data.readINT32())#错误码为0表示成功
                varList.roomID_1996 = data.readINT32()
                # roomID_1996 = data.readINT32()
                print("")

                print("打印房间号>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>：", varList.roomID_1996)
                # QS_net_tcp.printRecvData( data.readBuffer )
                # print("数据:",data.readBuffer)
                #需要判断一下，当返回的int32为0时，走创建房间，否则进入房间。
            elif data.getCmd() == 1999:
                varList.roomID_1999 = data.readINT32()
                print("房间号：",varList.roomID_1999)
                print("重新连接 - 房间号：",varList.roomID_1999)
                print("类型",data.readString() )
                print("***************************************************************************")

            elif varList.responseCode == 1001:
                print(varList.responseCode,": 加入房间的返回码为：",data.readINT32())
                print(varList.responseCode,": 加入房间未知",data.readINT32())
                print(varList.responseCode,": 加入房间剩余局数：",data.readINT32())
                print(varList.responseCode,": 加入房间房间的总局数：",data.readINT32())
                print(varList.responseCode,": 加入房间房间的ID：",data.readINT32())
                print(varList.responseCode,": 加入房间房间的类型：",data.readString())
                print(varList.responseCode,": 加入房间玩法：",data.readINT32())
                print(varList.responseCode,": 加入房间首局是否黑桃3先出：",data.readINT32())
                # print("目前房间总人数：",data.readINT32())
                # print("俱乐部ID：",data.readINT32())
                # print("俱乐部名称",data.readString())
                # print("未知",data.readINT32())
                # print("vip",data.readString())
                print("***************************************************************************")

            #服务器返回给client的房间信息
            # elif data.getCmd() == 1002:
            elif varList.responseCode == 1002:
                print(varList.responseCode,"：加入房间后，服务器返回的玩家人数: ", data.readINT32())
                print(varList.responseCode,"：加入房间后，服务器返回的座位号: ", data.readINT32())
                print(varList.responseCode,"：加入房间后，服务器返回的玩家MID: ", data.readINT32())
                print(varList.responseCode,"：加入房间后，服务器返回的玩家GP: ", data.readINT32())
                print(varList.responseCode,"：加入房间后，服务器返回的玩家性别: ", data.readINT32())
                print(varList.responseCode,"：加入房间后，服务器返回的玩家名称: ", data.readString())
                print(varList.responseCode,"：加入房间后，服务器返回的头像地址: ", data.readString())
                print(varList.responseCode,"：加入房间后，服务器返回的VIP: ", data.readINT32())
                print(varList.responseCode,"：加入房间后，服务器返回的金币数量: ", data.readLONG64())
                print(varList.responseCode,"：加入房间后，服务器返回的积分: ", data.readLONG64())
                print(varList.responseCode,"：加入房间后，服务器返回的ip: ", data.readString())

            #通知解散房间
            elif varList.responseCode == 1070:
                print(varList.responseCode,"：通知解散房间MID",data.readINT32())
                # print(varList.responseCode,"：通知解散房间的roomID",data.readINT32())
                print("")

            #同意解散房间
            elif varList.responseCode == 6002:
                print(varList.responseCode,"：解散房间返回的错误码",data.readINT32())
                print("")
                print("***************************************************************************")

            # #拒绝解散房间
            # elif arList.responseCode == 6002:
            #     print("解散房间",data.readINT32(2))
            #     print("")

            #离开房间
            elif data.getCmd() == 1004:
                print(varList.responseCode,"：离开房间返回的用户MID：", data.readINT32())
                print(varList.responseCode,"：离开房间返回的错误码(0：成功)：", data.readINT32())





            elif varList.responseCode == 1006:
                varList.midID_1006 = data.readINT32()
                print(varList.responseCode,"：准备后返回的用户MID：", varList.midID_1006)
                varList.seatNum_1006 = data.readINT32()
                print(varList.responseCode,"：准备后返回的座位号：", varList.seatNum_1006)
                print(varList.responseCode,"：准备后服务器返回的错误码：",data.readINT32())
                varList.seatList_1006.append({"midID_1006":varList.midID_1006,"seatNum_1006": varList.seatNum_1006})
                print(varList.responseCode,"：准备后服务器返回的seatNum：", varList.seatList_1006)
            # #所有玩家都准备后通知第一个出牌的人
            elif varList.responseCode == 1069:
                # print(varList.responseCode,":unknow.：")
                # currPlayer_1071 = data.readINT32()
                print(varList.responseCode,": 所有玩家都准备后通知第一个出牌的人的坐位号：", data.readINT32())

            #玩家准备后用户离开
                print("***************************************************************************")
            elif varList.responseCode == 1076:
                print(varList.responseCode,"：玩家准备后用户离开坐位号：",data.readINT32())
                print(varList.responseCode,"：玩家准备后用户离开返回的错误码：",data.readINT32())

                

            #断线后重发手牌
            elif varList.responseCode == 1083:
                card_recount =  data.readINT32()
                print(varList.responseCode,"：断线后重发手牌的数量：",card_recount)
                cards_1083 = []
                for card in range(card_recount):
                    cards_1083.append(data.readString())
                # varList.cards = varList.cards_1083
                print(varList.responseCode,"：断线后游戏开始发牌的[]牌面: ", cards_1083) 
                # allCards1083 = []
                # for 1083poker in range(cards_1083):
                # print(varList.responseCode,"断线后重发手牌的牌面：",data.readString())
            
            # # #通知解散房间
            # elif data.getCmd() == 1070:
            #     print("通知解散房间的用户MID：",data.readINT32())
            #     print("通知解散房间的房间ID：",data.readINT32())


            #游戏开始
                print("**************************************************************************")
            elif varList.responseCode == 1008:
                # print("1008",data.getReadData())
                print(varList.responseCode,"：准备后游戏开始返回码为：", data.readINT32())
                print(varList.responseCode,"：准备后游戏开始目前剩余的局数:", data.readINT32())
                print(varList.responseCode,"：准备后游戏开始房间的总局数:", data.readINT32())

                print("**************************************************************************")
            elif varList.responseCode == 1035:
                card_count =  data.readINT32()
                print(varList.responseCode,"：游戏开始发牌的数量:", card_count)
                cards = []
                for card in range(card_count):
                    cards.append(data.readString())
                print(varList.responseCode,"：游戏开始发牌的[]牌面: ", cards)  
                seatNum_1035 = data.readINT32()
                print(varList.responseCode,"：游戏开始显示的坐位号:", seatNum_1035)
                varList.cardList_1035.append({"seatNum_1035": seatNum_1035, "cards": cards})
                print("cardList: ",varList.cardList_1035)
                allCardsList = []
                for j in varList.cardList_1035:
                    varList.cardDict_1035 = mapping(pokers=j['cards'],seatNum=j['seatNum_1035'])
                    # print("cardDict: ",varList.cardDict_1035)
                    allCardsList.append(varList.cardDict_1035)
                #去重
                for i in allCardsList:
                  if i not in varList.allCardsList_1035:
                    varList.allCardsList_1035.append(i)
                print("所有人的牌规整后的集合: ", varList.allCardsList_1035)
                print("***************************************************************************") 

            ##客户端发给服务器出牌信息
            elif varList.responseCode == 1072:
                print(varList.responseCode,"：服务器返回(座位号)：",data.readINT32())
                print(varList.responseCode,"：服务器返回(错误码)：",data.readINT32())
                # # playCards = data.readINT32()
                # if i in range(playCards)
                #     print(playCards)

            
            elif varList.responseCode == 1071:
                varList.currPlayer_1071 = data.readINT32()
                print(varList.responseCode, ": 当前玩家出牌的座位号：", varList.currPlayer_1071)
                print(varList.responseCode, ": 下一家牌是否报单：", data.readINT32())
                print(varList.responseCode, ": 当前玩家是否要不起（1:要不起 0:出牌）：", data.readINT32())
                print(varList.responseCode, ": 最近一次出牌座位号：", data.readINT32())
                varList.card_count1 =  data.readINT32()
                print(varList.responseCode, ": 打出牌的数量", varList.card_count1)
                cardList = []
                for card in range(varList.card_count1):
                    cardList.append(data.readString())
                #去重
                for i in cardList:
                    if i not in varList.cardList_1071:
                        varList.cardList_1071.append(i)
                print(varList.responseCode,"[]牌面:" , varList.cardList_1071)
                print(varList.responseCode, ": 牌的类型（-1:无效、0:单张、1:一对、2:连队、3:三个、4:三带一、5:顺子、6:飞机、8:炸弹、10:四带二、12:四带三）")
            
            #服务器返回给客户端出的牌
            elif varList.responseCode == 1073:
                seatNum_1073 = data.readINT32()
                print(varList.responseCode, ": 出牌的座位号：", seatNum_1073)
                card_count1 =  data.readINT32()
                print(varList.responseCode, ": 出牌的数量：", card_count1)
                cardList_1073 = []
                for card in range(card_count1):
                    cardList_1073.append(data.readString())
                print(varList.responseCode,"：出牌的[]牌面: ", cardList_1073) 
                print(varList.responseCode, ": 牌型：", data.readINT32())#牌型（-1:无效、0:单张、1:一对、2:连队、3:三个、4:三带一、5:顺子、6:飞机、8:炸弹、10:四带二、12:四带三）
                print(varList.responseCode, ": 手上剩余的牌数量: ", data.readINT32())
                varList.lastPlayCard["seatNum"],varList.lastPlayCard["cards"] = seatNum_1073, cardList_1073
                print("lastPlay cards: ",varList.lastPlayCard)
            elif varList.responseCode == 1078:
                
                seat_number = data.readINT32()
                print(varList.responseCode,"：返回的桌面(座位号)：",seat_number)
                print(varList.responseCode,"：返回的桌面(玩家人数)：",data.readINT32())
                for k in range(seat_number):
                    print(varList.responseCode,"：服务器返回的桌面(座位号)：",data.readINT32())
                    print(varList.responseCode,"：服务器返回的桌面(玩家MID)：",data.readINT32())
                    print(varList.responseCode,"：服务器返回的桌面(当前分数)：",data.readLONG64())
                    print(varList.responseCode,"：服务器返回的桌面(是否准备(1:准备))：",data.readINT32())  
                    print(varList.responseCode,"：服务器返回的桌面(未知)：",data.readINT32())
                    print(varList.responseCode,"：服务器返回的桌面(是否暂离（1:离开）)：",data.readINT32())
                    print(varList.responseCode,"：返服务器回的桌面(手牌数量)：",data.readINT32())
                    # print("1078返回的桌面(桌面牌的数量)：",data.readINT32())
                    print(varList.responseCode,"：服务器返回的桌面(桌面打牌的数量)：",data.readINT32())#打牌有变动会有数据
                    print(varList.responseCode,"：服务器返回的桌面(牌型):", data.readINT32())
                print(varList.responseCode,"：服务器返回的桌面(目前出牌的座位号):", data.readINT32())
                # print("1078返回的桌面(剩余时间):", data.readINT32())#可以不用理会。

        #发送回调 
        def sendPackCallBack(data):
            sendPackCallBackData = data
            # print("---> 【sendPackCallBack】:", data)
            # print( "发送数据是否完整",data.sendPackCallBack() )
        #连接回调
        # connectState = False
        def connetCallBack(state):
            # global connectState
            varList.connectState = state
            print("---> 【connetCallBack】:", varList.connectState)

        #异常 
        def exceptionCallBack(errInfo):
            print("---> 【exceptionCallBack】:", errInfo)


        #ip和端口取了固定测试环境的值
        QS_net_tcp.Init()
        varList.transfer = QS_net_tcp.transferTCP(recvCallBack,sendPackCallBack,connetCallBack,exceptionCallBack)
        return varList.transfer



