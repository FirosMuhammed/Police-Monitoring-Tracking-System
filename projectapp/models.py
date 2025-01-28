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
    


class login(models.Model):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    usertype = models.IntegerField(null=True)
    status = models.IntegerField(default=0)

class user_reg(models.Model):
    name=models.CharField(max_length=100)
    contact=models.CharField(max_length=15)
    login_userid=models.ForeignKey('login',on_delete=models.CASCADE,blank=True,null=True)