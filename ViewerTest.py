import socket           #importing useful modules
import time
import datetime
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
url = 'https://api.twitch.tv/helix/streams?user_login=twitchrivals'
Client_ID = '95hkffpc2ng2zww4gttnp17y0ix14n'
oauth = 'Bearer '+app_access
head = {'client-id':Client_ID,'Authorization':oauth}
r = requests.get(url, headers = head)
print(type(r))
r = str(r.text)
print(r)
if r != "{\"data\":[],\"pagination\":{}}":
    filtered = r.replace("\"", "")
    start_time = re.findall("{data:\[{id:.+,user_id:.+,user_name:.+,game_id:.+,type:.+,title:.+,viewer_count:[0-9]+,started_at:(.+),language:.+", filtered)
    start_time = cleanup(start_time)
    start_time = start_time.replace("T", " ")
    start_time = start_time.replace("Z", "")
    start_time = datetime.datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
    from datetime import time
    start_time = start_time - datetime.datetime(1970, 1, 1, 4, 0, 0)
    print(datetime.datetime.now().replace(microsecond=0) - start_time)