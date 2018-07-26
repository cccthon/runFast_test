
import struct


class pack:
    headSize = 6
    
    def __init__(self,cmdNum=0,str_encode='utf-8'):
        self.str_encode = str_encode
        self.readBuffer = b""
        self.writeBuffer = b""
        self.cmdNum = cmdNum
        self.readIndex = pack.headSize
        
    #定义一个读取所有写数据的方法
    def getWriteData(self):
        return self.writeBuffer

    #定义一个读取所有数据的方法
    def getReadData(self):
        return self.readBuffer

    #返回值:设置是否成功
    def setHead(self,_data):
        if len(_data) < pack.headSize:
            return False
        
        head = struct.unpack("<2s", _data[:2])
        # print("hhkkj：",head[0])
               
        if bytes(head[0]).decode(self.str_encode) != "QS":
            raise RuntimeError('pack_rw error:head of pack is not QS.')
            return False
        
        self.readBuffer = _data
        return True
    
    def setBodyData(self,_data):
        self.readBuffer += _data
    
    def getPackBodyLen(self):
        bodyLen = struct.unpack("<2s", self.readBuffer[2:4])
        # print("555555:",bodyLen)
        bodyLen = struct.unpack("<h", bodyLen[0] )
        bodyLen = int(bodyLen[0])
        return bodyLen
        
    #检查读取包的完整性
    def checkReadPack(self):
        if len(self.readBuffer)<pack.headSize:
            return False
        
        head = struct.unpack("<2s", self.readBuffer[:2])
        # print("1123:",head)
        if bytes(head[0]).decode(self.str_encode) != "QS":
            return False
        
        total_size = self.getPackBodyLen()+pack.headSize
        if total_size==len(self.readBuffer):
            return True
        
        return False
        
    def getCmd(self):
        cmd = struct.unpack("<2s", self.readBuffer[4:6])
        cmd = struct.unpack("<h", cmd[0] )
        cmd = int(cmd[0])
        return cmd 

#写入    
    def writeINT16(self,_data):
        self.writeBuffer += struct.pack("<h", _data)
        
    def writeINT32(self,_data):
        self.writeBuffer += struct.pack("<i", _data)
    
    def writeLONG64(self,_data):
        self.writeBuffer += struct.pack("<q", _data)
        
    def writeString(self,_data):
        self.writeBuffer += struct.pack("<i", len(_data)+1)
        _format = "<{0}s".format(len(_data)+1)
        self.writeBuffer += struct.pack( _format, _data.encode(self.str_encode))
        
    def writeOver(self):
        head = struct.pack("<2s", b"QS" )        
        dataLen = struct.pack("<h", len(self.writeBuffer) )
        cmd = struct.pack("<h", self.cmdNum )
        # print("666666:",cmd)
        temp = head+dataLen+cmd+self.writeBuffer      
        return temp 

    def readINT16(self):        
        temp = struct.unpack("<h", self.readBuffer[self.readIndex:self.readIndex+2])
        temp = int(temp[0])
        self.readIndex += 2
        return temp
        
    def readINT32(self):
        temp = struct.unpack("<i", self.readBuffer[self.readIndex:self.readIndex+4])
        temp = int(temp[0])
        self.readIndex += 4
        return temp
    
    def readLONG64(self):
        temp = struct.unpack("<q", self.readBuffer[self.readIndex:self.readIndex+8])
        temp = int(temp[0])
        self.readIndex += 8
        return temp
        
    def readString(self):
        strSize = struct.unpack("<i", self.readBuffer[self.readIndex:self.readIndex+4])
        strSize = int(strSize[0])
        self.readIndex += 4
        
        #去掉末尾的结束符
        if strSize>0:
            strSize -=1
        #format字符串格式化
        _format = "<{0}s".format(strSize)
        temp = struct.unpack( _format, self.readBuffer[self.readIndex:self.readIndex+strSize] )
        if strSize>=0:
            strSize +=1
        self.readIndex += strSize
        return temp[0].decode(self.str_encode)
        