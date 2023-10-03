from django.contrib import admin
from .models import CustomUser
from .models import CustomerProfile# Register your models here.
admin.site.register(CustomUser)
admin.site.register(CustomerProfile)