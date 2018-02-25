from django import forms
from .models import User

class NameForm(forms.Form):
	name = forms.CharField(label='Name', max_length=100)

class SignupForm(forms.ModelForm):
	username = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'username'}))
	password = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'password'}))
	email = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'email address'}))

	class Meta:
		model = User
		fields = ['username', 'password', 'email']

class LoginForm(forms.Form):
	username = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'username'}))
	password = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'password'}))