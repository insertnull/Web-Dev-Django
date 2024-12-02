from django.contrib import admin
from django.urls import path
from .views import dashboard, item_list, add_item, delete_item, edit_item, backup_items, generate_report, notifications, recycle_bin, restore_item, permanently_delete_item

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', item_list, name='item_list'),
    path('add/', add_item, name='add_item'),
    path('edit/<int:item_id>/', edit_item, name='edit_item'),
    path('backup/', backup_items, name='backup_items'),
    path('generate-report/', generate_report, name='generate_report'),
    path('notifications/', notifications, name='notifications'),
    path('recycle_bin/', recycle_bin, name='recycle_bin'),
    path('delete_item/<int:item_id>/', delete_item, name='delete_item'),
    path('restore_item/<int:item_id>/', restore_item, name='restore_item'),
    path('permanently_delete_item/<int:item_id>/', permanently_delete_item, name='permanently_delete_item'),
    path('dashboard/', dashboard, name='dashboard')
]
