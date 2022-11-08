from django.contrib import admin
from .models import *


class СountryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']

class ManufacturerAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'country']

class CarAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'manufacturer', 'year_release', 'year_end']

class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'email', 'car']


admin.site.register(Сountry, СountryAdmin)
admin.site.register(Manufacturer, ManufacturerAdmin)
admin.site.register(Car, CarAdmin)
admin.site.register(Comment, CommentAdmin)