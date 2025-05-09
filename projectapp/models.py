from django.db import models


# Create your models here.

class police_station(models.Model):
    id = models.AutoField(primary_key=True)
    station_id = models.CharField(max_length=100)
    addressline1 = models.CharField(max_length=100)
    addressline2 = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    contact = models.CharField(max_length=15)
    login_id = models.OneToOneField('login', on_delete=models.CASCADE, related_name='station_as_loginid')

    def __str__(self):
        return f"{self.station_id} - {self.addressline1}"



class login(models.Model):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    usertype = models.IntegerField(null=True)
    status = models.IntegerField(default=0)

class user_reg(models.Model):
    name=models.CharField(max_length=100)
    contact=models.CharField(max_length=15)
    login_userid=models.OneToOneField('login',on_delete=models.CASCADE,blank=True,null=True,related_name='user_as_loginid')

class staff_reg(models.Model):
    id=models.AutoField(primary_key=True)
    staff_id=models.CharField(max_length=100)
    staff_name=models.CharField(max_length=100)
    staff_address=models.CharField(max_length=100)
    staff_district=models.CharField(max_length=100)
    staff_city=models.CharField(max_length=100)
    staff_contact=models.CharField(max_length=100)
    staff_dob=models.CharField(max_length=100)
    # staff_designation=models.CharField(max_length=100)

    ROLE_CHOICES = [
        ('Constable', 'Constable'),
        ('Head Constable', 'Head Constable'),
        ('SHO', 'SHO'),
        ('ASI', 'ASI'),
        ('Sub Inspector', 'Sub Inspector'),
        ('Inspector', 'Inspector'),
        ('DYSP', 'DYSP'),
        



    ]

    staff_designation = models.CharField(max_length=30, choices=ROLE_CHOICES, default='Constable')

    staff_station= models.ForeignKey('login',on_delete=models.CASCADE,blank=True,null=True,related_name='station_staff')

    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]

    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='Male')

    staff_login_id=models.ForeignKey('login',on_delete=models.CASCADE,null=True)

class criminals(models.Model):
   
    photo=models.FileField(upload_to='criminalface/')
    criminal_name=models.CharField(max_length=100) 
    crime_details=models.CharField(max_length=500)
    criminal_age=models.IntegerField()
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other')
        ]
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='Male')

    login_staffid=models.ForeignKey('staff_reg',on_delete=models.CASCADE,blank=True,null=True)




class duties(models.Model):
    duty = models.CharField(max_length=100)
    current_date = models.DateField(auto_now_add=True)
    staff_login_id = models.ForeignKey(login, on_delete=models.CASCADE, related_name='duties_as_staff')
    login_id = models.ForeignKey(login, on_delete=models.CASCADE, default=0, related_name='duties_as_login')





class petition(models.Model):
    case = models.CharField(max_length=100)
    case_details = models.CharField(max_length=100)
    day = models.CharField(max_length=15)
    date = models.DateField(null=True, blank=True)
    time = models.TimeField(blank=True, null=True)
    recieved_time1 = models.TimeField(auto_now_add=True)
    place = models.CharField(max_length=100)
    current_date = models.DateField(auto_now_add=True)
    suspect = models.CharField(max_length=150)
    properties_involved = models.TextField()
    total_value_property = models.CharField(max_length=100)

    login_userid = models.ForeignKey('login',on_delete=models.CASCADE,blank=True,null=True, related_name='petition_as_user')
    login_id = models.ForeignKey('login', on_delete=models.CASCADE,blank=True, null=True, related_name='petition_as_station',db_column='station_login_id' )
    case_status = models.CharField(max_length=200,null=True)



    def __str__(self):
        return f"Petition for {self.case} - {self.place}"
    


class fir(models.Model):
    district = models.CharField(max_length=50)
    pstation = models.CharField(max_length=50)
    fir_no = models.IntegerField()
    year = models.IntegerField()
    date_time = models.DateTimeField(auto_now_add=True)
    acts = models.CharField(max_length=50)
    sections = models.CharField(max_length=40)
    
    content_fir = models.TextField()
    staff_loginid = models.ForeignKey(login, on_delete=models.CASCADE, related_name='fir_as_staff')
    public_petition_id = models.ForeignKey(petition, on_delete=models.CASCADE, related_name='petition_as_id')





class complaints(models.Model):
    complaint = models.TextField()
    current_date = models.DateField(auto_now_add=True)
    user_logid =models.ForeignKey(login, on_delete=models.CASCADE)
    reply = models.CharField(max_length=400, null= True)


class enquiries(models.Model):
    enquiry =  models.TextField()
    current_date = models.DateField(auto_now_add=True)
    station_id = models.ForeignKey(login, on_delete=models.CASCADE, related_name='station_as_id')
    user_id = models.ForeignKey(login, on_delete=models.CASCADE, related_name='user_as_id')
    staff_reply =  models.TextField()


class attendance(models.Model):
    current_date = models.DateField(auto_now_add=True)
    staff_id =models.ForeignKey(staff_reg, on_delete=models.CASCADE)

class staff_assign(models.Model):
    current_date = models.DateField(auto_now_add=True)
    staff_id =models.ForeignKey(staff_reg, on_delete=models.CASCADE)
    petition_id = models.ForeignKey(petition, on_delete=models.CASCADE, related_name='userpetition_as_id')




   


  




















