from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Profile
from datetime import date 

class CustomUserForm(UserCreationForm):
    email = forms.EmailField(required=True)
    name = forms.CharField(max_length=150, required=True)

    class Meta:
        model = CustomUser
        fields = ['name', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['email']  # Use email as username
        if commit:
            user.save()
        return user

class UserEditForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['name']

class ProfileForm(forms.ModelForm):
    dob = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}),required=True)

    class Meta:
        model = Profile
        fields = ['phone_number', 'dob', 'gender', 'location', 'bio', 'profile_picture']
