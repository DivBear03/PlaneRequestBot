import socket           #importing useful modules
import re
import time
import os 
from datetime import datetime
from datetime import timedelta
import difflib
from difflib import SequenceMatcher
import random
import scipy.stats

aircraft = []
texthandle = open("Aircraft.txt", 'r')         #open file that contains all useful allied aircraft
for line in texthandle:                                 #iterate through text file
    aircraft.append(line.strip())                 #add the aircraft names to the list
bombers = []
bombhandle = open("Bomber_Blacklist.txt", 'r')
for line in bombhandle:
    bombers.append(line.strip())
#Populating Roman numeral duplicate checking dictionary:
rmnsDict = {}
    
with open("RMNS_NUMS_DICT.txt", 'r') as dfile:
    for line in dfile:
        pieces = line.split("$")
        rmnsDict.update({pieces[0] : pieces[1].replace("\n", "")})
def cleanup(chat):                                                      #function for cleaning up a list converted to a strings
    chat = str(chat)
    chat = chat.replace("[", "")
    chat = chat.replace("]", "")
    chat = chat.replace("\\r", "")
    return chat

def time_convert(sec):                                                  #function for converting seconds into a readable time
    mins = sec // 60
    sec = sec % 60
    hours = mins // 60
    mins = mins % 60
    return str(int(hours)) + ":" + str(int(mins)) + ":" + str(int(sec))

def millitime(time_diff):                                                  #function for converting seconds into a readable time
    execution_time = time_diff.total_seconds()
    return execution_time

def cleanup2(plane):                                    #function for cleaning up whitespace and non-alpha-numeric characters
    plane = plane.replace("-", "")
    plane = plane.replace(" ", "")
    plane = plane.lower()
    plane = plane.replace("\n", "")
    plane = plane.replace("(", "")
    plane = plane.replace(")", "")
    return plane

def gestalt(plane,plane1):
    return (100 * difflib.SequenceMatcher(None, plane, cleanup2(plane1)[:len(plane)+1]).ratio())

def defSim(plane, plane1):
    return gestalt(plane, plane1)

def inSim(plane,plane1):
    if plane in cleanup2(plane1):
        return 100
    else:
        return defSim(plane,plane1)

def isSim(plane, plane1):
    if plane == cleanup2(plane1):
        return 110
    else:
        return defSim(plane,plane1)

def orderSim():
    pass
    
def compSim():
    pass
    
def mineditDist(plane,plane1):
    plane1 = cleanup2(plane1)
    len1 = len(plane) +1
    len2 = len(plane1) +1    
    matrix = [[0 for x in range(len1+1)] for y in range(len2+1)]
        
    for x in range(len2+1):
        matrix[x][0] = x
    for y in range(len1+1):
        matrix[0][y] = y

    for xx in range(1,len2):
        for yy in range(1,len1):
                
            if plane1[xx-1] == plane[yy-1]:
                matrix[xx][yy] = matrix[xx-1][yy-1]
            else:
                matrix[xx][yy] = min([matrix[xx-1][yy],matrix[xx][yy-1],matrix[xx-1][yy-1]]) + 1
                #print(xx,yy,matrix[xx][yy])   
    dist = matrix[len2-1][len1-1]
        
    ret = scipy.stats.norm(0,3).pdf(dist)/scipy.stats.norm(0,3).pdf(0)

    return ret*100

