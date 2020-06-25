import socket           #importing useful modules
import re
import time
from datetime import datetime
import os
import difflib
from difflib import SequenceMatcher
import itertools


def search(plane):
    alliedaircraft = []             #all allied aircraft that could be considered useful
    texthandle = open("Aircraft - Allied.txt", 'r')         #open file that contains all useful allied aircraft
    for line in texthandle:                                 #iterate through text file
        alliedaircraft.append(line.strip())                 #add the aircraft names to the list
    axisaircraft = []
    texthandle2 = open("Aircraft - Axis.txt", 'r')
    for line in texthandle2:
        axisaircraft.append(line.lower())
    def cleanup2(plane):                                    #function for cleaning up whitespace and non-alpha-numeric characters
        plane = plane.replace("-", "")
        plane = plane.replace(" ", "")
        plane = plane.lower()
        plane = plane.replace("\n", "")
        plane = plane.replace("(", "")
        plane = plane.replace(")", "")
        return plane
    similarities = {}                                       #dictionary for holding all the planes and their respective match percentages
    plane = cleanup2(plane)
    for plane1 in alliedaircraft:                           #iterate through all allied planes
        if plane == cleanup2(plane1):                                 #if they are a perfect match
            similarities[plane1] = 100                      #set similarity percentage to 100 and break the while loop
            break
        elif len(plane) <= len(cleanup2(plane)):                     #if not a perfect match
            similarity = difflib.SequenceMatcher(None, plane, cleanup2(plane1)[:len(plane)+1]).ratio()    #calculate percent match
            similarities[plane1] = similarity * 100                                             #multiply by 100 for actual percent readings
    for plane1 in axisaircraft:                           #iterate through all allied planes
        if plane == cleanup2(plane1):                                 #if they are a perfect match
            similarities[plane1] = 100                      #set similarity percentage to 100 and break the while loop
            break
        elif len(plane) <= len(cleanup2(plane)):                     #if not a perfect match
            similarity = difflib.SequenceMatcher(None, plane, cleanup2(plane1)[:len(plane)+1]).ratio()    #calculate percent match
            similarities[plane1] = similarity * 100 
    sortedlist = list()                 #creating empty list to hold sorted users
    for thing in similarities.items():     #iterate through the keys and terms of usercount dictionary
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


    samesims = []                                   #list to hold all top results with the same similarity
    samesims.append(sortedlist[0])                  #add the top one
    for n in range(1, len(sortedlist)):
        if sortedlist[n][1] == samesims[0][1]:  #if the current similarity is equal to the similarity of the top result one
            samesims.append(sortedlist[n])          #add that plane and its similarity
    shortestindex = 0                               #algorithm to determine what the plane with the shortest name is
    shortest = len(samesims[0][0])                  #set the shortest string length to be the first plane's string length
    for n in range(1, len(samesims)):               #iterate through the next terms of the list of planes with the same similarities
        if len(samesims[n][0]) < shortest:          #if the present plane has a shorter string length
            shortest = len(samesims[n][0])          #make the shortest length to be that length
            shortestindex = n                       #set the index of the shortest string length to be that index
    if samesims[shortestindex][1] > 50:                       #if the match found is reasonably comparable to the request
        return samesims[shortestindex][0].replace("\n", "")   #return the plane with the highest match
    else:
        return "No match"


'''class Request:
    def __init__(self, priority, plane):
        self.priority = priority
        self.plane = plane'''


'''path = 'C:\\Users\\esben\\WarThunderFlightModels'
folder = os.fsencode(path)
filenames = []
for file in os.listdir(folder):
    filename = os.fsdecode(file)
    if filename.endswith('.blk'):
        filename = filename.replace("_", " ")
        filenames.append(filename[:len(filename)-4])'''


'''priorityusers = []                  #initializing the list of users with priority: mods, VIPs, etc
priorityhandle = open("VIPs.txt", 'r+')
for line in priorityhandle:
    priorityusers.append(line.strip())'''

authorized = ["adamtheenginerd", "zlayer___", "the_ssn", "kingsman784"]

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


'''def find(request):
    possibilities = []
    for fm in filenames:
        if request in fm:
            possibilities.append(fm)
    return possibilities'''


server = 'irc.chat.twitch.tv'       #server address
port = 6667                         #port number
sock = socket.socket()              #creating socket for connection to twitch
sock.settimeout(240.0)              #creating timeout timer
sock.connect((server, port))        #connecting to socket
token = 'oauth:dl7phno18xbouiwgkl9p6969fga10a'      #oauth key for planerequestbot user. Could be changed if you want to send from another twitch user account
sock.send(f"PASS {token}\n".encode('utf-8'))        #passing oauth key into twitch IRC
nickname = 'planerequestbot'                                       #doesn't really matter, could be anything
sock.send(f"NICK {nickname}\n".encode('utf-8'))     #passing nickname to twitch IRC
channel = '#adamtheenginerd'                        #channel name, must be all lowercase and have hashtag before channel name
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

requests = {}

requestlist.append("A-26C-45")
requestlist.append("ki-94-ii")
requestlist.append("F4F-4")
requestlist.append("P-47M-1-RE")
requestlist.append("J29A")
requestlist.append("ki-83")
requestlist.append("fw 190 a-4")
requestlist.append("Po-2")


