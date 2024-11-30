
from django.contrib import admin
from .models import Item

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'quantity', 'price', 'added_on')
    search_fields = ('name',)
