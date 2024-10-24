# Generated by Django 5.1.2 on 2024-10-24 02:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dasapp', '0032_alter_appointment_age'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='user_type',
            field=models.CharField(choices=[(2, 'doc'), (1, 'admin')], default=1, max_length=50),
        ),
        migrations.AlterField(
            model_name='payment',
            name='cardnumbers',
            field=models.BigIntegerField(blank=True, default=0),
        ),
        migrations.AlterField(
            model_name='payment',
            name='expirydate',
            field=models.CharField(max_length=10),
        ),
    ]
