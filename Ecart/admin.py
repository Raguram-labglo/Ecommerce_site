from django.contrib import admin
from Ecart.models import *


admin.site.register(Product)

class Cart_list(admin.ModelAdmin):
    list_display = ('id','user', 'product', 'price', 'quantity')
admin.site.register(Cart, Cart_list)

class Order_list(admin.ModelAdmin):
    list_display = ('id','user', 'order_price', 'order_status')
admin.site.register(Order, Order_list)

admin.site.register(Wish)