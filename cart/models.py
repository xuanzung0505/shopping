from django.db import models
from product.models import Product
from user.models import CustomerUser
# Create your models here.

class Cart(models.Model):
    user = models.ForeignKey(CustomerUser, on_delete=models.CASCADE)
    create_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    totalPrice = models.FloatField(default=0)
    is_ordered = models.BooleanField(default=False)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE)
    item = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.FloatField(default=0)
    quantity = models.IntegerField(default=0)
    totalPrice = models.FloatField(default=0) #hehehe