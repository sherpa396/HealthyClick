# Generated by Django 4.1.13 on 2024-10-24 05:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dasapp', '0047_alter_customuser_user_type_alter_payment_amount_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='user_type',
            field=models.CharField(choices=[(1, 'admin'), (2, 'doc')], default=1, max_length=50),
        ),
        migrations.AlterField(
            model_name='payment',
            name='amount',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='payment',
            name='cvv',
            field=models.IntegerField(default=0),
        ),
    ]
