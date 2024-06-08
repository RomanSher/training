from django.contrib import admin

from project.djnago_admin.admin import OrderModelAdmin
from user.models import User


@admin.register(User)
class UserAdmin(OrderModelAdmin):
    list_display = (
        'id', 'username', 'full_name', 'email',  'phone',
        'is_superuser', 'is_active', 'show_count_orders'
    )
    search_fields = ('id', 'username', 'email', 'full_name')
    list_filter = ('is_superuser', 'is_active')
