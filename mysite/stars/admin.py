from django.contrib import admin
from .models import Star

@admin.register(Star)
class StarAdmin(admin.ModelAdmin):
    list_display = ('title','date')
