from django.shortcuts import render,redirect
from django.http import JsonResponse
from product_server_app.models import Product,ProductImage,RootCategoryThree,Category
from order_server_app.models import ProductBag,BagItem,Order,ProductBag
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
            queryset=ProductImage.objects.filter(pimage_type="phone",pimage_priority = 1) 
        )
    products = Product.objects.prefetch_related(product_image).all().order_by('-p_id')
    slide_image = Slider.objects.filter(slide_priority = 1,slide_status = True).order_by('-id')[:3]
    slide_image2 = Slider.objects.filter(slide_priority = 2,slide_status = True).last()

    formal_shirt = products.filter(p_category__id = 2)
    polo_shirt = products.filter(p_third_category__id = 4)
    combo_offer = products.filter(p_third_category__id = 5)
    context = {
        'slide_images':slide_image,
        'polo_shirts':polo_shirt,
        'slide_image2':slide_image2,
        'formal_shirt':formal_shirt,
        'combo_offer':combo_offer
    }
    return render(request,'customer/home.html',context)

def category_product_list(request,category):
    product_image =Prefetch(
            'product_images',
            queryset=ProductImage.objects.filter(pimage_type="phone",pimage_priority = 1) 
        )
    category = RootCategoryThree.objects.filter(rc_three_name__icontains = category).first()
    products = Product.objects.prefetch_related(product_image).filter(p_third_category = category).order_by('-p_id')
    context={
        'products': products,
        'category':category
    }
    return render(request,'customer/product/products.html',context)


