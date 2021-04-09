#socket programming
from socket import *
import os
import sys
import struct
import time
import select
import binascii
import socket
ICMP_ECHO_REQUEST = 8
timeRTT = []
packageSent = 0
packageRev = 0


def checksum(string):
    csum = 0
    countTo = len(string) / 2 * 2
    count = 0
    while count < countTo:
        thisVal = ord(string[count + 1]) * 256 + ord(string[count])
        csum = csum + thisVal
        csum = csum & 0xfffffffff
        count = count + 2
    if countTo < len(string):
        csum = csum + ord(string[len(string) - 1])
        csum = csum & 0xfffffffff
    csum = (csum >> 16) + (csum & 65535)
    csum = csum + (csum >> 16)
    answer = ~csum
    answer = answer & 65535
    answer = answer >> 8 | answer << 8 & 0xff00
    return answer


def receiveOnePing(
    mySocket,
    ID,
    timeout,
    destAddr,
    ):
    global packageRev, timeRTT
    timeLeft = timeout
    while 1:
        startedSelect = time.time()
        whatReady = select.select([mySocket], [], [], timeLeft)
        howLongInSelect = time.time() - startedSelect
        if whatReady[0] == []:  # Timeout
            return 'Request timed out'
        timeReceived = time.time()
        (recPacket, addr) = mySocket.recvfrom(1024)

        # Fill in start
        # Fetch the ICMP header from the IP packet

        icmpHeader = recPacket[20:28]
        (requestType, code, revChecksum, revId, revSequence) = \
            struct.unpack('bbHHh', icmpHeader)
        if ID == revId:
            bytesInDouble = struct.calcsize('d')
            timeData = struct.unpack('d', recPacket[28:28
                    + bytesInDouble])[0]
            timeRTT.append(timeReceived - timeData)
            packageRev += 1
            return timeReceived - timeData
        else:
            return 'ID is not the same!'

        # Fill in end

        timeLeft = timeLeft - howLongInSelect
        if timeLeft <= 0:
            return 'Request timed out'


def sendOnePing(mySocket, destAddr, ID):
    global packageSent

    # Header is type (8), code (8), checksum (16), id (16), sequence (16)

    myChecksum = 0

    # Make a dummy header with a 0 checksum.
    # struct -- Interpret strings as packed binary data

    header = struct.pack('bbHHh',ICMP_ECHO_REQUEST,0,myChecksum,ID,1,)
    data = struct.pack('d', time.time())

    # Calculate the checksum on the data and the dummy header.

    myChecksum = checksum(header + data)

    # Get the right checksum, and put in the header

    if sys.platform == 'darwin':

        # Convert 16-bit integers from host to network byte order.

        myChecksum = socket.htons(myChecksum) & 65535
    else:

        myChecksum = socket.htons(myChecksum)
    header = struct.pack('bbHHh',ICMP_ECHO_REQUEST,0,myChecksum,ID,1,)
    packet = header + data
    mySocket.sendto(packet, (destAddr, 1))
    packageSent += 1


     # AF_INET address must be tuple, not str
    # Both LISTS and TUPLES consist of a number of objects
    # which can be referenced by their position number within the object

def doOnePing(destAddr, timeout):
    icmp = socket.getprotobyname('icmp')

# SOCK_RAW is a powerful socket type. For more details see:http://sock-raw.org/papers/sock_raw
    # Fill in start
    # Create Socket here

    try:
        mySocket = socket.socket(socket.AF_INET, socket.SOCK_RAW, icmp)
    except socket.error(errno, message):
        if errno == 1:
            raise socket.error(message)

    # Fill in end

    myID = os.getpid() & 65535  # Return the current process i
    sendOnePing(mySocket, destAddr, myID)
    delay = receiveOnePing(mySocket, myID, timeout, destAddr)
    mySocket.close()
    return delay


def ping(host, timeout=1):

    # timeout=1 means: If one second goes by without a reply from the server,

    dest = socket.gethostbyname(host)
    print ('Pinging ' + dest + ' using Python:')
    print ('')

    # Send ping requests to a server separated by approximately one second

    while 1:
        delay = doOnePing(dest, timeout)
        print ('RTT:', delay)
        print ('maxRTT:'), (max(timeRTT) if len(timeRTT) > 0 else 0), \
            '\tminRTT:', (min(timeRTT) if len(timeRTT) > 0 else 0), \
            '\naverageRTT:', float((sum(timeRTT)
                                   / len(timeRTT) if len(timeRTT)
                                   > 0 else float('nan')))
        print ('Package Lose Rate:'), ((packageSent - packageRev)
                / packageSent if packageRev > 0 else 0)
        time.sleep(1)  # one second
    return delay
ping("www.google.com")