def search(plane):                                                      #search algorithm
    
    plane = cleanup2(plane)                                 #bomber check

    if len(plane) <= 2:
        return "No match"

    for plane1 in bombers:
        substring = cleanup2(plane1)[:len(plane)]
        if plane in substring:
            return "Bombers are useless"

    preliminary = True                                      #logic gate to save time: users penalized if they don't match the first four characters of their request
    if len(plane) <= 4:
        for plane1 in aircraft:
            if plane not in cleanup2(plane1):
                preliminary = False
            else:
                preliminary = True
                break
    if preliminary == False:
        return "No match"

    similarities = {}                                       #dictionary for holding all the planes and their respective match percentages

    foreign = False
    if "usa" in plane or "ussr" in plane or 'japan' in plane or 'germany' in plane or 'italy' in plane or 'china' in plane or 'france' in plane or 'greatbritain' in plane:
        foreign = True


    if foreign == False:
        for plane1 in aircraft:                           #iterate through all allied planes
            if plane == cleanup2(plane1):                                 #if they are a perfect match
                similarities[plane1] = 100                      #set similarity percentage to 100 and break the while loop
                break
            elif len(plane) <= len(cleanup2(plane)) and "[" not in plane1:                     #if not a perfect match
                similarity = difflib.SequenceMatcher(None, plane, cleanup2(plane1)[:len(plane)+1]).ratio()    #calculate percent match
                plane1 = plane1.replace("\n", "")
                similarities[plane1] = similarity * 100                                             #multiply by 100 for actual percent readings

    else:
        for plane1 in aircraft:
            if plane == cleanup2(plane1):
                similarities[plane1] = 100
                break
            elif "[" in plane1 and len(plane) <= len(cleanup2(plane1)):
                similarity = difflib.SequenceMatcher(None, plane, cleanup2(plane1)[:len(plane)+1]).ratio()
                plane1 = plane1.replace("\n", "")
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
    if samesims[shortestindex][1] > 60:             #if the match found is reasonably comparable to the request
        return samesims[shortestindex]              #return the plane with the highest match
    else:
        return "No match"

def search2(plane):
    
    plane = cleanup2(plane)

    if len(plane) <= 2:
        return "No match"

    for plane1 in bombers:
        substring = cleanup2(plane1)[:len(plane)]
        if plane in substring:
            return "Bombers are useless"
  
    similarities = {}                                       #dictionary for holding all the planes and their respective match percentages
    plane = cleanup2(plane)

    foreign = False
    if "usa" in plane or "ussr" in plane or 'japan' in plane or 'germany' in plane or 'italy' in plane or 'china' in plane or 'france' in plane or 'greatbritain' in plane:
        foreign = True


    if foreign == False:
        
        for plane1 in aircraft:
                
            sim1 = isSim(plane,plane1)       
            sim = defSim(plane, plane1)
            if sim < 60:
                similarities[plane1] = sim
                continue
            sim2 = inSim(plane,plane1)
            sim3 = mineditDist(plane, plane1)
            plane1 = plane1.replace("\n", "")            
            similarities[plane1] = (sim + sim1 + sim2 + .5*sim3)/4                                             
        
    else:
        for plane1 in aircraft:
            if plane == cleanup2(plane1):
                similarities[plane1] = 100
                break
            elif "[" in plane1 and len(plane) <= len(cleanup2(plane1)):
                similarity = gestalt(plane, plane1)
                plane1 = plane1.replace("\n", "")
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
    if samesims[shortestindex][1] > 60:             #if the match found is reasonably comparable to the request
        return samesims[shortestindex]              #return the plane with the highest match
    else:
        return "No match"

def indexOf(plane, inputlist):
    index = 0
    if len(inputlist) > 0:
        for n in range(len(inputlist)):
            if inputlist[n] == plane:
                index = n
                return index
                break
    return -1

def indexDict(plane, inputdict):
    keys = list(inputdict.keys())
    index = 0
    if len(keys) > 0:
        for n in range(len(keys)):
            if keys[n] == plane:
                index = n
                return index
                break
    return -1

authorized = ["adamtheenginerd", "zlayer___", "the_ssn", "kingsman784"]     #users authorized for all commands except track

texthandle = open("logs.txt", 'a+')                 #opening logs file
texthandle.write("Tracking start time: ")
texthandle.write(str(datetime.now()))               #printing the start time of logging to the file each time the program is run

requesthandle = open("input-output.txt", 'a+')      #opening file for recording requests and the search results for algorithm improvement 

