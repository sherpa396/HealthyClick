# Generated by Django 4.1.13 on 2024-10-23 16:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dasapp', '0031_alter_appointment_address_alter_customuser_user_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='age',
            field=models.IntegerField(default=0, max_length=2),
        ),
    ]
