from django import forms

class RegisterForm(forms.Form):
	first_name = forms.CharField(max_length=255)
	last_name = forms.CharField(max_length=255)
	email = forms.EmailField()
	password = forms.CharField(max_length=255, widget=forms.PasswordInput)
	confirm_password = forms.CharField(max_length=255, widget=forms.PasswordInput)

class LoginForm(forms.Form):
	email_address = forms.EmailField()
	password = forms.CharField(max_length=255, widget=forms.PasswordInput)