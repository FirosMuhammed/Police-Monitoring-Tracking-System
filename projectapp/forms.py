from django import forms
from.models import police_station,login,user_reg,criminals,staff_reg

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
        fields = ['station_id','addressline1','addressline2','district','city','contact']

class station_email_form(forms.ModelForm):
    class Meta:
        model = login
        fields = ['email']

class Userform(forms.ModelForm):
    class Meta:
        model=user_reg
        fields=['name','contact']

class user_profile_form(forms.ModelForm):
     class Meta:
        model=user_reg
        fields=['name','contact']

class user_email_form(forms.ModelForm):
    class Meta:
        model=login
        fields=['email']

class stafform(forms.ModelForm):
    class Meta:
        model=staff_reg
        fields=['staff_name','staff_address','staff_district','staff_city','staff_contact','staff_dob','staff_designation','gender']

class staff_profile_form(forms.ModelForm):
    class Meta:
        model=staff_reg
        fields=['staff_name','staff_address','staff_district','staff_city','staff_contact','staff_dob','staff_designation','gender']

class staff_email_form(forms.ModelForm):
    class Meta:
        model= login
        fields=['email']      

class criminal_form(forms.ModelForm):
    class Meta:
        model= criminals
        fields=['photo','criminal_name','crime_details','criminal_age','gender']


class CriminalEdit(forms.ModelForm):
    class Meta:
        model=criminals
        fields=['photo','criminal_name','crime_details','criminal_age','gender']
