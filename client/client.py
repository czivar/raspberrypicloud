#!/usr/bin/python
import os
from bottle import route, run, template
from datetime import timedelta
import json

@route('/start/:name')
def startvm(name):
    with open('vms', 'a') as f:
	f.write(name+"\n")
	f.close()
    
@route('/stop/:name')
def stopvm(name):
    f=open('vms', 'r')
    lines = f.readlines()
    f.close()
    f = open('vms', 'w')
    for line in lines:
     if not line.startswith(name):
      f.write(line)
    f.close()

@route('/getvmlist')
def getvms():
    f = open('vms', 'r')
    vmlist = [ line.strip().split()[0] for line in f.readlines() ]
    return json.dumps(vmlist)

@route('/getloadavg')
def getload():
    return template('{{name}}', name=os.getloadavg())

@route('/getuptime')
def getuptime():
    with open('/proc/uptime', 'r') as f:
     uptime_seconds = float(f.readline().split()[0])
     uptime_string = str(timedelta(seconds = uptime_seconds))
    return template('{{name}}', name=uptime_string)

if not os.path.exists('vms'): 
    open('vms', 'w').close() 

run(host='0.0.0.0', port=9999, debug=True)
