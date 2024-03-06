from django.db import models

# Create your models here.
class UserGender(models.Model):
    gender_name = models.CharField(max_length=50,unique=True)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.gender_name
class ProductType(models.Model):
    ptype_name = models.CharField(max_length=50,unique=True)    
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.ptype_name
    
class PSize(models.Model):
    size_name = models.CharField(max_length =50)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.size_name
    
class PBrand(models.Model):
    brand_name = models.CharField(max_length =100,unique=True)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.brand_name
    
class PColor(models.Model):
    color_name = models.CharField(max_length =100,unique=True)
    color_code = models.CharField(max_length =100,unique=True)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.color_name
    