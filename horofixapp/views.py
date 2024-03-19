from django.shortcuts import render,redirect
from .models import CustomUser
from .models import CustomerProfile  # Import the correct model
from django.contrib.auth.decorators import login_required
# from django.contrib.sessions.models import Session
from django.contrib.auth import authenticate ,login as auth_login,logout 
from django.views.decorators.cache import never_cache
from django.contrib import messages
from .models import CustomUser
from .models import WatchProduct
from .models import Cart  # Import the Cart model
from django.http import HttpResponse
from .models import UserProfile
from .models import WishlistItem
from django.http import HttpResponseRedirect
from django.core.mail import send_mail
from django.urls import reverse

from django.shortcuts import get_object_or_404

 
@never_cache
def index(request):
    return render(request, 'index.html')
@login_required
def service(request):
    return render(request, 'service.html')
def repair(request):
    return render(request, 'repair.html')


def about(request):
    
    return render(request, 'about.html')

@never_cache
def register_user(request):
    if request.method == 'POST':
        name = request.POST.get('name', None)
        username = request.POST.get('username', None)
        email = request.POST.get('email', None)
        phone = request.POST.get('phone', None)
        password = request.POST.get('password', None)
        confirm_password = request.POST.get('confirm', None)
        # role = CustomUser.CUSTOMER
        if name and username and email and phone and password:
            if CustomUser.objects.filter(email=email).exists():
                messages.success(request,("Email is already registered."))
                return redirect('register_user')
            elif  CustomUser.objects.filter(username=username).exists():
                messages.success(request,("Username is already registered."))
                return redirect('register_user')

            
            elif password!=confirm_password:
                messages.success(request,("Password's Don't Match, Enter correct Password"))
            else:
                user = CustomUser(name=name,username=username, email=email, phone=phone)
                user.set_password(password)  # Set the password securely
                user.is_active=True
                user.save()
                user_profile = UserProfile(user=user)
                user_profile.save()

                # activateEmail(request, user, email)
                return redirect('login')  
            
    return render(request, 'register_user.html')

from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login
from django.shortcuts import render, redirect
from django.views.decorators.cache import never_cache
from .models import CustomUser

def login_user(request):
    if request.user.is_authenticated:
        return redirect('/')
      

    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")

        if username and password:
            user = authenticate(request, username=username, password=password)

            if user is not None:
                auth_login(request, user)

                if user.is_customer:
                    request.session["username"] = user.username
                    return redirect('/')
                elif user.is_deliveryteam :
                    request.session["username"] = user.username
                    return redirect('deliveryindex')
                elif user.is_technician :
                    request.session["username"] = user.username
                    return redirect('techindex')
                elif user.is_superadmin:
                    request.session["username"] = user.username
                    return redirect('panel')
            else:
                # Invalid credentials - user not authenticated
                messages.error(request, "Invalid credentials.")
                return redirect('/login')
        else:
            # Handle the case where username or password is missing
            messages.error(request, "Please provide both username and password.")
            return redirect('/login')
    
    return render(request,'login.html')



from django.shortcuts import render, redirect
from .models import CustomerProfile
from django.contrib import messages

def Customer_Profile(request):
    if not request.user.is_authenticated:
        return redirect('login')

    user_profile, created = CustomerProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        name = request.POST.get('name')
        street_address = request.POST.get('street_address')
        city = request.POST.get('city') 
        country = request.POST.get('country')
        state = request.POST.get('state')
        pincode = request.POST.get('pincode')
        phone = request.POST.get('phone')

        user_profile.name = name
        user_profile.street_address = street_address
        user_profile.city = city  
        user_profile.country = country
        user_profile.state = state
        user_profile.pincode = pincode
        user_profile.phone = phone
        user_profile.save()

        messages.success(request, 'Profile updated successfully')  # Display a success message
        return redirect('Customer_Profile')

    context = {
        'user_profile': user_profile,
        'form_submitted': True,
    }
    return render(request, 'Customer_Profile.html', context)


@login_required(login_url='login')
def custom_logout(request):
    #  if request.session.get('is_authenticated'):
    #     del request.session['is_authenticated'] 
    logout(request)
    return redirect('index')
@login_required
def adminpanel(request):
    
    return render(request, 'adminpanel.html')


@never_cache
def view_products(request):
    products = WatchProduct.objects.all()  # Retrieve all products from the database
    return render(request, 'view_products.html', {'products': products})


@login_required
def customer_product_view(request):
    products = WatchProduct.objects.all()
    return render(request, 'customer_product.html', {'products': products})

# Django view to delete the product





from django.shortcuts import get_object_or_404,reverse

def delete_product(request, product_id):
    product = get_object_or_404(WatchProduct, pk=product_id)
    product.status = 'Out of Stock'  # Mark the product as deactivated
    product.save()
    return redirect('view_products')


# views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import WatchProduct

@never_cache
def edit_product(request, product_id):
    product = get_object_or_404(WatchProduct, id=product_id)
    
    if request.method == 'POST':
        product_name = request.POST['product_name']
        product_price = request.POST['product_price']
        product_sale_price = request.POST['product_sale_price']
        discount = request.POST['discount']
        watch_description = request.POST['watch_description']
        watch_image = request.FILES.get('product_image')

        # Ensure the numerical fields are valid numbers before saving
        try:
            product_price = float(product_price)
            product_sale_price = float(product_sale_price)
            discount = float(discount)

            # Update the product instance with the new data
            product.product_name = product_name
            product.product_price = product_price
            product.product_sale_price = product_sale_price
            product.discount = discount
            product.watch_description = watch_description

            if watch_image:
                product.watch_image = watch_image

            product.save()
            messages.success(request, f"Product '{product.product_name}' edited successfully.")
            return redirect('view_products')
        except (ValueError, TypeError):
            messages.error(request, "Invalid numerical input.")

    return render(request, 'edit_product.html', {'product': product})
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import WatchProduct

