from django.shortcuts import render,redirect,get_object_or_404
from .forms import *
from .models import *
from django.contrib  import messages
from django.db.models import Q
from datetime import date
from django.db.models import Count
from datetime import datetime
from django.contrib.auth import logout



def home(request):
 
    return render (request,'home.html')

def adminhome(request):
 
    return render (request,'adminhome.html')

def services(request):
    return render(request,'services.html')

def Station_reg(request):
    if request.method == 'POST':
        form = StationForm(request.POST)
        logins = loginForm(request.POST)
        
        if form.is_valid() and logins.is_valid():
            a = logins.save(commit=False)
            a.usertype = 2 
            a.save()
            b = form.save(commit=False)
            b.login_id = a 
            b.save() 
            
            return redirect('home') 
        else:
            return render(request, 'station_register.html', {'form': form, 'log': logins})


            
    else:
        form = StationForm()
        logins = loginForm()

    return render(request, 'station_register.html', {'form': form, 'log': logins})

def user_regs(request):
    if request.method=='POST':
        form=Userform(request.POST)
        logins=loginForm(request.POST)
        if form.is_valid() and logins.is_valid():
            a=logins.save(commit=False)
            a.usertype=3
            a.save()
            b=form.save(commit=False)
            b.login_userid = a
            b.save()
            return redirect('home')
    else:
        form=Userform()
        logins=loginForm()
    return render(request,'user_registration.html',{'form':form,'logins':logins})

def user_home(request):
    return render(request,'user_home.html')

def station_home(request):
    return render(request,'station_home.html')

def login_page(request):
    if request.method=='POST':
        form= login_check(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            try:
                user = login.objects.get(email=email)
                if user.password == password:
                    if user.usertype == 2:
                        request.session['stationid']=user.id
                        return redirect('stationhome')
                    elif user.usertype == 1:
                        request.session['staffid']=user.id
                        return redirect('staffhome')
                    elif user.usertype == 3:
                        request.session['userid']=user.id
                        return redirect('userhome')
                    elif user.usertype == 4:
                        request.session['adminid']=user.id
                        return redirect('adminhome')
                    else:
                        messages.error(request, 'Invalid user type')
                else:
                    messages.error(request,'Invalid Password')
            except login.DoesNotExist:
                messages.error(request,'User does not exist')
        else:
            return render(request,'login.html',{'form': form})


    else:
        form=login_check()
    return render(request,'login.html',{'form': form})






def station_profile(request):
    loginid = request.session.get('stationid')
    if not loginid:  # If user is not logged in
        return redirect('login')  # Redirect to login page (update 'login' with your login URL name)
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

def staffreg(request):
    if request.method=='POST':
        form=stafform(request.POST)
        logins=loginForm(request.POST)
        if form.is_valid() and logins.is_valid():
            a=logins.save(commit=False)
            a.usertype=1
            a.save()
            b=form.save(commit=False)
            selected_station = form.cleaned_data['staff_station'] 
            b.staff_station = selected_station
            
            b.staff_login_id = a
            b.save()
            return redirect('home')
    else:
         form=stafform()
         logins=loginForm()
    return render(request,'staff_reg.html',{'forms':form,'log':logins})


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
    data = criminals.objects.all()
    return render(request,'view_criminal_details.html',{'details' : data})

def staff_view(request):
    # Get the station ID from the session
    data1 = request.session.get('stationid')

    if not data1:  # If user is not logged in
        return redirect('login')  # Redirect to login page (update 'login' with your login URL name)
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
    query=request.GET.get('q','')
    results=police_station.objects.all()
    if query:
        results=results.filter(
            Q(addressline1__icontains=query) |
            Q(district__icontains=query) |
            Q(city__icontains=query) 
        )
    return render(request,'search_station.html', {'results': results, 'query':query})
    

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




def view_petition(request):
    staffid = request.session.get('staffid')
    if not staffid:  # If user is not logged in
        return redirect('login')  # Redirect to login page (update 'login' with your login URL name)
    else:
        station = get_object_or_404(login, id=staffid)
        staff = get_object_or_404(staff_reg, staff_login_id=station.id)
        staff_stations = staff.staff_station  
        petitions = petition.objects.filter(login_id=staff_stations)
        user_details = user_reg.objects.filter(login_userid__in=petitions.values_list('login_userid', flat=True))

        return render(request, 'staffview_petition.html', {
            'petitions': petitions,
            'user_details': user_details
        }
        )

    

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
    staffid = request.session.get('staffid')

    if not staffid:  # If user is not logged in
        return redirect('login')  # Redirect to login page (update 'login' with your login URL name)
    else:
        station = get_object_or_404(login, id=staffid)
        staff = get_object_or_404(staff_reg, staff_login_id=station.id)
        staff_stations = staff.staff_station  
        petitions = petition.objects.filter(login_id=staff_stations)
        user_details = user_reg.objects.filter(login_userid__in=petitions.values_list('login_userid', flat=True))
        return render(request, 'station_petitionview.html', {
            'petitions': petitions,
            'user_details': user_details
        }
        )

def station_fir_view(request):
    station = request.session.get('stationid')
    if not station:  # If user is not logged in
        return redirect('login')  # Redirect to login page (update 'login' with your login URL name)
    else:
        stationid = get_object_or_404(login, id=station)

        petition_details = petition.objects.filter(login_id=stationid)

        fir_details = fir.objects.filter(public_petition_id__in=petition_details)

        return render(request, 'view_FIR.html', {'petition_details': petition_details, 'fir_details': fir_details,})


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






def make_enquiry(request, login_id):
    user_id=request.session.get('userid')
    if not user_id:  # If user is not logged in
        return redirect('login')  # Redirect to login page (update 'login' with your login URL name)
    else:
        login_details=get_object_or_404(login,id=user_id)
        station = get_object_or_404(login,id=login_id)
        # print(login_details.id)
        # print(station.login_id)

        if request.method == 'POST':
            form = EnquiryForm(request.POST, request.FILES)
            if form.is_valid():
                a=form.save(commit=False)
                a.user_id=login_details
                a.station_id=station
                a.save()
                return redirect('station_search') 
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
    logout(request)
    return redirect('home')


def assign_staff(request,id):
    # Get the station ID from the session
    data1 = request.session.get('stationid')
    petitionid = get_object_or_404(petition,id=id)  


    if not data1:  # If user is not logged in
        return redirect('login')  # Redirect to login page (update 'login' with your login URL name)
    else:
        staffdata = get_object_or_404(login, id=data1)
        data = staff_reg.objects.filter(staff_station=staffdata)
        return render(request, 'assign_staff.html', {'details': data , 'petition':petitionid.id} )
    
def assign_staff_process(request,staffid,petitionid):
    id_petition = get_object_or_404(petition,id=petitionid)
    staff = get_object_or_404(staff_reg,id=staffid) 
    staff_assign.objects.create(
        staff_id = staff,
        petition_id = id_petition
    )

    return redirect('petitionview') 




def view_assigned_petition(request):
    data = request.session.get('staffid')
    staff = get_object_or_404(staff_reg, staff_login_id=data)
    petition_data = staff_assign.objects.filter(staff_id=staff).select_related('petition_id__login_userid')
    return render(request, 'assigned_petitions.html', {'data': petition_data})
  
    
    


    
