import socket           #importing useful modules
import re
import time
from datetime import datetime
import os
import difflib
from difflib import SequenceMatcher
import itertools


def search(plane):
    alliedaircraft = []
    texthandle = open("Aircraft - Allied.txt", 'r')
    for line in texthandle:
        alliedaircraft.append(line.lower())
    def cleanup2(plane):
        plane = plane.replace("-", "")
        plane = plane.replace(" ", "")
        plane = plane.lower()
        plane = plane.replace("\n", "")
        return plane


class Request:
    def __init__(self, priority, plane):
        self.priority = priority
        self.plane = plane


path = 'C:\\Users\\esben\\WarThunderFlightModels'
folder = os.fsencode(path)
filenames = []
for file in os.listdir(folder):
    filename = os.fsdecode(file)
    if filename.endswith('.blk'):
        filename = filename.replace("_", " ")
        filenames.append(filename[:len(filename)-4])


priorityusers = []                  #initializing the list of users with priority: mods, VIPs, etc
priorityhandle = open("VIPs.txt", 'r+')
for line in priorityhandle:
    priorityusers.append(line.strip())


texthandle = open("logs.txt", 'a+')                                     #opening logs file
texthandle.write("Tracking start time: ")
texthandle.write(str(datetime.now()))                                        #printing the start time of logging to the file each time the program is run


def cleanup(chat):                                                      #function for cleaning up a list converted to a strings
    chat = str(chat)
    chat = chat.replace("[", "")
    chat = chat.replace("]", "")
    chat = chat.replace("\\r", "")
    return chat


def time_convert(sec):
    mins = sec // 60
    sec = sec % 60
    hours = mins // 60
    mins = mins % 60
    return str(int(hours)) + ":" + str(int(mins)) + ":" + str(int(sec))


def find(request):
    possibilities = []
    for fm in filenames:
        if request in fm:
            possibilities.append(fm)
    return possibilities


server = 'irc.chat.twitch.tv'       #server address
port = 6667                         #port number
sock = socket.socket()              #creating socket for connection to twitch
sock.settimeout(150.0)              #creating timeout timer
sock.connect((server, port))        #connecting to socket
token = 'oauth:dl7phno18xbouiwgkl9p6969fga10a'      #oauth key for planerequestbot user. Could be changed if you want to send from another twitch user account
sock.send(f"PASS {token}\n".encode('utf-8'))        #passing oauth key into twitch IRC
nickname = 'planerequestbot'                                       #doesn't really matter, could be anything
sock.send(f"NICK {nickname}\n".encode('utf-8'))     #passing nickname to twitch IRC
channel = '#kingsman784'                        #channel name, must be all lowercase and have hashtag before channel name
sock.send(f"JOIN {channel}\n".encode('utf-8'))      #passing channel name to twitch IRC
texthandle.write(f"\n{channel}")


requestlist = list()                                #creating empty list of requested planes
go = True                                           #setting program to default enable at start, use --close command to disable bot
tracking = True                                     #setting tracking to True as default
usercount = dict()                                  #creating empty dictionary for tracking user message counts
commands = {'--disable': 0, '--enable': 0, '--track': 0, '--stoptrack': 0, '--request': 0, '--reqdel': 0, '--skip': 0, '--requests': 0}
count = 0
specialuser = ""        #variable to hold the username of the person who made a request that returns multiple possible planes
feedback = False        #boolean to indicate whether the program is waiting for a feedback on index of list returned by --request command
'''timeout = time.time() + 20                     #manual timer for testing'''


