#!/usr/bin/python
import os, sys
from bottle import route, run, template
from datetime import timedelta
import json

PATH_APP='/home/richardson/public_html/management/'

if PATH_APP not in sys.path:
    sys.path.append(PATH_APP)

os.environ["DJANGO_SETTINGS_MODULE"] = "www.settings"

from cluster.models import *

@route('/getvms/:name')
def getvms(name):
	VM.objects.update()
	Node.objects.update()
	node = Node.objects.get(name=name)
	vms = VM.objects.filter(node=node)
	vmlist = dict()
	for vm in vms:
		if vm.state == 1:
			vmtemplate = Template.objects.get(pk=vm.template.id)
			templatelist = [vmtemplate.cpu, vmtemplate.memory, vmtemplate.disk]
			vmlist[vm.id] = templatelist
	return template('{{!vmlist}}', vmlist=json.dumps(vmlist, sort_keys=True))
	

run(reloader = True, host='0.0.0.0', port=9999, debug=False)
