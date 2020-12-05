from django.contrib import admin
from .models import Customer, Order, Product, Shop

admin.site.register(Shop)
admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Order)
