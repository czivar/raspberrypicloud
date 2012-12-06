from cluster import models
from django import forms

class TemplateForm(forms.ModelForm):
	
	class Meta:
		model = models.Template
		exclude =('user')	

class VMForm(forms.ModelForm):
	
	class Meta:
		model = models.VM
		exclude =('user', 'uuid', 'state', 'node')	
