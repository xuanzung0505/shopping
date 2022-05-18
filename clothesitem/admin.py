from django.contrib import admin

from .models import Clothes,ClothesItem

# Register your models here.
admin.site.register(ClothesItem)
admin.site.register(Clothes)