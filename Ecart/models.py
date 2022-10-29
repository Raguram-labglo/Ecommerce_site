from operator import mod
from django.db import models
from django.contrib.auth.models import User
order = [('pending', 'pending'), ('shipping', 'shipping'), ('delivered', 'delivered')]
class Product(models.Model):
    title = models.CharField(max_length= 100)
    image = models.ImageField(upload_to = "prodects_img/", null=True)
    name = models.CharField(max_length = 50)
    brand = models.CharField(max_length = 40)
    price = models.IntegerField()
    in_stock = models.IntegerField()
    
    
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    product = models.ForeignKey(Product,  null = True, on_delete = models.CASCADE)
    price = models.IntegerField(null = True)
    quantity = models.IntegerField(default = 1)
    is_active = models.BooleanField(default = True)

class Order(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    order_items = models.ManyToManyField(Cart)
    order_status = models.CharField(max_length = 60, choices = order, default = 'pending')

class Wish(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    favourite = models.ManyToManyField(Product)
    wished = models.BooleanField(default = True)
