import socket           #importing useful modules
import time
from datetime import datetime
from datetime import timedelta
import difflib
from difflib import SequenceMatcher
import random
import scipy.stats
from random import randrange
from time import sleep
import requests
import re



def cleanup(chat):                                                      #function for cleaning up a list converted to a strings
    chat = str(chat)
    chat = chat.replace("[", "")
    chat = chat.replace("]", "")
    chat = chat.replace("\\r", "")
    chat = chat.replace("'", "")
    chat = chat.strip()
    return chat



url = 'https://id.twitch.tv/oauth2/token?client_id=95hkffpc2ng2zww4gttnp17y0ix14n&client_secret=2anjpsryvwofq6l21o5bhkywltsidw&grant_type=client_credentials'
app_access = requests.post(url)
print(app_access.text)
response = str(app_access.text)
response = response.replace("\"", "")
app_access = re.findall('{access_token:(.+),expires_in:', response)
app_access = cleanup(app_access)
app_access = str(app_access)
print(app_access)
url = 'https://api.twitch.tv/helix/streams?user_login=dudewithopinions'
Client_ID = '95hkffpc2ng2zww4gttnp17y0ix14n'
oauth = 'Bearer '+app_access
head = {'client-id':Client_ID,'Authorization':oauth}
def getViewers():
    r = requests.get(url, headers = head)
    r = str(r.text)
    filtered = r.replace("\"", "")
    count = re.findall("{data:\[{id:.+,user_id:.+,user_name:.+,game_id:.+,type:.+,title:.+,viewer_count:([0-9]+),started_at:.+", filtered)
    viewercount = cleanup(count)
    viewercount = viewercount.replace("'", "")
    try:
        return int(viewercount)
    except:
        return -1
viewertotal = 0
samples = 0
average = 0
sampletimer = time.time()
while True:
    if time.time() > sampletimer:
        sampletimer = time.time() + 2
        r = requests.get(url, headers = head)
        r = str(r.text)
        filtered = r.replace("\"", "")
        count = re.findall("{data:\[{id:.+,user_id:.+,user_name:.+,game_id:.+,type:.+,title:.+,viewer_count:([0-9]+),started_at:.+", filtered)
        viewercount = cleanup(count)
        viewercount = viewercount.replace("'", "")
        try:
            viewercount = int(viewercount)
            print(viewercount)
            viewertotal += viewercount
            samples += 1
            average = viewertotal/samples
        except:
            continue
    