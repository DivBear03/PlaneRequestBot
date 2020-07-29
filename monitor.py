import socket
import time as timerclass
import re

def cleanup(chat):                                                      #function for cleaning up a list converted to a strings
    chat = str(chat)
    chat = chat.replace("[", "")
    chat = chat.replace("]", "")
    chat = chat.replace("\\r", "")
    return chat

def cleanup2(plane):                                    #function for cleaning up whitespace and non-alpha-numeric characters
    plane = plane.replace("-", "")
    plane = plane.replace(" ", "")
    plane = plane.lower()
    plane = plane.replace("\n", "")
    plane = plane.replace("(", "")
    plane = plane.replace(")", "")
    plane = plane.replace(".", "")
    return plane

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

sock.send("CAP REQ :twitch.tv/tags\r\n".encode('utf-8'))
sock.send("CAP REQ :twitch.tv/commands\r\n".encode('utf-8'))
while True:
    highmsg = False
    if timerclass.time() > timeout:                               #Contingency against disconnection from IRC
        sock.close()
        sock = socket.socket()                                  #creating socket for connection to twitch
        sock.connect((server, port))
        sock.settimeout(270.0)
        sock.send(f"PASS {token}\n".encode('utf-8'))
        sock.send(f"NICK {nickname}\n".encode('utf-8'))
        sock.send(f"JOIN {channel}\n".encode('utf-8'))
        timeout += 600
    
    chat = sock.recv(2048).decode('utf-8')
    chat = str(chat)
    print(chat)
    if chat.startswith("PING"):               #check for PING from Twitch IRC
        sock.send("PONG\n".encode('utf-8'))     #send "PONG" to stay connected
        continue
    user = re.findall(f"user-type=.*:.+!.+@(.+)\.tmi\.twitch\.tv PRIVMSG {channel} :", chat)
    user = cleanup(user)
    user = cleanup2(user)                                                #clean up the list object
    user = user.replace("'", "")
    message = re.findall(f"user-type=.*:.+!.+@.+\.tmi\.twitch\.tv PRIVMSG {channel} :(.+)", chat)
    message = str(message)
    message = message[2:(len(message)-4)]
    print(user + ": " + message)

    if "--whisper" in message:
        sock.send(f"PRIVMSG {channel} :/w AdamTheEnginerd Hello from newly verified PlaneRequestBot\r\n".encode('utf-8'))
        print("whisper sent")

    if "--moveup " in message or "—moveup " in message:
        highlighted = re.findall("@badge-info=.*mod=[0-9];msg-id=(.+);room-id=[0-9]+", str(chat))
        highlighted = cleanup(highlighted)
        highlighted = highlighted.replace("'", "")
        if highlighted == "highlighted-message":
            print("Highlighted message")
            plane = re.findall("moveup \{(.+)\} \|[0-9]+\|", message)
            plane = cleanup(plane).replace("'", "")
            newplane = search2(plane)
            if newplane == "No match":
                socksend("No match\r\n")
                continue
            elif newplane == "Bombers are useless":
                socksend("Bombers are useless\r\n")
                continue
            else:
                newplane = newplane[0]
                instring = '{'+newplane+'}'
                places = re.findall(f"moveup {instring} \|([0-9]+)\|", message)
                places = cleanup(places).replace("'", "")
                try:
                    places = int(places)
                except:
                    continue
                index = indexOf(newplane, requestlist)
                if index == -1:
                    socksend("No such plane in requestlist\r\n")
                else:
                    if places < index:
                        temp = requestlist.pop(index)
                        requestlist.insert(index-places, temp)
                        socksend(f"{newplane} moved up {places} places\r\n")
                    else:
                        temp = requestlist.pop(index)
                        requestlist.insert(0, temp)
                        socksend(f"{newplane} moved up to 1st in line\r\n")
        else:
            socksend("No channel points redeemed\r\n")