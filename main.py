import login
import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time
import matplotlib.pyplot as plt
import matplotlib.dates as md
import os
import dateutil
from config import *

with open(configFile, "r", encoding='utf-8') as f:
	info = json.load(f)

session = requests.Session()
session.cookies = requests.cookies.RequestsCookieJar()
session.headers["User-Agent"] = agent
session.headers["Accept"] = "application/json, text/plain, */*"
session.headers["Accept-Encoding"] = "gzip, deflate"
session.headers["Connection"] = "keep-alive"
session.headers["Accept-Language"] = "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7"

assert 'student_id' in info, "Expected infomation `student_id` not found. Check config.json"
assert "password" in info, "Expected infomation `password` not found. Check config.json"

login.login(session, username=info['student_id'], password=info['password'])
msg = session.get(urls['electric'])
# print(msg.text)
soup = BeautifulSoup(msg.text, 'html.parser')
txt = soup.find_all('script')[-1].text
index = txt.find('dfyl')
txt = txt[index:index+20]
index1 = txt.find(':')
index2 = txt.find('}')
try:
	ele = float(txt[index1+1:index2])
except ValueError:
	print("Login failed.")
	exit(-1)
cur_time = str(time.time())
with open(outputFile, "a") as f:
	f.write(cur_time + " " + str(ele) + "\n")

T = []
R = []
with open(outputFile, "r") as f:
	for line in f:
		line = line.strip()
		t, r = line.split(" ")
		t = dateutil.parser.parse(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(float(t))))
		r = float(r)
		T.append(t)
		R.append(r)
# print(T)
# print(R)
fig = plt.gca()
fig.set_xticks(T)
xfmt = md.DateFormatter("%m-%d %H")
fig.xaxis.set_major_formatter(xfmt)
fig.set_yticks(R)
plt.plot(T, R, "o-")
plt.savefig(outputFig, dpi = 500, bbox_inches = 'tight')