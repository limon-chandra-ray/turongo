from django.urls import path
from . import views
from customer_user_app.views import (customer_login,customer_add,login_view,register_view,user_logout,customer_change_password)
from order_server_app.views import place_order_confirm,checkout_gtag
app_name = 'customer'
urlpatterns = [
    path('',views.customer_home_view,name='customer_home_view'),
    path('product-<uuid:product_id>-details',views.product_details_view,name='product_details_view'),
    path('guest-to-auth-user-bag-update',views.guest_user_update_product_bag,name='guest_user_update_product_bag')

]

# customer product add card
urlpatterns +=[
    path('product-add-to-cart',views.product_add_to_cart,name='product_add_to_cart'),
    path('cart-product-items',views.card_product_view,name='card_product_view'),
    path('cart-product-items2',views.card_product_view2,name='card_product_view2'),
    path('cart-item-quantity-change',views.bag_item_quantity_change,name='bag_item_quantity_change'),
    path('cart-<int:item_id>-item-delete',views.customer_cart_item_delete,name='customer_cart_item_delete'),
    path('cart-igtam-get',views.view_cart_datalayer_item,name='view_cart_datalayer_item')
]

#checkout and order confirm
urlpatterns += [
    path('cart-product-checkout',views.checkout_view,name="checkout_view"),
    path('place-order-save',place_order_confirm,name='place_order_confirm'),
    path('checkout-gtag-data',checkout_gtag,name='checkout_gtag'),
    path('chckout-fbq-data',views.checkout_json_data,name='checkout_json_data')
]

#division,district,upazila
from server_object_app.views import district_get,upazila_get
urlpatterns +=[
    path('district',district_get,name='district_get'),
    path('upazila',upazila_get,name='upazila_get')
]


# customer authentication system
urlpatterns +=[
    path('log-in',login_view,name='login_view'),
    path('register',register_view,name='register_view'),
    path('log-out',user_logout,name='user_logout'),
    path('new-customer-add',customer_add,name='customer_add'),
    path('log-in-check',customer_login,name='customer_login'),
    path('change-password',customer_change_password,name='customer_change_password')
]

# customer profile section
urlpatterns +=[
    path('account',views.customer_profile_view,name="customer_profile_view"),
    path('account/orders',views.profile_order_list_view,name='profile_order_list_view'),
    path('account/edit-information',views.profile_customer_info_view,name='profile_customer_info_view'),
    path('account/edit-address',views.profile_address_view,name='profile_address_view'),
    path('account/address-update',views.profile_address_update,name='profile_address_update'),
    path('account/change-password',views.profile_password_change_view,name='profile_password_change_view')
]

#category product list
urlpatterns +=[
    path('<str:category>',views.category_product_list,name='category_product_list'),
]

# urlpatterns +=[
#     path("abr",views.abp_view,name='abp_view'),
#     path("cookie-policy",views.cookie_policy_view,name='cookie_policy_view'),
#     path('order-procedure',views.order_procedure_view,name='order_procedure_view'),

#     path("payment-method",views.payment_method_view,name='payment_method_view'),
#     path('payment-and-shipping-policy',views.payment_shipping_policy_view,name='payment_shipping_policy_view'),
#     path("privacy-policy",views.privacy_policy_view,name='privacy_policy_view'),
#     path("return-and-refund-policy",views.return_refund_policy_view,name='return_refund_policy_view'),
#     path('size-guide',views.size_guide_view,name='size_guide_view'),
#     path('trems-conditions',views.trems_conditions_view,name='trems_conditions_view'),
#     path("limon-work",views.limon_work,name='limon_work')
# ]
urlpatterns +=[
    path("about-us/",views.website_about_us,name='website_about_us'),
    path('trems-and-conditions/',views.website_trems_and_condition,name='website_trems_and_condition'),
    path('return-and-refund-policy/',views.website_return_and_refund,name='website_return_and_refund'),
    path('cookies-policy/',views.website_cookie_policy_,name='website_cookie_policy_'),
    path('product-size-guide/',views.website_product_size_guide,name='website_product_size_guide'),
    path('order-traking/',views.order_traking_view,name='order_traking_view'),
    path('payment-and-shipping-policy/',views.payment_shipping_policy_view,name='payment_shipping_policy_view'),
    path("privacy-policy/",views.privacy_policy_view,name='privacy_policy_view'),
]