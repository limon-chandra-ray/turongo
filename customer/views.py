from django.shortcuts import render,redirect
from django.http import JsonResponse
from product_server_app.models import Product,ProductImage
from order_server_app.models import ProductBag,BagItem,Order
from server_object_app.models import Slider,Division,District,Upazila
from customer_user_app.models import CustomerProfile
from product_accessorie_app.models import PSize
from product_accessorie_app import validetors
from user_app.models import CustomUser
from django.db.models import Prefetch,Q
import uuid, json
from django.contrib import messages
# Create your views here.
def customer_home_view(request):
    if request.session.get('guest'):
        try:
            guest_session = request.session['guest']
            product_bag = ProductBag.objects.get(session_key = guest_session,bag_status=False)
            request.session['bag_total_items'] = product_bag.bag_total_items
        except:
            request.session['bag_total_items'] = 0
    if request.user.is_authenticated:
        try:
            product_bag = ProductBag.objects.get(user = request.user,bag_status=False)
            request.session['bag_total_items'] = product_bag.bag_total_items
        except:
            request.session['bag_total_items'] = 0
    product_image =Prefetch(
            'product_images',
            queryset=ProductImage.objects.filter(pimage_type="phone") 
        )
    products = Product.objects.prefetch_related(product_image).all()
    slide_image = Slider.objects.filter(slide_priority = 1).order_by('-id')[:3]
    slide_image2 = Slider.objects.filter(slide_priority = 2).last()
    context = {
        'slide_images':slide_image,
        'products':products,
        'slide_image2':slide_image2
    }
    return render(request,'customer/home.html',context)

def product_details_view(request,product_id):
    product_iamge_prefetch = Prefetch('product_images')
    product_size_prefetch = Prefetch('product_sizes')
    product = Product.objects.prefetch_related(product_iamge_prefetch,product_size_prefetch).get(p_id= product_id)
    context = {
        'product':product
    }
    return render(request,'customer/product/product-details.html',context)

#product add to card section
def product_add_to_cart(request):
    if request.method == 'POST':
        product_id = request.POST['product_id']
        select_product_size = request.POST['select_product_size']
        product_quantity= int(request.POST['product_quantity'])
        product = Product.objects.get(p_id = product_id)
        if request.user.is_authenticated:
            cart, created = ProductBag.objects.get_or_create(user = request.user,bag_status = False)
            cart_item,created = BagItem.objects.get_or_create(bag = cart,
                                                              product= product,
                                                              product_size = select_product_size
                                                              )
            cart_item.quantity += product_quantity 
            cart_item.save()
            total_cart_product = cart.bag_total_items
        else:
            try:
                cart, created = ProductBag.objects.get_or_create(session_key = request.session['guest'],bag_status = False)
                cart_item,created = BagItem.objects.get_or_create(bag = cart,product= product,
                                                                  product_size = select_product_size
                                                                  )
                cart_item.quantity += product_quantity 
                cart_item.save()
                total_cart_product = cart.bag_total_items
            except:
                request.session['guest'] = str(uuid.uuid4())
                cart, created = ProductBag.objects.get_or_create(session_key = request.session['guest'],bag_status = False)
                cart_item,created = BagItem.objects.get_or_create(bag = cart,
                                                                  product= product,
                                                                  product_size = select_product_size)
                cart_item.quantity += product_quantity 
                cart_item.save()
                total_cart_product = cart.bag_total_items
        message_status = "success"
        message_text = f'this product {select_product_size} size {product_quantity} quantity add'	
        return JsonResponse({"total_product":total_cart_product,
                             'status':'success',
                             'message_status':message_status,
                             'message_text':message_text
                             })
    
def guest_user_update_product_bag(request):
    if request.user.is_authenticated:
        try:
            session_user = request.session['guest']
        except:
            session_user = 'None'
        guest_product_bag = ProductBag.objects.filter(session_key = session_user,bag_status=False).first()
        auth_user_product_bag = ProductBag.objects.filter(user = request.user,bag_status=False).first()
        if auth_user_product_bag and guest_product_bag:
            guest_bag_items = BagItem.objects.filter(bag = guest_product_bag)
            for item in guest_bag_items:
                already_add_bag = BagItem.objects.filter(product_size = item.product_size,product = item.product,bag = auth_user_product_bag).first()
                if already_add_bag:
                    already_add_bag.quantity = already_add_bag.quantity + item.quantity
                    already_add_bag.save()
                else:
                    item.bag = auth_user_product_bag
                    item.save()
            guest_product_bag.delete()
            del request.session['guest']
            success_status = "success when auth user already product select"

        if auth_user_product_bag is None and guest_product_bag:

            guest_product_bag.user = request.user
            guest_product_bag.save()
            del request.session['guest']
            success_status = "success when auth user product without select"
    return JsonResponse({"status":success_status})



def card_product_view(request):
    if request.user.is_authenticated:
        
        bagitem_prefetch = Prefetch('bag_items')
        cart = ProductBag.objects.prefetch_related(bagitem_prefetch).filter(user = request.user,bag_status=False).first()
    else:
        try:
            session_guest = request.session['guest']
        except:
            session_guest = "None"
        bagitem_prefetch = Prefetch('bag_items')

        cart = ProductBag.objects.prefetch_related(
                                bagitem_prefetch
                                ).filter(
                                    session_key = session_guest,
                                    bag_status=False
                                    ).first()
    context={
        'cart':cart
    }
    return render(request,'customer/order/card-product.html',context)
