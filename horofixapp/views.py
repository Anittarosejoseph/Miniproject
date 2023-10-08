from django.shortcuts import render,redirect
from .models import CustomUser,UserProfile
from .models import CustomerProfile  # Import the correct model
from django.contrib.auth.decorators import login_required
from django.contrib.sessions.models import Session
from django.contrib.auth import authenticate ,login as auth_login,logout 
from django.contrib import messages
from .models import CustomUser
from .models import WatchProduct

 #from django.contrib.auth.models import User
 #from .mode
# Create your views here.

def index(request):
    return render(request, 'index.html')


def about(request):
    return render(request, 'about.html')

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
            if CustomUser.objects.filter(email=email,username=username).exists():
                messages.success(request,("Email is already registered."))
            
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


def login_user(request):
    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]
        # if user is not None:
        #     auth_login(request, user)
        #     return redirect('/userhome')
        # else:
        #    messages.success(request,("Invalid credentials."))
        # print(username)  # Print the email for debugging
        # print(password)  # Print the password for debugging

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


def custom_logout(request):
     if request.session.get('is_authenticated'):
        del request.session['is_authenticated'] 
        logout(request)
        return redirect('index')
@login_required
def adminpanel(request):
    return render(request, 'adminpanel.html')



def view_products(request):
    products = WatchProduct.objects.all()  # Retrieve all products from the database
    return render(request, 'view_products.html', {'products': products})


@login_required
def customer_product_view(request):
    products = WatchProduct.objects.all()
    return render(request, 'customer_product.html', {'products': products})

# Django view to delete the product
from django.shortcuts import render, redirect

def delete_product(request, product_id):
    if request.method == 'POST':
        # Delete the product from the database
        try:
            product = WatchProduct.objects.get(pk=product_id)
            product.delete()
            return redirect('view_products')
        except WatchProduct.DoesNotExist:
            pass
    return redirect('view_products')  # Redirect back to the product list view



# views.py

from django.shortcuts import render, get_object_or_404, redirect
from .models import WatchProduct

def edit_product(request, product_id):
    # Get the existing product object
    product = get_object_or_404(WatchProduct, id=product_id)

    if request.method == 'POST':
        # Retrieve the data from the form
        product_name = request.POST['product_name']
        product_quantity = request.POST['product_quantity']
        product_price = request.POST['product_price']
        product_sale_price = request.POST['product_sale_price']
        discount = request.POST['discount']
        watch_description = request.POST['watch_description']

        # Update the fields of the existing product object
        product.product_name = product_name
        product.product_quantity = product_quantity
        product.product_price = product_price
        product.product_sale_price = product_sale_price
        product.discount = discount
        product.watch_description = watch_description

        # Save the changes
        product.save()

        return redirect('view_products')

    return render(request, 'edit_product.html', {'product': product})





def add_product(request):
    if request.method == 'POST':
        product_name = request.POST['productName']
        product_quantity = request.POST['productQuantity']
        product_price = request.POST['productPrice']
        product_sale_price = request.POST['productSalePrice']
        discount = request.POST['discount']
        watch_description = request.POST['watchDescription']
        watch_image = request.FILES['watchImage']

        # Check if a product with the same name already exists
        if WatchProduct.objects.filter(product_name=product_name).exists():
            messages.error(request, f"A product with the name '{product_name}' already exists.")
        else:
            try:
                # Ensure the numerical fields are valid numbers before saving
                product_quantity = int(product_quantity)
                product_price = float(product_price)
                product_sale_price = float(product_sale_price)
                discount = float(discount)
                
                # Create a new WatchProduct instance and save it
                WatchProduct.objects.create(
                    product_name=product_name,
                    product_quantity=product_quantity,
                    product_price=product_price,
                    product_sale_price=product_sale_price,
                    discount=discount,
                    watch_description=watch_description,
                    watch_image=watch_image
                )
                messages.success(request, "Product added successfully.")
            except (ValueError, TypeError):
                messages.error(request, "Invalid numerical input.")

        return redirect('view_products')
    
    return render(request, 'add_product.html')


from django.shortcuts import render, get_object_or_404, redirect
from .models import WatchProduct

def edit_product(request, product_id):
    # Get the existing product object
    product = get_object_or_404(WatchProduct, id=product_id)

    if request.method == 'POST':
        # Retrieve the data from the form
        product_name = request.POST['product_name']
        product_quantity = request.POST['product_quantity']
        product_price = request.POST['product_price']
        product_sale_price = request.POST['product_sale_price']
        discount = request.POST['discount']
        watch_description = request.POST['watch_description']

        # Update the fields of the existing product object
        product.product_name = product_name
        product.product_quantity = product_quantity
        product.product_price = product_price
        product.product_sale_price = product_sale_price
        product.discount = discount
        product.watch_description = watch_description

        # Save the changes
        product.save()

        return redirect('view_products')

    return render(request, 'edit_product.html', {'product': product})
