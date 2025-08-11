from django import forms
from .models import Rating, Comment , Profile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm



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


# update profile 

class ProfileForm(forms.ModelForm):
    # أضف حقول الاسم من User كحقول عادية في الفورم
    first_name = forms.CharField(required=False, max_length=150)
    last_name  = forms.CharField(required=False, max_length=150)

    class Meta:
        model = Profile
        fields = ['image']  # الصورة من Profile فقط

    def __init__(self, *args, **kwargs):
        # Extract the 'user' passed from the view and store it
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        #  If the user exists, pre-fill first_name and last_name fields
        if self.user:
            self.fields['first_name'].initial = self.user.first_name
            self.fields['last_name'].initial = self.user.last_name

    def save(self, commit=True):
        profile = super().save(commit=False)
        # Also update related User model fields
        if self.user:
            self.user.first_name = self.cleaned_data.get('first_name', '')
            self.user.last_name = self.cleaned_data.get('last_name', '')
            if commit:
                self.user.save()
        if commit:
            profile.save()
        return profile
