from django import forms

from .models import Profile, Skill


class Filling_Profile_form(forms.ModelForm):

    full_name = forms.CharField(label='full_name',widget=forms.TextInput(attrs={'placeholder':'Имя'}))
    email = forms.CharField(label='email',widget=forms.TextInput(attrs={'placeholder':'E-mail'}))
    contacts = forms.CharField(label='contacts',widget=forms.TextInput(attrs={'placeholder':'Telegram'}))
    language = forms.CharField(label='language',widget=forms.TextInput(attrs={'placeholder':'Язык'}))

    class Meta:
        model = Profile
        fields = ('full_name', 'email','contacts','language')

