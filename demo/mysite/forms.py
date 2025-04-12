from django import forms
from django.contrib.auth.models import User
from .models import Profile
from django import forms
from .models import ScheduledPost

class ScheduledPostForm(forms.ModelForm):
    class Meta:
        model = ScheduledPost
        fields = ['content', 'platform', 'scheduled_time']
        widgets = {
            'scheduled_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'twitter_username', 'facebook_username', 'profile_picture']  # ✅ Include this