@never_cache
def add_product(request):
    if request.method == 'POST':
        category = request.POST['category']
        product_name = request.POST['productName']
        watch_model_number = request.POST['watch_modelnumber']
        watch_serial_number = request.POST['watchSerialNumber']
        product_price = request.POST['productPrice']
        product_sale_price = request.POST['productSalePrice']
        discount = request.POST['discount']
        watch_description = request.POST['watchDescription']
        warranty = request.POST['warranty']
        stock = request.POST['stock']
        watch_image = request.FILES['watchImage']

        if WatchProduct.objects.filter(product_name=product_name, category=category, watch_modelnumber=watch_model_number).exists():
            messages.error(request, f"A product with the name '{product_name}', category '{category}', and watch model number '{watch_model_number}' already exists.")
        else:
            try:
                product_price = float(product_price)
                product_sale_price = float(product_sale_price)
                discount = float(discount)
                warranty = int(warranty)
                stock = int(stock)

                WatchProduct.objects.create(
                    category=category,
                    product_name=product_name,
                    watch_modelnumber=watch_model_number,
                    watch_serial_number=watch_serial_number,
                    product_price=product_price,
                    product_sale_price=product_sale_price,
                    discount=discount,
                    watch_description=watch_description,
                    warranty=warranty,
                    stock=stock,
                    watch_image=watch_image
                )

                messages.success(request, "Product added successfully.")
            except (ValueError, TypeError):
                messages.error(request, "Invalid numerical input.")

        return redirect('view_products')
    
    return render(request, 'add_product.html')




from django.shortcuts import render
from .models import Order

from django.shortcuts import render
from .models import Order

def admin_order_list(request):
    # Filter orders with payment_status=True
    orders = Order.objects.filter(payment_status=True)
    return render(request, 'admin_order_list.html', {'orders': orders})

from django.shortcuts import render, redirect, get_object_or_404
from .models import Order, DeliveryTeam

def assign_delivery_team(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    delivery_teams = DeliveryTeam.objects.all()

    if request.method == 'POST':
        selected_delivery_team_id = request.POST.get('delivery_team')

        if selected_delivery_team_id:
            selected_delivery_team = get_object_or_404(DeliveryTeam, id=selected_delivery_team_id)

            # Assign the selected delivery team to the order
            order.delivery_team = selected_delivery_team
            order.save()

            return redirect('admin_order_list')

    return render(request, 'assign_delivery_team.html', {'delivery_teams': delivery_teams, 'order_id': order_id})

from django.shortcuts import render, get_object_or_404, redirect



from .models import WatchProduct, Cart, CartItem
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect

@login_required(login_url='login')
def add_to_cart(request, product_id):
    product = get_object_or_404(WatchProduct, pk=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, item_created = CartItem.objects.get_or_create(cart=cart, product=product)
    
    if not item_created:
        cart_item.quantity += 1
        cart_item.save()
    
    return redirect('view_cart')




@login_required(login_url='login')
def remove_from_cart(request, product_id):
    # Get the WatchProduct object based on the product_id
    product = get_object_or_404(WatchProduct, pk=product_id)
    
    # Get the user's cart
    cart = Cart.objects.get(user=request.user)
    
    try:
        # Get the cart item for the product
        cart_item = cart.cartitem_set.get(product=product)
        
        if cart_item.quantity >= 1 and product.status == 'In Stock':
            cart_item.delete()
    except CartItem.DoesNotExist:
        pass
    
    return redirect('view_cart')
def view_cart(request):
    cart = request.user.cart
    cart_items = CartItem.objects.filter(cart=cart)
    for item in cart_items:
        item.total_price = item.product.product_sale_price * item.quantity
    
    total_amount = sum(item.total_price for item in cart_items)

    return render(request, 'view_cart.html', {'cart_items': cart_items,'total_amount': total_amount})

from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from django.shortcuts import get_object_or_404, redirect

@login_required(login_url='login')
def increase_cart_item(request, product_id):
    product = get_object_or_404(WatchProduct, pk=product_id)
    user = request.user
    cart, created = Cart.objects.get_or_create(user=user)
    
    # Get or create the cart item
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    
    if not created:
        
        cart_item.quantity += 1
        cart_item.save()
    
    return redirect('view_cart')

from django.shortcuts import get_object_or_404, redirect

@login_required(login_url='login')
def decrease_cart_item(request, product_id):
    product = get_object_or_404(WatchProduct, pk=product_id)
    user = request.user
    
    # Correct the variable name from CartItemt to CartItem
    cart_item = CartItem.objects.get(cart__user=user, product=product)
    
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    
    return redirect('view_cart')



from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

@login_required(login_url='login')
def fetch_cart_count(request):
    cart_count = 0
    if request.user.is_authenticated:
        user = request.user
        cart_count = CartItem.objects.filter(user=user, is_active=True).count()
    return JsonResponse({'cart_count': cart_count})


@login_required
def get_cart_count(request):
    cart_count = 0
    if request.user.is_authenticated:
        user = request.user
        cart = user.cart  # Get the user's cart
        cart_count = CartItem.objects.filter(cart=cart, is_active=True).count()
    return JsonResponse({'cart_count': cart_count})

def view_details(request, product_id):
    product = get_object_or_404(WatchProduct, pk=product_id)
    return render(request, 'viewdetails.html', {'product': product})

from django.http import JsonResponse
from django.conf import settings
import razorpay
import json
from django.views.decorators.csrf import csrf_exempt
from .models import Cart, CartItem, Order, OrderItem, WatchCustomization  # Import WatchCustomization
from django.http import JsonResponse
from django.conf import settings
import razorpay
import json
from django.views.decorators.csrf import csrf_exempt
from .models import Cart, CartItem, Order, OrderItem

@csrf_exempt
def create_order(request):
    if request.method == 'POST':
        user = request.user
        cart = user.cart

        cart_items = CartItem.objects.filter(cart=cart)
        total_amount = sum(item.product.product_sale_price * item.quantity for item in cart_items)

        try:
            # Create a new order object
            order = Order.objects.create(user=user, total_amount=total_amount)

            # Create order items for each cart item
            for cart_item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=cart_item.product,
                    quantity=cart_item.quantity,
                    item_total=cart_item.product.product_sale_price * cart_item.quantity
                )

            # Initialize Razorpay client
            client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))

            payment_data = {
                'amount': int(total_amount * 100),  # Amount should be in paisa (multiply by 100)
                'currency': 'INR',
                'receipt': f'order_{order.id}',
                'payment_capture': '1'  # Auto-capture payment
            }

            # Create a Razorpay order
            order_data = client.order.create(data=payment_data)

            # Update the order with the Razorpay order ID
            order.payment_id = order_data['id']
            order.save()

            # Return the order ID as a JSON response
            return JsonResponse({'order_id': order_data['id']})

        except Exception as e:
            # Log the error for debugging purposes
            print(f"Error creating order: {str(e)}")
            
            # Return an informative error response
            return JsonResponse({'error': f'An error occurred while creating the order: {str(e)}'}, status=500)

