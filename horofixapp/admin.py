from django.contrib import admin
from .models import *
#admin.site.register(CustomUser)
admin.site.register(CustomerProfile)
admin.site.register(WatchProduct)
# admin.site.register(CartProduct)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(WishlistItem)

from django.contrib.auth import get_user_model

User = get_user_model()

class SuperuserAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        return User.objects.filter(is_superuser=False)

# Register the custom admin class
admin.site.register(User, SuperuserAdmin)