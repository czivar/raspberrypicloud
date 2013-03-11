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

class CreateUserForm(forms.Form):
	username = forms.CharField(max_length=30)
	first_name = forms.CharField()
	last_name = forms.CharField()
	password=forms.CharField(max_length=30,widget=forms.PasswordInput()) #render_value=False
	email=forms.EmailField(required=False)
