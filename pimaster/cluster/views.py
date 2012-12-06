# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
import datetime
from django.template import RequestContext
import urllib
from cluster.models import *
from collections import defaultdict
import json
import os
import time
from random import choice
from django.http import HttpResponseRedirect
from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.admin.models import LogEntry
from cluster import forms
from django.core.urlresolvers import reverse

actives_file = "/home/richardson/public_html/management/cluster/actives"


@login_required
def templates(request):
	templates = Template.objects.filter(user = request.user)
	if request.method == 'POST':
		form = forms.TemplateForm(request.POST)
		if form.is_valid():
			newtemplate = form.save(commit=False)
			newtemplate.user = request.user
			newtemplate.save()
			return HttpResponseRedirect(reverse('templates'))
		else:
			return render_to_response('templates.html', { 'form' : form, 'templates': templates }, context_instance=RequestContext(request))
	else:                                    
		form = forms.TemplateForm()   
		return render_to_response('templates.html', { 'form' : form, 'templates': templates }, context_instance=RequestContext(request))

@login_required
def template_delete(request, id):
	template = get_object_or_404(Template, pk=id)
	template.delete()
	return HttpResponseRedirect(reverse('templates'))

@login_required
def template(request,id):
	template = get_object_or_404(Template, pk=id)
	return render_to_response('template.html', { 'template': template }, context_instance=RequestContext(request))

@login_required
def vms(request):
	vms = VM.objects.filter(user = request.user)
	if request.method == 'POST':
		form = forms.VMForm(request.POST)
		if form.is_valid():
			newvm = form.save(commit=False)
			newvm.user = request.user
			newvm.save()
			return HttpResponseRedirect(reverse('vms'))
		else:
			return render_to_response('vms.html', { 'form' : form, 'vms': vms }, context_instance=RequestContext(request))
	else:                                    
		form = forms.VMForm()
		form.fields["template"].queryset = Template.objects.filter(user=request.user)
		return render_to_response('vms.html', { 'form' : form, 'vms': vms }, context_instance=RequestContext(request))

@login_required
def vm_delete(request, id):
	vm = get_object_or_404(VM, pk=id)
	vm.delete()
	return HttpResponseRedirect(reverse('vms'))

@login_required
def vm(request,id):
	vm = get_object_or_404(VM, pk=id)
	return render_to_response('vm.html', { 'vm': vm }, context_instance=RequestContext(request))

@login_required
def services(request):
	return HttpResponseRedirect(reverse('templates'))

@login_required
def profile(request):
	user = request.user
	templates = Template.objects.filter( user = request.user).count()
	vms = VM.objects.filter( user = request.user).count()
	logentries = LogEntry.objects.filter(user = request.user)[:15]
	return render_to_response('profile.html', { 'user': user , 'logentries' : logentries, 'templates' : templates , 'vms': vms },
		 context_instance=RequestContext(request)) 

@login_required
def logout_view(request):
	logout(request)
	return HttpResponseRedirect('/management/')

def getVmList():
	cluster = dict()
	active = getActiveNodes()
	nodes = Node.objects.all()
	for node in nodes:
		if node.name in active:
			try:
				purelist = json.loads(urllib.urlopen("http://"+node.ip+":9999/getvmlist").read())
			except IOError:
				purelist = []
		else:
			purelist = []
		id = filter(lambda x: x.isdigit(), node.name)
		cluster[int(id)] = purelist
	return cluster

def getActiveNodes():
	return json.loads(open(actives_file).read())

@login_required
def vmstart(request):
	actives = getActiveNodes()
	nodeid = choice(actives)
	if request.method == 'POST':
		form = StartVMForm(request.POST)
		if form.is_valid():
			name = form.cleaned_data['name']
			node = form.cleaned_data['node']
			if not node.startswith('auto'):
				a = urllib.urlopen("http://"+node+":9999/start/"+name).read()
			else:
				a = urllib.urlopen("http://pi"+str(nodeid)+":9999/start/"+name).read()
		return HttpResponseRedirect('/management/')
	else:
		form = StartVMForm()
	return render(request, 'vm.html', {
	    'form': form,
	})


@login_required
def nodes(request):
	nodes = Node.objects.all()
	actives = Node.objects.filter(state=2)
	offlines = Node.objects.filter(state=1)
	lastcheck = time.ctime(os.path.getmtime(actives_file))
	usage = '{0:.0f}%'.format( float(len(actives)) / len(nodes) *100)
	return render_to_response('nodes.html', {'nodes': nodes, 'actives': actives, 'offlines': offlines, 'usage': usage, 'lastcheck': lastcheck}, context_instance=RequestContext(request))

@login_required
def node(request, nodeid):
    try:    
     load = urllib.urlopen("http://pi"+nodeid+":9999/getloadavg").read()
     uptime = urllib.urlopen("http://pi"+nodeid+":9999/getuptime").read()
     vms = json.loads(urllib.urlopen("http://pi"+nodeid+":9999/getvmlist").read())
     return render_to_response('node.html', {'nodeid': nodeid, 'load': load, 'vms': vms, 'uptime': uptime }, context_instance=RequestContext(request))
    except IOError:
     uptime = "offline"
     return render_to_response('node.html', { 'uptime': uptime }, context_instance=RequestContext(request))

@login_required
def home(request):
	nodes = Node.objects.all()
	return render_to_response('index.html', {'vmlist': getVmList(), 'nodes': nodes }, context_instance=RequestContext(request))
	 