while True:
    
    '''if time.time() > timeout:
        break'''
    try:
        chat = sock.recv(2048).decode('utf-8')      #receive message
        chat = str(chat)                            #convert to string
    except:
        break
    count += 1
    

    if "--" not in chat:
        continue

    user = re.findall(":.+!.+@(.+)\.tmi\.twitch\.tv", chat)             #pull username out of received message
    user = cleanup(user)                                                #clean up the list object
    user = user.replace("'", "")                                        #remove single quotes
    startmessage = (len(user)) * 3 + len(channel) + 28                  #calculate starting index of message
    message = chat[startmessage:]                                       #pull out the message text
    print(user + ": " + message.rstrip())                                        #print simplified version of user and message
    if "--disable" in chat:                 #check for disable command
        if user in authorized:
            go = False
            commands['--disable'] += 1
            print("BotOn = " + str(go))
        else:
            sock.send(f"PRIVMSG {channel} :You do not have permission to disable me\r\n".encode('utf-8'))


    elif "--enable" in chat:                      #check for enable command
        if user in authorized:
            go = True
            commands['--enable'] += 1
            print("BotOn = " + str(go))
        else:
            sock.send(f"PRIVMSG {channel} :You do not have permission to enable me\r\n".encode('utf-8'))

    elif "--end" in chat:                   #check for end program command
        if user in authorized:
            break
        else:
            sock.send(f"PRIVMSG {channel} :You do not have permission to kill the bot\r\n".encode('utf-8'))
        


    elif '--track' in chat:                     #check for tracking start command
        if user == "adamtheenginerd":
            tracking = True
            commands['--track'] += 1
            print("Tracking = " + str(tracking))
        else:
            sock.send(f"PRIVMSG {channel} :You do not have permission to initiate tracking\r\n".encode('utf-8'))


    elif '--stoptrack' in chat:                 #check for tracking end command
        if user == "adamtheenginerd":
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


    elif "--skip[" in message:          #check for a specific plane to skip in the message, only zlayer___  or AdamTheEnginerd can access this command
        if user in authorized:
            plane = re.findall("--skip\[(.+)\]", message)
            plane = cleanup(plane)
            plane = plane.replace("'", "")
            if len(requestlist) > 0:
                for n in range(len(requestlist)):
                    if requestlist[n-1] == plane:
                        requestlist.pop(n-1)
                sock.send(f"PRIVMSG {channel} :{plane} has been skipped\r\n".encode('utf-8'))
            else:
                sock.send(f"PRIVMSG {channel} :No planes in requestlist\r\n".encode('utf-8'))
        else:
            sock.send(f"PRIVMSG {channel} :You do not have permission to skip planes\r\n".encode('utf-8'))


    '''elif "--add" in chat and user == "adamtheenginerd":
        newpriuser = re.findall("--add (.+)", chat)
        newpriuser = cleanup(newpriuser)
        newpriuser = newpriuser.replace("'", "")
        priorityusers.append(newpriuser)'''


    if go == True:                              #all code after this only runs if the bot is enabled

        if "--request " in message:                                         #checking for request command
            commands['--request'] += 1
            plane = re.findall("--request (.+)", message)                   #pull out the plane name
            plane = cleanup(plane)                                          #clean up the list object
            plane = plane.replace("'", "")                                  #replace single quotes with nothing
            result = search(plane)
            if result == "No match":
                sock.send(f"PRIVMSG {channel} :Sorry, no match is found by algorithm\r\n".encode('utf-8'))
                requests[plane] = result
            else:
                requests[plane] = result
                duplicate = False
                for thing in requestlist:
                    if thing == result:
                        duplicate = True
                if duplicate == True:
                    sock.send(f"PRIVMSG {channel} :{result} is a duplicate\r\n".encode('utf-8'))
                else:
                    requestlist.append(result)
                    sock.send(f"PRIVMSG {channel} :{result} has been requested\r\n".encode('utf-8'))
            print(requestlist)              #print the list


        elif "--reqdel" in message:             #checking for reqdel command
            if user in authorized:
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
            if user in authorized:
                commands['--skip'] += 1
                if len(requestlist) > 0:            #if there are planes in the requestlist
                    aircraft = requestlist.pop(0)
                    sock.send(f"PRIVMSG {channel} :{aircraft} has been skipped\r\n".encode('utf-8'))
                else:
                    sock.send(f"PRIVMSG {channel} :No aircraft in request list\r\n".encode('utf-8'))


        elif "--requests" in message:               #check for requests message. Same code as before, but first plane is not removed
            commands['--requests'] += 1
            buildstring = ""
            for plane in requestlist:
                buildstring += plane + ", "
            if len(requestlist) > 0:
                sock.send(f"PRIVMSG {channel} :{buildstring}\r\n".encode('utf-8'))
            else:
                sock.send(f"PRIVMSG {channel} :No planes in request list\r\n".encode('utf-8'))


        elif "--commands" in chat:
            sock.send(f"PRIVMSG {channel} :Learn planerequestbot commands here: https://sites.google.com/view/planerequestbotcommands/home?authuser=0\r\n".encode('utf-8'))


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



#A-26C-45, ki-94-ii, F4F-4, A-26C-45, P-47M-1-RE, J29A, ki-83, fw 190 a-4, Po-2,