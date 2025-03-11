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
    path('admin_stationview' ,views.admin_stationview, name='admin_stationview'),
    path('admin_staffview' ,views.admin_staffview, name='admin_staffview'),
    path('admin_complaintview' ,views.admin_complaintview, name='admin_complaintview'),

    path('reply_complaint/<int:id>/' ,views.reply_complaint, name='reply_complaint'),




    path('criminals_userview' ,views.user_criminal_view, name='criminals_userview'),
    path('staff_details' ,views.staff_view, name='staff_details'),
    path('add_duty/<int:id>',views.add_duty,name='add_duty'),
    path('myduty' ,views.my_duty, name='myduty'),
    path('view_duty/<int:id>' ,views.view_duties, name='view_duty'),x 
    path('duty_delete/<int:id>' ,views.delete_duty, name='duty_delete'),
    path('duty_edit/<int:id>' ,views.edit_duty, name='duty_edit'),
    path('station_search' ,views.search_stations, name='station_search'),
    path('petition/<int:id>' ,views.file_petition, name='petition'),
    path('petitionview' ,views.view_petition, name='petitionview'),
    path('fir/<int:id>/', views.file_fir, name='file_fir'),


    path('petitionview_station' ,views.station_view_petition, name='petitionview_station'),
    path('stationview_fir' ,views.station_fir_view, name='stationview_fir'),

    path('case_status/<int:petition_id>' ,views.case_status, name='case_status'),

    path('petitionview_public' ,views.public_view_petition, name='petitionview_public'),

    path('petition_edit/<int:id>' ,views.edit_petition, name='petition_edit'),

    path('petition_delete/<int:id>' ,views.delete_petition, name='petition_delete'),

    path('complaint_form' ,views.file_complaint, name='complaint_form'),
    path('view_complaint/', views.view_complaints, name='view_complaint'),
    path('complaint_delete/<int:id>' ,views.delete_complaint, name='complaint_delete'),
    path('complaint_edit/<int:id>' ,views.edit_complaint, name='complaint_edit'),
    path('make_enquiry/<int:login_id>' ,views.make_enquiry, name='make_enquiry'),
    path('view_enquiry' ,views.view_enquiry, name='view_enquiry'),

    path('reply_enquiry/<int:id>' ,views.reply_enquiry, name='reply_enquiry'),
    path('enquiry_viewuser' ,views.enquiry_viewuser, name='enquiry_viewuser'),
    path('edit_enquiry/<int:id>' ,views.edit_enquiry, name='edit_enquiry'),
    path('delete_enquiry/<int:id>' ,views.delete_enquiry, name='delete_enquiry'),
    path('staff_attendance' ,views.staff_attendance, name='staff_attendance'),
    path('mark_attendance/<int:id>' ,views.mark_attendance, name='mark_attendance'),
    path('search_attendance' ,views.search_attendance, name='search_attendance'),



















    

    
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)