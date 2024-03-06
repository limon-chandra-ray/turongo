from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout,hashers
from django.db.models import Prefetch
from django.contrib import messages
from PIL import Image
from io import BytesIO
from django.core.files.storage import FileSystemStorage
from product_accessorie_app.models import PBrand,PSize
from product_server_app.models import Product,ProductImage,Category,ProductSize
from product_server_app.utils import date_to_str
from server_object_app.models import Slider
# Create your views here.

@login_required(login_url='/super-server/login')
def dashboard(request):
    return render(request,'server/super-admin/dashboard/main.html')


# Product Section
@login_required(login_url='super-server/login')
def product_add_view(request):
    category = Category.objects.all()
    brands = PBrand.objects.all()
    sizes = PSize.objects.all()
    context = {
        'categorys':category,
        'brands':brands,
        'sizes':sizes
    }
    return render(request,'server/super-admin/product/product-add.html',context)

def product_save(request):
    if request.method == 'POST':
        product_name = request.POST['product_name']
        regular_price = request.POST['regular_price']
        offer_price = request.POST['offer_price']
        product_category = request.POST['product_category']
        product_brand = request.POST['product_brand']
        product_description = request.POST['product_description']
        category = Category.objects.get(id = int(product_category))
        brand = PBrand.objects.get(id = int(product_brand))
        product = Product.objects.create(
            p_name = product_name,
            p_price = int(regular_price),
            p_offer_price = int(offer_price),
            p_category = category,
            p_brand = brand,
            p_description = product_description
        )
        product.save()
        product_size = request.POST.getlist('product_size')
        if product_size:
            for size in product_size:
                p_size = ProductSize.objects.create(
                    product = product,
                    p_size = PSize.objects.get(id = int(size))
                )
                p_size.save()
       
        product_image = request.FILES.getlist('product_image')
        if product_image:
            image_priority = 0
            for p_image in product_image:
                #Start product icon image created section
                image_priority += 1
                main_image = Image.open(p_image)
                main_image.thumbnail((100,100),Image.BICUBIC)
                thumbnail_buffer = BytesIO()
                main_image.save(thumbnail_buffer, format='WEBP')
                icon_fs = FileSystemStorage()
                icon_image = icon_fs.save(f'product/100X100/{date_to_str()}.webp',thumbnail_buffer)
                image_save = ProductImage.objects.create(
                    product = product,
                    p_image = icon_image,
                    pimage_type = 'icon',
                    pimage_priority = image_priority
                )
                image_save.save()
                #End Product icon image created section

                #Start product phone image created section
                phone_image = Image.open(p_image)
                phone_image.thumbnail((600,600),Image.BICUBIC)
                phone_thumbnail_buffer = BytesIO()
                phone_image.save(phone_thumbnail_buffer, format='WEBP')
                phone_fss = FileSystemStorage()
                phone_image = phone_fss.save(f'product/600X600/{date_to_str()}.webp',phone_thumbnail_buffer)
                phone_image_save = ProductImage.objects.create(
                    product = product,
                    p_image = phone_image,
                    pimage_type = 'phone',
                    pimage_priority = image_priority
                )
                phone_image_save.save()
                #End product phone image created section

                #Start product large image created section
                large_image = Image.open(p_image)
                large_image.thumbnail((1024,1024),Image.BICUBIC)
                large_thumbnail_buffer = BytesIO()
                large_image.save(large_thumbnail_buffer, format='WEBP')
                large_fss = FileSystemStorage()
                large_image = large_fss.save(f'product/1024X1024/{date_to_str()}.webp',large_thumbnail_buffer)
                large_image_save = ProductImage.objects.create(
                    product = product,
                    p_image = large_image,
                    pimage_type = 'large',
                    pimage_priority = image_priority
                )
                large_image_save.save()
                #End product large image created section
        
        messages.add_message(request,messages.SUCCESS,'New product add successfully')
        return redirect("server_app:active_product_view")
    

def delete_product(request,product__uuid):
    product = Product.objects.get(
        p_id = product__uuid
    )
    if product:
        product.delete()
        messages.add_message(request,messages.SUCCESS,'successfully Product delete')
    else:
        messages.add_message(request,messages.WARNING,'Empty Product')
    return redirect("server_app:active_product_view")