def product_details_view(request,product_id):
    product_iamge_prefetch = Prefetch('product_images',queryset=ProductImage.objects.all().order_by('pimage_priority'))
    product_size_prefetch = Prefetch('product_sizes')
    product_image =Prefetch(
            'product_images',
            queryset=ProductImage.objects.filter(pimage_type="phone",pimage_priority = 1) 
        )
    product = Product.objects.prefetch_related(product_iamge_prefetch,product_size_prefetch).get(p_id= product_id)
    related_product = Product.objects.prefetch_related(product_image).filter(p_category = product.p_category).order_by('-p_id')[:3]
    context = {
        'product':product,
        'related_product':related_product
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
        
        product_detail = dict()
        product_detail['title'] = product.p_name
        product_image = ProductImage.objects.filter(product=product,
                                                    pimage_type = 'icon',
                                                    pimage_priority=1,
                                                    image_status = True).first()
        product_detail['image'] = product_image.p_image.url
        product_detail['price'] = product.p_price
        product_detail['offer_price'] = product.p_offer_price
        product_detail['offer'] = product.p_offer
        return JsonResponse({"total_product":total_cart_product,
                             'status':'success',
                             'message_status':message_status,
                             'message_text':message_text,
                             'product':product_detail
                             })
    
def guest_user_update_product_bag(request):
    if request.user.is_authenticated:
        try:
            session_user = request.session['guest']
        except:
            session_user = 'None'
        guest_product_bag = ProductBag.objects.filter(session_key = session_user,bag_status=False).first()
        auth_user_product_bag = ProductBag.objects.filter(user = request.user,bag_status=False).first()
        success_status = ''
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
        if success_status == '':
            success_status = "error"
    else:
        success_status = "error"
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


def view_cart_datalayer_item(request):
    bagitem_prefetch = Prefetch('bag_items')
    if request.user.is_authenticated:
        cart_items = ProductBag.objects.prefetch_related(bagitem_prefetch).filter(user = request.user,bag_status = False).last()
    
    else:
        try:
            session_guest = request.session['guest']
            cart_items = ProductBag.objects.prefetch_related(bagitem_prefetch).filter(session_key = session_guest,bag_status = False).last()
        except:
            pass
    items = []
    cart_total_quantity = 0
    cart_total_price = 0
    if cart_items:
        for bitem in cart_items.bag_items.all():
            item = dict()
            item['item_id'] = bitem.product.p_id
            item['item_name'] = bitem.product.p_name
            item['discount'] = float(bitem.product.p_offer)
            item['regular_price'] = float(bitem.product.p_price)
            item['discount_price'] = float(bitem.product.p_offer_price)
            item['item_brand'] = bitem.product.p_brand.brand_name
            item['item_category'] = bitem.product.p_third_category.rc_three_name
            item['item_category2'] = bitem.product.p_category.category_name
            item['quantity'] = bitem.quantity
            item['size'] = bitem.product_size
            item['sub_total'] = float(bitem.sub_total)
            items.append(item)
        cart_total_quantity = cart_items.bag_total_items
        cart_total_price = cart_items.bag_total_amount


    return JsonResponse({'status':"success",'ctq':cart_total_quantity,'ctp':cart_total_price,'items':items})

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
    product_ids  = []
    fbq_items = []
    for bitem in cart.bag_items.all():
        fbq_item = dict()
        fbq_item['content_id'] = str(bitem.product.p_id)
        fbq_item['content_name'] = bitem.product.p_name
        fbq_item['value'] = int(bitem.product.p_offer_price)
        fbq_item['content_type'] = "product"
        if bitem.product.p_third_category:
            fbq_item['content_category'] = bitem.product.p_third_category.rc_three_name
        else:
            fbq_item['content_category'] = None
        fbq_item['quantity'] = int(bitem.quantity)
        fbq_items.append(fbq_item)
        product_ids.append(str(bitem.product.p_id))
    print(fbq_items)
    print(product_ids)
    divisions = Division.objects.all()
    context={
        'cart':cart,
        'divisions':divisions,
        'fbq_items':fbq_items,
        'product_ids':product_ids
    }
    return render(request,'customer/order/checkout.html',context)
def checkout_json_data(request):
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
    product_ids  = []
    fbq_items = []
    for bitem in cart.bag_items.all():
        fbq_item = dict()
        fbq_item['content_id'] = str(bitem.product.p_id)
        fbq_item['content_name'] = bitem.product.p_name
        fbq_item['value'] = int(bitem.product.p_offer_price)
        fbq_item['content_type'] = "product"
        if bitem.product.p_third_category:
            fbq_item['content_category'] = bitem.product.p_third_category.rc_three_name
        else:
            fbq_item['content_category'] = None
        fbq_item['quantity'] = int(bitem.quantity)
        fbq_items.append(fbq_item)
        product_ids.append(str(bitem.product.p_id))
    return JsonResponse({"status":'success','quantity':cart.bag_total_items,'value':cart.bag_total_amount,'fbq_items':fbq_items,'product_ids':product_ids},safe=False)


def customer_cart_item_delete(request,item_id):
    item = BagItem.objects.get(id = int(item_id))
    if item:
        item.delete()
        messages.add_message(request,messages.SUCCESS,'your cart to item delete successfully')
    else:
        messages.add_message(request,messages.WARNING,'Invalid cart item request')
    return redirect('customer:card_product_view')
    


#customer profile section
def customer_profile_view(request):
    return render(request,'customer/profile/profile.html')

def profile_order_list_view(request):
    order_list = Order.objects.filter(bag__user = request.user).order_by('-id')
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



#footer page about policy
def about_us_view(request):
    return render(request,'customer/about/about-us.html')
def cookie_policy_view(request):
    return render(request,'customer/about/cookie-policy.html')
def order_procedure_view(request):
    return render(request,'customer/about/order-procedure.html')
def order_traking_view(request):
    return render(request,'customer/about/order-traking.html')
def payment_method_view(request):
    return render(request,'customer/about/payment-method.html')

def payment_shipping_policy_view(request):
    return render(request,'customer/about/payment-shipping-policy.html')
def privacy_policy_view(request):
    return render(request,'customer/about/privacy-policy.html')
def return_refund_policy_view(request):
    return render(request,'customer/about/return-refund-policy.html')
def size_guide_view(request):
    return render(request,'customer/about/size-guide.html')
def trems_conditions_view(request):
    return render(request,'customer/about/trems-conditions.html')