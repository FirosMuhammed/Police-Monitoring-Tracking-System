from django.shortcuts import render,redirect,get_object_or_404
from .forms import StationForm,Userform,loginForm,login_check,station_profile_form,station_email_form,user_profile_form,user_email_form,criminal_form,stafform,staff_profile_form,staff_email_form
from .models import login,police_station,user_reg,staff_reg
from django.contrib  import messages


def home(request):
 
    return render (request,'home.html')

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
    return render(request,'user_registration.html',{'form':form,'log':logins})

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
                        request.session['userid']=user.id
                        return redirect('stationhome')
                    elif user.usertype == 1:
                        request.session['userid']=user.id
                        return redirect('staffhome')
                    elif user.usertype == 3:
                        request.session['userid']=user.id
                        return redirect('userhome')
                    elif user.usertype == 4:
                        request.session['userid']=user.id
                        return redirect('adminhome')
                    else:
                        messages.error(request, 'Invalid user type')
                else:
                    messages.error(request,'Invalid Password')
            except login.DoesNotExist:
                messages.error(request,'User does not exist')
    else:
        form=login_check()
    return render(request,'login.html',{'form': form})






def station_profile(request):
    loginid = request.session.get('userid')
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
    loginid = request.session.get('userid')
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
    if request.method == 'POST':
        form = criminal_form(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('staffhome') 
    else:
        form = criminal_form()
    return render(request, 'add_criminals.html', {'forms': form})


    