server = 'irc.chat.twitch.tv'                       #server address
port = 6667                                         #port number
sock = socket.socket()                              #creating socket for connection to twitch
sock.settimeout(240.0)                              #creating timeout timer
sock.connect((server, port))                        #connecting to socket
token = 'oauth:dl7phno18xbouiwgkl9p6969fga10a'      #oauth key for planerequestbot user. Could be changed if you want to send from another twitch user account
sock.send(f"PASS {token}\n".encode('utf-8'))        #passing oauth key into twitch IRC
nickname = 'planerequestbot'                        #doesn't really matter, could be anything
sock.send(f"NICK {nickname}\n".encode('utf-8'))     #passing nickname to twitch IRC
channel = '#kingsman784'                            #channel name, must be all lowercase and have hashtag before channel name
sock.send(f"JOIN {channel}\n".encode('utf-8'))      #passing channel name to twitch IRC
texthandle.write(f"\n{channel}")

requestlist = list()                                #creating empty list of requested planes
go = True                                          #setting program to default disable at start, use --enable command to enable bot
tracking = True                                     #setting tracking to True as default
usercount = dict()                                  #creating empty dictionary for tracking user message counts
commands = {'--disable': 0, '--enable': 0, '--track': 0, '--stoptrack': 0, '--request': 0, '--reqdel': 0, '--skip': 0, '--requests': 0}
count = 0
'''timeout = time.time() + 20                     #manual timer for testing'''

requests = {}                                       #dictionary to hold requests and results

