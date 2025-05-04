from django.shortcuts import render,redirect,get_object_or_404
from .forms import *
from .models import *
from django.contrib  import messages
from django.db.models import Q
from datetime import date
from django.db.models import Count
from datetime import datetime
from django.contrib.auth import logout

import nltk
nltk.download('punkt')
import nltk
from nltk.data import find

def ensure_punkt():
    try:
        # try the more standard path
        find('tokenizers/punkt/english.pickle')
    except LookupError:
        nltk.download('punkt', quiet=True)

    try:
        # also ensure punkt_tab if your code uses it
        find('tokenizers/punkt_tab/english.pickle')
    except LookupError:
        nltk.download('punkt_tab', quiet=True)

# call this once at startup, before any tokenization
ensure_punkt()



def home(request):
 
    return render (request,'home.html')

def adminhome(request):
 
    return render (request,'adminhome.html')

def services(request):
    return render(request,'services.html')

from django.contrib import messages  # make sure this is imported

def Station_reg(request):
    if request.method == 'POST':
        form = StationForm(request.POST)
        logins = loginForm(request.POST)

        if form.is_valid() and logins.is_valid():
            try:
                a = logins.save(commit=False)
                a.usertype = 2
                a.save()
                b = form.save(commit=False)
                b.login_id = a
                b.save()
                messages.success(request, 'Station registration successful!')
                return redirect('home')
            except Exception as e:
                messages.error(request, f'Station registration failed: {e}')
        else:
            messages.error(request, 'Form validation failed. Please check the input fields.')

    else:
        form = StationForm()
        logins = loginForm()

    return render(request, 'station_register.html', {'form': form, 'log': logins})

from django.contrib import messages

def user_regs(request):
    if request.method == 'POST':
        form = Userform(request.POST)
        logins = loginForm(request.POST)
        if form.is_valid() and logins.is_valid():
            try:
                a = logins.save(commit=False)
                a.usertype = 3
                a.save()
                b = form.save(commit=False)
                b.login_userid = a
                b.save()
                messages.success(request, ' Registration successful!')
                return redirect('home')  # redirect back to form or 'home' as needed
            except Exception as e:
                messages.error(request, f' Registration failed: {e}')
        else:
            messages.error(request, ' Form validation failed. Please correct the errors below.')
    else:
        form = Userform()
        logins = loginForm()

    return render(request, 'user_registration.html', {'form': form, 'logins': logins})


def user_home(request):
    return render(request,'user_home.html')

def station_home(request):
    return render(request,'station_home.html')

