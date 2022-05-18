from django.contrib import admin

from .models import Shoes,ShoesItem

# Register your models here.
admin.site.register(ShoesItem)
admin.site.register(Shoes)