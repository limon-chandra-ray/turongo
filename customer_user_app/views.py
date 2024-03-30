from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout,hashers
from user_app.models import CustomUser
from customer_user_app.models import CustomerProfile,Customer
from product_accessorie_app import validetors
from django.contrib import messages
# Create your views here.
def login_view(request):
    return render(request,'customer/auth/login.html')

def register_view(request):
    return render(request,'customer/auth/registration.html')

def user_logout(request):
    logout(request)
    return redirect("customer:customer_home_view")

def customer_add(request):
    if request.method == 'POST':
        user_name = request.POST['user_name']
        phone_number = request.POST['phone_number']
        # password = request.POST['password']
        # password2 = request.POST['password2']

        check_phone_number = CustomUser.objects.filter(phone_number = phone_number).first()
        valid_check = 0
        # if validetors.is_valid_username(user_name) != True:
        #     messages.add_message(request,messages.WARNING,'Bad request. user name min=3 max=15 letter and number')
        #     valid_check = 1
        
        
        if validetors.is_valid_bangladesh_phone_number(phone_number):
            if check_phone_number:
                messages.add_message(request,messages.WARNING,'Phone number already Add. Please add valid phone number')
                valid_check = 1
        else:
            messages.add_message(request,messages.WARNING,'bad request. Please add valid phone number')
            valid_check = 1
        # if password != password2:
        #     messages.add_message(request,messages.WARNING,"Password and confirm-password dont's match")
        #     valid_check = 1

        if valid_check != 1:
            new_customer = Customer.objects.create_customer(
                    phone_number = phone_number,
                    user_name = user_name,
                    password = phone_number
                )
            new_customer.save()
            user = authenticate(request,username = phone_number,password=phone_number)
            if user:
                login(request,user)
                if request.user.role == 'CUSTOMER':
                    messages.add_message(request,messages.SUCCESS,'your acctount create successfully')
                    return redirect('customer:customer_home_view')
                else:
                    logout(request)
        
        return redirect('customer:register_view')
    
def customer_login(request):
    if request.method == 'POST':
        phone_number = request.POST['phone_number']
        if CustomUser.objects.filter(phone_number = phone_number).exists():
            password = request.POST['phone_number']
            user = authenticate(request,username = phone_number,password=password)
            if user:
                login(request,user)
                if request.user.role == 'CUSTOMER':
                    messages.add_message(request,messages.SUCCESS,'your acctount active successfully')
                    return redirect('customer:customer_home_view')
                else:
                    logout(request)
                    messages.add_message(request,messages.WARNING,'Please add valid information')
            else:
                messages.add_message(request,messages.WARNING,'Please add valid information')
        else:
            messages.add_message(request,messages.WARNING,'Please add valid information')
    return redirect('customer:login_view')

def customer_change_password(request):
    if request.method == 'POST':
        password = request.POST['password']
        repassword = request.POST['repassword']
        password_check = password == repassword and len(repassword) >= 8
        if password_check:
            CustomUser.objects.filter(id = request.user.id).update(
                password = hashers.make_password(repassword)
            )
            
            user_login = authenticate(request,username=request.user.phone_number,password=repassword)
            if user_login is not None:
                login(request,user_login)
                if request.user.is_authenticated:
                    messages.add_message(request,messages.SUCCESS,"Password update successfully")
                    return redirect('customer:customer_profile_view')
