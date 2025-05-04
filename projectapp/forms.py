from django import forms
from.models import *
import re
class StationForm(forms.ModelForm):
    class Meta:
        model = police_station
        fields = ['station_id', 'addressline1', 'addressline2', 'district', 'city', 'contact']

    def clean_addressline1(self):
        address = self.cleaned_data.get("addressline1")
        # Relaxing the regex to allow alphanumeric characters, spaces, and common punctuation
        if not re.match(r'^[A-Za-z0-9\s,.-]+$', address):
            raise forms.ValidationError("Address line 1 must contain only letters, numbers, spaces, commas, and periods.")
        return address

    def clean_contact(self):
        contact_number = self.cleaned_data.get("contact")
        
        # Check if the contact number contains exactly 10 digits
        if not re.match(r'^\d{10}$', contact_number):
            raise forms.ValidationError("Contact number must be exactly 10 digits and contain no other characters.")
        
        # Check if it contains any non-digit characters (like spaces, hyphens, etc.)
        if not contact_number.isdigit():
            raise forms.ValidationError("Contact number must contain only digits.")
        
        return contact_number


class loginForm(forms.ModelForm):


    class Meta:
        model = login
        fields = ['email','password']


    def clean_password(self):
        password = self.cleaned_data.get("password")
        
        # Check if the password matches the regex pattern
        if not re.match(r'^(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$', password):
            raise forms.ValidationError(
                "Password must be at least 8 characters long, with one uppercase letter, one digit, and one special character."
            )
        return password

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

    # def clean_name(self):
        # address = self.cleaned_data.get("name")
        # Relaxing the regex to allow alphanumeric characters, spaces, and common punctuation
        # if not re.match(r'^[A-Za-z0-9\s,.-]+$', address):
        #     raise forms.ValidationError("Address line 1 must contain only letters, numbers, spaces, commas, and periods.")
        # return address

    def clean_contact(self):
        contact_number = self.cleaned_data.get("contact")
        
        # Check if the contact number contains exactly 10 digits
        if not re.match(r'^\d{10}$', contact_number):
            raise forms.ValidationError("Contact number must be exactly 10 digits and contain no other characters.")
        
        # Check if it contains any non-digit characters (like spaces, hyphens, etc.)
        if not contact_number.isdigit():
            raise forms.ValidationError("Contact number must contain only digits.")
        
        return contact_number

class user_profile_form(forms.ModelForm):
     class Meta:
        model=user_reg
        fields=['name','contact']

class user_email_form(forms.ModelForm):
    class Meta:
        model=login
        fields=['email']

class stafform(forms.ModelForm):
    staff_station = forms.ModelChoiceField(
        queryset=police_station.objects.all(),
        empty_label="Select station",
        label="Station"
    )

    class Meta:
        model = staff_reg
        fields = [
            'staff_name', 'staff_address', 'staff_district', 'staff_city',
            'staff_contact', 'staff_dob', 'staff_designation', 'gender', 'staff_station'
        ]
        widgets = {
            'staff_dob': forms.TextInput(attrs={'type': 'date'})
        }


    def clean_staff_contact(self):
        contact_number = self.cleaned_data.get("staff_contact")
        
        # Check if the contact number contains exactly 10 digits
        if not re.match(r'^\d{10}$', contact_number):
            raise forms.ValidationError("Contact number must be exactly 10 digits and contain no other characters.")
        
        # Check if it contains any non-digit characters (like spaces, hyphens, etc.)
        if not contact_number.isdigit():
            raise forms.ValidationError("Contact number must contain only digits.")
        
        return contact_number
    
class staff_profile_form(forms.ModelForm):
    class Meta:
        model=staff_reg
        fields=['staff_name','staff_address','staff_district','staff_city','staff_contact','staff_dob','staff_designation','gender']
        widgets = {'staff_designation':forms.TextInput(attrs={'disabled':'disabled'})}



class StaffPromoteForm(forms.ModelForm):
    class Meta:
        model = staff_reg
        fields = ['staff_designation']
        widgets = {
            'staff_designation': forms.Select(attrs={'class': 'form-control'})
        }
        

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


class dutyform(forms.ModelForm):
    class Meta:
        model = duties
        fields = ['duty']

class DutyEdit(forms.ModelForm):
    class Meta:
        model=duties
        fields=['duty']


class petition_form(forms.ModelForm):
    class Meta:
        model=petition
        fields=['case','case_details','day','date','place','time','suspect','properties_involved','total_value_property']

    properties_involved = forms.CharField(required=False)
    total_value_property = forms.CharField(required=False)

class fir_form(forms.ModelForm):
    class Meta:
        model = fir
        fields = ['district','pstation','fir_no','year','acts', 'sections',
                  'content_fir']
        
    
class CaseStatus(forms.ModelForm):
    class Meta:
        model=petition
        fields=['case_status']

class ComplaintForm(forms.ModelForm):
    class Meta:
        model=complaints
        fields=['complaint']


class ReplyComplaint(forms.ModelForm):
    class Meta:
        model=complaints
        fields=['reply']


class EnquiryForm(forms.ModelForm):
    class Meta:
        model=enquiries
        fields=['enquiry']


class ReplyEnquiry(forms.ModelForm):
    class Meta:
        model=enquiries
        fields=['staff_reply']



        
class FirCheckForm(forms.Form):
    Case_description = forms.CharField(widget=forms.Textarea)
