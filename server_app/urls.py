from django.urls import path
from . import views

app_name = 'server_app'
urlpatterns = [
    path('dashboard',views.dashboard,name='dashboard'),
    path('product-feed-make',views.product_feed,name='product_feed')
]

# product section urls
urlpatterns += [
    path('product-add',views.product_add_view,name='product_add_view'),
    path('product-save',views.product_save,name='product_save'),
    path('product-<uuid:product_id>-edit',views.product_edit_view,name='product_edit_view'),
    path('product-<uuid:product_id>-save-edit',views.product_edit_save,name='product_edit_save'),
    path('product-<uuid:product__uuid>-delete',views.delete_product,name='delete_product'),
    path('product-<uuid:product__uuid>-status-change',views.product_status_change,name='product_status_change'),
    path('active-products',views.active_product_view,name='active_product_view'),
    path('in-active-products',views.inactive_product_view,name='inactive_product_view'),
    path('category-get',views.category_get,name='category_get')
]
#product detials urls
urlpatterns +=[
    path('product-<uuid:product_id>-size-details',views.product_size_details,name='product_size_details'),
    path('product-size-details',views.product_size_detail_get,name='product_size_detail_get'),
    path('product-size-update',views.product_size_update,name='product_size_update'),
    path("product-<uuid:product_id>-image-gallery",views.product_image_gallery,name='product_image_gallery'),
    path('product-image-<int:image_id>-<uuid:product_id>-gallery-update',views.product_image_update,name='product_image_update'),
    path('product-new-image-upload-<uuid:product_id>',views.product_new_image_add,name='product_new_image_add'),
    path("product-image-delete-<uuid:product_id>-<int:product_priority>",views.product_gallery_image_delete,name='product_gallery_image_delete')
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

#order urls
urlpatterns +=[
    path('all-order-list',views.all_order_list,name='all_order_list'),
    path('request-order-list',views.request_order_list,name='request_order_list'),
    path('processing-order-list',views.processing_order_list,name='processing_order_list'),
    path('shipping-order-list',views.shipping_order_list,name='shipping_order_list'),
    path('completed-order-list',views.completed_order_list,name='completed_order_list'),
    path('return-order-list',views.return_order_list,name='return_order_list'),
    path('cancel-order-list',views.cancel_order_list,name='cancel_order_list'),
    path('order-<int:order_id>-details',views.order_detail_view,name='order_detail_view'),
    path('order-<int:order_id>-details-status-update',views.order_status_update,name='order_status_update'),
    path('order-<int:order>-invoice',views.order_invoice,name='order_invoice'),
    # path('order-invoice-download/',views.render_pdf_view,name='render_pdf_view')
]

urlpatterns +=[
    path('csv-file-upload',views.csv_file_upload_view,name='csv_file_upload_view'),
    path("division-uploads",views.division_upload,name='division_upload'),
    path('district-upload',views.district_upload,name='district_upload'),
    path('upazila-upload',views.upazila_upload,name='upazila_upload')
]
