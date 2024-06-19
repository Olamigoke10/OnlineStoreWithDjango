from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Item, Profile, Review, Video

class SignUpForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ('first_name', 'last_name','username', 'email', 'password1', 'password2')

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
        
class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.Select(choices=[(i, i) for i in range(1, 6)]),
            'comment': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Leave your comment...'}),
        }
        
class ContactForm(forms.Form):
    first_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
        'placeholder': 'Your name..', 'required': True
    }))
    last_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
        'placeholder': 'Your last name..', 'required': True
    }))
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'placeholder': 'Your Email..', 'required': True
    }))
    subject = forms.CharField(widget=forms.Textarea(attrs={
        'placeholder': 'Write something..', 'style': 'height:100px', 'required': True
    }))



class OrderFilterForm(forms.Form):
    STATUS_CHOICES = [
        ('', 'All'),  # Add an 'All' option to show all orders regardless of status
        ('pending', 'Pending'),
        ('delivered', 'Delivered'),
    ]
    status = forms.ChoiceField(choices=STATUS_CHOICES, required=False, label="Order Status")
    
    
class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['title', 'description', 'video_file']
        
class FeedbackForm(forms.Form):
    first_name = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'placeholder': 'Your first name..'}))
    last_name = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'placeholder': 'Your last name..'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'placeholder': 'Your email..'}))
    subject = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Write something..', 'rows': 5}), required=True)