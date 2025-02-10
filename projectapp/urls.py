from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',views.home, name='home'),
    path('Station_reg',views.Station_reg, name='Station_reg'),
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
    path('view_criminals' ,views.criminals_table, name='view_criminals'),
    path('criminal_delete/<int:id>' ,views.delete_criminals, name='criminal_delete'),
    path('criminal_edit/<int:id>' ,views.edit_criminals, name='criminal_edit'),
    path('adminhome' ,views.adminhome, name='adminhome'),
    path('admin_userview' ,views.admin_userview, name='admin_userview'),
    path('criminals_userview' ,views.user_criminal_view, name='criminals_userview'),
    path('staff_details' ,views.staff_view, name='staff_details'),
    path('add_duty/<int:id>',views.add_duty,name='add_duty'),
    path('myduty' ,views.my_duty, name='myduty'),

    path('view_duty/<int:id>' ,views.view_duties, name='view_duty'),
    path('duty_delete/<int:id>' ,views.delete_duty, name='duty_delete'),
    path('duty_edit/<int:id>' ,views.edit_duty, name='duty_edit'),



    

    
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)