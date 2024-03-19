from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth import authenticate,login
from product_accessorie_app import validetors
from .models import ProductBag, BagItem, Order
from server_object_app.models import Division,District,Upazila
from customer_user_app.models import Customer
from user_app.models import CustomUser
from customer_user_app.models import CustomerProfile
from customer.views import guest_user_update_product_bag
import random
# Create your views here.
#confirm Place order
def place_order_confirm(request):
    if request.method == 'POST':
        try:
            shipping_method = request.POST['shipping_method']
        except:
            shipping_method = None
        check_value = 0
        if shipping_method == None:
            check_value = 1
            messages.add_message(request,messages.WARNING,'Please add shipping method')
        payment_method = request.POST['payment_method']


        first_name = request.POST['first_name']
        last_name = request.POST['last_name']

        phone_number = request.POST['phone_number']
        if validetors.is_valid_bangladesh_phone_number(phone_number) != True:
            messages.add_message(request,messages.WARNING,'Bad request. user name min=3 max=15 letter and number')
            check_value = 1
        
        email = request.POST['email']
        try:
            address = request.POST['address']
        except:
            address = None
        if address == None:
            check_value = 1
            messages.add_message(request,messages.WARNING,'Please add Deliviery Address')
        try:
            division = request.POST['division']
        except:
            division = None
        if division == None:
            check_value = 1
            messages.add_message(request,messages.WARNING,'Please add your Division')
        try:
            district = request.POST['district']
        except:
            district = None
        if district == None:
            check_value = 1
            messages.add_message(request,messages.WARNING,'Please add your District')
        try:
            upazila = request.POST['upazila']
        except:
            upazila = None
        if upazila == None:
            check_value = 1
            messages.add_message(request,messages.WARNING,'Please add your Upazila')
        if check_value == 1:
            return redirect('customer:checkout_view')
        else:
            order_number = "Turongo-"+str(random.randint(111111,999999))
            while Order.objects.filter(order_number = order_number) is None:
                order_number = "Turongo-"+str(random.randint(111111,999999)) 
            if request.user.is_authenticated:
                product_bag = ProductBag.objects.filter(user = request.user,bag_status=False).first()
                order_save = Order.objects.create(
                    bag = product_bag,
                    payment_method = payment_method,
                    delivery_charge = int(shipping_method),
                    first_name = first_name,
                    last_name = last_name,
                    email = email,
                    phone_number = phone_number,
                    address = address,
                    order_number=order_number,
                    division = Division.objects.get(id = int(division)),
                    district = District.objects.get(id = int(district)),
                    upazila = Upazila.objects.get(id= int(upazila))
                )
                if order_save:
                    order_save.save()
                    product_bag.bag_status = True
                    product_bag.save()
                    bag_items = BagItem.objects.filter(bag = product_bag)
                    for item in bag_items:
                        item.regular_price = item.product.p_price
                        item.order_price = item.product.p_offer_price
                        item.save()
                    messages.add_message(request,messages.SUCCESS,'Congratulations,Your order create successfully')
                    request.session['checkout_gtag_url'] = 1
                    return redirect('customer:profile_order_list_view')
            else:
                check_phone_number = CustomUser.objects.filter(phone_number = phone_number).first()
                if check_phone_number is None:
                    new_customer = Customer.objects.create_customer(
                        phone_number = phone_number,
                        user_name = first_name,
                        password = phone_number,
                        )
                    new_customer.save()
                    user = authenticate(request,username = phone_number,password=phone_number)
                    if user:
                        CustomUser.objects.filter(phone_number = phone_number).update(
                            email =email,
                            first_name = first_name,
                            last_name = last_name
                        )
                        login(request,user)
                    guest_user_update_product_bag(request)
                    product_bag = ProductBag.objects.filter(user = request.user,bag_status=False).first()
                    
                    order_save = Order.objects.create(
                        bag = product_bag,
                        payment_method = payment_method,
                        delivery_charge = int(shipping_method),
                        first_name = first_name,
                        last_name = last_name,
                        email = email,
                        phone_number = phone_number,
                        address = address,
                        order_number=order_number,
                        division = Division.objects.get(id = int(division)),
                        district = District.objects.get(id = int(district)),
                        upazila = Upazila.objects.get(id= int(upazila))
                    )
                    profile = CustomerProfile.objects.get(user = request.user)
                    profile.address = address
                    profile.division = Division.objects.get(id = int(division))
                    profile.district = District.objects.get(id = int(district))
                    profile.upazila = Upazila.objects.get(id= int(upazila))
                    profile.save()
                    if order_save:
                        order_save.save()
                        product_bag.bag_status = True
                        product_bag.save()
                        bag_items = BagItem.objects.filter(bag = product_bag)
                        for item in bag_items:
                            item.regular_price = item.product.p_price
                            item.order_price = item.product.p_offer_price
                            item.save()
                        messages.add_message(request,messages.SUCCESS,'Congratulations,Your order create successfully')
                        request.session['checkout_gtag_url'] = 1
                        return redirect('customer:profile_order_list_view')
                else:
                    messages.add_message(request,messages.WARNING,'Please add valid phone number. Number already add')
            
        return redirect('customer:checkout_view')


def checkout_gtag(request):
    order = Order.objects.filter(bag__user = request.user,order_status = "PENDING").latest('order_id')
    bag_items = BagItem.objects.filter(bag = order.bag).order_by('id')
    items = []
    fbq_items = []
    for bitem in bag_items:
        item = dict()
        fbq_item = dict()
        item['item_id'] = bitem.product.p_id
        item['item_name'] = bitem.product.p_name
        item['discount'] = int(bitem.product.p_offer)
        item['regular_price'] = int(bitem.product.p_price)
        item['discount_price'] = int(bitem.product.p_offer_price)
        item['item_brand'] = bitem.product.p_brand.brand_name
        if bitem.product.p_third_category:
            item['item_category'] = bitem.product.p_third_category.rc_three_name
        else:
            item['item_category'] = None
        if bitem.product.p_category:
            item['item_category2'] = bitem.product.p_category.category_name
        else:
            item['item_category2'] = None
        item['quantity'] = bitem.quantity
        item['size'] = bitem.product_size
        item['sub_total'] = int(bitem.sub_total)

        fbq_item['content_id'] = bitem.product.p_id
        fbq_item['content_name'] = bitem.product.p_name
        fbq_item['value'] = int(bitem.product.p_offer_price)
        fbq_item['content_type'] = "product"
        if bitem.product.p_third_category:
            fbq_item['content_category'] = bitem.product.p_third_category.rc_three_name
        else:
            fbq_item['content_category'] = None
        items.append(item)
        fbq_items.append(fbq_item)
    order_layer = dict()
    order_layer['order_id'] = order.order_number
    order_layer['total_amount'] = order.total_amount
    order_layer['shipping_cost'] = order.delivery_charge
    order_layer['quantity'] = order.bag.bag_total_items
    order_layer['division'] = order.division.division_name
    order_layer['district'] = order.district.district_name
    order_layer['upazila'] = order.upazila.upazila_name
        
    del request.session['checkout_gtag_url']
    # ,'order':order_layer,'items':items
    return JsonResponse({"status":"success",'order':order_layer,'items':items,'fbq_items':fbq_items},safe=False)
    # return JsonResponse({"status":"success",})

