from django.contrib import admin
from .models import CustomUser
from .models import CustomerProfile# Register your models here.
#from .models import Category
from .models import WatchProduct
#admin.site.register(CustomUser)
admin.site.register(CustomerProfile)
admin.site.register(WatchProduct)


from django.contrib.auth import get_user_model

User = get_user_model()

class SuperuserAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        return User.objects.filter(is_superuser=False)

# Register the custom admin class
admin.site.register(User, SuperuserAdmin)