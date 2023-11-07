
from django.urls import path #, include

from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from . import views
urlpatterns = [
    path('',views.index,name="index"),
    #path('', views.home, name="index"),
    #path('login_user/', views.login_user, name='login_user'),  # Use the new view name
    path('login/', views.login_user, name='login'),

     #path('', views.index, name="index"),
    path('register_user/',views.register_user,name="register_user"),
    path('about/',views.index,name="about"),
    path('adminpanel/',views.adminpanel,name="adminpanel"),
    #path('user_list/',views.user_list,name="user_list"),
   
path('Customer_Profile/', views.Customer_Profile, name='Customer_Profile'),  # Add this line,
    path('logout/', views.custom_logout, name='logout'),

    #path('forgotpassword',views.forgotpassword,name="forgotpassword"),
  
    #path('userhome/logout',view.userlogout,name="logout")
    path('add_product/',views.add_product,name='add_product'),
    path('view_products/',views.view_products,name='view_products'),
    path('service/', views.service, name='service'),
    path('repair/', views.repair, name='repair'),
    

    path('reset_password/', auth_views.PasswordResetView.as_view(), name="reset_password"),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),

    path('customer_products/', views.customer_product_view, name='customer_products'),

    path('edit_product/<int:product_id>/', views.edit_product, name='edit_product'),


    path('delete_product/<int:product_id>/', views.delete_product, name='delete_product'),
    path('view_cart/', views.view_cart, name='view_cart'),
#          path('product/<int:product_id>/', views.view_details, name='view_details'),
    path('view_details/<int:product_id>/', views.view_details, name='view_details'),

 path('increase-cart-item/<int:product_id>/', views.increase_cart_item, name='increase-cart-item'),
    path('decrease-cart-item/<int:product_id>/', views.decrease_cart_item, name='decrease-cart-item'),
 path('fetch-cart-count/', views.fetch_cart_count, name='fetch-cart-count'),
 path('add_address/', views.add_address, name='add_address'),
    path('remove-from-cart/<int:product_id>/', views.remove_from_cart, name='remove-from-cart'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
path('add_another_address/', views.add_another_address, name='add_another_address'),
  path('create-order/', views.create_order, name='create-order'),
    path('handle-payment/',views. handle_payment, name='handle-payment'),
    path('checkout/', views.checkout, name='checkout'),
]




 

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


