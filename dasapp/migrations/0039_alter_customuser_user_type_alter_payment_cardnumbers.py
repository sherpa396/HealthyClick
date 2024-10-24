# Generated by Django 4.1.13 on 2024-10-24 05:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dasapp', '0038_alter_payment_cardnumbers'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='user_type',
            field=models.CharField(choices=[(1, 'admin'), (2, 'doc')], default=1, max_length=50),
        ),
        migrations.AlterField(
            model_name='payment',
            name='cardnumbers',
            field=models.CharField(default=0, max_length=255),
        ),
    ]