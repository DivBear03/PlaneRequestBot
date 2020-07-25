import socket
import time as timerclass

server = 'irc.chat.twitch.tv'                       #server address
port = 6667                                         #port number
sock = socket.socket()                              #creating socket for connection to twitch
sock.connect((server, port))                        #connecting to socket
sock.settimeout(270.0)
token = 'oauth:zsnamwt00lh6bsd7pv0ovywtbhympj'      #oauth key for planerequestbot user. Could be changed if you want to send from another twitch user account
sock.send(f"PASS {token}\n".encode('utf-8'))        #passing oauth key into twitch IRC
nickname = 'planerequestbot'                        #doesn't really matter, could be anything
sock.send(f"NICK {nickname}\n".encode('utf-8'))     #passing nickname to twitch IRC
channel = input("Enter the channel name with hash sign: ")
if channel.__contains__("#"):
    sock.send(f"JOIN {channel}\n".encode('utf-8'))      #passing channel name to twitch IRC
else:
    channel = "#"+channel
    sock.send(f"JOIN {channel}\n".encode('utf-8'))


timeout = timerclass.time() + 600                         #anti-disconnect timer


while True:
    
    if timerclass.time() > timeout:                               #Contingency against disconnection from IRC
        sock.close()
        sock = socket.socket()                              #creating socket for connection to twitch
        sock.connect((server, port))
        sock.settimeout(270.0)
        sock.send(f"PASS {token}\n".encode('utf-8'))
        sock.send(f"NICK {nickname}\n".encode('utf-8'))
        sock.send(f"JOIN {channel}\n".encode('utf-8'))
        timeout += 600
    
    chat = sock.recv(2046).decode('utf-8')
    print(str(chat))

    if chat.startswith("PING"):               #check for PING from Twitch IRC
        sock.send("PONG\n".encode('utf-8'))     #send "PONG" to stay connected