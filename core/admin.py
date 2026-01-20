from django.contrib import admin
from store.models import Product, Collection, Customer, Order, OrderItem
from store.admin import ProductAdmin, ProductImageInline
from tags.models import TaggedItem  
from django.contrib.contenttypes.admin import GenericTabularInline
from django.contrib.auth.admin import UserAdmin as BaseUSerAdmin
from .models import User
# Register your models here.
@admin.register(User)
class UserAdmin(BaseUSerAdmin):
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "usable_password", "email", "password1", "password2", "first_name", "last_name"),
            },
        ),
    )

    


class TagInline(GenericTabularInline):
    autocomplete_fields = ['tag']
    model = TaggedItem

class CustomProductAdmin(ProductAdmin):
    inlines = [TagInline, ProductImageInline]

admin.site.unregister(Product)
admin.site.register(Product, CustomProductAdmin)