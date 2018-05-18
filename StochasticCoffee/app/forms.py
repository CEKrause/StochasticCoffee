from django import forms

class LoginForm(forms.Form):
    email = forms.CharField(max_length=100)
    password = forms.CharField(max_length=100)

    
class RegistrationForm(forms.Form):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    email = forms.CharField(max_length=100)
    branch = forms.CharField(max_length=100)
    division = forms.CharField(max_length=100)
    frequency = forms.CharField(max_length=100)
    password = forms.CharField(max_length=100)
