from django.urls import path
from . import views

urlpatterns = [
    path('',views.home, name='home'),
    path('station_reg',views.Station_reg, name='station_registration'),
    path('userreg',views.user_regs,name='userreg'),
    path('login',views.login_page,name='login'),
    path('stationhome',views.station_home, name='stationhome'),
    path('stationprofile',views.station_profile, name='stationprofile'),
    path('userhome',views.user_home,name='userhome'),
    path('userprofile',views.user_profile,name='userprofile'),
    path('staff_reg',views.staffreg,name='staff_reg'),
    path('staffhome',views.staff_home,name='staffhome'),
    path('staffprofile',views.staff_profile,name='staffprofile'),
    path('uploadcriminals',views.form_criminal,name='uploadcriminals'),

    
]