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
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.admin.models import LogEntry
from cluster import forms
from django.core.urlresolvers import reverse
from django.core.exceptions import ValidationError
from django.db.models import Count
import operator
from django.contrib.admin.models import LogEntry
from django.contrib.contenttypes.models import ContentType

@login_required
def log_it(request, object, change_message, action_name):
	if action_name == "insert" : action_flag = 1
	if action_name == "update" : action_flag = 2
	if action_name == "delete" : action_flag = 3
	
	LogEntry.objects.log_action(
        user_id         = request.user.id, 
        content_type_id = ContentType.objects.get_for_model(object).pk, 
        object_id       = object.pk, 
        object_repr     = change_message, # Message you want to show in admin action list
        change_message  = change_message, # I used same
        action_flag     = action_flag
    )

@staff_member_required
def users(request):
	users = User.objects.all()
	for user in users:
		user.vms = VM.objects.filter(user=user).count()
		user.templates = Template.objects.filter(user=user).count()
	if request.method == 'POST':
		form = forms.CreateUserForm(request.POST)
		if form.is_valid():
			try:
				User.objects.get(username=form.cleaned_data['username']) 
			except User.DoesNotExist:
				new_user=User.objects.create_user(form.cleaned_data['username'],
												  form.cleaned_data['email'],
												  form.cleaned_data['password'])
				new_user.first_name = form.cleaned_data['first_name']
				new_user.last_name = form.cleaned_data['last_name']
				new_user.save()
				log_it(request, new_user, "User has been created.", "insert")
			return HttpResponseRedirect(reverse('users'))
		else:
			return render_to_response('users.html', { 'form' : form, 'users': users }, context_instance=RequestContext(request))
	else:                                    
		form = forms.CreateUserForm() 
		return render_to_response('users.html', { 'form' : form, 'users': users }, context_instance=RequestContext(request))

@staff_member_required
def user_delete(request, id):
	user = get_object_or_404(User, pk=id)
	user.delete()
	log_it(request, user, "User has been deleted.", "delete")
	return HttpResponseRedirect(reverse('users'))

@login_required
def templates(request):
	if request.user.is_staff:
		templates = Template.objects.all()
	else:
		templates = Template.objects.filter(user = request.user)
	if request.method == 'POST':
		form = forms.TemplateForm(request.POST)
		if form.is_valid():
			newtemplate = form.save(commit=False)
			newtemplate.user = request.user
			newtemplate.save()
			log_it(request, newtemplate, "Template has been created.", "insert")
			return HttpResponseRedirect(reverse('templates'))
		else:
			return render_to_response('templates.html', { 'form' : form, 'templates': templates, 'user': request.user }, context_instance=RequestContext(request))
	else:                                    
		form = forms.TemplateForm() 
		return render_to_response('templates.html', { 'form' : form, 'templates': templates, 'user': request.user }, context_instance=RequestContext(request))

@login_required
def template_delete(request, id):
	template = get_object_or_404(Template, pk=id)
	if template.user == request.user or request.user.is_staff :
		template.delete()
		log_it(request, template, "Template has been deleted.", "delete")
	return HttpResponseRedirect(reverse('templates'))

@login_required
def template(request,id):
	template = get_object_or_404(Template, pk=id)
	if template.user == request.user or request.user.is_staff:
		if request.method == 'POST':
			form = forms.TemplateForm(request.POST, instance=template)
			if form.is_valid():
				template = form.save(commit=False)
				template.save()
				log_it(request, template, "Template has been updated.", "update")
				return HttpResponseRedirect(reverse('templates'))
			else:
				return render_to_response('template.html', { 'form' : form, 'id': id }, context_instance=RequestContext(request))
		else:
			form = forms.TemplateForm(instance=template)
			return render_to_response('template.html', { 'form' : form, 'id' : id }, context_instance=RequestContext(request))
	else:
		return HttpResponseRedirect(reverse('templates'))
	
def getFreeNode():
	return Node.objects.all().filter(state=1).annotate(num_vms=Count('vm')).filter(state=1).order_by('num_vms')[0]

@login_required
def vms(request):
	if request.user.is_staff:
		vms = VM.objects.all()
	else:
		vms = VM.objects.filter(user = request.user)
	if request.method == 'POST':
		form = forms.VMForm(request.POST)
		if form.is_valid():
			newvm = form.save(commit=False)
			newvm.user = request.user
			if Node.objects.all().filter(state=1) :
				newvm.node = getFreeNode() 
				newvm.save()
				log_it(request, newvm, "Virtual machine has been created.", "insert")
			return HttpResponseRedirect(reverse('vms'))
		else:
			return render_to_response('vms.html', { 'form' : form, 'vms': vms, 'user': request.user }, context_instance=RequestContext(request))
	else:                                    
		form = forms.VMForm()
		form.fields["template"].queryset = Template.objects.filter(user=request.user)
		return render_to_response('vms.html', { 'form' : form, 'vms': vms }, context_instance=RequestContext(request))

