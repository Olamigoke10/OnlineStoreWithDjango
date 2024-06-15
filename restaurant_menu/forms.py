from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Item, Profile

class SignUpForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class LoginForm(AuthenticationForm):
    class Meta:
        fields = ('username', 'password')
        

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['meal', 'description', 'price', 'meal_type', 'status', 'image']
        
        
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['address', 'city', 'state', 'zip_code', 'phone_number']
        
class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']