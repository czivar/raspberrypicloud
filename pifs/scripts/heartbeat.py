#!/usr/bin/python 
import socket, time
import urllib2
import json
import subprocess
import sys, getopt
import json
import signal


SERVER = 'pimaster'
SERVER_PORT = 43278
BEAT_PERIOD = 4
MAX_MHZ = 500

lookbusy_path = '/home/pi/pifs/lookbusy'

hostname = socket.gethostname()

# { vm: subprocess_reference , vm: subprocess_reference }
runningvms = dict()

def vmmanagement(vmlist):
	delvms = list()
	for vm, template in vmlist.iteritems():
		if runningvms.get(vm) is None:
			if __debug__: print 'starting load'
			cpupercent = int(100 * float(template[0])/float(MAX_MHZ))
			loadprocess = subprocess.Popen([lookbusy_path,
				'-q',
				'-n 1',
				'-c', str(cpupercent),
				'-m', str(template[1])+'MB',
				'-d', str(template[2])+'MB'])
			runningvms[vm] = loadprocess
	for vm, process in runningvms.iteritems():
		if vmlist.get(vm) is None:
			if __debug__: print 'ending load'
			process.terminate()
			delvms.append(vm)
	for vm in delvms:
		del runningvms[vm]

while True:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
     s.connect((SERVER, SERVER_PORT))
     rawdata = urllib2.urlopen("http://"+SERVER+":9999/getvms/"+hostname).read()
     vmlist = json.loads(rawdata)
     vmmanagement(vmlist)
     print runningvms
     s.sendto('hello', (SERVER, SERVER_PORT))
     s.close()
    except Exception as e:
     if __debug__: print 'Where are you, server', e
    if __debug__: print 'Time: %s' % time.ctime()
    time.sleep(BEAT_PERIOD)
