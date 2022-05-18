from django.db import models
from item.models import Item

# Create your models here.
class Clothes(models.Model):
    title = models.CharField(default='', max_length=255)
    size = models.CharField(default='', max_length=255)
    brand = models.CharField(default='', max_length=255)

    def __str__(self):
        return self.title

class ClothesItem(Item):
    clothes = models.ForeignKey(Clothes, on_delete=models.CASCADE)