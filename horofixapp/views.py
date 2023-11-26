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

@never_cache
def login_user(request):
    if request.user.is_authenticated:
        return redirect('index')
    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]
        

        if username and password:
            user = authenticate(request, username =username , password=password)
            if user is not None:
                auth_login(request,user)
            
                if request.user.user_types==CustomUser.CUSTOMER:
                    request.session['is_authenticated'] = True
                
                    return redirect('/')
               
                elif request.user.user_types == CustomUser.ADMIN:
                    print("user is admin")                   
                    return redirect('adminpanel')
                elif user.user_types == CustomUser.DELIVERYTEAM:
                    return redirect('deliveryteam_dashboard') 
            else:
                messages.success(request,("Invalid credentials."))
        else:
            messages.success(request,("Please fill out all fields."))
        
    return render(request, 'login.html')



def Customer_Profile(request):
    if not request.user.is_authenticated:
        return redirect('login')  
    user_profile, created = CustomerProfile.objects.get_or_create(customer=request.user)

    if request.method == 'POST':
        name = request.POST.get('name')
        street_address=request.POST.get('street_address')
        country=request.POST.get('country')
        state=request.POST.get('state')
        pincode=request.POST.get('pincode')
        phone = request.POST.get('phone')

        user_profile.name = name
        user_profile.street_address=street_address
        user_profile.country=country
        user_profile.state=state
        user_profile.pincode=pincode
        
        user_profile.phone= phone
        user_profile.save()

        messages.success(request, 'Profile updated successfully')  # Display a success message
        return redirect('Customer_Profile')  
    context = {
        'user_profile': user_profile,
        'form_submitted': False,
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




@never_cache
def add_product(request):
    if request.method == 'POST':
        product_name = request.POST['productName']
        product_price = request.POST['productPrice']
        product_sale_price = request.POST['productSalePrice']
        discount = request.POST['discount']
        watch_description = request.POST['watchDescription']
        watch_image = request.FILES['watchImage']
        category = request.POST['category']  # Get the category field from the form

        # Check if a product with the same name and category already exists
        if WatchProduct.objects.filter(product_name=product_name, category=category).exists():
            messages.error(request, f"A product with the name '{product_name}' in the category '{category}' already exists.")
        else:
            try:
                # Ensure the numerical fields are valid numbers before saving
                product_price = float(product_price)
                product_sale_price = float(product_sale_price)
                discount = float(discount)
                
                # Create a new WatchProduct instance and save it
                WatchProduct.objects.create(
                    product_name=product_name,
                    product_price=product_price,
                    product_sale_price=product_sale_price,
                    discount=discount,
                    watch_description=watch_description,
                    watch_image=watch_image,
                    category=category  # Set the category field
                )
                messages.success(request, "Product added successfully.")
            except (ValueError, TypeError):
                messages.error(request, "Invalid numerical input.")

        return redirect('view_products')
    
    return render(request, 'add_product.html')


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

from django.shortcuts import render, redirect
from .models import Cart
@login_required(login_url='login')
def view_cart(request):
    # Check if the user is authenticated
    if request.user.is_authenticated:
        try:
            # Try to get the user's cart
            cart = request.user.cart
        except Cart.DoesNotExist:
            # If the cart does not exist, create a new one
            cart = Cart.objects.create(user=request.user)

        # Now you can access the user's cart and retrieve cart items
        cart_items = CartItem.objects.filter(cart=cart)

        context = {
            'cart_items': cart_items,
            'cart': cart,
        }

        return render(request, 'view_cart.html', context)
    else:
        # If the user is not authenticated, you may want to redirect them to the login page
        return redirect('login')  # Replace 'login' with the actual name of your login URL pattern

def deliveryteam_dashboard(request):
    # Add any logic specific to the delivery team dashboard
    return render(request, 'deliveryteam_dashboard.html')


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

from django.shortcuts import render
from .models import CustomerProfile
@login_required
def add_address(request):
    # Retrieve the customer profile associated with the currently logged-in user
    customer_profile = CustomerProfile.objects.get(customer=request.user)

    context = {
        'name': customer_profile.name,
        'street_address': customer_profile.street_address,
        'state': customer_profile.state,
        'country': customer_profile.country,
        'phone': customer_profile.phone,
    }

    return render(request, 'add_address.html', context)
from .models import Address  # Import the Address model from your models.py
from django.contrib.auth.decorators import login_required

@login_required
def add_another_address(request):
    if request.method == 'POST':
        # Get the form data from the request
        street_address = request.POST['street_address']
        country = request.POST['country']
        state = request.POST['state']
        pincode = request.POST['pincode']
        phone = request.POST['phone']
        is_default = request.POST.get('is_default') == 'on'  # Check if the checkbox is checked

        # Create a new Address instance
        address = Address(
            user=request.user,  # Ensure the user is a CustomUser instance
            street_address=street_address,
            country=country,
            state=state,
            pincode=pincode,
            phone=phone,
            is_default=is_default
        )

        # Save the new address to the database
        address.save()

        # Redirect to a success page or any other appropriate view
        return redirect('add_address')

    return render(request, 'add_another_address.html')
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
            customer_profile = CustomerProfile.objects.get(customer=user)
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

                # Keep a record of purchased items in the order
                for cart_item in request.user.cart.cartitem_set.all():
                    OrderItem.objects.create(
                        order=order,
                        product=cart_item.product,
                        quantity=cart_item.quantity,
                        item_total=cart_item.product.product_price * cart_item.quantity
                    )

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
from .models import OrderItem, CustomerProfile

def ordersummary(request):
    if request.user.is_authenticated:
        try:
            # Try to fetch the customer profile for the logged-in user
            customer_profile = CustomerProfile.objects.get(customer=request.user)
        except CustomerProfile.DoesNotExist:
            # Handle the case where the CustomerProfile does not exist
            # You can redirect the user to a profile creation page or display a message.
            messages.warning(request, 'Please complete your profile to proceed.')
            return redirect('Customer_Profile')  # Replace 'profile_creation' with your actual view name for profile creation

        # Fetch only the orders with a paid status
        order_items = OrderItem.objects.filter(order__user=request.user, order__payment_status=True)

        total_amount = sum(item.item_total for item in order_items)

        context = {
            'order_items': order_items,
            'total_amount': total_amount,
            'shipping_address': customer_profile.street_address,
            'country': customer_profile.country,
            'state': customer_profile.state,
            'phone': customer_profile.phone,
            # Add other context variables as needed for the shipping address, etc.
        }

        return render(request, 'ordersummary.html', context)
    else:
        # Redirect the user to the login page
        return redirect('login')  # Replace 'login' with your actual login view name

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Order, CustomUser

@login_required
def all_user_orders(request):
    users = CustomUser.objects.filter(is_superadmin=False)
    user_orders = {}
    
    for user in users:
        orders = Order.objects.filter(user=user, payment_status=True)
        user_orders[user] = orders

    return render(request, 'all_user_orders.html', {'user_orders': user_orders})

# Add a function to handle approval and disapproval (in the same view)
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
from django.shortcuts import render, redirect
from .models import ShippingAddress

def add_shipping_address(request):
    if request.method == 'POST':
        # Get data from the request
        street_address = request.POST.get('street_address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        pincode = request.POST.get('pincode')

        # Validate the data (add your validation logic here)

        # Create a new ShippingAddress instance
        new_address = ShippingAddress.objects.create(
            street_address=street_address,
            city=city,
            state=state,
            pincode=pincode
        )

        return redirect('ordersummary', address_id=new_address.id)

    return render(request, 'add_shipping_address.html')
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
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import OrderItem, WatchProduct

def rate_product(request):
    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        rating = request.POST.get('rating')

        # Get the OrderItem and associated product
        order_item = get_object_or_404(OrderItem, id=item_id)
        product = order_item.product

        # Update the product's ratings
        product.ratings += int(rating)
        product.save()

        # You can also store the rating and review in the OrderItem model if needed
        order_item.rating = int(rating)
        order_item.save()

        messages.success(request, 'Product rated successfully.')
    else:
        messages.error(request, 'Invalid request.')

    # Redirect back to the order summary page
    return redirect('ordersummary')
from django.shortcuts import get_object_or_404, redirect

def remove_order_item(request, item_id):
    order_item = get_object_or_404(OrderItem, id=item_id)

    # Set the 'is_removed' flag to True
    order_item.is_removed = True
    order_item.save()

    # Redirect back to the order summary page or any desired page
    return redirect('ordersummary')
# views.py

from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from .models import DeliveryTeam, CustomUser

def register_delivery_team(request):
    if request.method == 'POST':
        # Get data from the request
        name = request.POST.get('name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        location = request.POST.get('location')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # Basic password validation
        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return redirect('register_delivery_team')

        # Create a new CustomUser instance
        user = CustomUser(
            name=name,
            username=username,
            email=email,
            phone=phone,
            password=password
        )
        user.save()

        # Create a new DeliveryTeam instance linked to the user
        delivery_team = DeliveryTeam(
            user=user,
            location=location
        )
        delivery_team.save()

        # Send a welcome email to the new delivery boy
        subject = 'Welcome to our Delivery Team'
        message = render_to_string('welcome_email_template.txt', {'user': user, 'password': password})
        from_email = 'admin@horofix.com'
        recipient_list = [email]  # Use the actual email field from your model

        send_mail(subject, message, from_email, recipient_list)

        messages.success(request, 'Delivery team added successfully. Welcome email sent.')
        return redirect('delivery_team_list')  # Replace with the actual URL pattern for the delivery team list

    return render(request, 'register_delivery_team.html')


def delivery_team_list(request):
    delivery_teams = DeliveryTeam.objects.all()
    return render(request, 'delivery_team_list.html', {'delivery_teams': delivery_teams})
def delete_delivery_boy(request, user_id):
   
    return redirect('delivery_team_list')