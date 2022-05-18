from django.db import models
from product.models import Category

# Create your models here.
class Item(models.Model):
    title = models.CharField(default='', max_length=255)
    description = models.CharField(default='', max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    item_img = models.CharField(default='', max_length=255)
    price = models.FloatField(default=0)
    quantity = models.IntegerField(default=0)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

