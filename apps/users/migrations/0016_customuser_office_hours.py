# Generated by Django 5.1.5 on 2025-03-09 11:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0015_customuser_languages'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='office_hours',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
