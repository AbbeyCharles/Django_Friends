from django import forms
from .models import User
from django.core.exceptions import ValidationError
from django.forms import extras
import re

def passwordRequirements(value):
	if len(value) < 8:
		raise ValidationError(
			'Password should be at least 8 characters'
		)

class RegistrationForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super(RegistrationForm, self).__init__(*args, **kwargs)
		self.fields['password1'].validators.append(passwordRequirements)
	password1 = forms.CharField(widget=forms.PasswordInput,
								label="Password")
	password2 = forms.CharField(widget=forms.PasswordInput,
								label="Confirm Password")
	dob = forms.DateField(widget=extras.SelectDateWidget, label="Date of Birth")
	def save(self, commit=True):
		user = super(RegistrationForm, self).save(commit=False)
		user.alias = self.cleaned_data["alias"]
		user.email = self.cleaned_data["email"]
		user.name = self.cleaned_data["name"]
		if commit:
			user.save()
		return user
	def clean(self):
		cleaned_data = super(RegistrationForm, self).clean()
		if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
			if self.cleaned_data['password1'] != self.cleaned_data['password2']:
				raise forms.ValidationError("Passwords don't match. Please enter both fields again.")
		return self.cleaned_data
	def save(self, commit=True):
		user = super(RegistrationForm, self).save(commit=False)
		user.set_password(self.cleaned_data['password1'])
		if commit:
			user.save()
		return user
	class Meta:
		model = User
		fields = 'name', 'alias', 'email', 'password1', 'password2', 'dob'
		exclude = 'is_admin', 'is_active', 'password', 'last_login'


class LoginForm(forms.Form):
	email = forms.EmailField(max_length=100)
	password = forms.CharField(max_length=100, widget=forms.PasswordInput)
	class Meta:
		model = User
		fields = 'email', 'password'