from django.db import models
from item.models import Item

# Create your models here.
class Book(models.Model):
    title = models.CharField(default='', max_length=255)
    author = models.CharField(default='', max_length=255)
    publisher = models.CharField(default='', max_length=255)

    def __str__(self):
        return self.title

class BookItem(Item):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)