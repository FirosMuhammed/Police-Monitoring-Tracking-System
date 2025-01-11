from django import forms
from.models import police_station,login

class StationForm(forms.ModelForm):


    class Meta:
        model = police_station
        fields = ['station_id','addressline1','addressline2','district','city','contact']


class loginForm(forms.ModelForm):


    class Meta:
        model = login
        fields = ['email','password']

class login_check(forms.Form):

    email = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)


class station_profile_form(forms.ModelForm):
    class Meta:
        model = police_station
        fields = ['addressline1','addressline2','district','city','contact']

class station_email_form(forms.ModelForm):
    class Meta:
        model = login
        fields = ['email']

       