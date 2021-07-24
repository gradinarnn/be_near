from django import forms

from .models import Profile, Skills


class Filling_Profile_form(forms.ModelForm):

    # full_name = forms.CharField(max_length=50)
    # email = forms.CharField(max_length=50)

    class Meta:
        model = Profile
        fields = ('full_name', 'email','goal','contacts','language')

