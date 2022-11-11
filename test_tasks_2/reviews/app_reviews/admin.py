from django.contrib import admin
from .models import *
from import_export.admin import ImportExportModelAdmin


class СountryAdmin(ImportExportModelAdmin):
    list_display = ['id', 'name']

class ManufacturerAdmin(ImportExportModelAdmin):
    list_display = ['id', 'name', 'country']

class CarAdmin(ImportExportModelAdmin):
    list_display = ['id', 'name', 'manufacturer', 'year_release', 'year_end']

class CommentAdmin(ImportExportModelAdmin):
    list_display = ['id', 'email', 'car']


admin.site.register(Сountry, СountryAdmin)
admin.site.register(Manufacturer, ManufacturerAdmin)
admin.site.register(Car, CarAdmin)
admin.site.register(Comment, CommentAdmin)

