import socket           #importing useful modules
import re
import time
import datetime
import difflib
from difflib import SequenceMatcher
import random
import scipy.stats
from random import randrange
from time import sleep
import requests 
class Action:
    def __init__(self, add, delete, plane, index):
        self.add = add
        self.delete = delete
        self.plane = plane
        self.index = index
        self.time = time
    def getAdd(self):
        return self.add
    def getDelete(self):
        return self.delete
    def getPlane(self):
        return self.plane
    def getIndex(self):
        return self.index
class Clear:
    def __init__(self, planelist):
        self.planelist = planelist
    def getPlaneList(self):
        return self.planelist

actions = []

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

server = 'irc.chat.twitch.tv'                       #server address
port = 6667                                         #port number
sock = socket.socket()                              #creating socket for connection to twitch
sock.connect((server, port))                        #connecting to socket
sock.settimeout(270.0)
token = 'oauth:zsnamwt00lh6bsd7pv0ovywtbhympj'      #oauth key for planerequestbot user. Could be changed if you want to send from another twitch user account
sock.send(f"PASS {token}\n".encode('utf-8'))        #passing oauth key into twitch IRC
nickname = 'planerequestbot'                        #doesn't really matter, could be anything
sock.send(f"NICK {nickname}\n".encode('utf-8'))     #passing nickname to twitch IRC
channel = '#adamtheenginerd'                            #channel name, must be all lowercase and have hashtag before channel name
sock.send(f"JOIN {channel}\n".encode('utf-8'))      #passing channel name to twitch IRC

#Retrieving a new app access token for the viewer count average
url = 'https://id.twitch.tv/oauth2/token?client_id=95hkffpc2ng2zww4gttnp17y0ix14n&client_secret=2anjpsryvwofq6l21o5bhkywltsidw&grant_type=client_credentials'
app_access = requests.post(url)                                                 #getting app access code for oauth credentials
response = str(app_access.text)
response = response.replace("\"", "")
app_access = re.findall('{access_token:(.+),expires_in:', response)
app_access = cleanup(app_access)
app_access = str(app_access)
app_access = app_access.replace("'", "")
print(app_access)
url = 'https://api.twitch.tv/helix/streams?user_login=adamtheenginerd'          #url for getting viewer count
Client_ID = '95hkffpc2ng2zww4gttnp17y0ix14n'                                    #client ID of my program
oauth = 'Bearer '+app_access                                                    #oauth token is Bearer <app_access>
head = {'client-id':Client_ID,'Authorization':oauth}                            #headers to be passed into the API

def getViewers():
    r = requests.get(url, headers = head)
    r = str(r.text)
    if r == "{\"data\":[],\"pagination\":{}}":
        return -1
    else:
        filtered = r.replace("\"", "")
        vcount = re.findall("{data:\[{id:.*,user_id:.*,user_name:.*,game_id:.*,type:.*,title:.*,viewer_count:([0-9]*),started_at:.*", filtered)
        viewercount = cleanup(vcount)
        viewercount = viewercount.replace("'", "")
        viewercount = int(viewercount)
        if viewercount > -1:
            return viewercount
        else:
            return -1

def getUptime():
    r = requests.get(url, headers = head)
    r = str(r.text)
    if r != "{\"data\":[],\"pagination\":{}}":
        filtered = r.replace("\"", "")
        start_time = re.findall("{data:\[{id:.*,user_id:.*,user_name:.*,game_id:.*,type:.*,title:.*,viewer_count:[0-9]*,started_at:(.*),language:.*", filtered)
        start_time = cleanup(start_time)
        start_time = start_time.replace("T", " ")
        start_time = start_time.replace("Z", "")
        start_time = start_time.replace("'", "")
        start_time = datetime.datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
        from datetime import time
        start_time = start_time - datetime.datetime(1970, 1, 1, 4, 0, 0)
        print(datetime.datetime.now().replace(microsecond=0) - start_time)
        return (datetime.datetime.now().replace(microsecond=0) - start_time)

def getAPI():
    r = requests.get(url, headers = head)
    r = str(r.text)
    print(r)

