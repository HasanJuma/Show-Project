from django import forms
from .models import Rating, Comment
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['stars']
        widgets = {
            'stars': forms.NumberInput(attrs={'min': 1, 'max': 5}),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
