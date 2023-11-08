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
from django.core.mail import send_mail


 
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
                # elif request.user.user_typ == CustomUser.VENDOR:
                #     print("user is therapist")
                #     return redirect(reverse('therapist'))
                elif request.user.user_types == CustomUser.ADMIN:
                    print("user is admin")                   
                    return redirect('adminpanel')
                # else:
                #     print("user is normal")
                #     return redirect('')

            else:
                messages.success(request,("Invalid credentials."))
        else:
            messages.success(request,("Please fill out all fields."))
        
    return render(request, 'login.html')



def Customer_Profile(request):
    # Ensure that the user is authenticated
    if not request.user.is_authenticated:
        # Handle the case where the user is not authenticated, e.g., redirect to the login page.
        return redirect('login')  # Replace 'login' with the name of your login view.

    # Get or create the user's profile
    user_profile, created = CustomerProfile.objects.get_or_create(customer=request.user)

    if request.method == 'POST':
        # Handle the POST request for updating user profile fields
        name = request.POST.get('name')
        street_address=request.POST.get('street_address')
        country=request.POST.get('country')
        state=request.POST.get('state')
        pincode=request.POST.get('pincode')
        #last_name = request.POST.get('last_name')
        phone = request.POST.get('phone')

        # Update the user profile fields
        user_profile.name = name
        user_profile.street_address=street_address
        user_profile.country=country
        user_profile.state=state
        user_profile.pincode=pincode
        
        user_profile.phone= phone
        user_profile.save()

        messages.success(request, 'Profile updated successfully')  # Display a success message
        return redirect('Customer_Profile')  # Redirect to the same page or another page after update

    # Handle the GET request for displaying the user profile form
    context = {
        'user_profile': user_profile,
        'form_submitted': False,
    }
    return render(request, 'Customer_Profile.html', context)

# def forgotpassword(request):
#     return render(request, 'forgotpassword.html')

@login_required(login_url='login')
def custom_logout(request):
     if request.session.get('is_authenticated'):
        del request.session['is_authenticated'] 
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
from django.shortcuts import render, redirect





from django.shortcuts import get_object_or_404

def delete_product(request, product_id):
    product = get_object_or_404(WatchProduct, pk=product_id)
    product.status = 'disabled'  # Mark the product as deactivated
    product.save()
    return redirect('view_products')


# views.py

from django.shortcuts import render, get_object_or_404, redirect

def edit_product(request, product_id):
    # Get the existing product object
    product = get_object_or_404(WatchProduct, id=product_id)

    if request.method == 'POST':
        # Retrieve the data from the form
        product_name = request.POST['product_name']
        product_price = request.POST['product_price']
        product_sale_price = request.POST['product_sale_price']
        discount = request.POST['discount']
        watch_description = request.POST['watch_description']

        # Update the fields of the existing product object
        product.product_name = product_name
        product.product_price = product_price
        product.product_sale_price = product_sale_price
        product.discount = discount
        product.watch_description = watch_description

        # Save the changes
        product.save()

        return redirect('view_products')

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


def edit_product(request, product_id):
    # Retrieve the product you want to edit (you need to fetch it from your database)
    product = WatchProduct.objects.get(pk=product_id)

    if request.method == 'POST':
        product_name = request.POST['product_name']
        category = request.POST['category']  # Retrieve the category field
        product_price = request.POST['product_price']
        product_sale_price = request.POST['product_sale_price']
        discount = request.POST['discount']
        watch_description = request.POST['watch_description']
        watch_image = request.FILES.get('product_image')  # Use get() to avoid errors

        # Update the product fields
        product.product_name = product_name
        product.category = category  # Update the category
        product.product_price = product_price
        product.product_sale_price = product_sale_price
        product.discount = discount
        product.watch_description = watch_description

        if watch_image:
            product.watch_image = watch_image

        product.save()  # Save the updated product

        # Redirect to the view product page or wherever you want
        return redirect('view_products')
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
@login_required(login_url='login')
def view_cart(request):
    user = request.user
    
   
    cart_items = CartItem.objects.filter(cart=request.user.cart)
    # Rest of your code
    return render(request, 'view_cart.html', {'cart_items': cart_items})




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

from django.shortcuts import get_object_or_404

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
            order = Order.objects.create(user=user, total_amount=total_amount)
            for cart_item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=cart_item.product,
                    quantity=cart_item.quantity,
                    item_total=cart_item.product.product_sale_price * cart_item.quantity
                )

            client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
            payment_data = {
                'amount': int(total_amount * 100),
                'currency': 'INR',
                'receipt': f'order_{order.id}',
                'payment_capture': '1'
            }
            orderData = client.order.create(data=payment_data)
            order.payment_id = orderData['id']
            order.save()

            return JsonResponse({'order_id': orderData['id']})
        
        except Exception as e:
            print(str(e))
            return JsonResponse({'error': 'An error occurred. Please try again.'}, status=500)

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.conf import settings
from .models import Order, CustomerProfile

@csrf_exempt
def checkout(request):
    cart_count = get_cart_count(request)
    email = ""

    if request.user.is_authenticated:
        user = request.user
        cart_items = CartItem.objects.filter(cart=user.cart)
        total_amount = sum(item.product.product_sale_price * item.quantity for item in cart_items)

        # Access the user's name from the related CustomerProfile
        customer_profile = CustomerProfile.objects.get(customer=user)
        email = user.email
        full_name = customer_profile.name

    else:
        # Handle the case where the user is not authenticated
        user = None
        cart_items = []
        total_amount = 0
        full_name = ""

    context = {
        'cart_count': cart_count,
        'cart_items': cart_items,
        'total_amount': total_amount,
        'email': email,
        'full_name': full_name,
    }
    return render(request, 'checkout.html', context)

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import razorpay
from django.conf import settings
from .models import Order

@csrf_exempt
def handle_payment(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        razorpay_order_id = data.get('order_id')
        payment_id = data.get('payment_id')

        try:
            order = Order.objects.get(payment_id=razorpay_order_id)

            client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
            payment = client.payment.fetch(payment_id)

            if payment['status'] == 'captured':
                order.payment_status = True
                order.save()
                # Add your logic for clearing the cart or marking the order as paid
                return JsonResponse({'message': 'Payment successful'})
            else:
                return JsonResponse({'message': 'Payment failed'})

        except Order.DoesNotExist:
            return JsonResponse({'message': 'Invalid Order ID'})
        except Exception as e:
            print(str(e))
            return JsonResponse({'message': 'Server error, please try again later.'})




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
