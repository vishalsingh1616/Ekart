from django.contrib import admin
from .models import Product, Collection, Customer, Order, OrderItem, ProductImage
from django.db.models import Count
from django.utils.html import format_html
from django.urls import reverse
from django.utils.http import urlencode

# Register your models here.


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    search_fields = ['title']
    list_display = ['title', 'products_count']
    list_per_page = 10
    
    @admin.display(ordering='products_count')
    def products_count(self, collection):
        url = (reverse('admin:store_product_changelist')
                + '?' 
                + urlencode(
                    {'collection__id' : str(collection.id)}
                           )
                )
        return format_html('<a href="{}">{}</a>', url, collection.products_count)
        

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            products_count = Count('product')
        )

class InventoryFilter(admin.SimpleListFilter):
    
    title = 'Inventory'
    parameter_name = 'inventory'

    def lookups(self, request, model_admin):
        return [
            ('<10', 'Low')
        ]

    def queryset(self, request, queryset):
        if self.value() == '<10':
            return queryset.filter(inventory__lt=10)
        
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    readonly_fields = ['thumbnail']
    
    def thumbnail(self, instance):
        if instance.image.name != '':
            return format_html('<img src="{}" class="thumbnail" />', instance.image.url)
        return ''

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    search_fields = ['title']
    autocomplete_fields = ['collection']
    actions = ['clear_inevntory']
    list_display=['title','unit_price', 'inventory_status', 'collection']
    inlines = [ProductImageInline]
    list_editable = ['unit_price']
    list_per_page = 10
    list_select_related = ['collection']
    list_filter = ['collection', 'last_update', InventoryFilter]



    @admin.display(ordering='inventory')
    def inventory_status(self, product):
        if product.inventory < 10:
            return 'Low'
        return 'OK'

    @admin.action(description='Clear_inventory')
    def clear_inevntory(self, request, queryset):
        updated_count = queryset.update(inventory=0)
        self.message_user(
            request,
            f'{updated_count} products were successfully updated.'
        )

    class Meta:
        css = {
            'all': ['store/style.css']
        }

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'membership']
    list_editable = ['membership']
    ordering = ['user__first_name', 'user__last_name']
    list_per_page = 10
    search_fields = ['first_name__istartswith', 'last_name__istartswith']

class OrderitemInline(admin.TabularInline):
    autocomplete_fields = ['product']
    min_num = 1
    model = OrderItem
    max_num = 10
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    autocomplete_fields = ['customer']
    inlines = [OrderitemInline]
    list_display = ['id', 'placed_at', 'customer']
    list_per_page = 10