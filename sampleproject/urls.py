from django.contrib import admin
from django.urls import path
from .views import (
    search_items, restore_all_items, delete_all_items, dashboard, item_list, 
    add_item, delete_item, edit_item, backup_items, generate_report, notifications, 
    recycle_bin, restore_item, permanently_delete_item, logout_view
)
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required

urlpatterns = [ 
    path('admin/', admin.site.urls),
    path('', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    # Secure views with login_required
    path('dashboard/', login_required(dashboard), name='dashboard'),
    path('add/', login_required(add_item), name='add_item'),
    path('edit/<int:item_id>/', login_required(edit_item), name='edit_item'),
    path('backup/', login_required(backup_items), name='backup_items'),
    path('generate-report/', login_required(generate_report), name='generate_report'),
    path('notifications/', login_required(notifications), name='notifications'),
    path('recycle_bin/', login_required(recycle_bin), name='recycle_bin'),
    path('search/', login_required(search_items), name='search_items'),
    path('delete_item/<int:item_id>/', login_required(delete_item), name='delete_item'),
    path('restore_item/<int:item_id>/', login_required(restore_item), name='restore_item'),
    path('permanently_delete_item/<int:item_id>/', login_required(permanently_delete_item), name='permanently_delete_item'),
    path('item_list/', login_required(item_list), name='item_list'),
    path('recycle-bin/restore-all/', login_required(restore_all_items), name='restore_all_items'),
    path('recycle-bin/delete-all/', login_required(delete_all_items), name='delete_all_items'),
    path('logout/', logout_view, name='logout')
]