def active_product_view(request):
    product_image_prefetch = Prefetch('product_images',queryset=ProductImage.objects.filter(pimage_type="phone"))
    products = Product.objects.prefetch_related(product_image_prefetch).all()
    context={
        'products':products
    }
    return render(request,'server/super-admin/product/active-product.html',context)

# slider section
@login_required(redirect_field_name='super_admin_login_view')
def slider_list_view(request):
    slides = Slider.objects.all().order_by('-id')
    context = {
        'slides':slides
    }
    return render(request,'server/super-admin/slider-image/slide-image-list.html',context)
@login_required(redirect_field_name='super_admin_login_view')
def slider_add_view(request):
    return render(request,'server/super-admin/slider-image/slide-image-add.html')
@login_required(redirect_field_name='super_admin_login_view')
def slider_add(request):
    if request.method == 'POST':
        priority = request.POST['slide_priority']
        slide_image = request.FILES['slide_image']
        slide_link = request.POST['slide_link']

        #Start product phone image created section
        slide = Image.open(slide_image)
        slide.resize((982,500),Image.BICUBIC)
        slide_thumbnail_buffer = BytesIO()
        slide.save(slide_thumbnail_buffer,format="WEBP")
        phone_fss = FileSystemStorage()
        slide = phone_fss.save(f'slide-image/{date_to_str()}982X500.jpg',slide_thumbnail_buffer)
        slide_save = Slider.objects.create(
            slide_link = slide_link,
            slide_image = slide,
            slide_priority = priority
        )
        slide_save.save()
        #End product phone image created section
        messages.add_message(request,messages.SUCCESS,'New slide add successfully')
        return redirect('server_app:slider_list_view')
@login_required(redirect_field_name='super_admin_login_view')
def slider_delete(request,slide_id):
    slide = Slider.objects.get(id = int(slide_id))
    if slide:
        slide.delete()
        messages.add_message(request,messages.SUCCESS,'delete successfully')
    else:
        messages.add_message(request,messages.WARNING,'In-valid request')
    return redirect('server_app:slider_list_view')

@login_required(redirect_field_name='super_admin_login_view')
def slider_edit(request,slide_id):
    slide = Slider.objects.get(id = int(slide_id))
    if request.method == 'POST':
        try:
            slide_image = request.FILES['slide_image']
        except:
            slide_image = None
        slide_link = request.POST['slide_link']
        slide_priority = request.POST['slide_priority']
        if slide_image is not None:
            slide.slide_image = slide_image
        slide.slide_link = slide_link
        slide.slide_priority = int(slide_priority)
        slide.save()
        messages.add_message(request,messages.SUCCESS,'update slide successfully')
        return redirect('server_app:slider_list_view')
    else:
        context = {
            'slide':slide
        }
        return render(request,'server/super-admin/slider-image/slide-image-edit.html',context)
@login_required(redirect_field_name='super_admin_login_view')
def slide_status_change(request,slide_id):
    slide = Slider.objects.get(id = int(slide_id))
    if slide.slide_status is True:
        slide.slide_status = False
    else:
        slide.slide_status = True
    slide.save()
    messages.add_message(request,messages.SUCCESS,'slide status updated')
    return redirect('server_app:slider_list_view')
        

# super-server authentication
def super_admin_login_view(request):
    return render(request,'server/auth/login.html')

def super_admin_check(request):
    url_link = request.GET.get('next')
    if request.method == 'POST':
        phone_number = request.POST['phone_number'] 
        password = request.POST['password'] 
        
        print(url_link)
        user = authenticate(request,username = phone_number,password=password)
        if user:
            login(request,user)
            if request.user.role == 'ADMIN':
                messages.add_message(request,messages.SUCCESS,'your acctount active successfully')
                
            else:
                logout(request)
                messages.add_message(request,messages.WARNING,'Please add valid information')
        
        return redirect('super_app:dashboard')
    
def super_admin_logout(request):
    logout(request)
    return redirect("super_app:dashboard")

