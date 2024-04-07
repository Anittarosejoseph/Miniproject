from django.urls import path
from .views import upload_video
from .views import display_videos

from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from . import views 

urlpatterns = [
    path('', views.index, name="index"),
    path('login/', views.login_user, name='login'),
    path('register_user/', views.register_user, name="register_user"),
    path('about/', views.index, name="about"),
    path('adminpanel/', views.adminpanel, name="adminpanel"),
    path('Customer_Profile/', views.Customer_Profile, name='Customer_Profile'),
    path('logout/', views.custom_logout, name='logout'),
    path('add_product/', views.add_product, name='add_product'),
    path('view_products/', views.view_products, name='view_products'),
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
    path('view_details/<int:product_id>/', views.view_details, name='view_details'),
    path('increase-cart-item/<int:product_id>/', views.increase_cart_item, name='increase-cart-item'),
    path('decrease-cart-item/<int:product_id>/', views.decrease_cart_item, name='decrease-cart-item'),
    path('fetch-cart-count/', views.fetch_cart_count, name='fetch-cart-count'),
    path('add_address/', views.add_address, name='add_address'),
    path('remove-from-cart/<int:product_id>/', views.remove_from_cart, name='remove-from-cart'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('create-order/', views.create_order, name='create-order'),
    path('handle-payment/', views.handle_payment, name='handle-payment'),
    path('checkout/', views.checkout, name='checkout'),
    path('user_list/', views.user_list, name='user_list'),
    # path('customize/<int:product_id>/', views.customize_watch, name='customize_watch'),
    # path('view_entered_details/<int:product_id>/', views.view_entered_details, name='view_entered_details'),
    path('upload_video/', upload_video, name='upload_video'),
  path('add_custom/', views.add_custom, name='add_custom'),
      path('edit_custom/', views.edit_custom, name='edit_custom'),
        path('custpro/', views.custpro, name='custpro'),
# urls.py
    path('view_custom/<int:product_id>/', views.custom_view, name='view_custom'),
    path('customize_watch/<int:product_id>/', views.customize_watch, name='customize_watch'),

    
    path('view_custom/', views.view_custom, name='view_custom'),
    path('block_unblock_user/<int:user_id>/', views.block_unblock_user, name='block_unblock_user'),
    path('all_user_orders/', views.all_user_orders, name='all_user_orders'),
    path('approve_disapprove_order/', views.approve_disapprove_order, name='approve_disapprove_order'),
    path('search_products/',views.search_products, name='search_products'),
    path('sort-products/', views.sort_products, name='sort_products'),
    path('filter-products-by-category/', views.filter_products_by_category, name='filter_products_by_category'),
    path('remove_order_item/<int:item_id>/', views.remove_order_item, name='remove_order_item'),
    path('ordersummary/', views.ordersummary, name='ordersummary'),
    path('deliveryteamreg/', views.delivery_team_registration, name='deliveryteamreg'),
    path('deliveryindex/',views. deliveryindex, name='deliveryindex'),
    path('delivery_team_list/', views.delivery_team_list, name='delivery_team_list'),
    path('change_password/', views.change_password, name='change_password'),
    path('wishlist/', views.wishlist, name='wishlist'),
    path('myorders/', views.myorders, name='myorders'),
    path('update-order-status/', views.update_order_status, name='update_order_status'),
    path('deliverorders/', views.deliver_orders, name='deliverorders'),
    path('all_orders/', views.all_orders, name='all_orders'),
    path('update-order-status/<int:order_id>/', views.update_order_status, name='update_order_status'),
    path('delete-order/<int:order_id>/', views.delete_order, name='delete_order'),
    path('order_history/', views.order_history, name='order_history'),
    path('bill/<int:order_id>/', views.bill, name='bill'),
    path('admin_order_list/', views.admin_order_list, name='admin_order_list'),
    path('assign_delivery_team/', views.assign_delivery_team, name='assign_delivery_team'),
        path('assign_technician/<int:repair_request_id>/<int:technician_id>/', views.assign_technician, name='assign_technician'),
    path('financial-report/', views.financial_report_pdf, name='financial-report'),  # Define the URL pattern with the correct name
   path('display_videos/', display_videos, name='display_videos'),
    path('delivery-team-orders/', views.delivery_team_orders, name='delivery_team_orders'),
    # path('unisex_products/', views.unisex_products, name='unisex_products'),
  path('videos/delete/<int:video_id>/',views.delete_video, name='delete_video'),
  path('order_status/', views.order_status, name='order_status'),
    path('videos/', views.video_list, name='videos'),
    path('edit/<int:video_id>/', views.edit_video, name='edit_video'),
    path('save_edits/<int:video_id>/', views.save_edits, name='save_edits'),
    path('remove_from_wishlist/<int:wishlist_item_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),
    path('add_to_wishlist/<int:id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('panel/',views.panel,name='panel'),
    path('techlist/', views.techlist, name='techlist'),
    path('techindex/',views.techindex, name='techindex'),
    path('edit_profile/',views.edit_profile, name='edit_profile'),
    path('repairing/',views.repairing,name='repairing'),
    path('techreg/', views.techreg, name='techreg'),
    path('thank-you/', views.thank_you_page, name='thank_you_page'),
    path('repair/',views.repair,name='repair'),
    path('watchrepairrequest/', views.watchrepairrequest_list, name='watchrepairrequest_list'),
    # path('email_template/', views.email_template, name='email_template'),
    path('faq/', views.faq_view, name='faq'),
    path('approve_repair/<int:repair_id>/', views.approve_repair, name='approve_repair'),
    path('reject_repair/<int:repair_id>/', views.reject_repair, name='reject_repair'),
    path('messages_page/', views.messages_page,name='messages_page'),
    path('user_repair_history/', views.user_repair_history, name='user_repair_history'),
  path('repair_payment/<int:repair_id>/',views.repair_payment, name='repair_payment'),
    path('repair_payment_success/<int:repair_id>/',views.repair_payment_success, name='repair_payment_success'),
  path('add_service/', views.add_service, name='add_service'),
    path('view_bill/<int:repair_id>/', views.view_bill, name='view_bill'),
    path('add_address/', views.add_address, name='add_address'),
    
    path('add_to_shopping_cart/<int:watch_id>/', views.add_to_shopping_cart, name='add_to_shopping_cart'),
    path('remove_from_/<int:watch_id>/', views.remove_from_shopping_cart, name='remove_from_cart'),

    path('view_shopping_cart/', views.view_shopping_cart, name='view_shopping_cart'),  # Changed from view_cart
    path('view_service/', views.view_service, name='view_service'),
    path('order_status/', views.order_status, name='order_status'),
    path('ordercancellation/<int:order_id>/', views.order_cancellation, name='order_cancellation'),
]



if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