from django.shortcuts import render
from .models import CartItem, CustomerProfile  # Import CartItem

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.conf import settings

@csrf_exempt
def checkout(request):
    cart_count = get_cart_count(request)
    email = ""
    full_name = ""

    if request.user.is_authenticated:
        user = request.user
        cart_items = CartItem.objects.filter(cart=user.cart)
        total_amount = sum(item.product.product_sale_price * item.quantity for item in cart_items)

        try:
            # Try to access the user's name from the related CustomerProfile
            customer_profile = CustomerProfile.objects.get(user=user)
            email = user.email
            full_name = customer_profile.name
        except CustomerProfile.DoesNotExist:
            # Handle the case where the CustomerProfile does not exist
            # You can create a new profile, redirect the user, or set default values
            pass

    else:
        # Handle the case where the user is not authenticated
        user = None
        cart_items = []
        total_amount = 0

    context = {
        'cart_count': cart_count,
        'cart_items': cart_items,
        'total_amount': total_amount,
        'email': email,
        'full_name': full_name,
    }
    return render(request, 'checkout.html', context)

from django.shortcuts import get_object_or_404

@csrf_exempt
def handle_payment(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        razorpay_order_id = data.get('order_id')
        payment_id = data.get('payment_id')

        try:
            order = get_object_or_404(Order, payment_id=razorpay_order_id)

            client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
            payment = client.payment.fetch(payment_id)

            if payment['status'] == 'captured':
                order.payment_status = True
                order.save()

                
                # for cart_item in request.user.cart.cartitem_set.all():
                #     OrderItem.objects.create(
                #         order=order,
                #         product=cart_item.product,
                #         quantity=cart_item.quantity,
                #         item_total=cart_item.product.product_price * cart_item.quantity)
    

                # Clear the user's cart after a successful payment
                request.user.cart.cartitem_set.all().delete()

                return JsonResponse({'message': 'Payment successful', 'redirect_url': '/ordersummary/'})
            else:
                return JsonResponse({'error': 'Payment failed'}, status=400)

        except Exception as e:
            print(str(e))
            return JsonResponse({'error': 'Server error, please try again later.'}, status=500)

def user_list(request):
    users = CustomUser.objects.filter(is_superadmin=False)
    
    return render(request, 'user_list.html', {'users': users})
@login_required
def block_unblock_user(request, user_id):
    user = CustomUser.objects.get(pk=user_id)
    if user.is_active:
        user.is_active = False  # Block the user
        subject = 'Account Blocked'
        message = 'Your account has been blocked by the admin.'
        from_email = 'anittarosejoseph2024a@mca.ajce.in'  # Use your admin's email address
        recipient_list = [user.email]
        send_mail(subject, message, from_email, recipient_list, fail_silently=False)
    else:
        user.is_active = True  # Unblock the user
    user.save()
    return redirect('user_list')  # Assuming 'user_list' is the name of your user list view

from django.shortcuts import render, get_object_or_404, redirect
from .models import WatchProduct, WishlistItem
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse

def wishlist(request):
    if request.user.is_authenticated:
        wishlist_items = WishlistItem.objects.filter(user=request.user)
        return render(request, 'wishlist.html', {'wishlist_items': wishlist_items})
    else:
        return redirect('login')
def remove_from_wishlist(request, wishlist_item_id):
    try:
        wishlist_item = get_object_or_404(WishlistItem, id=wishlist_item_id)
        # Perform the logic to remove the wishlist item here
        # ...
        wishlist_item.delete()  # Remove the item from the wishlist
        return redirect('wishlist')  # Redirect the user back to their wishlist page
    except WishlistItem.DoesNotExist:
        # Handle the case where the item with the specified ID doesn't exist
        return HttpResponseNotFound("Wishlist item not found")
def add_to_wishlist(request, id):
    if request.user.is_authenticated:
        product = WatchProduct.objects.get(id=id)
        wishlist_item, created = WishlistItem.objects.get_or_create(user=request.user, product=product)
        if created:
            # The item was added to the wishlist
            messages.success(request, f'{product.product_name} has been added to your wishlist.')
        else:
            # The item is already in the wishlist
            messages.warning(request, f'{product.product_name} is already in your wishlist.')
    return redirect('wishlist')

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Order, CustomUser

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Order  # Import your Order model

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Order

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Order

@login_required
def all_user_orders(request):
    # Retrieve orders for the current user with payment_status=True
    user_orders = Order.objects.filter(user=request.user, payment_status=True)

    context = {
        'user_orders': user_orders,
    }

    return render(request, 'all_user_orders.html', context)

from django.core.mail import send_mail
from django.shortcuts import redirect
from django.contrib import messages

from django.contrib import messages

def approve_disapprove_order(request):
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        action = request.POST.get('action')

        try:
            order = Order.objects.get(pk=order_id)

            if action == 'approve' and not order.payment_status:
                # Update payment status to True (approved) only if it's not already approved
                order.payment_status = True
                order.save()

                # Send an approval message to the user
                subject = 'Order Approved'
                message = 'Your Order Has been placed by Horofix. For any query, email us at support@horofix.com'
                from_email = 'admin@horofix.com'
                user_email = order.user.email
                send_mail(subject, message, from_email, [user_email], fail_silently=False)

                # Add a success message for the admin
                messages.success(request, f'Order {order_id} has been approved.')
            elif action == 'disapprove':
                # Handle disapproval logic here
                order.payment_status = False  # Assuming you want to mark it as not paid
                order.save()

                # Send a disapproval message to the user
                subject = 'Order Disapproved'
                message = 'Your Order has been rejected by Horofix.'
                from_email = 'admin@horofix.com'
                user_email = order.user.email
                send_mail(subject, message, from_email, [user_email], fail_silently=False)

                # Add a success message for the admin
                messages.success(request, f'Order {order_id} has been disapproved.')

        except Order.DoesNotExist:
            messages.error(request, f'Order {order_id} does not exist.')

    return redirect('all_user_orders')


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import OrderItem

@csrf_exempt
def cancel_order(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        item_id = data.get('item_id')

        try:
            order_item = OrderItem.objects.get(id=item_id)

            # Implement your cancellation logic here
            # For example, you might want to update the order item status
            order_item.status = 'cancelled'
            order_item.save()

            return JsonResponse({'message': 'Order cancelled successfully'})
        except OrderItem.DoesNotExist:
            return JsonResponse({'message': 'Invalid Order Item ID'}, status=400)
        except Exception as e:
            print(str(e))
            return JsonResponse({'message': 'Server error, please try again later.'}, status=500)

# views.py


from django.shortcuts import render
from .models import WatchProduct

def search_products(request):
    query_name = request.GET.get('search_name')
    query_category = request.GET.get('search_category')

    products = WatchProduct.objects.filter(status='In Stock')

    if query_name:
        products = products.filter(product_name__icontains=query_name)

    if query_category:
        products = products.filter(category=query_category)

    return render(request, 'customer_product.html', {'products': products})

# views.py

from django.shortcuts import render
from .models import WatchProduct
def sort_products(request):
    # Get the sort option from the request
    sort_option = request.GET.get('sort_option', 'asc')

    # Retrieve the products from the database
    if sort_option == 'asc':
        products = WatchProduct.objects.filter(status='In Stock').order_by('product_price')
    elif sort_option == 'desc':
        products = WatchProduct.objects.filter(status='In Stock').order_by('-product_price')
    else:
        # Handle other cases or default sorting
        products = WatchProduct.objects.filter(status='In Stock').order_by('product_price')

    # Render the template with the sorted products
    context = {'products': products}
    return render(request, 'customer_product.html', context)


def filter_products_by_category(request):
    category = request.GET.get('category')

    if category == 'All':
        products = WatchProduct.objects.filter(status='In Stock')
    else:
        products = WatchProduct.objects.filter(category=category, status='In Stock')



    return render(request, 'customer_product.html', {'products': products})

from django.shortcuts import get_object_or_404, redirect

def remove_order_item(request, item_id):
    order_item = get_object_or_404(OrderItem, id=item_id)

    # Set the 'is_removed' flag to True
    order_item.is_removed = True
    order_item.save()

    # Redirect back to the order summary page or any desired page
    return redirect('ordersummary')

def delivery_team_registration(request):
    if request.method == 'POST':
        name = request.POST.get('name')  # Make sure 'name' is present in your form
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        team_name = request.POST.get('team_name')
        vehicle_number = request.POST.get('vehicle_number')
        pincode = request.POST.get('pincode')
        city = request.POST.get('city')

        user_type = 'DELIVERYTEAM'

        if CustomUser.objects.filter(username=username, user_type=user_type).exists():
            return render(request, 'delivery_team_list.html')
        else:
            user = CustomUser.objects.create_user(name=name, username=username, email=email, phone=phone, password=password)
            user.user_type = user_type
            user.is_deliveryteam = True
            user.is_customer = False
            user.save()

            delivery_team = DeliveryTeam(user=user, team_name=team_name, vehicle_number=vehicle_number, pincode=pincode, city=city)
            delivery_team.save()

            # Send a welcome email to the newly registered delivery team
            subject = 'Delivery Team Login Details'
            message = f'Registered as a delivery team. Your username: {user.username}, Password: {password}'
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [user.email]

            send_mail(subject, message, from_email, recipient_list)

            return redirect('delivery_team_list')
    else:
        return render(request, 'deliveryteamreg.html')

# views.py
from django.http import JsonResponse
from django.contrib.auth import update_session_auth_hash

from django.shortcuts import render

def deliveryindex(request):
    delivery_team = request.user.deliveryteam

    # Fetch orders assigned to the delivery team
    assigned_orders = Order.objects.filter(delivery_team=delivery_team)

    context = {
        'assigned_orders': assigned_orders,
    }   
    return render(request, 'deliveryindex.html')  
from django.shortcuts import render

def delivery_team_list(request):
    # Your logic to retrieve data from the database goes here
    # For example, you can retrieve the DeliveryTeam objects and pass them to the template
    delivery_teams = DeliveryTeam.objects.all()
    return render(request, 'delivery_team_list.html', {'delivery_teams': delivery_teams})
from django.http import JsonResponse
from django.contrib.auth import update_session_auth_hash

def change_password(request):
    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        user = request.user

        # Check if the entered old password matches the user's current password
        if not user.check_password(old_password):
            return JsonResponse({'error': 'Incorrect old password'}, status=400)

        if new_password == confirm_password:
            try:
                # Change the user's password and save it to the database
                user.set_password(new_password)
                user.save()

                # Update the session to keep the user logged in
                update_session_auth_hash(request, user)

                return JsonResponse({'message': 'Password changed successfully'})
            except Exception as e:
                # Print the error to the console for debugging
                print(f"Password change error: {e}")

                # Return a JsonResponse with an error message
                return JsonResponse({'error': 'An error occurred while changing the password'}, status=500)
        else:
            return JsonResponse({'error': 'Passwords do not match'}, status=400)

    return render(request, 'change_password.html')

from django.shortcuts import render, redirect
from .models import CustomUser, Address

def add_address(request):
    if request.method == 'POST':
        # Assuming you have a CustomUser instance for the current user
        user = request.user  # Adjust this based on your authentication logic

        # Address 1
        street_address_1 = request.POST.get('street_address_1')
        city_1 = request.POST.get('city_1')
        country_1 = request.POST.get('country_1')  # Adjust based on your form fields
        state_1 = request.POST.get('state_1')
        pincode_1 = request.POST.get('pincode_1')
        phone_1 = request.POST.get('phone_1')
        is_default_1 = request.POST.get('is_default_1')

        # Address 2
        street_address_2 = request.POST.get('street_address_2')
        city_2 = request.POST.get('city_2')
        country_2 = request.POST.get('country_2')  # Adjust based on your form fields
        state_2 = request.POST.get('state_2')
        pincode_2 = request.POST.get('pincode_2')
        phone_2 = request.POST.get('phone_2')
        is_default_2 = request.POST.get('is_default_2')

        # Create Address instances
        address_1 = Address.objects.create(
            user=user,
            street_address=street_address_1,
            city=city_1,
            country=country_1,
            state=state_1,
            pincode=pincode_1,
            phone=phone_1,
            is_default=is_default_1 == 'on'  # Convert string 'on' to boolean
        )

        address_2 = Address.objects.create(
            user=user,
            street_address=street_address_2,
            city=city_2,
            country=country_2,
            state=state_2,
            pincode=pincode_2,
            phone=phone_2,
            is_default=is_default_2 == 'on'  # Convert string 'on' to boolean
        )

        # Redirect or perform additional logic as needed
        return redirect('checkout.html')

    return render(request, 'add_address.html')

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Order


# views.py

from django.shortcuts import render
from .models import Order, OrderItem, CustomUser

def all_orders(request):
    # Fetch all orders with payment complete
    orders = Order.objects.filter(payment_status=True)

    # Create a list to store order details with associated user details
    order_details = []

    for order in orders:
        # Fetch user details associated with the order
        user = CustomUser.objects.get(id=order.user_id)

        # Fetch order items associated with the order
        order_items = OrderItem.objects.filter(order=order)

        # Create a dictionary to store order details and associated user details
        order_detail = {
            'user': user,
            'order': order,
            'order_items': order_items,
        }

        # Append the dictionary to the order_details list
        order_details.append(order_detail)

    context = {'order_details': order_details}
    return render(request, 'myorders.html', context)

from django.shortcuts import render
from .models import Order

def ordersummary(request, order_id):
    order = Order.objects.prefetch_related('watch_customization').get(id=order_id)

    context = {
        'order': order,
    }
    return render(request, 'order_summary.html', context)


# views.py
from django.shortcuts import render
from .models import Order, OrderItem

def myorders(request):
    # Fetch orders with payment_status as True
    orders = Order.objects.filter(payment_status=True)

    # Create a list to store order details
    order_details = []

    for order in orders:
        order_items = OrderItem.objects.filter(order=order)

        # Calculate total amount for the order
        total_amount = sum(item.item_total for item in order_items)

        # Aggregate order items to avoid duplicates
        unique_items = {}
        for item in order_items:
            key = (item.product.id, item.product.product_name)  # Use a tuple as the key
            if key in unique_items:
                unique_items[key]['quantity'] += item.quantity
            else:
                unique_items[key] = {
                    'quantity': item.quantity,
                    'product_name': item.product.product_name,
                    # Add more fields as needed
                }

        order_detail = {
            'order_id': order.id,
            'order_date': order.created_at.date(),
            'order_time': order.created_at.time(),
            'status': order.status,
            'payment_status': order.payment_status,
            'total_amount': total_amount,
            'items': unique_items.values(),
        }

        order_details.append(order_detail)

    return render(request, 'myorders.html', {'order_details': order_details})

# views.py
from django.shortcuts import render, get_object_or_404
from .models import Order, DeliveryTeam
from django.contrib.auth.decorators import login_required

@login_required
def delivery_team_orders(request):
    # Retrieve the delivery team associated with the logged-in user
    delivery_team = DeliveryTeam.objects.get(user=request.user)

    # Fetch orders assigned to the delivery team's city
    assigned_orders = Order.objects.filter(delivery_team__city=delivery_team.city)

    return render(request, 'delivery_team_orders.html', {'assigned_orders': assigned_orders})
# views.py
from django.shortcuts import redirect, get_object_or_404
from .models import Order
from django.http import HttpResponseForbidden
from django.views.decorators.http import require_POST

@require_POST
def update_order_status(request):
    order_id = request.POST.get('order_id')
    new_status = request.POST.get('new_status')

    order = get_object_or_404(Order, id=order_id)

    # Add logic to ensure the delivery team matches the logged-in user
    if request.user != order.delivery_team.user:
        return HttpResponseForbidden("You don't have permission to update this order.")

    # Update the order status
    order.status = new_status
    order.save()

    # Redirect to the delivery team orders page
    return redirect('delivery_team_orders')
# views.py
from django.shortcuts import render
from .models import Order, DeliveryTeam
from django.contrib.auth.decorators import login_required

@login_required
def delivery_team_orders_by_city(request, city):
    # Retrieve the delivery team associated with the logged-in user
    delivery_team = DeliveryTeam.objects.get(user=request.user)

    # Fetch orders assigned to the delivery team's city
    assigned_orders = Order.objects.filter(delivery_team__city=city)

    return render(request, 'delivery_team_orders_by_city.html', {'assigned_orders': assigned_orders})
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Order, CustomUser, CustomerProfile, DeliveryTeam

@login_required
def deliver_orders(request, city=None):
    # If a city is provided, filter delivery teams based on that city
    if city:
        delivery_teams = DeliveryTeam.objects.filter(city=city, active=True)
    else:
        # If no city is provided, get all active delivery teams
        delivery_teams = DeliveryTeam.objects.filter(active=True)

    orders_by_team = {}

    for team in delivery_teams:
        # Fetch orders assigned to the delivery team with payment_status=True
        orders = Order.objects.filter(delivery_team=team, payment_status=True)

        # Store team details and orders in a dictionary
        orders_by_team[team] = {
            'team_name': team.team_name,
            'orders': orders
        }

    context = {'orders_by_team': orders_by_team, 'selected_city': city}
    return render(request, 'deliverorders.html', context)
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Order, CustomUser

@login_required
def all_orders(request):
    # Fetch all users excluding superadmin
    users = CustomUser.objects.filter(is_superadmin=False)
    orders = Order.objects.filter(payment_status=True)

    return render(request, 'all_orders.html', {'orders': orders})
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Order

def update_order_status(request, order_id):
    if request.method == 'POST':
        status = request.POST.get('status')
        order = Order.objects.get(id=order_id)
        order.status = status
        order.save()
        messages.success(request, f"Order {order_id} status updated to {status}.")
    return redirect('all_orders')

def delete_order(request, order_id):
    if request.method == 'POST':
        order = Order.objects.get(id=order_id)
        order.delete()
        messages.success(request, f"Order {order_id} deleted successfully.")
    return redirect('all_orders')
from django.shortcuts import render


@login_required
def order_history(request):
    user = request.user
    orders = Order.objects.filter(user=user, payment_status=True)
    
    context = {
        'orders': orders,
        'user': user,
    }
    return render(request, 'order_history.html', context)
from django.shortcuts import render, get_object_or_404
from .models import Order, WatchCustomization

def bill(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    customization = WatchCustomization.objects.filter(order=order).first()
    context = {
        'order': order,
        'customization': customization,
    }
    return render(request, 'bill.html', context)



@login_required
def panel(request):
    if request.user.is_superuser:
      
        total_users = CustomUser.objects.filter(is_superuser=False).count()

        context = {
            'total_users': total_users,
        }

        return render(request, 'panel.html', context)
    else:
        # Handle the case where the user is not a superuser (optional)
        return render(request, 'access_denied.html')

from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import get_user_model
from .models import Technician

CustomUser = get_user_model()

def techreg(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        experience = request.POST.get('experience')
        city = request.POST.get('city')
        pincode = request.POST.get('pincode')

        user_type = 'TECHNICIAN'

        if CustomUser.objects.filter(username=username, user_type=user_type).exists():
            return render(request, 'techlist.html')  # Redirect or render a specific page for existing technicians
        else:
            user = CustomUser.objects.create_user(name=name, username=username, email=email, phone=phone, password=password)
            user.user_type = user_type
            user.is_technician = True
            user.is_customer = False
            user.save()

            technician = Technician(user=user,  experience=experience, city=city, pincode=pincode)
            technician.save()

            # Send a welcome email to the newly registered technician
            subject = 'Technician Login Details'
            message = f'Registered as a technician. Your username: {user.username}, Password: {password}'
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [user.email]

            send_mail(subject, message, from_email, recipient_list)

            return redirect('techlist')  # Redirect to a page displaying a list of registered technicians
    else:
        return render(request, 'techreg.html')
# views.py

from django.shortcuts import render
from .models import Technician  # Import the Technician model (adjust the import path as needed)

def techlist(request):
    technicians = Technician.objects.all()  # Fetch all Technician objects from the database
    return render(request, 'techlist.html', {'technicians': technicians})
# views.py

# views.py

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required(login_url='login')  # Ensure the user is logged in
def techindex(request):
    # Assuming you have a foreign key from Repair to Technician
    repair_requests = WatchRepairRequest.objects.filter(requested_by=request.user)

    return render(request, 'techindex.html', {'repair_requests': repair_requests})


from django.shortcuts import render, redirect
from django.contrib import messages
from .models import CustomUser

def edit_profile(request):
    # Assuming the user is already authenticated, you can access the user instance
    user = request.user

    if request.method == 'POST':
        # Handle form submission
        name = request.POST.get('name')
        mobile = request.POST.get('mobile')
        address = request.POST.get('address')
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')

        # Update user fields
        user.name = name
        user.phone = mobile
        user.save()

        messages.success(request, 'Profile updated successfully!')
        return redirect('edit_profile')  # Redirect to the same page after successful form submission

    return render(request, 'edit_profile.html', {'user': user})


def repairing(request):
    return render(request, 'repairing.html')

def thank_you_page(request):
    return render(request, 'thank_you_page.html')

from .models import WatchRepairService, WatchRepairRequest
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import WatchRepairService, WatchRepairRequest
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.contrib.auth.decorators import login_required

@login_required
def repair(request):
    services = WatchRepairService.objects.all()

    if request.method == 'POST':
        user = request.user
        watch_name = request.POST.get('watchName')
        watch_model_number = request.POST.get('watchBrand')
        issue_description = request.POST.get('issueDescription')
        image_upload = request.FILES.get('imageUpload')
        additional_info = request.POST.get('additionalInfo')
        purchase_date = request.POST.get('purchaseDate')
        warranty_duration = request.POST.get('warrantyDuration')

        # Save data to the database
        repair_request = WatchRepairRequest.objects.create(
            user=user,
            watch_name=watch_name,
            watch_model_number=watch_model_number,
            issue_description=issue_description,
            image_upload=image_upload,
            additional_info=additional_info,
            purchase_date=purchase_date,
            warranty_duration=warranty_duration,
        )

        # Retrieve selected services from the form
        selected_services = request.POST.getlist('selectedService')

        # Add selected services to the issue_types field of the repair_request
        repair_request.issue_types.add(*selected_services)

        # Send email
        subject = 'Watch Repair Request Submitted'
        message = render_to_string('email_template.html', {'repair_request': repair_request})
        from_email = settings.DEFAULT_FROM_EMAIL
        to_email = [user.email]  # You can add additional recipients if needed
        send_mail(subject, message, from_email, to_email, fail_silently=True)

        # Redirect to thank-you page
        messages.success(request, 'Your watch repair request has been submitted successfully!')
        return redirect('thank_you_page')

    return render(request, 'repair.html', {'services': services})


from django.core.mail import EmailMessage
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings

def email_template(request):
    # Your logic to get user and other data
    user = request.user  # Replace with your actual way of getting the user

    # Render the email template with user data
    context = {'user': user}
    email_html_message = render_to_string('email_template.html', context)
    email_plaintext_message = strip_tags(email_html_message)

    # Your email subject, 'from' address, and 'to' address for repair request
    subject = 'Subject of Your Repair Request Email'
    from_email = settings.DEFAULT_FROM_EMAIL
    to_email = [user.email]  # Replace with the actual email address

    # Create the EmailMessage object for repair request
    email_message = EmailMessage(
        subject,
        email_plaintext_message,
        from_email,
        to_email,
    )

    # Attach the HTML content for repair request
    email_message.attach_alternative(email_html_message, "text/html")

    # Send the email for repair request
    email_message.send()

    # Your logic after sending the repair request email

    # Render the thank-you email template
    thank_you_html_message = render_to_string('thank_you_template.html', context)
    thank_you_plaintext_message = strip_tags(thank_you_html_message)

    # Your email subject, 'from' address, and 'to' address for thank-you message
    thank_you_subject = 'Subject of Your Thank You Email'
    thank_you_to_email = [user.email]  # Replace with the actual email address

    # Create the EmailMessage object for thank-you message
    thank_you_email_message = EmailMessage(
        thank_you_subject,
        thank_you_plaintext_message,
        from_email,
        thank_you_to_email,
    )

    # Attach the HTML content for thank-you message
    thank_you_email_message.attach_alternative(thank_you_html_message, "text/html")

    # Send the thank-you email
    thank_you_email_message.send()

    # Your logic after sending the thank-you email (e.g., redirect to a thank-you page)
    return render(request, 'thank_you_page.html')  # Replace with the actual template name

from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404, redirect

from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Case, When, Value

def watchrepairrequest_list(request):
    repair_requests = WatchRepairRequest.objects.all() \
        .order_by(
            '-created_at',
            Case(
                When(is_approved=True, then=Value(1)),
                When(is_rejected=True, then=Value(2)),
                default=Value(0),
            ),
        )
    return render(request, 'watchrepairrequest_list.html', {'repair_requests': repair_requests})


def send_approval_email(repair):
    subject = 'Watch Repair Request Approved'
    message = f'Your watch repair request for {repair.watch_name} with ID {repair.id} has been approved. The watch will be sent to Horofix, Kochi, Kerala. Address: Horofix, Kochi, Kerala, 7306139495. Email: anittarosejoseph2024a@mca.ajce.in'
    from_email = 'anittarosejoseph2024a@mca.ajce.in'  # Update with your email
    recipient_list = [repair.user.email]  # Access user's email through the ForeignKey relationship
    send_mail(subject, message, from_email, recipient_list)

def send_rejection_email(repair):
    subject = 'Watch Repair Request Rejected'
    message = f'Sorry, your watch repair request for {repair.watch_name} with ID {repair.id} has been rejected. If you have any questions, please contact us at anittarosejoseph2024a@mca.ajce.in'
    from_email = 'anittarosejoseph2024a@mca.ajce.in'  # Update with your email
    recipient_list = [repair.user.email]  # Access user's email through the ForeignKey relationship
    send_mail(subject, message, from_email, recipient_list)



def approve_repair(request, repair_id):
    repair = get_object_or_404(WatchRepairRequest, id=repair_id)

    # Perform approval actions
    repair.is_approved = True
    repair.is_rejected = False
    repair.save()

    # Send approval email
    send_approval_email(repair)

    return redirect('watchrepairrequest_list')

def reject_repair(request, repair_id):
    repair = get_object_or_404(WatchRepairRequest, id=repair_id)

    # Perform rejection actions
    repair.is_approved = False
    repair.is_rejected = True
    repair.save()

    # Send rejection email
    send_rejection_email(repair)

    return redirect('watchrepairrequest_list')
def faq_view(request):
    # Add any context data if needed
    return render(request, 'faq.html')

# from .models import Thread

from horofixapp.models import Thread

@login_required
def messages_page(request):
    threads = Thread.objects.by_user(user=request.user).prefetch_related('chatmessage_thread').order_by('timestamp')
    context = {
        'Threads': threads
    }
    return render(request, 'messages.html', context)
# views.py

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def user_repair_history(request):
    # Fetch repair history for the logged-in user with issue_types
    repair_history = WatchRepairRequest.objects.filter(user=request.user).prefetch_related('issue_types')
    
    # Fetch payment details for each repair request
    for repair in repair_history:
        repair.payments = repair.repairpayment_set.all()

    context = {'repair_history': repair_history}
    return render(request, 'user_repair_history.html', context)

# views.py
from .models import WatchRepairRequest

from django.shortcuts import render, redirect
from .models import WatchRepairService

def add_service(request):
    if request.method == 'POST':
        issue_type = request.POST.get('issueType')
        price = request.POST.get('price')

        # Save the data to the database
        WatchRepairService.objects.create(issue_type=issue_type, price=price)

        # Redirect to the view_service page
        return redirect('view_service')

    return render(request, 'add_service.html')

def view_service(request):
    # Retrieve all services from the database
    services = WatchRepairService.objects.all()
    return render(request, 'view_service.html', {'services': services})
from django.shortcuts import get_object_or_404, redirect

def assign_technician(request, repair_request_id, technician_id):
    # Retrieve the RepairRequest object and Technician object
    repair_request = get_object_or_404(WatchRepairRequest, pk=repair_request_id)
    technician = get_object_or_404(Technician, pk=technician_id)
    
    # Perform the assignment logic here, e.g., setting the assigned technician for the repair request
    repair_request.assigned_technician = technician
    repair_request.save()
    
    # Redirect to some appropriate URL after the assignment
    return redirect('some_redirect_url')


from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib import messages
from .models import WatchRepairRequest, RepairPayment  # Import RepairPayment model
from django.conf import settings
import razorpay
from django.template.defaultfilters import floatformat

from decimal import Decimal  # Add this import

def repair_payment(request, repair_id):
    if request.method == 'POST':
        repair_request = get_object_or_404(WatchRepairRequest, pk=repair_id)

        # Load Razorpay API key and secret from settings
        razorpay_key = settings.RAZOR_KEY_ID
        razorpay_secret = settings.RAZOR_KEY_SECRET

        client = razorpay.Client(auth=(razorpay_key, razorpay_secret))

        # Example amount calculation, adjust as needed
        order_amount = sum(issue.price for issue in repair_request.issue_types.all()) * 100

        data = {
            "amount": float(order_amount),  # Convert to float here
            "currency": "INR",
            "receipt": f"repair_rcptid_{repair_id}"
        }
        payment = client.order.create(data=data)

        rupee_amount = floatformat(payment['amount'] / 100, 2)
        return render(request, 'repair_payment.html', {'payment': payment, 'repair_request': repair_request, 'rupee_amount': rupee_amount})


def repair_payment_success(request, repair_id):
    repair_request = get_object_or_404(WatchRepairRequest, pk=repair_id)

    # Load Razorpay API key and secret from settings
    razorpay_key = settings.RAZOR_KEY_ID
    razorpay_secret = settings.RAZOR_KEY_SECRET

    client = razorpay.Client(auth=(razorpay_key, razorpay_secret))

    # Corrected amount calculation for multiple issue_types
    order_amount = int(sum(issue.price for issue in repair_request.issue_types.all()) * 100)

    data = {
        "amount": order_amount,
        "currency": "INR",
        "receipt": f"repair_rcptid_{repair_id}"
    }
    payment = client.order.create(data=data)

    new_payment = RepairPayment(
        order=repair_request,
        razor_pay_order_id=payment['id'],
        amount=order_amount,
        is_paid=True,
        customer=request.user
    )
    new_payment.save()
    send_payment_confirmation_email(request.user.email, repair_request, order_amount)

    # Handle other logic here (e.g., updating repair_request status)

    messages.success(request, 'Payment successfully done.')
    return redirect('user_repair_history')

from django.shortcuts import render, get_object_or_404
from .models import WatchRepairRequest, RepairPayment

def view_bill(request, repair_id):
    repair = get_object_or_404(WatchRepairRequest, id=repair_id)
    payments = RepairPayment.objects.filter(order=repair)

    context = {
        'repair': repair,
        'payments': payments,
    }

    return render(request, 'view_bill.html', context)
# horofixapp/utils.pyen
from django.core.mail import send_mail
from django.conf import settings

def send_payment_confirmation_email(user_email, repair_request, amount):
    subject = 'Payment Confirmation'
    message = f'Thank you for your payment of {amount} INR. Your repair request (ID: {repair_request.id}) has been successfully processed.'
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [user_email]

    send_mail(subject, message, from_email, recipient_list)
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import WatchProduct, Order, OrderItem, WatchCustomization

@login_required
def customize_watch(request, product_id):
    if request.method == 'POST':
        # Extract form data from the request
        strap_material = request.POST['strap_material']
        strap_color = request.POST['strap_color']
        watch_color = request.POST['watch_color']
        dial_shape = request.POST['dial_shape']
        watch_size = request.POST['watch_size']
        watch_hands_color = request.POST['watch_hands_color']
        owner_name = request.POST['owner_name']
        watch_image = request.FILES.get('watch_image')  # Use get() to avoid KeyError if image is not provided

        # Create a new WatchCustomization instance
        product = WatchProduct.objects.get(pk=product_id)
        customization = WatchCustomization.objects.create(
            user=request.user,
            strap_material=strap_material,
            strap_color=strap_color,
            watch_color=watch_color,
            dial_shape=dial_shape,
            watch_size=watch_size,
            watch_hands_color=watch_hands_color,
            owner_name=owner_name,
            watch_image=watch_image,
            product=product,
            # Assuming there's an order associated with the customization
            order=request.user.order_set.last()
        )

        # Redirect to view_entered_details page with the created product's ID
        return redirect('view_entered_details', product_id=product_id)
    else:
        # If the request method is GET, render the form template
        product = get_object_or_404(WatchProduct, pk=product_id)
        return render(request, 'customize_watch.html', {'product': product})

def view_entered_details(request, product_id):
    product = get_object_or_404(WatchProduct, pk=product_id)
    customization = WatchCustomization.objects.filter(product_id=product_id).last()

    if customization:
        context = {
            'product': product,
            'strap_material': customization.strap_material,
            'strap_color': customization.strap_color,
            'watch_color': customization.watch_color,
            'dial_shape': customization.dial_shape,
            'watch_size': customization.watch_size,
            'watch_hands_color': customization.watch_hands_color,
            'owner_name': customization.owner_name,
        }
    else:
        context = {
            'product': product,
            'strap_material': None,
            'strap_color': None,
            'watch_color': None,
            'dial_shape': None,
            'watch_size': None,
            'watch_hands_color': None,
            'owner_name': None,
        }

    return render(request, 'view_entered_details.html', context)




from reportlab.pdfgen import canvas
from io import BytesIO
from django.utils import timezone
import matplotlib.pyplot as plt
from reportlab.lib.utils import ImageReader

def financial_report_pdf(request):
    # Retrieve orders data or any other financial data you need, ordered by creation date in descending order
    orders = Order.objects.order_by('-created_at')
    
    # Create a BytesIO buffer for the PDF content
    buffer = BytesIO()
    
    # Create a PDF document
    pdf = canvas.Canvas(buffer, pagesize='A4')
    
    # Define PDF filename
    filename = "financial_report.pdf"
    
    # Set PDF metadata
    pdf.setTitle(filename)
    
    # Define PDF title and formatting
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawCentredString(300, 800, "Financial Report")

    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(50, 770, "Summary of Financial Data")
    
    
    # Set up table headers
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(50, 750, 'Order ID')
    # pdf.drawString(150, 750, 'User')
    pdf.drawString(250, 750, 'Total Amount')
    pdf.drawString(350, 750, 'Status')
    pdf.drawString(450, 750, 'Purchased On')
    
    # Set up table rows
    pdf.setFont("Helvetica", 12)
    y_position = 730  # Initial y-position for the first row
    
    for order in orders:
        pdf.drawString(50, y_position, str(order.id))
        # pdf.drawString(150, y_position, order.user.fullName)  # Assuming full_name is a field in your User model
        pdf.drawString(250, y_position, str(order.total_amount))
        pdf.drawString(350, y_position, order.status)
        pdf.drawString(450, y_position, order.created_at.strftime("%Y-%m-%d %H:%M:%S"))  # Format the date as needed
        y_position -= 20  # Move to the next row
    
    # Save the PDF document
    pdf.save()
    
    # Get PDF content from the BytesIO buffer
    pdf_data = buffer.getvalue()
    buffer.close()
    
    # Prepare HTTP response with PDF content
    response = HttpResponse(pdf_data, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    
    return response