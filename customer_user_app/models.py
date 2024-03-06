from django.db import models
from django.shortcuts import get_object_or_404
from user_app.models import CustomUser
from django.dispatch import receiver
from django.db.models.signals import post_save,pre_delete
from PIL import Image
from server_object_app.models import Division,District,Upazila
# Create your models here.
class CustomerManager(models.Manager):
    def get_queryset(self,*args, **kwargs):
        result =  super().get_queryset(*args, **kwargs)
        return result.filter(role = CustomUser.Role.CUSTOMER)
class Customer(CustomUser):
    base_role = CustomUser.Role.CUSTOMER

    customer = CustomerManager()
    class Meta:
        proxy = True
        
@receiver(post_save,sender = Customer)
def create_staff_profile(sender,instance,created,*args, **kwargs):
    if created and instance.role == "CUSTOMER":
        CustomerProfile.objects.create(user = instance)

class CustomerProfile(models.Model):
    user = models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    profile_image = models.ImageField(upload_to='customer-profile/',null=True,blank=True)
    address = models.TextField(null=True,blank=True)
    division = models.ForeignKey(Division,on_delete= models.SET_NULL,null=True,blank=True)
    district = models.ForeignKey(District,on_delete= models.SET_NULL,null=True,blank=True)
    upazila = models.ForeignKey(Upazila,on_delete= models.SET_NULL,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    updated_at = models.DateTimeField(auto_now=True,null=True,blank=True)

    def __str__(self):
        return self.user.email

    def save(self,*args, **kwargs):
        if self.id:
            existing = get_object_or_404(CustomerProfile,id = self.id)
            if existing.profile_image != self.profile_image:
                existing.profile_image.delete(save=False)
        super(CustomerProfile,self).save(*args, **kwargs)
        if self.profile_image:
            logo = Image.open(self.profile_image.path)
            logo_size = (150,150)
            logo.thumbnail(logo_size,Image.BICUBIC)
            logo.save(self.profile_image.path)

    @receiver(pre_delete,sender="customer_user_app.CustomerProfile")
    def customer_profile_iamge_update(sender,instance,*args, **kwargs):
        for field in instance._meta.fields:
            if field.name == 'profile_image':
                logo = getattr(instance,field.name)
                if logo:
                    logo.delete(save=False)