def login_page(request):
    if request.method == 'POST':
        form = login_check(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            try:
                user = login.objects.get(email=email)
                # Check if user status is approved
                if user.password == password:
                    if user.usertype == 2 and user.status == 1:
                        request.session['stationid'] = user.id
                        return redirect('stationhome')
                    elif user.usertype == 1:
                        request.session['staffid'] = user.id
                        return redirect('staffhome')
                    elif user.usertype == 3:
                        request.session['userid'] = user.id
                        return redirect('userhome')
                    elif user.usertype == 0:
                        request.session['adminid'] = user.id
                        return redirect('adminhome')
                    else:
                        messages.error(request, 'Station not approved')
                else:
                    messages.error(request, 'Invalid Password')
            
            except login.DoesNotExist:
                messages.error(request, 'User does not exist')
        else:
            return render(request, 'login.html', {'form': form})
    else:
        form = login_check()
    return render(request, 'login.html', {'form': form})







def station_profile(request):
    loginid = request.session.get('stationid')
    if not loginid:  # If user is not logged in
        return redirect('home')  # Redirect to login page (update 'login' with your login URL name)
    else:
        login_details = get_object_or_404(login,id=loginid)
        details = get_object_or_404(police_station,login_id= login_details)
        if request.method == 'POST':
            form = station_profile_form(request.POST, instance=details)
            form2 = station_email_form(request.POST,instance=login_details)
            if form.is_valid() and form2.is_valid():
                form.save()
                form2.save()
                return redirect('stationhome')
        else:
            form = station_profile_form(instance = details)
            form2 = station_email_form(instance=login_details)
        return render(request,'edit_station.html',{'form' : form,'form2' : form2})

# In your staffreg view
def staffreg(request):
    if request.method == 'POST':
        form = stafform(request.POST)
        logins = loginForm(request.POST)

        if form.is_valid() and logins.is_valid():
            try:
                # Save the login instance for the staff (usertype = 1)
                a = logins.save(commit=False)
                a.usertype = 1
                a.save()

                # Save the staff registration form (without committing to DB yet)
                b = form.save(commit=False)

                # Fix: Get the related login instance from the selected police station
                selected_station = form.cleaned_data['staff_station']  # this is a police_station instance
                b.staff_station = selected_station.login_id  # Assign the login instance associated with the police_station

                # Save the staff form with the associated login
                b.staff_login_id = a
                b.save()

                messages.success(request, 'Staff registration successful!')
                return redirect('home')

            except Exception as e:
                messages.error(request, f'Staff registration failed: {e}')

        else:
            messages.error(request, 'Form validation failed. Please check the input fields.')

    else:
        form = stafform()
        logins = loginForm()

    return render(request, 'staff_reg.html', {'forms': form, 'log': logins})




def staff_home(request):
    return render(request,'staff_home.html')


def staff_profile(request):
    loginid = request.session.get('staffid')
    if not loginid:  # If user is not logged in
        return redirect('login')  # Redirect to login page (update 'login' with your login URL name)
    else:
   
        login_details = get_object_or_404(login,id=loginid)
        details = get_object_or_404(staff_reg,staff_login_id= login_details)
        if request.method == 'POST':
            form = staff_profile_form(request.POST, instance=details)
            forms = staff_email_form(request.POST,instance=login_details)
            if form.is_valid() and forms.is_valid():
                form.save()
                forms.save()
                return redirect('staffhome')
        else:
            form = staff_profile_form(instance = details)
            forms = staff_email_form(instance = login_details)
        return render(request , 'edit_staff.html',{'form': form,'forms' : forms})




# def edit_station_profile(request,id):
    
def user_profile(request):
    loginid=request.session.get('userid')
    if not loginid:  # If user is not logged in
        return redirect('login')  # Redirect to login page (update 'login' with your login URL name)
    else:
        login_details=get_object_or_404(login,id=loginid)
        details = get_object_or_404(user_reg,login_userid=login_details)
        if request.method == 'POST':
            form = user_profile_form(request.POST, instance=details)
            form2=user_email_form(request.POST,instance=login_details)
            if form.is_valid() and form2.is_valid():
                form.save()
                form2.save()
                return redirect('userhome')
        else:
            form = user_profile_form(instance = details)
            form2=user_email_form(instance=login_details)
        return render(request,'edit_user.html',{'form' : form,'form2':form2})

# def form_criminal(request):
#     if request.method == 'POST':
#         form = criminal_form(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('staffhome')
#     else:
#         form = criminal_form()
#     return render(request,'add_criminals.html',{'forms' :form})

   
def form_criminal(request):
    staff_login_id=request.session.get('staffid')
    if not staff_login_id:  # If user is not logged in
        return redirect('login')  # Redirect to login page (update 'login' with your login URL name)
    else:
        login_details=get_object_or_404(login,id=staff_login_id)
        details = get_object_or_404(staff_reg,staff_login_id=login_details)
        if request.method == 'POST':
            form = criminal_form(request.POST, request.FILES)
            if form.is_valid():
                a=form.save(commit=False)
                a.login_staffid=details
                a.save()
                return redirect('staffhome') 
        else:
            form = criminal_form()
        return render(request, 'add_criminals.html', {'forms': form})




def criminals_table(request):
    data1 = request.session.get('staffid')
    if not data1:  # If user is not logged in
        return redirect('login')  # Redirect to login page (update 'login' with your login URL name)
    else:
        staffdata = get_object_or_404(login, id=data1)
        staff=get_object_or_404(staff_reg,staff_login_id=staffdata)
        data = criminals.objects.filter(login_staffid=staff)
        return render(request, 'criminalsview.html' , {'data':data})


def delete_criminals(request, id):
    criminal = criminals.objects.get( id=id)
    criminal.delete()
    return redirect('view_criminals')  


def edit_criminals(request,id):
    data = get_object_or_404(criminals, id=id)
    if request.method == 'POST':
        form = CriminalEdit(request.POST,request.FILES,instance=data)
        if form.is_valid():
            form.save()
            return redirect('view_criminals')
    else:
        form = CriminalEdit(instance=data)
    return render(request, 'edit_criminals.html',{'form':form})


def admin_userview(request):
    admin = user_reg.objects.all()
    return render(request,'admin_userview.html',{'data':admin})

def admin_stationview(request):
    admin = police_station.objects.all()
    return render(request,'admin_stationview.html',{'data':admin})

def admin_staffview(request):
    admin = staff_reg.objects.all()
    return render(request,'admin_staffview.html',{'data':admin})

def admin_complaintview(request):
    admin = complaints.objects.all()
    return render(request,'admin_complaintview.html',{'data':admin})



def user_criminal_view(request):
    # data = staff_reg.objects.all()
    data1 = request.session.get('userid')
    if not data1:  # If user is not logged in
        return redirect('login')  # Redirect to login page (update 'login' with your login URL name)
    else:
        data = criminals.objects.all()
        return render(request,'view_criminal_details.html',{'details' : data})

def staff_view(request):
    # Get the station ID from the session
    data1 = request.session.get('stationid')
    if not data1:
        return redirect('login')

  
    else:
        # Retrieve the login record for the given station ID
        staffdata = get_object_or_404(login, id=data1)
        # Use staffdata directly (no need to fetch again)
        data = staff_reg.objects.filter(staff_station=staffdata)
        return render(request, 'view_staff_details.html', {'details': data})




def add_duty(request, id):
    stationid = request.session.get('stationid')
    if not stationid:  # If user is not logged in
        return redirect('login')  # Redirect to login page (update 'login' with your login URL name)
    else:
        station = get_object_or_404(login, id=stationid)   
        staff = get_object_or_404(staff_reg, staff_login_id_id=id)  
        
        if request.method == 'POST':
            form = dutyform(request.POST)
            
            if form.is_valid():
                a = form.save(commit=False)
                a.login_id = station
                a.staff_login_id = staff.staff_login_id  
                a.save()
                return redirect('staff_details')
        else:
            form = dutyform()
        
        return render(request, 'add_duty.html', {'forms': form})



def my_duty(request):
    # data = staff_reg.objects.all()
    data1 = request.session.get('staffid')
    if not data1:  # If user is not logged in
        return redirect('login')  # Redirect to login page (update 'login' with your login URL name)
    else:
        staffdata = get_object_or_404(login, id=data1)
        duty=get_object_or_404(staff_reg,staff_login_id=staffdata)
        data = duties.objects.filter(staff_login_id=duty.staff_login_id)
        return render(request,'duty_view_staff.html',{'details' : data})





def view_duties(request, id):
    stationid = request.session.get('stationid')
    if not stationid:  # If user is not logged in
        return redirect('login')  # Redirect to login page (update 'login' with your login URL name)
    else:
        station = get_object_or_404(login, id=stationid)
        staff = get_object_or_404(staff_reg, staff_login_id=id)  
        # print("dataaa...",staff)
        data = duties.objects.filter(staff_login_id=staff.staff_login_id, login_id=station)
        # print("dattaaaa...",data)
        
        return render(request, 'view_staff_duty.html', {'data': data})




def delete_duty(request, id):
    duty = duties.objects.get(id=id)
    
    duty.delete()
    return redirect('staff_details')  


def edit_duty(request,id):
    data = get_object_or_404(duties, id=id)
    if request.method == 'POST':
        form = DutyEdit(request.POST,instance=data)
        if form.is_valid():
            form.save()
            return redirect('staff_details')
    else:
        form = DutyEdit(instance=data)
    return render(request, 'edit_duty.html',{'form':form})



def search_stations(request):
    data = request.session.get('userid')
    if not data:  # If user is not logged in
        return redirect('login')

    query = request.GET.get('q', '')
    results = police_station.objects.all()

    if query:
        results = results.filter(
            Q(addressline1__icontains=query) |
            Q(district__icontains=query) |
            Q(city__icontains=query)
        )

    show_alert = request.session.pop('enquiry_success', False)

    return render(request, 'search_station.html', {
        'results': results,
        'query': query,
        'show_alert': show_alert
    })


    

def file_petition(request, id):
    user_id=request.session.get('userid')
    if not user_id:  # If user is not logged in
        return redirect('login')  # Redirect to login page (update 'login' with your login URL name)
    else:
        login_details=get_object_or_404(login,id=user_id)
        station = get_object_or_404(police_station,login_id_id=id)
        print(login_details.id)
        print(station.login_id_id)

        if request.method == 'POST':
            form = petition_form(request.POST, request.FILES)
            if form.is_valid():
                a=form.save(commit=False)
                a.login_userid=login_details
                a.login_id=station.login_id
                a.save()
                return redirect('userhome') 
        else:
            form = petition_form()
        return render(request, 'file_petition.html', {'forms': form})




from django.shortcuts import render, redirect, get_object_or_404
from .models import login, police_station, petition, user_reg

def view_petition(request):
    staffid = request.session.get('stationid')
    if not staffid:
        return redirect('login')

    station = get_object_or_404(login, id=staffid)
    staff = get_object_or_404(police_station, login_id=station)
    petitions = petition.objects.filter(login_id=station)

    # Check which petitions already have assigned staff
    assigned_petitions = staff_assign.objects.filter(petition_id__in=petitions)
    assigned_petition_ids = {assignment.petition_id.id for assignment in assigned_petitions}

    # User data mapping
    user_qs = user_reg.objects.filter(login_userid__in=petitions.values_list('login_userid', flat=True))
    user_details_dict = {user.login_userid_id: user for user in user_qs}

    return render(request, 'staffview_petition.html', {
        'petitions': petitions,
        'user_details_dict': user_details_dict,
        'assigned_petition_ids': assigned_petition_ids
    })



    

def file_fir(request, id):
    staff_id = request.session.get('staffid')
    if not staff_id:  # If user is not logged in
        return redirect('login')  # Redirect to login page (update 'login' with your login URL name)
    else:
        staff_lg = get_object_or_404(login, id=staff_id)
        petition_instance = get_object_or_404(petition, id=id)

        if request.method == "POST":
            form = fir_form(request.POST)
            if form.is_valid():
                fir_instance = form.save(commit=False)
                fir_instance.public_petition_id = petition_instance
                fir_instance.staff_loginid = staff_lg
                fir_instance.details_suspect = petition_instance.case_details    
                fir_instance.save()
                return redirect('staffhome')
        else:
            form = fir_form()

        return render(request, 'file_fir.html', {
            'form': form, 
            'petition': petition_instance,
            'occurrence_day': petition_instance.day,
            'occurrence_date': petition_instance.date,
            'occurrence_time': petition_instance.time,
            'occurrence_place': petition_instance.place,
            'recieved_time': petition_instance.recieved_time1,
            'details_case': petition_instance.case_details,
            'details_suspect': petition_instance.suspect,
            'properties_involved': petition_instance.properties_involved,
            'total_value_property':petition_instance.total_value_property
        })




def station_view_petition(request):
    staffid = request.session.get('stationid')

    if not staffid:
        return redirect('login')
    else:
        station = get_object_or_404(login, id=staffid)
       
        staff = get_object_or_404(police_station,login_id=station.id)
        # staff_stations = staff.staff_station  
        petitions = petition.objects.filter(login_id=station)
        user_details = user_reg.objects.filter(login_userid__in=petitions.values_list('login_userid', flat=True))

        # Pop flag to show modal only once
        show_modal = request.session.pop('staff_already_assigned', False)

        return render(request, 'station_petitionview.html', {
            'petitions': petitions,
            'user_details': user_details,
            'show_modal': show_modal
        })


def station_fir_view(request,id):
    station = request.session.get('stationid')
    if not station:  # If user is not logged in
        return redirect('login')  # Redirect to login page (update 'login' with your login URL name)
    else:
        stationid = get_object_or_404(login, id=station)
        peti=get_object_or_404(petition,id=id)
        # petition_details = petition.objects.filter(login_id=stationid)

        fir_details = fir.objects.filter(public_petition_id=peti)

        return render(request, 'view_FIR.html', {'petition_details': peti, 'fir_details': fir_details})


def case_status(request, petition_id):
    petition_instance = get_object_or_404(petition, id=petition_id)

    if request.method == 'POST':
        form = CaseStatus(request.POST)

        if form.is_valid():
            petition_instance.case_status = form.cleaned_data['case_status']
            petition_instance.save()  
            return redirect('petitionview')
    else:
        form = CaseStatus(initial={'case_status': petition_instance.case_status})

    return render(request, 'case_status.html', {'form': form, 'petition': petition_instance})



def public_view_petition(request):
    userid = request.session.get('userid')
    if not userid:  # If user is not logged in
        return redirect('login')  # Redirect to login page (update 'login' with your login URL name)
    else:
        user = get_object_or_404(login, id=userid)
        petitions = petition.objects.filter(login_userid=user)
        return render(request, 'public_viewpetition.html', {'petitions': petitions })


def edit_petition(request,id):
    data = get_object_or_404(petition, id=id)
    if request.method == 'POST':
        form = petition_form(request.POST,request.FILES,instance=data)
        if form.is_valid():
            form.save()
            return redirect('petitionview_public')
    else:
        form = petition_form(instance=data)
    return render(request, 'edit_petitionpublic.html',{'form':form})



def delete_petition(request, id):
    petition_details = petition.objects.get( id=id)
    petition_details.delete()
    return redirect('petitionview_public')


def file_complaint(request):
    userid = request.session.get('userid')
    if not userid:  # If user is not logged in
        return redirect('login')  # Redirect to login page (update 'login' with your login URL name)
    else:
        user = get_object_or_404(login,id=userid)
        if request.method == 'POST':
            form = ComplaintForm(request.POST)

            if form.is_valid():
                a = form.save(commit=False)
                a.user_logid=user
                a.save()
                return redirect('userhome')
        else:
            form = ComplaintForm()

        return render(request, 'file_complaint.html', {'form': form})






def view_complaints(request):
    userid = request.session.get('userid')  
    if not userid:  # If user is not logged in
        return redirect('login')  # Redirect to login page (update 'login' with your login URL name)
    else:
        user = get_object_or_404(login, id=userid)  
        data = complaints.objects.filter(user_logid=user)  
        return render(request, 'view_complaint.html', {'data': data})


def edit_complaint(request,id):
    data = get_object_or_404(complaints, id=id)
    if request.method == 'POST':
        form = ComplaintForm(request.POST,request.FILES,instance=data)
        if form.is_valid():
            form.save()
            return redirect('view_complaint')
    else:
        form = ComplaintForm(instance=data)
    return render(request, 'edit_complaint.html',{'form':form})



def delete_complaint(request, id):
    complaint_details = complaints.objects.get( id=id)
    complaint_details.delete()
    return redirect('view_complaint')


def reply_complaint(request,id):  
    complaint = get_object_or_404(complaints,id=id)
    if request.method == 'POST':
        form = ReplyComplaint(request.POST)
        
        if form.is_valid():
            complaint.reply=form.cleaned_data['reply']
            complaint.save()
            return redirect('admin_complaintview')
    else:
        form = ReplyComplaint(initial={'reply':complaint.reply})
    
    return render(request, 'reply_complaint.html', {'forms': form,'complaint':complaint})






from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import login
from .forms import EnquiryForm

# In views.py
def make_enquiry(request, login_id):
    user_id = request.session.get('userid')
    if not user_id:
        return redirect('login')

    login_details = get_object_or_404(login, id=user_id)
    station = get_object_or_404(login, id=login_id)

    if request.method == 'POST':
        form = EnquiryForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                a = form.save(commit=False)
                a.user_id = login_details
                a.station_id = station
                a.save()
                # Set the flag for successful enquiry submission
                request.session['enquiry_success'] = True  
                return redirect('station_search')
            except Exception as e:
                messages.error(request, f"Failed to send enquiry: {str(e)}")
        else:
            messages.error(request, "Form validation failed.")
    else:
        form = EnquiryForm()

    return render(request, 'make_enquiry.html', {'forms': form})






def view_enquiry(request):
    staffid = request.session.get('staffid')  
    if not staffid:  # If user is not logged in
        return redirect('login')  # Redirect to login page (update 'login' with your login URL name)
    else:
        station = get_object_or_404(login, id=staffid) 
        staff = get_object_or_404(staff_reg, staff_login_id=station.id) 
        staff_stations = staff.staff_station 
        enquiries_list = enquiries.objects.filter(station_id=staff_stations).select_related('user_id__user_as_loginid') 
        # user_details = user_reg.objects.filter(user_id__in=enquiries.enquiries_list('user_id', flat=True))


        return render(request, 'enquiries_viewstaff.html', {'enquiries': enquiries_list})



def reply_enquiry(request,id):  
    enquiry = get_object_or_404(enquiries,id=id)
    if request.method == 'POST':
        form = ReplyEnquiry(request.POST)
        
        if form.is_valid():
            enquiry.staff_reply=form.cleaned_data['staff_reply']
            enquiry.save()
            return redirect('view_enquiry')
    else:
        form = ReplyEnquiry(initial={'staff_reply':enquiry.staff_reply})
    
    return render(request, 'reply_enquiry.html', {'forms': form,'enquiries':enquiry})




def enquiry_viewuser(request):
    userid = request.session.get('userid')
    if not userid:  # If user is not logged in
        return redirect('login')  # Redirect to login page (update 'login' with your login URL name)
    else:
        user = get_object_or_404(login, id=userid)
        enquiry = enquiries.objects.filter(user_id=user)
        return render(request, 'public_viewenquiry.html', {'enquiries': enquiry })



def edit_enquiry(request,id):
    data = get_object_or_404(enquiries, id=id)
    if request.method == 'POST':
        form = EnquiryForm(request.POST,request.FILES,instance=data)
        if form.is_valid():
            form.save()
            return redirect('enquiry_viewuser')
    else:
        form = EnquiryForm(instance=data)
    return render(request, 'edit_enquirypublic.html',{'form':form})



def delete_enquiry(request, id):
    enquiry_details = enquiries.objects.get( id=id)
    enquiry_details.delete()
    return redirect('enquiry_viewuser')




def staff_attendance(request):
    data1 = request.session.get('stationid')
    if not data1:  # If user is not logged in
        return redirect('login')  # Redirect to login page (update 'login' with your login URL name)
    else:
        staffdata = get_object_or_404(login, id=data1)
        staff_list = staff_reg.objects.filter(staff_station=staffdata)

        staff_details = []
        for staff in staff_list:
            is_marked = attendance.objects.filter(staff_id=staff, current_date=date.today()).exists()
            staff_details.append({'staff': staff, 'is_marked': is_marked})

        return render(request, 'staff_attendance.html', {'staff_details': staff_details})


def mark_attendance(request, id):
    staff = get_object_or_404(staff_reg, id=id)

    if attendance.objects.filter(staff_id=staff, current_date=date.today()).exists():
        messages.warning(request, 'Attendance already marked for this staff!')
    else:
        attendance.objects.create(staff_id=staff)
        messages.success(request, 'Attendance marked successfully!')

    return redirect('staff_attendance')


def search_attendance(request):

    station_id = request.session.get('stationid')
    if not station_id:  # If user is not logged in
        return redirect('login')  # Redirect to login page (update 'login' with your login URL name)  
    else:
        station = get_object_or_404(login, id=station_id)
        query = request.GET.get('q', '')  
        results = []

        if query:
            results = attendance.objects.filter(current_date=query, staff_id__staff_station=station ).select_related('staff_id')

        return render(request, 'search_attendance.html', {'results': results, 'query': query})


def month_attendance(request):
    station_id = request.session.get('stationid')  
    if not station_id:  # If user is not logged in
        return redirect('login')  # Redirect to login page (update 'login' with your login URL name)
    else:
        station = get_object_or_404(login, id=station_id)
        name = request.GET.get('name', '')  
        date = request.GET.get('date', '')  

        results = []

        if name and date:
            try:
                month = int(date)  
                if 1 <= month <= 12: 
                    current_year = datetime.now().year

    
                    results = attendance.objects.filter(
                        current_date__month=month,
                        current_date__year=current_year,
                        staff_id__staff_name__icontains=name,
                        

                    ).select_related('staff_id__staff_name__station_as_loginid')  # Get the staff info as well

                    results = results.values('staff_id').annotate(present_days=Count('id'))

                print(results)
                
            except ValueError:
                results = []

        return render(request, 'month_attendance.html', {
            'results': results, 
            'query': name, 
            'query2': date
        })



def staff_promotion(request,id):
   
    staff = get_object_or_404(staff_reg,staff_login_id=id)  

    if request.method == 'POST':
        form = StaffPromoteForm(request.POST,instance=staff)
        print(form)
        if form.is_valid():
            a=form.cleaned_data['staff_designation']
            staff.staff_designation=a
            staff.save()
           
            return redirect('staff_details')
    else:
        form = StaffPromoteForm(instance=staff)
    return render(request , 'promote_staff.html',{'form': form,'staff':staff})

def adminstationapprove(request,id):
    data=get_object_or_404(login,id=id)
    data.status=1
    data.save()
    return redirect('admin_stationview')

def adminstationreject(request,id):
    data=get_object_or_404(login,id=id)
    data.status=2
    data.save()
    return redirect('admin_stationview')

def logouts(request):
    
    request.session.flush()
    return redirect('home')


def assign_staff(request, id):
    data1 = request.session.get('stationid')
    petitionid = get_object_or_404(petition, id=id)

    # if not data1:
    #     return redirect('login')
    # else:
    staffdata = get_object_or_404(login, id=data1)
    data = staff_reg.objects.filter(staff_station=staffdata)
        
    if staff_assign.objects.filter(petition_id=petitionid).exists():
        request.session['staff_already_assigned'] = True  # Set flag
        return redirect('petitionview')

    return render(request, 'assign_staff.html', {'details': data , 'petition': petitionid.id})
    
def assign_staff_process(request,staffid,petitionid):
    id_petition = get_object_or_404(petition,id=petitionid)
    staff = get_object_or_404(staff_reg,id=staffid) 
    if staff_assign.objects.filter(staff_id=staff,petition_id=id_petition).exists():
        messages.error(request, 'Staff is already assigned')
        return redirect('petitionview')
    else:
        staff_assign.objects.create(
        staff_id = staff,
        petition_id = id_petition
    )

    return redirect('petitionview') 

# def assign_staff_process(request, staffid, petitionid):
#     id_petition = get_object_or_404(petition, id=petitionid)
#     staff = get_object_or_404(staff_reg, id=staffid)

#     # Check if already assigned
#     if staff_assign.objects.filter(staff_id=staff, petition_id=id_petition).exists():
#         messages.error(request, 'Staff is already assigned')
#     else:
#         staff_assign.objects.create(
#             staff_id=staff,
#             petition_id=id_petition
#         )
#         messages.success(request, 'Staff assigned successfully')

#     return redirect('petitionview')


# Update the view
# Update the view
def view_assigned_petition(request):
    data = request.session.get('staffid')
    if not data:  # If user is not logged in
        return redirect('login')
    else:
        staff = get_object_or_404(staff_reg, staff_login_id=data)
        petition_data = staff_assign.objects.filter(staff_id=staff).select_related('petition_id__login_userid')

        # Check if the FIR is created for each petition
        for petition in petition_data:
            # Check if FIR exists for the petition using the reverse relationship (fir_set)
            petition.petition_id.is_fir_created = fir.objects.filter(public_petition_id=petition.petition_id).exists()

        return render(request, 'assigned_petitions.html', {'data': petition_data})


  
    
import cv2,os
import numpy as np

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

def load_criminals():
    """Loads criminal data (images and encodings)"""
    criminal_images = []
    criminal_encodings = []
    for criminal in criminals.objects.all():
        image_path = criminal.photo.path
        try:
            image = cv2.imread(image_path)
            if image is not None:
                rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                faces = face_cascade.detectMultiScale(rgb_image, scaleFactor=1.1, minNeighbors=7, minSize=(30, 30))
                
                if len(faces) == 1:
                    x, y, w, h = faces[0]
                    face_image = rgb_image[y:y+h, x:x+w]
                    
                    face_encoding = encode_face(face_image)
                    
                    if face_encoding is not None:
                        criminal_images.append(face_image)
                        criminal_encodings.append(face_encoding)
        except Exception as e:
            print(f"Error loading image: {image_path} - {e}")
    return criminal_images, criminal_encodings

def encode_face(face_image):
    """Encodes a face image into a feature vector using a pre-trained model"""
    model_path = os.path.join(os.path.dirname(__file__), 'openface.nn4.small2.v1.t7')
    model = cv2.dnn.readNetFromTorch(model_path)

    target_size = (96, 96)
    resized_image = cv2.resize(face_image, target_size)
    normalized_image = resized_image.astype(float) / 255.0

    if normalized_image.dtype != np.float32:
        normalized_image = normalized_image.astype(np.float32)

    blob = cv2.dnn.blobFromImage(normalized_image, 1.0, target_size, (0, 0, 0), swapRB=True, crop=False)
    model.setInput(blob)
    face_encoding = model.forward()

    return face_encoding.flatten() if face_encoding is not None else None

def face_recognition_view(request):
    criminal_images, criminal_encodings = load_criminals()
    cv2.namedWindow('Criminal Detecting', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('Criminal Detecting', 1280, 720)

    if request.method == 'POST':
        threshold = 0.6
        display_duration = 60
        details_text = ""
        display_details = False
        frame_count = 0

        cap = cv2.VideoCapture(0)

        while True:
            ret, frame = cap.read()

            if not ret:
                print("Error capturing frame")
                break

            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            faces = face_cascade.detectMultiScale(rgb_frame, scaleFactor=1.1, minNeighbors=7, minSize=(30, 30))

            for (x, y, w, h) in faces:
                face_image = rgb_frame[y:y+h, x:x+w]
                face_encoding = encode_face(face_image)

                if face_encoding is not None:
                    distances = [np.linalg.norm(face_encoding - enc) for enc in criminal_encodings]
                    min_distance = min(distances)
                    
                    if min_distance < threshold:
                        min_index = distances.index(min_distance)
                        criminal = criminals.objects.all()[min_index]
                        
                        details_text = f"Name: {criminal.criminal_name}, Gender: {criminal.gender}, Crime Details: {criminal.crime_details}"
                        display_details = True
                        frame_count = 0

                        cv2.imshow("Criminal Image", criminal_images[min_index])

            if display_details:
                text_size, _ = cv2.getTextSize(details_text, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2)
                text_width = text_size[0]
                text_height = text_size[1]

                max_text_width = frame.shape[1] - 20
                max_text_height = frame.shape[0] - 20
                text_position = (10, max_text_height - text_height) if max_text_height > text_height else (10, 30)

                cv2.putText(frame, details_text, text_position, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
                frame_count += 1

                if frame_count >= display_duration:
                    display_details = False

            cv2.imshow('Criminal Detecting', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

    return render(request, 'face_recognition.html')


from django.shortcuts import render

from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd

def preprocess_text(text):
    tokens = word_tokenize(text)
    tokens = [word.lower() for word in tokens if word.isalpha()]
    return " ".join(tokens)

def match_fir(request):
    form = FirCheckForm()
    matches = []
    
    if request.method == 'POST':
        form = FirCheckForm(request.POST)
        if form.is_valid():
            description = form.cleaned_data['Case_description']
            
            # Preprocess the input description
            cleaned_description = preprocess_text(description)
            
            # Get all FIR case descriptions from the database
            all_firs = fir.objects.all()
            fir_descriptions = [preprocess_text(fir.content_fir) for fir in all_firs]
            
            # Add the new description to the list for comparison
            fir_descriptions.append(cleaned_description)
            
            # Convert the descriptions to a matrix of token counts
            vectorizer = CountVectorizer().fit_transform(fir_descriptions)
            vectors = vectorizer.toarray()
            
            # Calculate cosine similarity between the vectors
            cosine_sim = cosine_similarity(vectors)
            
            # Get similarity scores for the last description (input)
            last_index = len(fir_descriptions) - 1
            similarity_scores = cosine_sim[last_index]
            
            # Find similar FIRs (with a threshold)
            threshold = 0.3  # Lowering the threshold to capture more similarities
            for i, score in enumerate(similarity_scores[:-1]):
                if score > threshold:
                    matches.append(all_firs[i])
    
    context = {
        'form': form,
        'matches': matches
    }
    
    return render(request, 'FIRcheck.html', context)






def admin_dashboard(request):
    user_count = login.objects.filter(usertype=3).count()  # Adjust filter as needed
    return render(request, 'admin_home.html', {'user_count': user_count})



    