confirmations = ['Attack the D point!', 'Bravo, team!', 'Con-gratu-lations!', 'Affirmative!', 'Yes!', 'I agree!', 'Roger that!', 'Excellent!', 'Thank you!',]

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
    print(user + ": " + message.rstrip())                               #print simplified version of user and message
    if tracking == True and count > 2:                        #if tracking is turned on
        if usercount.get(user, 0) == 0:         #check to see if the user already exists in the dictionary
            usercount[user] = 1                 #if the user is not there, create a new term and make it equal to one
        else:
            usercount[user] = usercount[user] + 1       #otherwise, add one to the user's current count
    
    if "--" not in chat:
        continue

    if "--disable" in chat:                 #check for disable command
        if user in authorized:
            go = False
            commands['--disable'] += 1
            print("BotOn = " + str(go))

    elif "--enable" in chat:                      #check for enable command
        if user in authorized:
            go = True
            commands['--enable'] += 1
            print("BotOn = " + str(go))

    elif "--end" in chat:                   #check for end program command
        if user in authorized:
            break        

    elif '--track' in chat:                     #check for tracking start command
        if user == "adamtheenginerd":
            tracking = True
            commands['--track'] += 1
            print("Tracking = " + str(tracking))

    elif '--stoptrack' in chat:                 #check for tracking end command
        if user == "adamtheenginerd":
            tracking = False
            commands['--stoptrack'] += 1
            if usercount.get(user, 0) == 0:         #check to see if the user already exists in the dictionary
                usercount[user] = 1                 #if the user is not there, create a new term and make it equal to one
            else:
                usercount[user] = usercount[user] + 1  
            print("Tracking = " + str(tracking))

    elif chat.startswith("PING"):               #check for PING from Twitch IRC
        sock.send("PONG\n".encode('utf-8'))     #send "PONG" to stay connected

    elif "--skip[" in message:          #check for a specific plane to skip in the message, only zlayer___  or AdamTheEnginerd can access this command
        if user in authorized:
            plane = re.findall("--skip\[(.+)\]", message)
            plane = cleanup(plane)
            plane = plane.replace("'", "")
            try:
                plane = int(plane)
                skipped = requestlist.pop(plane)
                sock.send(f"PRIVMSG {channel} :{skipped} has been skipped\r\n".encode('utf-8'))
            except:
                selected = indexOf(plane, requestlist)
                skipped = requestlist.pop(selected)
                if skipped in requestlist:
                    sock.send(f"PRIVMSG {channel} :Skip failed\r\n".encode('utf-8'))
                else:
                    sock.send(f"PRIVMSG {channel} :{skipped} has been skipped\r\n".encode('utf-8'))
        else:
            sock.send(f"PRIVMSG {channel} :Requestlist is empty\r\n".encode('utf-8'))

    elif "--delLast" in message or "--dellast" in message:
        if user in authorized:
            plane = requestlist.pop(len(requestlist)-1)
            sock.send(f"PRIVMSG {channel} :{plane} deleted\r\n".encode('utf-8'))

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
                sock.send(f"PRIVMSG {channel} :Requestlist is empty\r\n".encode('utf-8'))      #if no planes in the list, send the message that there are no planes in the list

    elif "--requests" in message:               #check for requests message. Same code as before, but first plane is not removed
            commands['--requests'] += 1
            buildstring = ""
            for plane in requestlist:
                buildstring += plane + ", "
            if len(requestlist) > 0:
                sock.send(f"PRIVMSG {channel} :{buildstring}\r\n".encode('utf-8'))
            else:
                sock.send(f"PRIVMSG {channel} :Requestlist is empty\r\n".encode('utf-8'))

    elif "--commands" in chat:
        sock.send(f"PRIVMSG {channel} :Learn planerequestbot commands here: https://sites.google.com/view/planerequestbotcommands/home?authuser=0\r\n".encode('utf-8'))
    if go == True:                              #all code after this only runs if the bot is enabled

        if "--request " in message:                                         #checking for request command
            startrequesttime = datetime.now()
            commands['--request'] += 1
            plane = re.findall("--request (.+)", message)                   #pull out the plane name
            plane = cleanup(plane)                                          #clean up the list object
            plane = plane.replace("'", "")                                  #replace single quotes with nothing
            result = search2(plane)                                         #perform search algorithm
            requests[plane] = str(result)
            if result == "No match":                                        #if match is not above threshold, algo returns "No match"
                sock.send(f"PRIVMSG {channel} :No match\r\n".encode('utf-8'))   #send chat
            elif result == "Bombers are useless":                           #if algo determines that the request is a bomber
                sock.send(f"PRIVMSG {channel} :Bombers are useless\r\n".encode('utf-8'))    #send chat message
            else:
                planeresult = str(result[0])                                #pull out the actual plane
                planeresult = planeresult.replace("\n", "")                 #replace newline character
                if indexOf(planeresult, requestlist) > -1:                  #if the plane is in the requestlist already
                    sock.send(f"PRIVMSG {channel} :{planeresult} is a duplicate\r\n".encode('utf-8'))   #duplicate message to chat
                elif planeresult in rmnsDict:                               #if it is a roman numeral plane with mulitple correct versions
                    if rmnsDict[planeresult] in requestlist:                #and if the counterpart of the planeresult is already in the request list
                        sock.send(f"PRIVMSG {channel} :{planeresult} is a duplicate\r\n".encode('utf-8'))   #send duplicate message
                    else:
                        confirmation = random.randint(0, len(confirmations)-1)  #random War Thunder quote
                        if indexDict(planeresult, rmnsDict) > 54:
                            requestlist.append(rmnsDict[planeresult])
                            original = rmnsDict[planeresult]
                            sock.send(f"PRIVMSG {channel} :{confirmations[confirmation]} {original} requested!\r\n".encode('utf-8'))
                        else:
                            requestlist.append(planeresult)                     #Otherwise, add the request to the request list
                            sock.send(f"PRIVMSG {channel} :{confirmations[confirmation]} {planeresult} requested!\r\n".encode('utf-8'))     #confirmation message
                else:
                    requestlist.append(planeresult)                         #same as above
                    confirmation = random.randint(0, len(confirmations)-1)
                    sock.send(f"PRIVMSG {channel} :{confirmations[confirmation]} {planeresult} requested!\r\n".encode('utf-8'))
                    print(requestlist)              #print the list

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

for request in requests:                        #writing requests and results to the input-output file for debugging purposes
    buildstring = ""
    buildstring += request
    for n in range(23-len(request)):
        buildstring += "-"
    buildstring += ">"
    buildstring += str(requests[request])
    buildstring += "\n"
    requesthandle.write(buildstring)

texthandle.close()      #closing connection to file
sock.close()            #closing connection to Twitch IRC
