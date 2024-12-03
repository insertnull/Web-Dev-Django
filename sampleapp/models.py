from django.db import models
from datetime import datetime

class Item(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    added_on = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)  # Automatically updated on change
    created_at = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)  # Soft delete flag

    def __str__(self):
        return self.name

class RecycleBin(models.Model):
    name = models.CharField(max_length=255)
    action = models.CharField(max_length=20)  # e.g., Added, Updated, Deleted
    action_date = models.DateTimeField(default=datetime.now)
    
class ActionLog(models.Model):
    name = models.CharField(max_length=255)
    action = models.CharField(max_length=20)  # e.g., Added, Updated, Deleted
    action_date = models.DateTimeField(default=datetime.now)