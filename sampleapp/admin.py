from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Item, CustomUser


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'quantity', 'price', 'added_on')
    search_fields = ('name',)

    def save_model(self, request, obj, form, change):
        if not change and Item.objects.filter(name__iexact=obj.name).exists():
            raise ValueError("An item with this name already exists.")
        super().save_model(request, obj, form, change)

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'is_active', 'is_staff')}
        ),
    )
    list_display = ('username', 'is_staff', 'is_active')
    search_fields = ('username',)
    ordering = ('username',)