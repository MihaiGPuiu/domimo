from django import forms
# forms.py
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class AnnouncementForm(forms.Form):
    title = forms.CharField(label='Title', max_length=50)
    type = forms.CharField(label='Type', max_length=50)
    city = forms.CharField(label='City', max_length=50)
    district = forms.CharField(label='District', max_length=50)
    surface = forms.CharField(label='Surface', max_length=50)
    price = forms.CharField(label='Price', max_length=20)
    image_links = forms.URLField(label='Image Links', max_length=200)
    location = forms.CharField(label='Location', max_length=100)
