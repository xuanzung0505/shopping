from django.db import models
from item.models import Item

# Create your models here.
class Electronics(models.Model):
    title = models.CharField(default='', max_length=255)
    RAM = models.CharField(default='', max_length=255)
    OS = models.CharField(default='', max_length=255)

    def __str__(self):
        return self.title

class ElectronicsItem(Item):
    electronics = models.ForeignKey(Electronics, on_delete=models.CASCADE)