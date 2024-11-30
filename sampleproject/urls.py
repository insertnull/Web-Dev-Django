from django.contrib import admin
from django.urls import path
from .views import item_list, add_item, delete_item  # Correctly importing views from 'sampleapp'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', item_list, name='item_list'),
    path('add/', add_item, name='add_item'),
    path('delete/<int:item_id>/', delete_item, name='delete_item'),
]
