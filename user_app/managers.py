from django.contrib.auth.models import BaseUserManager


class CustomUserManager(BaseUserManager):
    def create_staff(self,user_name,phone_number,password=None):
        staff = self.model(
            user_name = user_name,
            phone_number = phone_number
        )
        staff.set_password(password)
        staff.save(using = self._db)
        return staff
    
    def create_customer(self,user_name,phone_number,password=None):
        customer = self.model(
            user_name = user_name,
            phone_number = phone_number
        )
        customer.set_password(password)
        customer.save(using = self._db)
        return customer
    
    def create_superuser(self,user_name,phone_number,password=None):
        admin = self.model(
            phone_number = phone_number,
            user_name    = user_name
        )
        admin.set_password(password)
        admin.is_admin  = True
        admin.is_staff  = True
        admin.save(using = self._db)
        return admin