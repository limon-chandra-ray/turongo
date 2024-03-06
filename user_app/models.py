from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from .managers import CustomUserManager
# Create your models here.
class CustomUser(AbstractBaseUser):
    class Role(models.TextChoices):
        ADMIN = 'ADMIN','Admin'
        CUSTOMER = 'CUSTOMER','Customer'
        STAFF   = 'STAFF', 'Staff'
    base_role = Role.ADMIN

    first_name = models.CharField(max_length=50,null=True,blank=True)
    last_name = models.CharField(max_length=50,null=True,blank=True)
    user_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=250,null=True,blank=True)
    phone_number = models.CharField(unique=True,max_length=11)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    role = models.CharField(max_length=30,choices=Role.choices)
    created_at = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    updated_at = models.DateTimeField(auto_now=True,null=True,blank=True)
    
    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['user_name']
    objects = CustomUserManager()
    def __str__(self):
        return self.user_name + " " + self.phone_number
    
    def has_perm(self,prem,obj=None):
        return True
    def has_module_perms(self,app_label):
        return True
    
    def save(self,*args, **kwargs):
        if not self.pk:
            self.role = self.base_role
            return super().save(*args, **kwargs)
