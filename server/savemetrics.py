#!/usr/bin/env python
import os, sys

PATH_APP='/home/richardson/public_html/management/'

if PATH_APP not in sys.path:
    sys.path.append(PATH_APP)

os.environ["DJANGO_SETTINGS_MODULE"] = "www.settings"

import time
import datetime
import urllib
from cluster.models import *

CHECK_PERIOD = 30

while True:
	for node in Node.objects.all():
		currenttime = datetime.datetime.now()
		if node.state == 1:
			try:
				load = urllib.urlopen("http://"+node.name+":9999/getloadavg").read() #TODO modell ala vinni minden ilyet
				perfdata = NodePerformanceData(node=node, date=currenttime, value=load)
				perfdata.save()
				if __debug__: print 'Node info saved %s' % node.name
			except IOError as e:
				if __debug__ : print 'problem: %s' % e.strerror
		else:
				perfdata = NodePerformanceData(node=node, date=currenttime, value=0)
				perfdata.save()
			
	time.sleep(CHECK_PERIOD)	
