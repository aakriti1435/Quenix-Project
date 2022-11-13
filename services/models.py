from django.db import models
from accounts.constants import *
from accounts.models import *


class Services(models.Model):
    name = models.CharField(null=True, blank=True, max_length=255)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='service_images/', blank=True, null=True)
    created_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    created_on = models.DateTimeField(null=True, blank=True, auto_now_add=True)
    updated_on = models.DateTimeField(null=True, blank=True, auto_now=True)
    
    class Meta:
        managed = True;
        db_table = 'tbl_services'
        
        
        
        
