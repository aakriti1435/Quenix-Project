from django.contrib.auth.models import AbstractUser
from django.db import models
from .constants import *


"""
User Model
"""
class User(AbstractUser):
    username = models.CharField(max_length=255,blank=True, null=True, unique=True)
    first_name = models.CharField(null=True, blank=True, max_length=255)
    last_name = models.CharField(null=True, blank=True, max_length=255)
    full_name = models.CharField(max_length=255,null=True,blank=True)
    dob = models.DateField(auto_now=False, auto_now_add=False, null=True, blank=True)
    gender = models.PositiveIntegerField(choices=GENDER, null=True, blank=True, default=MALE)
    email = models.EmailField("email address", null=True, blank=True)
    mobile_no = models.CharField(null=True, blank=True, max_length=255)
    profile_pic = models.ImageField(upload_to='profile_pic/', blank=True, null=True)
    role_id = models.PositiveIntegerField(default=CUSTOMER,choices=USER_ROLE, null=True, blank=True)
    state = models.PositiveIntegerField(default=ACTIVE, choices=USER_STATUS, null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    service_role = models.PositiveIntegerField(choices=SERVICE_USER_ROLE, null=True, blank=True)
    temp_otp = models.CharField(null=True, blank=True, max_length=10)


    class Meta:
        managed = True;
        db_table = 'tbl_user'

    def __str__(self):
        return str(self.username)


"""
Login History
"""
class LoginHistory(models.Model):
    user_ip = models.CharField( max_length=255, null=True, blank=True)
    user_agent = models.CharField(max_length=255, null=True, blank=True)
    status = models.PositiveIntegerField(choices=LOGIN_STATUS, null=True, blank=True, default=LOGIN_SUCCESS)
    code = models.CharField(max_length=255, null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    user = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        managed = True
        db_table = 'tbl_login_history'


"""
Cities
"""
class Cities(models.Model):
    city = models.CharField(null=True, blank=True, max_length=255)
    created_on = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    class Meta:
        managed = True
        db_table = 'tbl_cities'

