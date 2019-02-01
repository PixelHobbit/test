from django.contrib import admin
from .models import ShareType, Share

@admin.register(ShareType)
class ShareTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'type_name')

@admin.register(Share)
class ShareAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'share_type', 'author', 'get_read_num', 'created_time', 'last_updated_time')
