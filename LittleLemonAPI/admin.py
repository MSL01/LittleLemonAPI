from django.contrib import admin
from .models import Profile, MenuItem, Category, Order, OrderItem
# Register your models here.

admin.site.register(Profile)
admin.site.register(MenuItem)
admin.site.register(Category)
admin.site.register(Order)
admin.site.register(OrderItem)