def cleanup2(plane):                                    #function for cleaning up whitespace and non-alpha-numeric characters
    plane = plane.replace("-", "")
    plane = plane.replace(" ", "")
    plane = plane.lower()
    plane = plane.replace("\n", "")
    plane = plane.replace("(", "")
    plane = plane.replace(")", "")
    plane = plane.replace(".", "")
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

def search2(plane):                                                     #better search algorithm
    
    plane = cleanup2(plane)

    if len(plane) <= 2 and plane != "j2" and plane != "j4" and plane != "j6" and plane != "j7" and plane != "t2":
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

def add(string, dictionary):
    if dictionary.get(string, 0) == 0:         #check to see if the user already exists in the dictionary
        dictionary[string] = 1                 #if the user is not there, create a new term and make it equal to one
    else:
        dictionary[string] = dictionary[string] + 1

writerequests = dict()
with open("AllRequests.txt", "r+") as overallhandle:
    for line in overallhandle:
        (key, val) = line.split(",")
        val = val.replace("\n", "")
        val = int(val)
        writerequests[key] = val

authorized = ["adamtheenginerd", "zlayer___", "the_ssn", "kingsman784"]     #users authorized for all commands except track
texthandle = open("logs.txt", 'a+')                 #opening logs file
texthandle.write("Tracking start time: ")
texthandle.write(str(datetime.datetime.now()))               #printing the start time of logging to the file each time the program is run

requesthandle = open("input-output.txt", 'a+')      #opening file for recording requests and the search results for algorithm improvement 

texthandle.write(f"\n{channel}")

def socksend(message):
    sock.send(f"PRIVMSG {channel} :{message}".encode('utf-8'))

requestlist = list()                                #creating empty list of requested planes
go = False                                           #setting program to default disable at start, use --enable command to enable bot
tracking = True                                     #setting tracking to True as default
usercount = dict()                                  #creating empty dictionary for tracking user message counts
commands = {'--disable': 0, '--enable': 0, '--track': 0, '--stoptrack': 0, '--request': 0, '--reqdel': 0, '--skip': 0, '--requests': 0, '--batchrequest':0, '--dellast':0, '--topsimp':0}
count = int(0)
timeout = time.time() + 600                         #anti-disconnect timer

