from django.db import models
import uuid
from django.db.models import signals
from django.dispatch import receiver
from product_accessorie_app.models import PBrand,PSize,PColor
from django_ckeditor_5.fields import CKEditor5Field
from user_app.models import CustomUser
# Create your models here.
class RootCategory(models.Model):
    rc_name = models.CharField(max_length=150,unique=True)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True) 
    def __str__(self):
                return self.rc_name

class RootCategoryTwo(models.Model):
    rc_two_name = models.CharField(max_length=150)
    root_category = models.ForeignKey(RootCategory,on_delete=models.CASCADE)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True) 
    def __str__(self):
                return self.rc_two_name
class RootCategoryThree(models.Model):
    rc_three_name = models.CharField(max_length=150)
    root_category_two = models.ForeignKey(RootCategoryTwo,on_delete=models.CASCADE)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True) 
    def __str__(self):
                return self.rc_three_name

class Category(models.Model):
    category_name = models.CharField(max_length=150)
    root_category_three = models.ForeignKey(RootCategoryThree,on_delete=models.CASCADE)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
            return self.category_name

class Product(models.Model):
    p_id = models.UUIDField(primary_key=True,default=uuid.uuid4,unique=True,editable=False,auto_created=True)
    p_name = models.CharField(max_length=250)
    p_price = models.BigIntegerField()
    p_offer_price = models.BigIntegerField(null=True,blank=True)
    p_offer = models.DecimalField(max_digits=5,decimal_places=2,null=True,blank=True)
    p_status = models.BooleanField(default=False)
    p_third_category = models.ForeignKey(RootCategoryThree,on_delete=models.SET_NULL,null=True,blank=True)
    p_category = models.ForeignKey(Category,on_delete = models.SET_NULL,null=True,blank=True)
    p_brand = models.ForeignKey(PBrand,on_delete=models.SET_NULL,null=True,blank=True)
    p_description = CKEditor5Field()
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.p_name
    
    def save(self,*args, **kwargs):
        if self.p_price and self.p_offer_price is None:
              self.p_offer_price = self.p_price
        if self.p_price != self.p_offer_price:
            lose_price = self.p_price - self.p_offer_price
            offer_percentage = (lose_price*100)//self.p_price
            self.p_offer = offer_percentage
        return super(Product,self).save(*args, **kwargs)
    @property
    def total_product(self):
        product_size = self.product_sizes.all()
        total = sum([product.quantity for product in product_size])
        return total
class ProductSize(models.Model):
    product = models.ForeignKey(Product,on_delete = models.CASCADE,related_name="product_sizes")
    p_size = models.ForeignKey(PSize,on_delete = models.CASCADE)
    quantity = models.BigIntegerField(default=0,null=True,blank=True)
    psize_status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def save(self,*args, **kwargs):
        if self.quantity == 0:
            self.psize_status = False
        else:
             self.psize_status = True
        return super(ProductSize,self).save(*args, **kwargs)

class ProductImage(models.Model):
    product = models.ForeignKey(Product,on_delete = models.CASCADE,related_name="product_images")
    p_image = models.FileField(upload_to='product/')
    pimage_type = models.CharField(max_length = 50)
    pimage_priority = models.IntegerField(default = 0,null=True,blank=True)
    image_status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)


    def save(self,*args, **kwargs):
        if self.id:
            product_image = ProductImage.objects.get(id = self.id)

            if product_image.p_image != self.p_image:
                product_image.p_image.delete(save=False)
            
        super(ProductImage,self).save(*args, **kwargs)

    @receiver(signals.pre_delete, sender='product_server_app.ProductImage')
    def product_image_pre_delete_signal(sender,instance, **kwargs):
        for field in instance._meta.fields:
            if field.name == 'p_image':
                product_image = getattr(instance,field.name)
                if product_image:
                    product_image.delete(save=False)
    
class ProductAsk(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser,on_delete=models.SET_NULL,null=True,blank=True)
    question = models.TextField(null=True,blank=True)
    ask_answer = models.TextField(null=True,blank=True)
    ask_status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)