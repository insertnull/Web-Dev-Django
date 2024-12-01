from django.contrib import admin
from django.urls import path
from .views import item_list, add_item, delete_item, edit_item, backup_items

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', item_list, name='item_list'),
    path('add/', add_item, name='add_item'),
    path('delete/<int:item_id>/', delete_item, name='delete_item'),
    path('edit/<int:item_id>/', edit_item, name='edit_item'),
    path('backup/', backup_items, name='backup_items')
]
