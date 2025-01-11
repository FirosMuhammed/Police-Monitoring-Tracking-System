from django.urls import path
from . import views

urlpatterns = [
    path('',views.home, name='home'),
    path('station_reg',views.Station_reg, name='station_registration'),
    path('login',views.login_page,name='login'),
    path('stationhome',views.station_home, name='stationhome'),
    path('stationprofile',views.station_profile, name='stationprofile'),
    
]