viewertotal = 0
samples = 0
average = 0
planerequests = {}                                       #dictionary to hold requests and results
users = []
confirmations = ['Attack the D point!', 'Bravo, team!', 'Con-gratu-lations!', 'Affirmative!', 'Yes!', 'I agree!', 'Roger that!', 'Excellent!', 'Thank you!',]
getAPI()
print(str(getUptime())[11:])
while True:

    if time.time() > timeout:                               #Contingency against disconnection from IRC
        sock.close()
        sock = socket.socket()                              #creating socket for connection to twitch
        sock.connect((server, port))
        sock.settimeout(270.0)
        sock.send(f"PASS {token}\n".encode('utf-8'))
        sock.send(f"NICK {nickname}\n".encode('utf-8'))
        sock.send(f"JOIN {channel}\n".encode('utf-8'))
        timeout = time.time() + 600

    if getViewers() > -1:
        viewertotal += getViewers()
        samples += 1
        average = viewertotal/samples

    try:
        chat = sock.recv(2048).decode('utf-8')      #receive message
        chat = str(chat)                            #convert to string
    except:
        break
    count = count + 1
    user = re.findall(":.+!.+@(.+)\.tmi\.twitch\.tv", chat)             #pull username out of received message
    user = cleanup(user)
    user = cleanup2(user)                                                #clean up the list object
    user = user.replace("'", "")                                        #remove single quotes
    startmessage = (len(user)) * 3 + len(channel) + 28                  #calculate starting index of message
    message = chat[startmessage:]                                       #pull out the message text
    try:
        print(user + ": " + message.rstrip())                               #print simplified version of user and message
    except:
        if tracking == True and count > 2:
            add(user, usercount)
        continue
    
    if chat.startswith("PING"):               #check for PING from Twitch IRC
        sock.send("PONG\n".encode('utf-8'))     #send "PONG" to stay connected

    if tracking == True and count > 2:                        #if tracking is turned on
        add(user, usercount)
    
    if message.startswith('ssn') or message.startswith("SSN"):
        socksend("Praise ssn!\r\n")

    if "!merch" in message:
        socksend("Adam-scented condoms when?\r\n")

    if "--" not in message and "—" not in message:
        continue

    if "--topsimp" in message or "—topsimp" in message:
        commands['--topsimp'] += 1
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
        socksend(f"{sortedlist[0][0]} is the top simp with {sortedlist[0][1]} messages\r\n")

    if "--disable" in message or "—disable" in message:                 #check for disable command
        if user in authorized:
            go = False
            commands['--disable'] += 1
            print("BotOn = " + str(go))

    elif "--enable" in message or "—enable" in message:                      #check for enable command
        if user in authorized:
            go = True
            commands['--enable'] += 1
            print("BotOn = " + str(go))

    elif "--end" in message or "—end" in message:                   #check for end program command
        if user in authorized:
            break        

    elif '--track' in message or "—track" in message:                     #check for tracking start command
        if user == "adamtheenginerd":
            tracking = True
            commands['--track'] += 1
            print("Tracking = " + str(tracking))

    elif '--stoptrack' in message or "—stoptrack" in message:                 #check for tracking end command
        if user == "adamtheenginerd":
            tracking = False
            commands['--stoptrack'] += 1
            if usercount.get(user, 0) == 0:         #check to see if the user already exists in the dictionary
                usercount[user] = 1                 #if the user is not there, create a new term and make it equal to one
            else:
                usercount[user] = usercount[user] + 1  
            print("Tracking = " + str(tracking))

    elif "--skip[" in message or "—skip[" in message:          #check for a specific plane to skip in the message, only zlayer___  or AdamTheEnginerd can access this command
        if user in authorized:
            commands['--skip'] += 1
            if len(requestlist) > 0:
                plane = re.findall("skip\[(.+)\]", message)
                plane = cleanup(plane)
                plane = plane.replace("'", "")
                try:
                    plane = int(plane)
                    print(plane)
                    skipped = requestlist.pop(plane)
                    socksend(f"{skipped} has been skipped\r\n")
                    actions.insert(0, Action(False, True, skipped, plane))
                except:
                    planeresult = search2(plane)
                    print(planeresult)
                    if planeresult == "No match" or planeresult == "Bombers are useless":
                        planeresult = str(planeresult)
                        socksend(f"Skip failed; {planeresult}\r\n")
                    else:
                        plane = planeresult[0]
                        selected = indexOf(plane, requestlist)
                        skipped = requestlist.pop(selected)
                        if search2(plane)[0] in requestlist:
                            socksend("Skip failed\r\n")
                        else:
                            socksend(f"{skipped} has been skipped\r\n")
                            actions.insert(0, Action(False, True, skipped, selected))
            else:
                socksend("Requestlist is empty\r\n")

    elif "--delLast" in message or "--dellast" in message or "—delLast" in message or "—dellast" in message:
        if user in authorized:
            commands['--dellast'] += 1
            try:
                plane = requestlist.pop(len(requestlist)-1)
                socksend(f"{plane} deleted\r\n")
                actions.insert(0, Action(False, True, plane, len(requestlist)-1))
            except:
                continue

    elif "--reqdel" in message or "—reqdel" in message:             #checking for reqdel command
        if user in authorized:
            commands['--reqdel'] += 1
            buildstring = ""                    #create empty string that will show the list of requested planes
            for plane in requestlist:           #iterate through the planes in the list
                buildstring += plane + ", "     #add the plane to the string and a comma
            if len(requestlist) > 0:            #if there are planes in the requestlist
                socksend(f"{buildstring}\r\n")          #send the string of requested planes to the chat
                removedplane = requestlist.pop(0)                                           #remove the first plane in the list since it will be played. 
                actions.insert(0, Action(False, True, removedplane, 0))
            else:
                socksend("Requestlist is empty\r\n")      #if no planes in the list, send the message that there are no planes in the list

    elif "--requests" in message or "—requests" in message:               #check for requests message. Same code as before, but first plane is not removed
        commands['--requests'] += 1
        buildstring = ""
        for plane in requestlist:
            buildstring += plane + ", "
        if len(requestlist) > 0:
            socksend(f"{buildstring}\r\n")
        else:
            socksend("Requestlist is empty\r\n")

    elif "--commands" in message or "—commands" in message:
        socksend("Learn planerequestbot commands here: https://sites.google.com/view/planerequestbotcommands/home?authuser=0\r\n")
    
    elif "--clear" in message or "—clear" in message:
        if user in authorized:
            planelist = []
            for n in range(len(requestlist)):
                planelist.append(requestlist[n])
            obj = Clear(planelist)
            actions.insert(0, obj)
            requestlist.clear()
            socksend("Request list has been cleared\r\n")
            print(requestlist)

    elif "--batchrequest" in message or "—batchrequest" in message:
        if user in authorized:
            commands['--batchrequest'] += 1
            batch = re.findall("--batchrequest (.+)", message)
            batch = cleanup(batch)
            batch = batch.replace("'", "")
            batchlist = batch.split(",")
            for plane in batchlist:
                result = search2(plane)
                planerequests[plane] = str(result)
                if result == "No match":
                    continue
                elif result == "Bombers are useless":
                    continue
                else:
                    planeresult = str(result[0])
                    planeresult = planeresult.replace("\n", "")
                    if indexOf(planeresult, requestlist) > -1:
                        socksend(f"{planeresult} is a duplicate\r\n")
                    elif planeresult in rmnsDict:
                        if rmnsDict[planeresult] in requestlist:
                            socksend(f"{planeresult} is a duplicate\r\n")
                        else:
                            confirmation = random.randint(0, len(confirmations)-1)
                            if indexDict(planeresult, rmnsDict) > 54:
                                requestlist.append(rmnsDict[planeresult])
                                obj = Action(True, False, rmnsDict[planeresult], len(requestlist)-1)
                                actions.insert(0, obj)
                                add(rmnsDict[planeresult], writerequests)
                            else:
                                requestlist.append(planeresult)
                                obj = Action(True, False, planeresult, len(requestlist)-1)
                                actions.insert(0, obj)
                                add(planeresult, writerequests)
                    else:
                        requestlist.append(planeresult)                         #same as above
                        obj = Action(True, False, planeresult, len(requestlist)-1)
                        actions.insert(0, obj)
                        add(planeresult, writerequests)
                        print(requestlist)              #print the list

    elif "--undo" in message or "—undo" in message:
        if user in authorized:
            if len(actions) > 0:
                obj = actions[0]
                if type(obj) == Clear:
                    for plane in obj.getPlaneList():
                        requestlist.append(plane)
                elif type(obj) == Action:
                    if obj.getAdd():
                        requestlist.pop(obj.getIndex())
                    elif obj.getDelete():
                        requestlist.insert(obj.getIndex(), obj.getPlane())
                actions.pop(0)
            else:
                socksend("No previous actions\r\n")
            print(requestlist)

    elif "--avgvcount" in message or "—avgvcount" in message:
        sentin = str(int(average))
        socksend(f"Average viewer count: {sentin}\r\n")

    elif "--uptime" in message or "—uptime" in message:
        uptime = getUptime()
        uptime = str(uptime)[11:]
        print(uptime)
        sock.send(f"PRIVMSG {channel} :Stream uptime: {uptime}\r\n".encode('utf-8'))

    if go == True:                              #--request command only works when go is True
        
        if "--pick" in message or "—pick" in message:
            if user in authorized:
                try:
                    socksend(f"{requestlist[randrange(len(requestlist))]} has been chosen by the gods\r\n")
                except:
                    continue
                                                                
        if "--request " in message or "—request" in message:                                         #checking for request command
            if user not in users:
                commands['--request'] += 1
                plane = re.findall("request (.+)", message)                   #pull out the plane name
                plane = cleanup(plane)                                          #clean up the list object
                plane = plane.replace("'", "")                                  #replace single quotes with nothing
                result = search2(plane)                                         #perform search algorithm
                planerequests[plane] = str(result)
                if result == "No match":                                        #if match is not above threshold, algo returns "No match"
                    socksend("No match\r\n")                                    #send chat
                elif result == "Bombers are useless":                           #if algo determines that the request is a bomber
                    socksend("Bombers are useless\r\n")    #send chat message
                else:
                    planeresult = str(result[0])                                #pull out the actual plane
                    planeresult = planeresult.replace("\n", "")                 #replace newline character
                    if indexOf(planeresult, requestlist) > -1:                  #if the plane is in the requestlist already
                        socksend(f"{planeresult} is a duplicate\r\n")   #duplicate message to chat
                    elif planeresult in rmnsDict:                               #if it is a roman numeral plane with mulitple correct versions
                        if rmnsDict[planeresult] in requestlist:                #and if the counterpart of the planeresult is already in the request list
                            socksend(f"{planeresult} is a duplicate\r\n")   #send duplicate message
                        else:
                            confirmation = random.randint(0, len(confirmations)-1)  #random War Thunder quote
                            if indexDict(planeresult, rmnsDict) > 54:
                                requestlist.append(rmnsDict[planeresult])
                                original = rmnsDict[planeresult]
                                socksend(f"{confirmations[confirmation]} {original} requested!\r\n")
                                actions.insert(0, Action(True, False, original, len(requestlist)-1))
                                add(original, writerequests)
                                users.append(user)
                            else:
                                requestlist.append(planeresult)                     #Otherwise, add the request to the request list
                                socksend(f"{confirmations[confirmation]} {planeresult} requested!\r\n")     #confirmation message
                                actions.insert(0, Action(True, False, planeresult, len(requestlist)-1))
                                add(planeresult, writerequests)
                                users.append(user)
                    else:
                        requestlist.append(planeresult)                         #same as above
                        confirmation = random.randint(0, len(confirmations)-1)
                        socksend(f"{confirmations[confirmation]} {planeresult} requested!\r\n")
                        actions.insert(0, Action(True, False, planeresult, len(requestlist)-1))
                        add(planeresult, writerequests)
                        print(requestlist)              #print the list
                        users.append(user)
            else:
                socksend("You have already made your request")
                continue

