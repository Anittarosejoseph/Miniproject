from django.contrib import admin
from .models import CustomUser
from .models import CustomerProfile# Register your models here.
#from .models import Category
from .models import WatchProduct
admin.site.register(CustomUser)
admin.site.register(CustomerProfile)
admin.site.register(WatchProduct)