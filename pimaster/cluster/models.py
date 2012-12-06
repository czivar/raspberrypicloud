from django.db import models
from django import forms
from django.contrib.auth.models import User

NODE_STATE = (
    (0, 'No State'),
    (1, 'On'),
    (2, 'Off')
)

VM_STATE = (
    (0, 'No State'),
    (1, 'Running'),
    (2, 'Running'),
    (3, 'Paused by user '),
    (4, 'Being shut down'),
    (5, 'Shut off'),
    (6, 'Crashed'),
    (95,'Reboot by user'),
    (96,'Powered Off by user'),
    (97,'Wait Migrate'),
    (98,'Powered Off'),
    (99,'Disabled')
    )

class StartVMForm(forms.Form):
	name = forms.CharField(max_length=100)
	node = forms.CharField(max_length=100)

class Rack(models.Model):
	def __unicode__(self):
		return self.name

	name = models.CharField(max_length=30)

class Node(models.Model):
	def __unicode__(self):
		return self.name

	name = models.CharField(max_length=30, null=False)
	ip = models.IPAddressField( null=False, unique=True)
	rack = models.ForeignKey(Rack)
	state = models.IntegerField(default=0, choices=NODE_STATE, null=False)
	lastchecked = models.DateTimeField(auto_now=True, null=False)

	def getNumber():
		return filter(lambda x: x.isdigit(), name)

class Template(models.Model):
	def __unicode__(self):
		return self.name

	name = models.CharField(max_length=30)
	user = models.ForeignKey(User)
	memory = models.IntegerField()
	cpu = models.IntegerField()
	comment = models.CharField(max_length=80)
	datecreated = models.DateTimeField(auto_now_add=True, null=False)
	datemodified = models.DateTimeField(auto_now=True, null=False)
	
class VM(models.Model):
	def __unicode__(self):
		return self.name

	name = models.CharField(max_length=30)
	user = models.ForeignKey(User)
	uuid = models.CharField(max_length=36,blank=True)
	node = models.ForeignKey(Node)
	template = models.ForeignKey(Template)
	state = models.IntegerField(default=0, choices=VM_STATE)
	datecreated = models.DateTimeField(auto_now_add=True, null=False)
	datemodified = models.DateTimeField(auto_now=True, null=False)
	
