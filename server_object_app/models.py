from django.db import models

# Create your models here.
class Slider(models.Model):
    slide_link = models.URLField(max_length=250,null=True,blank=True)
    slide_image = models.FileField(upload_to="slide-image/")
    slide_status = models.BooleanField(default = False)
    slide_priority = models.IntegerField(default = 1)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True) 

    def __str__(self):
        return self.slide_link
    

class Division(models.Model):
    division_name = models.CharField(max_length=150,unique=True, null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.division_name
    

class District(models.Model):
    division = models.ForeignKey(Division,on_delete=models.CASCADE)
    district_name = models.CharField(max_length=150,unique=True,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.district_name

class Upazila(models.Model):
    district = models.ForeignKey(District,on_delete=models.CASCADE)
    upazila_name = models.CharField(max_length=150,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.upazila_name
    
