from django.contrib import admin
from .models import ViewType, View

@admin.register(ViewType)
class ViewTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'type_name')

@admin.register(View)
class ViewAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'view_type', 'author', 'get_read_num', 'created_time', 'last_updated_time')
