#from django.db import models
from django.contrib.auth.models import User

from django.db import models
from datetime import date
from django.db.models.signals import post_save
from django.dispatch import receiver

from django.contrib.auth.models import AbstractUser, BaseUserManager

# Create your models here.

class UserManager(BaseUserManager):
     def create_user(self,name, username, phone, email, password=None):
         if not email:
             raise ValueError('User must have an email address')

         user = self.model(
             email=self.normalize_email(email),
             name= name,
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
         user.role=1
         user.save(using=self._db)
         return user

class CustomUser(AbstractUser):
    ADMIN = 1
    CUSTOMER = 2
    DELIVERYTEAM = 3
    TECHNICIAN = 4

    USER_TYPES = (
        (ADMIN, 'Admin'),
        (CUSTOMER, 'Customer'),
        (DELIVERYTEAM, 'Deliveryteam'),
        (TECHNICIAN,'Technician'),
    )

    #username=None
    user_types = models.PositiveSmallIntegerField(choices=USER_TYPES,default='2')
    name = models.CharField(max_length=50)
    username=models.CharField(max_length=50,unique=True)


    #last_name = models.CharField(max_length=50)
    #USERNAME_FIELD = 'email'
    email = models.EmailField(max_length=100, unique=True)
    phone = models.CharField(max_length=10,blank=True,unique=True)
    password = models.CharField(max_length=128)
   # confirmPassword = models.CharField(max_length=128)
    #role = models.PositiveSmallIntegerField(choices=ROLE_CHOICE, blank=True, null=True,default='1')


    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superadmin = models.BooleanField(default=False)

    
    #REQUIRED_FIELDS = ['first_name','last_name', 'phone']

    objects = UserManager()

    def str(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True



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
    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, default=None)
    name = models.CharField(max_length=100)
    street_address=models.CharField(max_length=100,null=True,blank=True)
    country = models.CharField(max_length=15, default="India", blank=True, null=True)
    state = models.CharField(max_length=50, blank=True, null=True)
    pincode = models.CharField(max_length=50, blank=True, null=True)
   
    phone = models.CharField(max_length=10,blank=True, null=True)

    def str(self):
        return self.user.email 
 
from django.db import models

class WatchProduct(models.Model):
    product_name = models.CharField(max_length=255, unique=True)  # Add unique=True to prevent duplicates
    watch_description = models.TextField()
    watch_image = models.ImageField(upload_to='watch_images/', null=True, blank=True)
    product_price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    product_sale_price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    discount = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    category = models.CharField(max_length=10, choices=[('Men', 'Men'), ('Women', 'Women')], default=None)
    stock = models.PositiveIntegerField(default=1, null=True)  # Add the 'stock' field

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
        return f"{self.quantity} x {self.product.name}"

class Cart(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    products = models.ManyToManyField(WatchProduct, through='CartItem')

    def __str__(self):
        return f"Cart for {self.user.username}"

class Address(models.Model):
    user = models.ForeignKey( CustomUser, on_delete=models.CASCADE, related_name='addresses')
    street_address = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    pincode = models.CharField(max_length=10)
    phone = models.CharField(max_length=15)
    is_default = models.BooleanField(default=False)

    def __str__(self):
        return f"Address for {self.user.username}"



class Order(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    products = models.ManyToManyField(WatchProduct, through='OrderItem')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_id = models.CharField(max_length=100, null=True, blank=True)
    payment_status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"
from django.db import models

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(WatchProduct, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    item_total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.product.product_name} in Order {self.order.id}"
