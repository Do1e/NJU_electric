from bs4 import BeautifulSoup
import ddddocr
import execjs
import urllib
import re
from config import *

def encrypt(password, encrypt_salt):
	with open(encrypt_js_script, 'r') as f: 
		script = ''.join(f.readlines())
	context = execjs.compile(script)
	return context.call('encryptAES', password, encrypt_salt)

def readcode(session):
	r = session.get(urls['captcha'])
	ocr = ddddocr.DdddOcr(show_ad=False)
	res = ocr.classification(r.content)
	return res

def login(session, username, password):
	code = readcode(session)
	r = session.get(urls['login'])
	soup = BeautifulSoup(r.text, 'html.parser')
	input_boxes = soup.find_all('input')
	
	input_info = {}
	for i in input_boxes:
		name, value = i.get('name'), i.get('value')
		if name not in ["username", "password", "captchaResponse", None]:
			input_info[name] = value 
	
	pattern = re.compile(r"var pwdDefaultEncryptSalt = (.*?);", re.MULTILINE | re.DOTALL)
	encrypt_script = str(soup.find("script", text=pattern))
	pwdDefaultEncryptSalt = re.search('pwdDefaultEncryptSalt = "(.*?)";', encrypt_script).group(1)
	headers = {
		'User-Agent': agent,
		'Origin': "https://authserver.nju.edu.cn",
		'Referer': urls['login'],
		'Content-Type': 'application/x-www-form-urlencoded',
		'Connection': 'keep-alive',
		'Accept': 'application/json, text/plain, */*',
		'Accept-Encoding': 'gzip, deflate',
		'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7'
	}

	data = {
		'username': username,
		'password': encrypt(password, pwdDefaultEncryptSalt),
		'captchaResponse': code,
		'lt': input_info["lt"],
		'dllt': input_info["dllt"],
		'execution': input_info["execution"],
		'_eventId': input_info["_eventId"],
		'rmShown': input_info["rmShown"]
	}
	session.post(urls['login'], data=urllib.parse.urlencode(data), headers=headers)