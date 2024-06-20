from django.contrib import admin
from .models import Item, Cart, CartItem, Order, OrderItem
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User


class MenuItemAdmin(admin.ModelAdmin):
    list_display = ("meal", "status")
    list_filter = ("status",)
    search_fields = ("meal", "description")

admin.site.register(Item, MenuItemAdmin)

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'status', 'total_price', 'created_at', 'estimated_delivery')
    list_filter = ('status',)
    inlines = [OrderItemInline]


admin.site.register(Order, OrderAdmin)
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
admin.site.register(Cart)
admin.site.register(CartItem)