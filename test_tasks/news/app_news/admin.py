from django.contrib import admin
from .models import *

class NewsAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'description']


admin.site.register(News, NewsAdmin)