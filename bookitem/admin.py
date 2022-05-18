from django.contrib import admin

from .models import BookItem, Book

# Register your models here.
admin.site.register(BookItem)
admin.site.register(Book)