def card_product_view2(request):
    if request.user.is_authenticated:
        
        bagitem_prefetch = Prefetch('bag_items')
        cart = ProductBag.objects.prefetch_related(bagitem_prefetch).get(user = request.user,bag_status=False)
    else:
        session_guest = request.session['guest']
        bagitem_prefetch = Prefetch('bag_items')

        cart = ProductBag.objects.prefetch_related(
                                bagitem_prefetch
                                ).get(
                                    session_key = session_guest,
                                    bag_status=False
                                    )
    bag = []
    for item in cart.bag_items.all():
        item_dict = dict()
        product_image = item.product.product_images.filter(pimage_type='icon',pimage_priority=1).first()
        item_dict['image'] = product_image.p_image.url
        item_dict['size'] = item.product_size
        item_dict['quantity'] = item.quantity
        item_dict['sub_total'] = item.sub_total
        item_dict['title'] = item.product.p_name
        item_dict['price'] = item.product.p_price
        item_dict['offer_price'] = item.product.p_offer_price
        item_dict['offer'] = item.product.p_offer
        item_dict['item'] = item.id
        bag.append(item_dict)
 
    return JsonResponse({"status":'success',
                         "bag_items":bag,
                         'total_amount':cart.bag_total_amount,
                         'total_items':cart.bag_total_items,
                         'bag_status':cart.bag_status
                         },safe=False)

def bag_item_quantity_change(request):
    if request.method == 'POST':
        item_id = request.POST['item']
        action_type = request.POST['action']
        bag_item = BagItem.objects.get(id = int(item_id))
        if action_type == 'remove':
            bag_item.quantity -= 1
            message_status = "success"
            message_text = 'product 1 quantity minus'
        if action_type == 'add':
            bag_item.quantity += 1
            message_status = "success"
            message_text = 'product 1 quantity add'	
        bag_item.save()
        if bag_item.quantity == 0:
            bag_item.delete()
            message_status = "warning"
            message_text = 'cart items to delete product'
        product_bag = ProductBag.objects.get(bag_id = bag_item.bag.bag_id)
        request.session['bag_total_items'] = product_bag.bag_total_items
        return JsonResponse({'status':"success","message_status":message_status,"message_text":message_text})
# product order section
def checkout_view(request):
    if request.user.is_authenticated:
        
        bagitem_prefetch = Prefetch('bag_items')
        cart = ProductBag.objects.prefetch_related(bagitem_prefetch).filter(user = request.user,bag_status=False).first()
    else:
        try:
            session_guest = request.session['guest']
        except:
            session_guest = "None"
        bagitem_prefetch = Prefetch('bag_items')

        cart = ProductBag.objects.prefetch_related(
                                bagitem_prefetch
                                ).filter(
                                    session_key = session_guest,
                                    bag_status=False
                                    ).first()
    divisions = Division.objects.all()
    context={
        'cart':cart,
        'divisions':divisions
    }
    return render(request,'customer/order/checkout.html',context)


        

#customer profile section
def customer_profile_view(request):
    return render(request,'customer/profile/profile.html')

def profile_order_list_view(request):
    order_list = Order.objects.filter(bag__user = request.user).order_by('order_id')
    context={
        'order_list':order_list
    }
    return render(request,'customer/profile/order.html',context)

def profile_address_view(request):
    divisions = Division.objects.all()
    context={
        'divisions':divisions
    }
    return render(request,'customer/profile/address.html',context)
def profile_address_update(request):
    if request.method == 'POST':
        address = request.POST['address']
        division = request.POST['division']
        district = request.POST['district']
        upazila = request.POST['upazila']
        customer_profile = CustomerProfile.objects.get(user = request.user)
        customer_profile.address = address
        customer_profile.division = Division.objects.get(id = int(division))
        customer_profile.district = District.objects.get(id = int(district))
        customer_profile.upazila = Upazila.objects.get(id = int(upazila))
        customer_profile.save()
        messages.add_message(request,messages.SUCCESS,'your address update successfully')
        return redirect('customer:profile_address_view')

def profile_customer_info_view(request):
    if request.method == 'POST':
        user_name = request.POST['user_name']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        phone_number = request.POST['phone_number']
        email = request.POST['email']
        check_value = 0
        if user_name != request.user.user_name:
            check_value = 1
        if first_name != request.user.first_name:
            check_value = 1
        if last_name != request.user.last_name:
            check_value = 1
        
        if email != request.user.email:
            check_value = 1
        if phone_number != request.user.phone_number:
            custom_user = CustomUser.objects.filter(phone_number = phone_number).exclude(phone_number = request.user.phone_number).count()
            if custom_user > 0:
                phone_number = request.user.phone_number
                messages.add_message(request,messages.WARNING,'your update phone number already added')
            else:
                if validetors.is_valid_bangladesh_phone_number(phone_number):
                    check_value = 1
                else:
                    phone_number = request.user.phone_number
                    messages.add_message(request,messages.WARNING,'bad request. Please add valid phone number')
        if check_value == 1:
            CustomUser.objects.filter(id = request.user.id).update(
                email = email,
                user_name = user_name,
                phone_number = phone_number,
                first_name = first_name,
                last_name = last_name
            )
            return redirect('customer:profile_customer_info_view')
    return render(request,'customer/profile/edit-account.html')
def profile_password_change_view(request):
    return render(request,'customer/profile/change-password.html')