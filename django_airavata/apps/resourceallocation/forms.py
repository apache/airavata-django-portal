from django.contrib.auth.models import User
from django import forms


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']


class RequestCreateForm(forms.Form):
    title = forms.CharField(required=True)
    projectDescription = forms.CharField()
    typeOfAllocation = forms.CharField()