sortedlist = list()                         #creating empty list to hold sorted users
for thing in usercount.items():             #iterate through the keys and terms of usercount dictionary
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
texthandle.write("{0:<12}{1:>12}\n".format("Username", "Messages"))
for item in sortedlist:
    print(item[0], str(item[1]))
    texthandle.write("{0:<20}{1:>4}\n".format(str(item[0]), str(item[1])))        #writing sortedlist data to file

texthandle.write("Number of requests: " + str(commands['--request']) + "\n")
texthandle.write("Tracking end time: ")
texthandle.write(str(datetime.datetime.now()) + "\n\n")

for request in planerequests:                                    #writing requests and results to the input-output file for debugging purposes
    buildstring = ""
    buildstring += request
    for n in range(23-len(request)):
        buildstring += "-"
    buildstring += ">"
    buildstring += str(planerequests[request])
    buildstring += "\n"
    requesthandle.write(buildstring)

with open("AllRequests.txt", "r+") as overallhandle:        #writing overall requests to the permanent record
    sortedlist2 = list()
    for thing in writerequests.items():
        sortedlist2.append(thing)
    for i in range(1, len(sortedlist2)):         #insertion sort algorithm
        nextElementValue = sortedlist2[i][1]
        temp = sortedlist2[i]
        j = i-1
        while j >= 0 and sortedlist2[j][1] < nextElementValue:
            item = sortedlist2[j]
            sortedlist2[j+1] = item
            j = j-1
        sortedlist2[j+1] = temp
    texthandle.write("\n")
    for request in writerequests.items():
        overallhandle.write(request[0] + "," + str(request[1]) + "\n")

requesthandle.close()
overallhandle.close()
texthandle.close()      #closing connection to file
sock.close()            #closing connection to Twitch IRC