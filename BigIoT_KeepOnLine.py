#!/usr/bin/python3
import socket
import os
import time
from datetime import datetime

#must be modified===
DEVICEID='your_device_id'
APIKEY='your_api_key'
DATAID='your_data_id'
#modify end=========

host="www.bigiot.net"
port=8181
checkinBytes=bytes('{\"M\":\"checkin\",\"ID\":\"'+DEVICEID+'\",\"K\":\"'+APIKEY+'\"}\n',encoding='utf8')
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
while True:
	try:
		s.connect((host,port))
		break
	except:
		print('waiting for connect bigiot.net...')
		time.sleep(2)
		
s.settimeout(0)
s.sendall(checkinBytes)
data=b''
flag=1
t=time.time()

def keepOnline(t):
	if time.time()-t>15:
		output=os.popen('cat /sys/devices/virtual/hwmon/hwmon1/temp1_input')
		temp=(output.read()).replace('\n','')
		print(temp)
		line='{\"M\":\"update\",\"ID\":\"'+DEVICEID+'\",\"V\":{\"'+DATAID+'\":\"'+temp+'\"}}\n'
		s.sendall(bytes(line,encoding='utf8'))
		return time.time()
	else:
		return t
	
while True:
	try:
		d=s.recv(1)
		flag=True
	except:
		flag=False
		time.sleep(2)
		t = keepOnline(t)
	if flag:
		if d!=b'\n':
			data+=d
		else:
			#do something here...
			print(str(data,encoding='utf-8'))
			data=b''
			
