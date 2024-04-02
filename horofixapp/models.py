#from django.db import models
from django.contrib.auth.models import User
from django.db import models
from datetime import date
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db.models import Q
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib import messages
# # Create your models here.

class UserManager(BaseUserManager):
    def create_user(self,name, username, phone, email, password=None):
         if not email:
             raise ValueError('User must have an email address')

         user = self.model(
             email=self.normalize_email(email),
             name= name,
             username=username,
             #last_name=last_name,
             phone=phone, 
         )
         user.set_password(password)
         user.save(using=self._db)
         return user
    
    def create_superuser(self,name,phone, email, password=None):
        
         user = self.create_user(
              email=self.normalize_email(email),
              password=password,
              name=name,
              #last_name=last_name,
              phone=phone,
              )
         user.is_admin = True
         user.is_active = True
         user.is_staff = True
         user.is_superadmin = True
         user.save(using=self._db)
         return user


class CustomUser(AbstractUser):

    USER_TYPES = (
        ('ADMIN','Admin'),
        ('VENDOR', 'Vendor'),
        ('DELIVERYTEAM', 'Deliveryteam'),
        ('CUSTOMER', 'Customer'),
        ('TECHNICIAN',' Technician')
    )

    user_type = models.CharField(max_length=20,choices=USER_TYPES,blank=True, null=True, default='CUSTOMER')

    name = models.CharField(max_length=50)
    username=models.CharField(max_length=50,unique=True)


  
    email = models.EmailField(max_length=100, unique=True)
    phone = models.CharField(max_length=10,blank=True)
    password = models.CharField(max_length=128)
    city = models.CharField(max_length=50, blank=True, null=True, default=None)


    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superadmin = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=True)
    is_deliveryteam = models.BooleanField(default=False)
    is_technician=models.BooleanField(default=False)

    REQUIRED_FIELDS = []
   
    objects = UserManager()
   
    def str(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True
    def set_delivery_team_role(self):
        self.user_type = 'DELIVERYTEAM'
        self.save()

class UserProfile(models.Model):

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='media/profile_picture', blank=True, null=True)
    address = models.CharField(max_length=50, blank=True, null=True)
    addressline1 = models.CharField(max_length=50, blank=True, null=True)
    addressline2 = models.CharField(max_length=50, blank=True, null=True)
    country = models.CharField(max_length=15, default="India", blank=True, null=True)
    country = models.CharField(max_length=50, blank=True, null=True)
    state = models.CharField(max_length=50, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    pin_code = models.CharField(max_length=50, blank=True, null=True)
    gender = models.CharField(max_length=50, blank=True, null=True)
    dob = models.DateField(blank=True, null=True)
    profile_created_at = models.DateTimeField(auto_now_add=True)
    profile_modified_at = models.DateTimeField(auto_now=True)


    def calculate_age(self):
        today = date.today()
        age = today.year - self.dob.year - ((today.month, today.day) < (self.dob.month, self.dob.day))
        return age
    age = property(calculate_age)


    def get_gender_display(self):
        return dict(self.GENDER_CHOICES).get(self.gender)

    def str(self):
        return self.user.email
    
    def get_role(self): 
        if self.user_type == 2:
            user_role = 'Customer'
        elif self.user_type == 3:
            user_role = 'Deliveryteam'
        elif self.user_type == 4:
            user_role = 'Technician'
        
        return user_role

#cmd  -- python manage.py makemigrations
#        python manage.py migrate

class CustomerProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, default=None)
    name = models.CharField(max_length=100)
    street_address = models.CharField(max_length=100, null=True, blank=True, default=None)
    country = models.CharField(max_length=15, default="India", blank=True, null=True)
    state = models.CharField(max_length=50, blank=True, null=True, default=None)
    city = models.CharField(max_length=50, blank=True, null=True, default=None)
    pincode = models.CharField(max_length=50, blank=True, null=True)
    phone = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return self.user.email