@login_required
def vm_delete(request, id):
	vm = get_object_or_404(VM, pk=id)
	if vm.user == request.user or request.user.is_staff :
		vm.delete()
		log_it(request, vm, "Virtual machine has been deleted.", "delete")
	return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))	

@login_required
def vm_start(request, id):
	vm = get_object_or_404(VM, pk=id)
	if vm.user == request.user or request.user.is_staff :
		vm.state = 1
		vm.save() 
		log_it(request, vm, "Virtual machine has been started.", "update")
	return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))	

@login_required
def vm_stop(request, id):
	vm = get_object_or_404(VM, pk=id)
	if vm.user == request.user or request.user.is_staff :
		vm.state = 6
		vm.save() 
		log_it(request, vm, "Virtual machine has been stopped.", "update")
	return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))	

@staff_member_required
def vm_migrate(request, vmid, destnode):
	vm = get_object_or_404(VM, pk=vmid)
	dnode = get_object_or_404(Node, name=destnode)
	if dnode.state == 1 :
		vm.node = dnode
		vm.save() 
		log_it(request, vm, "Virtual machine has been migrated.", "update")
	return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))	

@login_required
def profile(request):
	user = request.user
	templates = Template.objects.filter(user = user).count()
	vms = VM.objects.filter(user = user)
	usingcpu = 0
	usingmem = 0
	usingdisk = 0
	for i in vms:
		if i.state == 1:
			usingcpu += i.template.cpu
			usingmem += i.template.memory
			usingdisk += i.template.disk
	logentries = LogEntry.objects.order_by('-action_time').filter(user = user)[:15]
	return render_to_response('profile.html', { 'user': user , 'logentries' : logentries, 'templates' : templates , 'vms': vms.count(), 'usingcpu': usingcpu , 'usingmem': usingmem, 'usingdisk': usingdisk },
		 context_instance=RequestContext(request)) 

@login_required
def logout_view(request):
	logout(request)
	return HttpResponseRedirect('/management/')

@staff_member_required
def nodes(request):
	nodes = Node.objects.all()
	actives = Node.objects.filter(state=2)
	offlines = Node.objects.filter(state=1)
	usage = '{0:.0f}%'.format( float(len(actives)) / len(nodes) *100)
	return render_to_response('nodes.html', {'nodes': nodes, 'actives': actives, 'offlines': offlines, 'usage': usage }, context_instance=RequestContext(request))

@staff_member_required
def node(request, nodename):
    try:    
     load = urllib.urlopen("http://"+nodename+":9999/getloadavg").read()
     uptime = urllib.urlopen("http://"+nodename+":9999/getuptime").read()
    except IOError:
     uptime = "offline"
     node = get_object_or_404(Node, name=nodename)
     node.state = 2
     node.save() 
     load = 0
    node = Node.objects.get(name=nodename) 
    vms = VM.objects.filter(node=node)
    perfdata = NodePerformanceData.objects.values_list('value', flat=True).order_by('-date').filter(node=node)[:20]
    return render_to_response('node.html', {'node': node, 'load': load, 'vms': vms, 'uptime': uptime, 'perfdata': reversed(perfdata) }, context_instance=RequestContext(request))

@login_required
def home(request):
	nodes = Node.objects.all()
	if request.user.is_staff:
		cluster = dict()
		perfdata = list()
		for node in Node.objects.all():
			cluster[int(filter(lambda x: x.isdigit(), node.name))] = VM.objects.filter(node=node)
		for i in nodes:
			perf = NodePerformanceData.objects.values_list('value', flat=True).order_by('-date').filter(node=i)[:20]
			if not perf:
				perf = [-1]
			perfdata.append(','.join(str(v) for v in reversed(perf)))
		return render_to_response('index.html', {'vmlist': cluster, 'nodes': nodes, 'perfdata': perfdata }, context_instance=RequestContext(request))
	else:
		vms = VM.objects.filter(user=request.user)
		usingcpu = 0
		usingmem = 0
		usingdisk = 0
		allcpu = nodes.filter(state=1).count()*500
		allmem = nodes.filter(state=1).count()*110
		alldisk = nodes.filter(state=1).count()*12288
		for i in vms:
			if i.state == 1:
				usingcpu += i.template.cpu
				usingmem += i.template.memory
				usingdisk += i.template.disk
				allcpu -= i.template.cpu
				allmem -= i.template.memory
				alldisk -= i.template.disk
		return render_to_response('index_user.html', { 'usingcpu': usingcpu , 'usingmem': usingmem, 'usingdisk': usingdisk, 'allcpu': allcpu, 'allmem': allmem, 'alldisk': alldisk, 'user': request.user }, context_instance=RequestContext(request))
	
 
@staff_member_required
def loadbalance(request):
	if request.user.is_staff:
		i = 0
		vms = VM.objects.all().order_by('-state')
		vmssorted = sorted(vms, key=operator.attrgetter('utilization'), reverse = True)
		nodes = Node.objects.filter(state=1)
		for vm in vmssorted:
			dnode = nodes[i % nodes.count()]
			i += 1
			vm.node = dnode
			vm.save()
		return HttpResponseRedirect('/management/')
	else:
		return HttpResponseRedirect('/management/')
