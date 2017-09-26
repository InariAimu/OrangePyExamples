#!/usr/bin/env python

from pyA20.gpio import gpio
from pyA20.gpio import port

import socket
import time
import json


#must be modified===
DEVICEID='your_device_id'
APIKEY='your_api_key'
#modify end=========

host="www.bigiot.net"
port=8181

gpio.init() #Initialize module. Always called first
gpio.setcfg(10, 1)

#connect bigiot
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.settimeout(0)
while True:
	try:
		s.connect((host,port))
		break
	except:
		print('waiting for connect bigiot.net...')
		time.sleep(2)

#check in bigiot
checkinBytes=bytes('{\"M\":\"checkin\",\"ID\":\"'+DEVICEID+'\",\"K\":\"'+APIKEY+'\"}\n')
s.sendall(checkinBytes)

#keep online with bigiot function
data=b''
flag=1
t=time.time()
def keepOnline(t):
	if time.time()-t>40:
		s.sendall(b'{\"M\":\"status\"}\n')
		print('check status')
		return time.time()
	else:
		return t

#say something to other device function
def say(s,id,content):
	sayBytes=bytes('{\"M\":\"say\",\"ID\":\"'+id+'\",\"C\":\"'+content+'\"}\n')
	s.sendall(sayBytes)

#deal with message coming in
def process(msg,s,checkinBytes):
	msg=json.loads(msg)
	if msg['M'] == 'connected':
		s.sendall(checkinBytes)
	if msg['M'] == 'login':
		say(s,msg['ID'],'Welcome! Your public ID is '+msg['ID'])
	if msg['M'] == 'say':
		say(s,msg['ID'],'You have send to me:{'+msg['C']+'}')
		if msg['C'] == "play":
			#led.on()
			gpio.output(10,0)
			say(s,msg['ID'],'LED turns on!')
		if msg['C'] == "stop":
			#led.off()
			gpio.output(10,1)
			say(s,msg['ID'],'LED turns off!')
	#for key in msg:
	#	print(key,msg[key])
	#print('msg',type(msg))

#main while
while True:
	try:
		d=s.recv(1)
		flag=True
	except:
		flag=False
		time.sleep(1)
		t = keepOnline(t)
	if flag:
		if d!=b'\n':
			data+=d
		else:
			msg=str(data)
			process(msg,s,checkinBytes)
			print(msg)
			data=b''
