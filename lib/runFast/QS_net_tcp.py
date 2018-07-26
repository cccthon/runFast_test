
import asyncio
import socket
from threading import Thread
import time
import string
import random
import QS_pack

def printRecvData(_data,align=8):
	print("pack total length is ",len(_data))
	print("head of pack:")
	xRow = 1
	for i in _data:
		print( "0x%02x" % int(i), end=' ' )
		if xRow%QS_pack.pack.headSize == 0:
			print("\n")
			break
		xRow += 1
	
	print("body of pack:")
	xRow = 1   
	temp_data = _data[QS_pack.pack.headSize:]
	for i in temp_data:
		print( "0x%02x" % int(i), end=' ' )
		if xRow%align == 0:
			print("\n")
			xRow += 1
	print("\n")

def base_str():
	return ('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'+string.digits)

def get_key():
	keylist = [random.choice(base_str()) for i in range(20)]
	return ("".join(keylist))

def thEventLoop(loop):
	asyncio.set_event_loop(loop)
	loop.run_forever()

localEventLoop = asyncio.new_event_loop()
localEventThread = Thread(target=thEventLoop, args=(localEventLoop,))
localEventThread.start()

errNum = {'100':'100','101':'101','102':'102','103':'103','104':'104',}

def Init():
	pass	

def UnInit():
	for task in asyncio.Task.all_tasks():
		print(task.cancel())
	localEventLoop.stop()

#exceptionCallBack异常
class transferTCP(asyncio.Protocol):
	def __init__(self,recvPackCallBack,sendPackCallBack,connectCallBack,exceptionCallBack):
		self.recvPackCallBack_ = recvPackCallBack
		self.exceptionCallBack_ = exceptionCallBack
		self.connectCallBack_ = connectCallBack
		self.sendPackCallBack_ = sendPackCallBack 
		self.transport_ = None
		self.recvBuffer = b''
		self.socket_ = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.name = get_key()#测试使用
	
	async def conncet(self,remote):
		try:
			self.socket_.connect(remote)
		except BaseException:
			self.connectCallBack_(False)
			return

		result_ = await localEventLoop.create_connection(lambda:
			transferTCP(self.recvPackCallBack_,self.sendPackCallBack_,self.connectCallBack_,self.exceptionCallBack_),
			sock=self.socket_)
			
		if len(result_)==2:
			self.connectCallBack_(True)
			return
		
		self.connectCallBack_(False)
	
	def Connect(self,ip="",port=0):
		asyncio.run_coroutine_threadsafe(self.conncet((ip,port)),localEventLoop)
	
	# async def sendData(self,data):
	async def sendData(self,data):
		try:
			sendSize = self.socket_.sendall( data )
			if sendSize == None:
				self.sendPackCallBack_(len(data))
		except BaseException:
			self.exceptionCallBack_((errNum['101'],"send data failed."))
	
	def SendPack(self,sendData):
		asyncio.run_coroutine_threadsafe(self.sendData(sendData), localEventLoop)
	
	def __del__(self):
		self.socket_.close()
		self.transport_.close()
	
	def connection_made(self, transport):
		self.transport_ = transport
	
	def connection_lost(self, exc):
		self.exceptionCallBack_((errNum['102'],"connection_lost"))
	
	def data_received(self, data):
		self.recvBuffer += data

		#print("data_received数据:",data)
		while True:
			if len(self.recvBuffer)<QS_pack.pack.headSize:
				return
	# 		print("data_received",len(data))
			temp_pack = QS_pack.pack()
	
			if not temp_pack.setHead(self.recvBuffer[:QS_pack.pack.headSize]):
				return self.exceptionCallBack_((errNum['103'],"There is not find head in pack."))
	
			bodySize_pack = temp_pack.getPackBodyLen()
			if bodySize_pack<0:
				return self.exceptionCallBack_((errNum['104'],"Body size of pack is minus."))
	
			if len(self.recvBuffer)>=(QS_pack.pack.headSize+bodySize_pack):
				temp_pack.setBodyData(self.recvBuffer[QS_pack.pack.headSize:QS_pack.pack.headSize+bodySize_pack])
				self.recvPackCallBack_(temp_pack)
				self.recvBuffer = self.recvBuffer[QS_pack.pack.headSize+bodySize_pack:]
				

				# print(self.name,self.recvBuffer,len(self.recvBuffer))
			else:
				print("recved data is too litter.")
				return
			