while True:
    
    '''if time.time() > timeout:
        break'''

    try:
        chat = sock.recv(2048).decode('utf-8')      #receive message
        chat = str(chat)                            #convert to string
    except:
        break
    count += 1

    user = re.findall(":.+!.+@(.+)\.tmi\.twitch\.tv", chat)             #pull username out of received message
    user = cleanup(user)                                                #clean up the list object
    user = user.replace("'", "")                                        #remove single quotes
    startmessage = (len(user)) * 3 + len(channel) + 28                  #calculate starting index of message
    message = chat[startmessage:]                                       #pull out the message text
    print(user + ": " + message.rstrip())                                        #print simplified version of user and message
    if "--disable" in chat:                 #check for disable command
        if user == "adamtheenginerd" or user == "zlayer___":
            go = False
            commands['--disable'] += 1
            print("BotOn = " + str(go))
        else:
            sock.send(f"PRIVMSG {channel} :You do not have permission to disable me\r\n".encode('utf-8'))


    elif "--enable" in chat:                      #check for enable command
        if user == "adamtheenginerd" or user == "zlayer___":
            go = True
            commands['--enable'] += 1
            print("BotOn = " + str(go))
        else:
            sock.send(f"PRIVMSG {channel} :You do not have permission to enable me\r\n".encode('utf-8'))

    elif (user == "zlayer___" or user == "adamtheenginerd") and "--end" in chat:                   #check for end program command
        break
        


    elif '--track' in chat:                     #check for tracking start command
        if user == "adamtheenginerd" or user == "zlayer___":
            tracking = True
            commands['--track'] += 1
            print("Tracking = " + str(tracking))
        else:
            sock.send(f"PRIVMSG {channel} :You do not have permission to initiate tracking\r\n".encode('utf-8'))


    elif '--stoptrack' in chat:                 #check for tracking end command
        if user == "adamtheenginerd" or user == "zlayer___":
            tracking = False
            commands['--stoptrack'] += 1
            if usercount.get(user, 0) == 0:         #check to see if the user already exists in the dictionary
                usercount[user] = 1                 #if the user is not there, create a new term and make it equal to one
            else:
                usercount[user] = usercount[user] + 1  
            print("Tracking = " + str(tracking))
        else:
            sock.send(f"PRIVMSG {channel} :You do not have permission to halt tracking\r\n".encode('utf-8'))


    elif chat.startswith("PING"):               #check for PING from Twitch IRC
        sock.send("PONG\n".encode('utf-8'))     #send "PONG" to stay connected

    elif "--commands" in chat:
        sock.send(f"PRIVMSG {channel} :Learn commands here: https://sites.google.com/view/planerequestbotcommands/home?authuser=0\r\n".encode('utf-8'))


    elif "--add" in chat and user == "adamtheenginerd":
        newpriuser = re.findall("--add (.+)", chat)
        newpriuser = cleanup(newpriuser)
        newpriuser = newpriuser.replace("'", "")
        priorityusers.append(newpriuser)


    if go == True:                              #all code after this only runs if the bot is enabled

        if "--request " in message:                                         #checking for request command
            commands['--request'] += 1
            plane = re.findall("--request (.+)", message)                   #pull out the plane name
            plane = cleanup(plane)                                          #clean up the list object
            plane = plane.replace("'", "")                                  #replace single quotes with nothing
            if user in priorityusers:
                request = Request(True, plane)
                sock.send(f"PRIVMSG {channel} :{plane} has been requested by priority user {user}\r\n".encode('utf-8'))
            else:
                request = Request(False, plane)
                sock.send(f"PRIVMSG {channel} :{plane} has been requested\r\n".encode('utf-8'))
            '''checked = False
            for actual in filenames:
                if plane in actual:
                    checked = True
            if checked == False:
                sock.send(f"PRIVMSG {channel} :No aircraft with that name exists\r\n".encode('utf-8'))
            else:'''
            requestlist.append(request)                                       #add the plane name to the list of requested planes
            print(requestlist)              #print the list


        elif "--reqdel" in message:             #checking for reqdel command
            if user == "zlayer___" or user == "adamtheenginerd":
                commands['--reqdel'] += 1
                buildstring = ""                    #create empty string that will show the list of requested planes
                for plane in requestlist:           #iterate through the planes in the list
                    buildstring += plane + ", "     #add the plane to the string and a comma
                if len(requestlist) > 0:            #if there are planes in the requestlist
                    sock.send(f"PRIVMSG {channel} :{buildstring}\r\n".encode('utf-8'))          #send the string of requested planes to the chat
                    removedplane = requestlist.pop(0)                                           #remove the first plane in the list since it will be played. 
                else:
                    sock.send(f"PRIVMSG {channel} :No planes in request list\r\n".encode('utf-8'))      #if no planes in the list, send the message that there are no planes in the list


        elif "--skip" in message:                      #check for skip command, skip the first plane in the list
            if user == "zlayer___" or user == "adamtheenginerd":
                commands['--skip'] += 1
                if len(requestlist) > 0:            #if there are planes in the requestlist
                    aircraft = requestlist.pop(0)
                    sock.send(f"PRIVMSG {channel} :{aircraft} has been skipped\r\n".encpde('utf-8'))
                else:
                    sock.send(f"PRIVMSG {channel} :No aircraft in request list\r\n".encode('utf-8'))

        elif "--skip[" in message:          #check for a specific plane to skip in the message, only zlayer___  or AdamTheEnginerd can access this command
            if user == "zlayer___" or user == "adamtheenginerd":
                plane = re.findall("--skip\[(.+)\]", message)
                plane = cleanup(plane)
                plane = plane.replace("'", "")
                if len(requestlist) > 0:
                    for n in range(len(requestlist)):
                        if requestlist[n] == plane:
                            requestlist.pop(n)
                    sock.send(f"PRIVMSG {channel} :{plane} has been skipped\r\n".encode('utf-8'))
                else:
                    sock.send(f"PRIVMSG {channel} :No planes in requestlist\r\n".encode('utf-8'))

        elif "--requests" in message:               #check for requests message. Same code as before, but first plane is not removed
            commands['--requests'] += 1
            buildstring = ""
            for plane in requestlist:
                buildstring += plane + ", "
            if len(requestlist) > 0:
                sock.send(f"PRIVMSG {channel} :{buildstring}\r\n".encode('utf-8'))
            else:
                sock.send(f"PRIVMSG {channel} :No planes in request list\r\n".encode('utf-8'))


        '''elif "ssn" in message and count > 2:
            sock.send(f"PRIVMSG {channel} :Praise SSN!\r\n".encode('utf-8'))'''


        '''elif "adam" in message or "Adam" in message and count > 2: 
            sock.send(f"PRIVMSG {channel} :Praise AdamTheEnginerd!\r\n".encode('utf-8'))'''


        if tracking == True and count > 2:                        #if tracking is turned on
            if usercount.get(user, 0) == 0:         #check to see if the user already exists in the dictionary
                usercount[user] = 1                 #if the user is not there, create a new term and make it equal to one
            else:
                usercount[user] = usercount[user] + 1       #otherwise, add one to the user's current count

sortedlist = list()                 #creating empty list to hold sorted users
for thing in usercount.items():     #iterate through the keys and terms of usercount dictionary
    sortedlist.append(thing)        #add each key,value pair to sortedlist
for i in range(1, len(sortedlist)):         #insertion sort algorithm
    nextElementValue = sortedlist[i][1]
    temp = sortedlist[i]
    j = i-1
    while j >= 0 and sortedlist[j][1] < nextElementValue:
        item = sortedlist[j]
        sortedlist[j+1] = item
        j = j-1
    sortedlist[j+1] = temp
texthandle.write("\n")
for item in sortedlist:
    print(item[0], str(item[1]))
    texthandle.write(str(item[0])+": "+str(item[1])+" messages\n")        #writing sortedlist data to file
texthandle.write("Number of requests: " + str(commands['--request']) + "\n")
texthandle.write("Tracking end time: ")
texthandle.write(str(datetime.now()) + "\n\n")

texthandle.close()      #closing connection to file
sock.close()            #closing connection to Twitch IRC
# Receiving message format :<user>!<user>@<user>.tmi.twitch.tv PRIVMSG <channel> :<message>
# Sending message format  PRIVMSG <channel> :<message>