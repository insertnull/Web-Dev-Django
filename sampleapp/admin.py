from django.contrib import admin
from .models import Item

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'quantity', 'price', 'added_on')
    search_fields = ('name',)

    def save_model(self, request, obj, form, change):
        if not change and Item.objects.filter(name__iexact=obj.name).exists():
            raise ValueError("An item with this name already exists.")
        super().save_model(request, obj, form, change)
