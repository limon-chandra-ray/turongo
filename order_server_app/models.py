from django.db import models
from user_app.models import CustomUser
from product_server_app.models import Product
from server_object_app.models import Division,District,Upazila
import uuid
# Create your models here.

class DeliveryMethod(models.Model):
    name = models.CharField(max_length = 250,unique = True)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True) 
    def __str__(self):
        return self.name

class PickupPoint(models.Model):
    pickup_name = models.TextField()
    address = models.TextField()
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True) 
    def __str__(self):
        return self.pickup_name




class ProductBag(models.Model):
    bag_id = models.UUIDField(primary_key=True,default=uuid.uuid4,unique=True,editable=False,auto_created=True)
    user = models.ForeignKey(CustomUser,on_delete = models.SET_NULL,null=True,blank=True)
    bag_status = models.BooleanField(default=False)
    session_key = models.CharField(max_length = 250,null=True,blank=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True) 

    @property
    def bag_total_amount(self):
        orderitems = self.bag_items.all()
        total = sum([item.sub_total for item in orderitems])
        return total
    @property
    def bag_total_items(self):
        orderitems = self.bag_items.all()
        total = sum([item.quantity for item in orderitems])
        return total
    
    # def __str__(self):
    #     return self.user.user_name
    

class BagItem(models.Model):
    bag = models.ForeignKey(ProductBag,on_delete=models.CASCADE,related_name="bag_items")
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    order_price = models.IntegerField(null=True,blank=True)
    regular_price = models.IntegerField(null=True,blank=True)
    product_size = models.CharField(max_length=50)
    quantity = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True) 

    @property
    def sub_total(self):
        total = self.quantity * self.product.p_offer_price
        return total
    

class Order(models.Model):
    class OrderStatus(models.TextChoices):
        INCOMPLETED = 'INCOMPLETED','Incompleted'
        COMPLETED = 'COMPLETED','Completed'
        CANCEL = 'CANCEL','Cancel'
        SHIPPING = 'SHIPPING','Shipping'
        PENDING = 'PENDING', 'Pending'
        HOLD = 'HOLD','Hold'
        PROCESSING = 'PROCESSING', 'Processing'
    default_status = OrderStatus.PENDING
    bag = models.ForeignKey(ProductBag,on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=8,decimal_places = 2,null=True,blank=True)
    order_status = models.CharField(max_length=100,choices = OrderStatus.choices,default = default_status)
    payment_method = models.CharField(max_length=250,null=True,blank=True)
    delivery_charge = models.IntegerField(default = 0)
    first_name = models.CharField(max_length = 250,null=True,blank=True)
    last_name = models.CharField(max_length = 250,null=True,blank=True)
    full_name = models.CharField(max_length=255, null=True, blank=True)
    phone_number = models.CharField(max_length = 250,null=True,blank=True)
    email = models.EmailField(null=True,blank=True)
    address = models.TextField(null=True,blank=True)
    division = models.ForeignKey(Division,on_delete= models.SET_NULL,null=True,blank=True)
    district = models.ForeignKey(District,on_delete= models.SET_NULL,null=True,blank=True)
    upazila = models.ForeignKey(Upazila,on_delete= models.SET_NULL,null=True,blank=True)
    order_number = models.CharField(max_length=150,null=True,blank=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    # def __str__(self):
    #     return self.order_id

    def save(self,*args, **kwargs):
        if self.delivery_charge:
            self.total_amount = self.delivery_charge + self.bag.bag_total_amount
            super(Order,self).save(*args, **kwargs)
    
   
    

