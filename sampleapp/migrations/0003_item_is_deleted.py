# Generated by Django 5.1.3 on 2024-12-02 06:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sampleapp', '0002_item_delete_student'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='is_deleted',
            field=models.BooleanField(default=False),
        ),
    ]
