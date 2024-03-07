from django.urls import path
from . import views

app_name = 'server_app'
urlpatterns = [
    path('dashboard',views.dashboard,name='dashboard')
]

# product section urls
urlpatterns += [
    path('product-add',views.product_add_view,name='product_add_view'),
    path('product-save',views.product_save,name='product_save'),
    path('product-<uuid:product_id>-edit',views.product_edit_view,name='product_edit_view'),
    path('product-<uuid:product_id>-save-edit',views.product_edit_save,name='product_edit_save'),
    path('product-<uuid:product__uuid>-delete',views.delete_product,name='delete_product'),
    path('active-products',views.active_product_view,name='active_product_view'),
    path('category-get',views.category_get,name='category_get')
]
#product detials urls
urlpatterns +=[
    path('product-<uuid:product_id>-size-details',views.product_size_details,name='product_size_details'),
    path('product-size-details',views.product_size_detail_get,name='product_size_detail_get'),
    path('product-size-update',views.product_size_update,name='product_size_update')
]

#order section
# urlpatterns +=[
#     path('product-add-to-card/',product_add_to_card,name='product_add_to_card')
# ]

# slider image section
urlpatterns +=[
    path('all-slides',views.slider_list_view,name='slider_list_view'),
    path('new-slide-save',views.slider_add,name='slider_add'),
    path('slide-add',views.slider_add_view,name='slider_add_view'),
    path('slide-<int:slide_id>-delete',views.slider_delete,name='slider_delete'),
    path('slide-<int:slide_id>-edit',views.slider_edit,name='slider_edit'),
    path('slide-<int:slide_id>-status-change',views.slide_status_change,name='slide_status_change'),
    
]

#super-admin auth
urlpatterns += [
    path('login',views.super_admin_login_view,name='super_admin_login_view'),
    path('super-admin-authentication-check',views.super_admin_check,name='super_admin_check'),
    path('log-out',views.super_admin_logout,name='super_admin_logout')
]
