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
    path('product-<uuid:product__uuid>-delete',views.delete_product,name='delete_product'),
    path('active-products',views.active_product_view,name='active_product_view')
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
]