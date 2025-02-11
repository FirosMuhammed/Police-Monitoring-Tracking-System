from django.db import models


# Create your models here.

class police_station(models.Model):
    station_id = models.CharField(max_length=100)
    addressline1= models.CharField(max_length=100)
    addressline2 = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    contact = models.CharField(max_length=15)
    login_id = models.ForeignKey('login',on_delete=models.CASCADE)
    
    def __str__(self):
        
        return self.addressline1


class login(models.Model):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    usertype = models.IntegerField(null=True)
    status = models.IntegerField(default=0)

class user_reg(models.Model):
    name=models.CharField(max_length=100)
    contact=models.CharField(max_length=15)
    login_userid=models.ForeignKey('login',on_delete=models.CASCADE,blank=True,null=True)

class staff_reg(models.Model):
    id=models.AutoField(primary_key=True)
    staff_id=models.CharField(max_length=100)
    staff_name=models.CharField(max_length=100)
    staff_address=models.CharField(max_length=100)
    staff_district=models.CharField(max_length=100)
    staff_city=models.CharField(max_length=100)
    staff_contact=models.CharField(max_length=100)
    staff_dob=models.CharField(max_length=100)
    staff_designation=models.CharField(max_length=100)
    staff_station= models.ForeignKey('police_station',on_delete=models.CASCADE,blank=True,null=True)

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

   