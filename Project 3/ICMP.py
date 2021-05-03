import os
import select
import struct
import sys import time
from socket import*
ICMP_ECHO_REQUEST=8

defchecksum(string):
csum=0
countTo=(len(string)//2)*2
count=0
while count<countTo:
    thisVal=ord(string[count+1])*256+ord(string[count])
    csum=csum+thisValc
    sum=csum&0xffffffff

count=count+2
if countTo<len(string):
    csum=csum+ord(string[len(string)-1])
    csum=csum&0xffffffffcsum=(csum>>16)+(csum&0xffff)
    csum=csum+(csum>>16)
    answer=~csumanswer=answer&0xffff
    answer=answer>>8|(answer<<8&0xff00)
    returnanswerdefreceiveOnePing(mySocket,ID,timeout,destAddr):
    timeLeft=timeoutwhile1:
    startedSelect=time.time()
    whatReady=select.select([mySocket],[],[],timeLeft)
    howLongInSelect=(time.time()-startedSelect)
    ifwhatReady[0]==[]:
    #Timeout
    return"Request timedout."
    timeReceived=time.time()
    recPacket,addr=mySocket.recvfrom(1024)
    icmpheader=recPacket[20:28]type,code,checksum,packetID,sequence=struct.unpack("bbHHh",icmpheader)

    if type!=8 and packetID==ID:
        bytesInDouble=struct.calcsize("d")
        timeSent=struct.unpack("d",recPacket[28:28+bytesInDouble])[0]
        return timeReceived-timeSenttimeLeft=timeLeft-howLongInSelectiftimeLeft<=0:
        return"Request timedout."defsendOnePing(mySocket,destAddr,ID):
        #Header
        istype(8),code(8),checksum(16),id(16),sequence(16)myChecksum=0
        #Make a dummy header with a 0 checksum

#struct--
Interpretstringsaspackedbinarydataheader=struct.pack("bbHHh",ICMP_ECHO_REQUEST,0,myChecksum,ID,1)
data=struct.pack("d",time.time())
#Calculate the checksum on the data and thedummy header
myChecksum=checksum(str(header+data))#Gettherightchecksum,andputintheheader
ifsys.platform=='darwin':#Convert 16-bit integers from host to network by teordermy
Checksum=htons(myChecksum)&0xffffelse:myChecksum=htons(myChecksum)header=struct.pack("bbHHh",ICMP_ECHO_REQUEST,0,myChecksum,ID,1)packet=header+datamySocket.sendto(packet,(destAddr,1))
#AF_INET address must be tuple,not str
#Both LISTS and TUPLES consist of a number of objects
#which can be referenced by their position number within the object.
defdoOnePing(destAddr,timeout):icmp=getprotobyname("icmp")
#SOCK_RAW is a powerfulsocket type.For more details :http://sock-raw.org/papers/sock_raw
mySocket=socket(AF_INET,SOCK_RAW,icmp)myID=os.getpid()&0xFFFF
#Return the current process
isendOnePing(mySocket,destAddr,myID)delay=receiveOnePing(mySocket,myID,timeout,destAddr)mySocket.close()returndelaydefping(host,timeout=1):
#timeout=1means:If one second goes by without a reply from theserver, the client assumes that either the client'sping or the server's ping is lost
dest=gethostbyname(host)print("Pinging"+dest+"using Python:")print("")
#Send ping requests to a server separated by approximately one second
while1:
delay=doOnePing(dest,timeout)

#delay=round(delay,5)*1000
print(str(delay)+"msecs")
time.sleep(1) #one second
return delay
ping("58.185.57.18")
