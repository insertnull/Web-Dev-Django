# Generated by Django 5.1.3 on 2024-11-30 14:06

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ln', models.CharField(max_length=100)),
                ('fn', models.CharField(max_length=100)),
                ('mn', models.CharField(blank=True, max_length=100, null=True)),
                ('bd', models.DateField(max_length=100)),
            ],
        ),
    ]
