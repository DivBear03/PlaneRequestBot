import requests
import re
from bs4 import BeautifulSoup 
ign = input("Enter your ign: ")
content_length = 0
url = f"https://warthunder.com/en/community/userinfo/?nick={ign}"
print("POSTing ", url)
headers = {
    "User-Agent" : "PostmanRuntim/7.26.1",
    "Accept" : "*/*",
    "Postman-Token" : "56d530b5-8783-4c1e-bd07-d1331ad877ad",
    "Host" : "warthunder.com",
    "Accept-Encoding" : "gzip, deflate, br",
    "Connection" : "keep-alive",
    "Cookie" : "__cfduid=dac78b3134a76b92845ca7cf5ae3483cc1594903861; language=en; conntrack=jlsIbF8QTdai4Ui6A8+wAg==",
    "Content-Length" : "0"
}
r = requests.post(url = url, headers = headers)
r = str(r.text)
print(r)
li_tags = re.findall("<li class=\"profile-stat_list-item\">(.+)</li>", r)
print(li_tags)