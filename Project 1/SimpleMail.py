from socket import *
import base64
import ssl
msg = "\r\n I love computer networks."
endmsg = "\r\n.\r\n"
# Choose a mail server (e.g. Google mail server) and call it mailserver
mailserver = ("smtp.gmail.com", 465)
# Create socket called clientSocket and establish a TCP connection with mailserver
#Fill in start
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocketSSL = ssl.wrap_socket(clientSocket)
clientSocketSSL.connect(mailserver)
#Fill in end
recv = clientSocketSSL.recv(1024).decode()
print(recv)
if recv[:3] != '220':
print('220 reply not received from server.')
# Send HELO command and print server response.
helloCommand = 'EHLO localhost\r\n'
starttls = 'STARTTLS\r\n'

clientSocketSSL.send(helloCommand.encode())
recv1 = clientSocketSSL.recv(1024).decode()
print(recv1)
if recv1[:3] != '250':
print('250 reply not received from server.')
#Username and password info (Base64 format)
username = 'AUTH LOGIN A1klo097bhtYbWFpbC5j98tY3=\r\n'
password = '9564AyuonftHK9kLop34==\r\n'
#Input Username
clientSocketSSL.send(username.encode())
recv1 = clientSocketSSL.recv(1024).decode()
print(recv1)
#Input Password
clientSocketSSL.send(password.encode())
recv1 = clientSocketSSL.recv(1024).decode()
print(recv1)
# Send MAIL FROM command and print server response.
# Fill in start
mailFrom = "MAIL FROM: <testmail@gmail.com>\r\n"
clientSocketSSL.send(mailFrom.encode())
recv2 = clientSocketSSL.recv(1024).decode()
print("After MAIL FROM command: "+recv2)
# Fill in end
# Send RCPT TO command and print server response.

#Fill in start
rcptTo = "RCPT TO: <rcvmail@gmail.com>\r\n"
clientSocketSSL.send(rcptTo.encode())
recv3 = clientSocketSSL.recv(1024).decode()
print("After RCPT TO command: "+recv3)
# Fill in end
# Send DATA command and print server response.
# Fill in startdata = "DATA\r\n"
data = "DATA\r\n"
clientSocketSSL.send(data.encode())
recv4 = clientSocketSSL.recv(1024)
print("After DATA command: "+recv4.decode())
# Fill in end
# Send message data.
# Fill in start
clientSocketSSL.send(msg.encode())
# Fill in end
# Message ends with a single period.
# Fill in start
clientSocketSSL.send(endmsg.encode())
recv_msg = clientSocketSSL.recv(1024)
print("Response after sending message body:"+recv_msg.decode())
# Fill in end
# Send QUIT command and get server response.
# Fill in start

quit = "QUIT\r\n"
clientSocketSSL.send(quit.encode())
recv5 = clientSocketSSL.recv(1024)
print("Responce after sending quit:" +recv5.decode())
clientSocketSSL.close()
# Fill in end