class Technician(models.Model):
    user = models.OneToOneField(
        'CustomUser',
        on_delete=models.CASCADE,
        primary_key=True,
    )
    experience = models.PositiveIntegerField()
    city = models.CharField(max_length=100)
    pincode = models.CharField(max_length=6)

    def __str__(self):
        return self.user.username
    
 
class DeliveryTeam(models.Model):
    team_name = models.CharField(max_length=100, default='', null=True)  # Field for the delivery team's name
    vehicle_number = models.CharField(max_length=20, default='', null=True)  # Field for the vehicle number
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    pincode = models.CharField(max_length=50)
    city = models.CharField(max_length=50, blank=True, null=True)  

    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username} - {self.team_name}"
    def get_assigned_orders(self):
        return Order.objects.filter(delivery_team=self)
    
from django.db import models

class WatchProduct(models.Model):
    product_name = models.CharField(max_length=255, unique=True,null=True) 
    watch_modelnumber = models.CharField(max_length=255, null=True)
    watch_serial_number = models.CharField(max_length=255, unique=True, null=True)
    watch_description = models.TextField()
    watch_image = models.ImageField(upload_to='watch_images/', null=True, blank=True)
    product_price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    product_sale_price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    discount = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    category = models.CharField(max_length=10, choices=[('Men', 'Men'), ('Women', 'Women'),('Kids', 'Kids'),('Unisex', 'Unisex'),], default=None)
    stock = models.PositiveIntegerField(default=1, null=True)  # Add the 'stock' field
    ratings = models.IntegerField(default=0) 
    warranty = models.IntegerField(null=True) 
    # Modify the STATUS_CHOICES
    STATUS_CHOICES = [
        ('In Stock', 'In Stock'),
        ('Out of Stock', 'Out of Stock'),
    ]

    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default='In Stock')

    def save(self, *args, **kwargs):
        # Update the status based on the stock value
        if self.stock == 0:
            self.status = 'Out of Stock'
        else:
            self.status = 'In Stock'
        super(WatchProduct, self).save(*args, **kwargs)

    def __str__(self):
        return self.product_name





