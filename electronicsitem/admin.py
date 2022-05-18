from django.contrib import admin

from .models import Electronics,ElectronicsItem

# Register your models here.
admin.site.register(ElectronicsItem)
admin.site.register(Electronics)