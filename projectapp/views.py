from django.shortcuts import render,redirect,get_object_or_404
from .forms import StationForm,loginForm,login_check,station_profile_form,station_email_form
from .models import login,police_station
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
    



# def edit_station_profile(request,id):
    

    