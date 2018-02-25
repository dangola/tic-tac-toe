from django import forms
from .models import User


class NameForm(forms.Form):
	name = forms.CharField(label='Name', max_length=100)

class SignupForm(forms.ModelForm):
	username = forms.CharField(label='Username')
	password = forms.CharField(label='Password')
	email = forms.CharField(label='Email')

	class Meta:
		model = User
		fields = ['username', 'password', 'email']

class LoginForm(forms.Form):
	username = forms.CharField(label='Username')
	password = forms.CharField(label='Password')