from django.db import models

# Create your models here.

class Category(models.Model):
    title = models.CharField(default='', max_length=255)
    slug = models.CharField(default='', max_length=255)
    description = models.CharField(default='', max_length=255)
    active = models.BooleanField(default=True)

class Product(models.Model):
    title = models.CharField(default='', max_length=255)
    description = models.CharField(default='', max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    product_img = models.CharField(default='', max_length=255)
    price = models.FloatField(default=0)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.title