class CartItem(models.Model):
    cart = models.ForeignKey('Cart', on_delete=models.CASCADE)
    product = models.ForeignKey(WatchProduct, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    is_active = models.BooleanField(default=True)


    def __str__(self):
        return f"{self.quantity} x {self.product.product_name}"

class Cart(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    products = models.ManyToManyField(WatchProduct, through='CartItem')

    def __str__(self):
        return f"Cart for {self.user.username}"

from django.db import models
from django.contrib.auth import get_user_model
from .models import WatchProduct

CustomUser = get_user_model()

class Order(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    products = models.ManyToManyField(WatchProduct, through='OrderItem')

    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_id = models.CharField(max_length=100, null=True, blank=True)
    payment_status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    status_choices = [
        ('Placed', 'Placed'),
        ('Processing', 'Processing'),
        ('Delivered', 'Delivered'),
    ]
    status = models.CharField(max_length=20, choices=status_choices, default='Placed')

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"

   
from django.db import models
from django.db import models

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(WatchProduct, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    item_total = models.DecimalField(max_digits=10, decimal_places=2)
    order_date = models.DateField(auto_now_add=True)
    order_time = models.TimeField(auto_now_add=True)
    is_removed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.quantity} x {self.product.product_name} in Order {self.order.id}"



class WishlistItem(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product = models.ForeignKey('WatchProduct', on_delete=models.CASCADE)

    def __str__(self):
        return self.product.product_name
from django.db import models

class ShippingAddress(models.Model):
    street_address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.street_address}, {self.city}, {self.state} - {self.pincode}"


class Customer(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    pincode = models.CharField(max_length=10, blank=True, null=True) 
    # Add any customer-specific fields here

    def __str__(self):
        return self.user.email
from django.db import models





from django.db import models
from django.contrib.auth import get_user_model
from django.db.models import Q

User = get_user_model()

# Create your models here.

class ThreadManager(models.Manager):
    def by_user(self, **kwargs):
        user = kwargs.get('user')
        lookup = Q(first_person=user) | Q(second_person=user)
        qs = self.get_queryset().filter(lookup).distinct()
        return qs


class Thread(models.Model):
    first_person = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True, related_name='thread_first_person')
    second_person = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True,
                                     related_name='thread_second_person')
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = ThreadManager()
    class Meta:
        unique_together = ['first_person', 'second_person']


class ChatMessage(models.Model):
    thread = models.ForeignKey(Thread, null=True, blank=True, on_delete=models.CASCADE, related_name='chatmessage_thread')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

from django.db import models
from django.utils import timezone

class WatchRepairService(models.Model):
    issue_type = models.CharField(max_length=255, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.issue_type

class WatchRepairRequest(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    watch_name = models.CharField(max_length=255, null=True)
    watch_model_number = models.CharField(max_length=255, null=True)
    issue_types = models.ManyToManyField(WatchRepairService)
    issue_description = models.TextField(null=True)
    image_upload = models.ImageField(upload_to='watch_images/', null=True, blank=True)
    additional_info = models.TextField(blank=True, null=True)
    purchase_date = models.DateField(null=True)
    warranty_duration = models.IntegerField(null=True)
    created_at = models.DateTimeField(default=timezone.now)
    is_approved = models.BooleanField(default=False)
    is_rejected = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.name}'s Watch Repair Request"

   

  

class RepairPayment(models.Model):
    order = models.ForeignKey(WatchRepairRequest, on_delete=models.CASCADE)
    razor_pay_order_id = models.CharField(max_length=255)
    amount = models.IntegerField()  # or DecimalField, depending on your requirements
    is_paid = models.BooleanField(default=False)
    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)

    # other fields...

    def __str__(self):
        return f"Payment for Repair Request: {self.order.user.name}'s Watch Repair Request"

from django.contrib.auth.models import User

class Address(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    street_address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)
    country = models.CharField(max_length=100, default='', blank=True)  # Add country field

    def __str__(self):
        return f"{self.street_address}, {self.city}, {self.state}, {self.country} - {self.pincode}"

class Appoinment(models.Model):
   
    preffered_date = models.DateField()
    preffered_time = models.TimeField()
    email = models.EmailField(null=True, blank=True)
    phone_number = models.CharField(max_length=10, null=True, blank=True)
    address = models.ForeignKey(
        Address,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
   
    appoinment_type = models.CharField(max_length=10)
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    prescription = models.FileField(
        upload_to="media/prescriptions/",
        null=True,
        blank=True,
    )
    location = models.ForeignKey(
        "Location",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    razorpay_order_id = models.CharField(max_length=100, null=True, blank=True)
    appointment_status = models.CharField(max_length=20,default='pending')
   
class Location(models.Model):
    address = models.TextField(null=True,blank=True)
    distance = models.DecimalField(max_digits=10, decimal_places=2,null=True,blank=True)
    latitude = models.CharField(max_length=50,null=True,blank=True)
    longitude = models.CharField(max_length=50,null=True,blank=True)
class Video(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()  # Add a description field
    video_file = models.FileField(upload_to='videos/')
    # Add any other fields you need, such as tags, etc.

    def _str_(self):
        return self.title
from django.db import models

class Watch(models.Model):
    product_name = models.CharField(max_length=255, unique=True,null=True) 
    watch_modelnumber = models.CharField(max_length=255, null=True)
    watch_serial_number = models.CharField(max_length=255, unique=True, null=True)
    watch_description = models.TextField()
    watch_image = models.ImageField(upload_to='watch_images/', null=True, blank=True)
    product_price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    product_sale_price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    discount = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    category = models.CharField(max_length=10, choices=[('Men', 'Men'), ('Women', 'Women'),('Kids', 'Kids'),('Unisex', 'Unisex'),], default=None)
    stock = models.PositiveIntegerField(default=1, null=True)  # Add the 'stock' field
    ratings = models.IntegerField(default=0) 
    warranty = models.IntegerField(null=True) 
    # Modify the STATUS_CHOICES
    STATUS_CHOICES = [
        ('In Stock', 'In Stock'),
        ('Out of Stock', 'Out of Stock'),
    ]

    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default='In Stock')

    def save(self, *args, **kwargs):
        # Update the status based on the stock value
        if self.stock == 0:
            self.status = 'Out of Stock'
        else:
            self.status = 'In Stock'
        super(WatchProduct, self).save(*args, **kwargs)

    def __str__(self):
        return self.product_name



from django.db import models
from django.contrib.auth import get_user_model

CustomUser = get_user_model()

class CustomWatch(models.Model):
    product_name = models.CharField(max_length=255, unique=True,null=True) 
    watch_modelnumber = models.CharField(max_length=255, null=True)
    watch_serial_number = models.CharField(max_length=255, unique=True, null=True)
    watch_description = models.TextField()
    watch_image = models.ImageField(upload_to='watch_images/', null=True, blank=True)
    product_price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    product_sale_price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    discount = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    category = models.CharField(max_length=10, choices=[('Men', 'Men'), ('Women', 'Women'),('Kids', 'Kids'),('Unisex', 'Unisex'),], default=None)
    stock = models.PositiveIntegerField(default=1, null=True)  # Add the 'stock' field
    ratings = models.IntegerField(default=0) 
    warranty = models.IntegerField(null=True) 
    # Modify the STATUS_CHOICES
    STATUS_CHOICES = [
        ('In Stock', 'In Stock'),
        ('Out of Stock', 'Out of Stock'),
    ]

    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default='In Stock')

    def save(self, *args, **kwargs):
        # Update the status based on the stock value
        if self.stock == 0:
            self.status = 'Out of Stock'
        else:
            self.status = 'In Stock'
        super(CustomWatch, self).save(*args, **kwargs)

    def __str__(self):
        return self.product_name


class CustomizationDetail(models.Model):
    watch = models.ForeignKey(CustomWatch, on_delete=models.CASCADE)
    strap_material = models.CharField(max_length=100, null=True, blank=True)
    strap_color = models.CharField(max_length=50, null=True, blank=True)
    dial_color = models.CharField(max_length=50, null=True, blank=True)
    case_material = models.CharField(max_length=100, null=True, blank=True)
    case_color = models.CharField(max_length=50, null=True, blank=True)
    engraving_text = models.CharField(max_length=255, null=True, blank=True)
    engraving_font = models.CharField(max_length=50, null=True, blank=True)
    engraving_location = models.CharField(max_length=100, null=True, blank=True)
    special_requests = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Customization for {self.watch.product_name}"


class CustomCartItem(models.Model):
    cart = models.ForeignKey('CustomCart', on_delete=models.CASCADE)
    product = models.ForeignKey(CustomWatch, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.quantity} x {self.product.product_name}"


class CustomCart(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    products = models.ManyToManyField(CustomWatch, through='CustomCartItem')

    def __str__(self):
        return f"Cart for {self.user.username}"


class CustomOrder(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    products = models.ManyToManyField(CustomWatch, through='CustomOrderItem')

    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_id = models.CharField(max_length=100, null=True, blank=True)
    payment_status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    status_choices = [
        ('Placed', 'Placed'),
        ('Processing', 'Processing'),
        ('Delivered', 'Delivered'),
    ]
    status = models.CharField(max_length=20, choices=status_choices, default='Placed')

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"


class CustomOrderItem(models.Model):
    order = models.ForeignKey(CustomOrder, on_delete=models.CASCADE)
    product = models.ForeignKey(CustomWatch, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    item_total = models.DecimalField(max_digits=10, decimal_places=2)
    order_date = models.DateField(auto_now_add=True)
    order_time = models.TimeField(auto_now_add=True)
    is_removed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.quantity} x {self.product.product_name} in Order {self.order.id}"
