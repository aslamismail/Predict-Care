# Generated by Django 5.1.5 on 2025-03-02 07:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prediction', '0002_alter_diseaseprediction_disease_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='diseaseprediction',
            name='patient_values',
            field=models.JSONField(blank=True, null=True),
        ),
    ]
