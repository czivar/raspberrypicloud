#!/usr/bin/python
import os
from bottle import route, run, template
from datetime import timedelta
import json

@route('/getloadavg')
def getload():
    return template('{{name}}', name=os.getloadavg()[0])

@route('/getuptime')
def getuptime():
    with open('/proc/uptime', 'r') as f:
     uptime_seconds = float(f.readline().split()[0])
     uptime_string = str(timedelta(seconds = uptime_seconds))
    return template('{{name}}', name=uptime_string)

run(host='0.0.0.0', port=9999, debug=False)
