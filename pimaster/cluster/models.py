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
    (5, 'Crashed'),
    (6, 'Powered Off'),
    )

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
	datemodified = models.DateTimeField(auto_now=True, null=False)

	def getNumber():
		return filter(lambda x: x.isdigit(), name)

	def _get_utilization(self):
		util = 0
		for i in VM.objects.filter(node=self):
			util += i.utilization
		return util
	utilization = property(_get_utilization)

class Template(models.Model):
	def __unicode__(self):
		return self.name

	name = models.CharField(max_length=30)
	user = models.ForeignKey(User)
	cpu = models.IntegerField(null=False)
	memory = models.IntegerField(null=False)
	disk = models.IntegerField(null=False)
	comment = models.CharField(max_length=80, null=True, blank=True)
	datecreated = models.DateTimeField(auto_now_add=True, null=False)
	datemodified = models.DateTimeField(auto_now=True, null=False)

	def _get_utilization(self):
		return int((7 * self.cpu + 2 * self.memory + 1 * self.disk) / 10)
	utilization = property(_get_utilization)
	
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
	
	def _get_utilization(self):
		return self.template.utilization
	utilization = property(_get_utilization)

class NodePerformanceData(models.Model):
	def __unicode__(self):
		return self.node.name

	node = models.ForeignKey(Node)
	date = models.DateTimeField(auto_now_add=True, null=False)
	metric = models.IntegerField(default=0)
	value = models.FloatField(null=False)
